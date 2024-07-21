import bpy, bmesh, gpu
from bpy.types import Operator
from bpy.props import EnumProperty
from mathutils import Vector, Matrix
from gpu_extras.batch import batch_for_shader

from ..utils import OpInfo, get_addon_preferences


class PIESPLUS_OT_origin_to_bottom(OpInfo, Operator):
    bl_idname = "pies_plus.origin_to_bottom"
    bl_label = "Origin to Bottom"
    bl_description = "Set the origin to the bottom of the mesh"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        for ob in context.selected_objects:
            min_z = min([vertex.co.z for vertex in ob.data.vertices])

            for vertex in ob.data.vertices:
                vertex.co.z -= min_z

            ob.location.z += min_z
        return {'FINISHED'}


class PIESPLUS_OT_reset_origin(OpInfo, Operator):
    bl_idname = "pies_plus.reset_origin"
    bl_label = "Origin Reset"
    bl_description = "Resets the Origin to the respective selected axis"

    origin_reset_axis: EnumProperty(
        items=(
            ('origin_all', "All", ""),
            ('origin_x', "X", ""),
            ('origin_y', "Y", ""),
            ('origin_z', "Z", "")
        ),
        name='Reset Axis'
    )

    def create_pivot(self, context, ob):
        if self.origin_reset_axis == 'origin_all':
            bpy.ops.object.empty_add(type='ARROWS', location = (0, 0, 0))
        else:
            bpy.ops.object.empty_add(type='ARROWS', location = ob.location)

        pivot = context.active_object
        pivot.name = ob.name + ".OriginHelper"

        if self.origin_reset_axis == 'origin_x':
            pivot.location[0] = 0
        elif self.origin_reset_axis == 'origin_y':
            pivot.location[1] = 0
        else:
            pivot.location[2] = 0

        ob = bpy.data.objects[pivot.name[:-13]]
        piv_loc = pivot.location
        cl = context.scene.cursor.location
        piv = (cl[0], cl[1], cl[2])
        context.scene.cursor.location = piv_loc
        context.view_layer.objects.active = ob
        bpy.data.objects[ob.name].select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        context.scene.cursor.location = (piv[0], piv[1], piv[2])
        bpy.data.objects[ob.name].select_set(False)
        bpy.data.objects[pivot.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[ob.name].select_set(True)
        context.view_layer.objects.active = ob

    def execute(self, context):
        saved_mode = context.object.mode

        bpy.ops.object.mode_set(mode='OBJECT')

        for ob in context.selected_objects:
            self.create_pivot(context, ob)

        bpy.ops.object.mode_set(mode=saved_mode)
        return{'FINISHED'}


class PIESPLUS_OT_origin_to_com(OpInfo, Operator):
    bl_idname = "pies_plus.origin_to_com"
    bl_label = "Origin to Mass"
    bl_description = "Snap 3D Cursor to the center of mass"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        return{'FINISHED'}


class EdgeRotAlign: # Mix-in class
    '''Helper properties, ui and functions for operators with Edge Align capabilities'''
    def get_active_geo_rotation(self, context) -> str:
        '''Get and set the normal direction of the 3D Cursor based on the active geo'''
        return_msg = None
        ob = context.object
        me = ob.data

        self.bm = bmesh.from_edit_mesh(me)
        self.bm.faces.ensure_lookup_table()
        self.bm.edges.ensure_lookup_table()

        if 'VERT' in self.bm.select_mode:
            return_msg = 'This operator does not work on vertices'
            return return_msg

        active_geo = self.bm.select_history.active
        if active_geo is None:
            return_msg = "Could not find the active geo to copy rotation"
            return return_msg

        if isinstance(active_geo, bmesh.types.BMFace):
            direction_vec = active_geo.normal
        else: # Edge
            if self.edge_rot_type == 'face_1_angle':
                if len(active_geo.link_faces):
                    direction_vec = active_geo.link_faces[0].normal
                else:
                    return_msg = "There is no face to sample from, using edge angle as fallback"
            elif self.edge_rot_type == 'face_2_angle':
                if len(active_geo.link_faces) > 1:
                    direction_vec = active_geo.link_faces[1].normal
                else:
                    return_msg = "There is no second face to sample from, using edge angle as fallback"
            elif self.edge_rot_type == 'average_face_angle':
                if len(active_geo.link_faces) > 1:
                    direction_vec = (active_geo.link_faces[0].normal + active_geo.link_faces[1].normal) / 2
                else:
                    return_msg = "There isn't 2 faces to average from, using edge angle as fallback"

            if self.edge_rot_type == 'edge_angle' or return_msg is not None: # Also use as fallback
                direction_vec = active_geo.verts[0].co - active_geo.verts[1].co

        _loc, rot, scl = ob.matrix_world.decompose()
        rot_mat = rot.to_matrix().to_4x4()
        scl_mat = Matrix.Diagonal(scl.to_4d())
        direction_vec = rot_mat @ scl_mat @ direction_vec

        normal_quat = direction_vec.to_track_quat('Z', 'Y')
        normal_euler = normal_quat.to_euler('XYZ')
        normal_axis = normal_quat.to_axis_angle()

        if self.internal_align_type == 'cursor':
            cursor = context.scene.cursor

            if cursor.rotation_mode == 'QUATERNION':
                cursor.rotation_quaternion = normal_quat
            elif cursor.rotation_mode == 'AXIS_ANGLE':
                cursor.rotation_axis_angle[0] = normal_axis[1]
                cursor.rotation_axis_angle[1] = normal_axis[0][0]
                cursor.rotation_axis_angle[2] = normal_axis[0][1]
                cursor.rotation_axis_angle[3] = normal_axis[0][2]
            else:
                cursor.rotation_euler = normal_euler
        else: # origin
            ob_mat = ob.matrix_world

            bpy.ops.object.mode_set(mode='OBJECT')

            # Make local space = world space
            me.transform(ob_mat)

            # Faster way to calculate new matrix - without refreshing the View Layer
            loc, _rot, scl = ob_mat.decompose()
            ob.matrix_world = (
                Matrix.Translation(loc)
                @ normal_euler.to_matrix().to_4x4()
                @ Matrix.Diagonal(scl.to_4d())
            )

            # Apply the inverted matrix on the mesh
            me.transform(ob.matrix_world.inverted())

            bpy.ops.object.mode_set(mode='EDIT')
            self.bm = bmesh.from_edit_mesh(ob.data)

            # Wierd rounding errors without this, less accurate but looks nicer
            ob.rotation_euler[0] = round(ob.rotation_euler[0], 5)
            ob.rotation_euler[1] = round(ob.rotation_euler[1], 5)
            ob.rotation_euler[2] = round(ob.rotation_euler[2], 5)

        if return_msg is not None:
            self.report({'WARNING'}, return_msg)

    def draw(self, context):
        if context.object.mode != 'EDIT':
            return

        try:
            getattr(PIESPLUS_OT_origin_to_selection, 'bm')
        except AttributeError:
            self.bm = bmesh.from_edit_mesh(context.object.data)

        if 'FACE' in self.bm.select_mode:
            self.selection_type = 'face'
        elif 'EDGE' in self.bm.select_mode:
            self.selection_type = 'edge'
        elif 'VERT' in self.bm.select_mode:
            self.selection_type = 'vertex'

        layout = self.layout

        row = layout.row()
        row.enabled = False
        row.prop(self, 'selection_type', expand=True)

        if self.selection_type in {'edge', 'face'} and not self.internal_enable_lock:
            layout.separator()
            layout.enabled = context.mode == 'EDIT_MESH'
            layout.prop(self, "copy_active_selections_rot")

        if self.selection_type in 'edge':
            split = layout.split(factor=.2)
            split.enabled = self.copy_active_selections_rot
            split.label(text='Copy Type')
            split.row().prop(self, 'edge_rot_type', expand=True)

    copy_active_selections_rot: bpy.props.BoolProperty(
        description="Copy the rotation of the active face or edge",
        name='Copy Active Rotation',
        default=False,
        options={'SKIP_SAVE'}
    )
    selection_type: bpy.props.EnumProperty(
        items=(
            ('vertex', "Vert", ""),
            ('edge', "Edge", ""),
            ('face', "Face", "")
        ),
        description='',
        name='Selection Type'
    )
    edge_rot_type: bpy.props.EnumProperty(
        items=(
            ('edge_angle', "Edge", ""),
            ('average_face_angle', "Average", ""),
            ('face_1_angle', "Face 1", ""),
            ('face_2_angle', "Face 2", "")
        ),
        description='Method of getting the rotation angle to copy from',
        name='Copy Type'
    )
    internal_enable_lock: bpy.props.BoolProperty(default=False)
    internal_align_type: bpy.props.EnumProperty(
        items=(
            ('cursor', "Cursor", ""),
            ('origin', "Origin", "")
        )
    )

class PIESPLUS_OT_draw_vectors_with_fade(bpy.types.Operator):
    bl_idname = "pies_plus.draw_vectors_with_fade"
    bl_label = "Draw Vectors"
    bl_options = {'INTERNAL'}

    time: bpy.props.FloatProperty(name="Time", default=1)
    steps: bpy.props.FloatProperty(name="Steps", default=0.05)
    alpha: bpy.props.FloatProperty(name="Alpha", default=0.3, min=0.1, max=1)
    use_fade: bpy.props.IntProperty(default=True)
    vec_color: bpy.props.FloatVectorProperty(
        subtype='COLOR_GAMMA',
        default=[1, 1, 1],
        size=3,
        min=0,
        max=1
    )

    def draw_vectors(self, coords, mx=Matrix(), color=(1, 1, 1), width=1, alpha=1, xray=True, use_fade=True):
        def draw():
            # Hard coded idx order
            indices = (
                (0, 1), (0, 3), (1, 2), (2, 3),
                (4, 5), (4, 7), (5, 6), (6, 7),
                (0, 4), (1, 5), (2, 6), (3, 7)
            )

            shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
            shader.bind()
            shader.uniform_float("color", (*color, alpha))

            gpu.state.depth_test_set('NONE' if xray else 'LESS_EQUAL')
            gpu.state.blend_set('ALPHA' if alpha < 1 else 'NONE')
            gpu.state.line_width_set(width)

            batch = batch_for_shader(shader, 'LINES', {"pos": coords}, indices=indices)
            batch.draw(shader)

        # If in a modal, repeatedly draw
        if use_fade:
            draw()
        else:
            bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_VIEW')

    def draw_VIEW3D(self, args):
        alpha = (self.countdown / self.time) * self.alpha

        ob = bpy.context.object
        bbox_corners = [ob.matrix_world @ Vector(point) for point in ob.bound_box]

        self.draw_vectors(
            bbox_corners,
            mx=Matrix(),
            color=self.vec_color,
            width=3,
            alpha=alpha,
            xray=True,
            use_fade=True
        )

    def modal(self, context, event):
        context.area.tag_redraw()

        if self.countdown < 0:
            context.window_manager.event_timer_remove(self.TIMER)

            bpy.types.SpaceView3D.draw_handler_remove(self.VIEW3D, 'WINDOW')
            return {'FINISHED'}

        if event.type == 'TIMER':
            self.countdown -= self.steps
        return {'PASS_THROUGH'}

    def execute(self, context):
        self.TIMER = context.window_manager.event_timer_add(self.steps, window=context.window)
        self.countdown = self.time

        args = (self, context)
        self.VIEW3D = bpy.types.SpaceView3D.draw_handler_add(self.draw_VIEW3D, (args, ), 'WINDOW', 'POST_VIEW')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PIESPLUS_OT_origin_to_selection(OpInfo, EdgeRotAlign, Operator):
    bl_idname = "pies_plus.origin_to_selection"
    bl_label = "Origin to Selection"
    bl_description = "Sets the Active Objects Origin to the current selection"

    def invoke(self, context, event):
        self.saved_mat = context.object.matrix_world.copy()
        return self.execute(context)

    def execute(self, context):
        ob = context.object
        ob.matrix_world = self.saved_mat # Invoke undo safety net

        if self.copy_active_selections_rot:
            self.internal_align_type = 'origin'
            return_msg = self.get_active_geo_rotation(context)

            if return_msg is not None:
                self.report({'ERROR'}, return_msg)
                return{'CANCELLED'}

            bpy.ops.pies_plus.draw_vectors_with_fade(vec_color=(0, 1, 0))

        saved_mode = ob.mode
        saved_cursor_loc = context.scene.cursor.location.copy()

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        bpy.ops.object.mode_set(mode=saved_mode)
        context.scene.cursor.location = saved_cursor_loc
        return {'FINISHED'}


class PIESPLUS_OT_cursor_to_selected(OpInfo, EdgeRotAlign, Operator):
    bl_idname = "pies_plus.cursor_to_selection"
    bl_label = "Cursor to Selection"
    bl_description = "Snap 3D Cursor to the middle of the selected items"

    def execute(self, context):
        if self.copy_active_selections_rot:
            self.internal_align_type = 'cursor'
            return_msg = self.get_active_geo_rotation(context)

            if return_msg is not None:
                self.report({'ERROR'}, return_msg)
                return{'CANCELLED'}

        bpy.ops.view3d.snap_cursor_to_selected()
        return{'FINISHED'}


class PIESPLUS_OT_cursor_to_active(OpInfo, EdgeRotAlign, Operator):
    bl_idname = "pies_plus.cursor_to_active"
    bl_label = "Cursor to Active"
    bl_description = "Snap 3D Cursor to active item"

    def execute(self, context):
        if self.copy_active_selections_rot:
            self.internal_align_type = 'cursor'
            return_msg = self.get_active_geo_rotation(context)

            if return_msg is not None:
                self.report({'ERROR'}, return_msg)
                return{'CANCELLED'}

        bpy.ops.view3d.snap_cursor_to_active()
        return{'FINISHED'}


class PIESPLUS_OT_cursor_to_active_orient(OpInfo, EdgeRotAlign, Operator):
    bl_idname = "pies_plus.cursor_to_active_orient"
    bl_label = "Cursor to Orient"
    bl_description = "Align only rotation of the 3D Cursor to the active edge or face"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        self.copy_active_selections_rot = True
        self.internal_align_type = 'cursor'
        self.internal_enable_lock = True
        return_msg = self.get_active_geo_rotation(context)

        if return_msg is not None:
            self.report({'ERROR'}, return_msg)
            return{'CANCELLED'}
        return{'FINISHED'}


class PIESPLUS_OT_origin_to_active_orient(OpInfo, EdgeRotAlign, Operator):
    bl_idname = "pies_plus.origin_to_active_orient"
    bl_label = "Origin to Orient"
    bl_description = "Align only rotation of the Origin to the active edge or face"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def invoke(self, context, event):
        self.saved_mat = context.object.matrix_world.copy()
        return self.execute(context)

    def execute(self, context):
        context.object.matrix_world = self.saved_mat # Invoke undo safety net

        self.copy_active_selections_rot = True
        self.internal_align_type = 'origin'
        self.internal_enable_lock = True
        return_msg = self.get_active_geo_rotation(context)

        if return_msg is not None:
            self.report({'ERROR'}, return_msg)
            return{'CANCELLED'}

        bpy.ops.pies_plus.draw_vectors_with_fade(vec_color=(0, 1, 0))
        return{'FINISHED'}


class PIESPLUS_OT_reset_cursor(OpInfo, Operator):
    bl_idname = "pies_plus.reset_cursor"
    bl_label = "Cursor Reset"
    bl_description = "Reset 3D Cursor to the selected axis"

    cursor_reset_axis: EnumProperty(items=(('cursor_all', "All", ""),
                                           ('cursor_x', "X", ""),
                                           ('cursor_y', "Y", ""),
                                           ('cursor_z', "Z", "")), name = 'Reset Axis')

    def draw(self, context):
        layout = self.layout
        layout.separator()

        split = layout.split(factor=.2)
        split.label(text='Reset Axis')
        split.row().prop(self, 'cursor_reset_axis', expand=True)

    def execute(self, context):
        cursor = context.scene.cursor

        if self.cursor_reset_axis == 'cursor_all':
            cursor.location = (0, 0, 0)
        elif self.cursor_reset_axis == 'cursor_x':
            cursor.location[0] = 0
        elif self.cursor_reset_axis == 'cursor_y':
            cursor.location[1] = 0
        else: # Z
            cursor.location[2] = 0

        if get_addon_preferences().reset_3d_cursor_rot_pref:
            bpy.ops.pies_plus.reset_cursor_rot()
        return{'FINISHED'}


class PIESPLUS_OT_reset_cursor_rot(OpInfo, Operator):
    bl_idname = "pies_plus.reset_cursor_rot"
    bl_label = "Reset Cursor Rot"
    bl_description = "Reset 3D Cursor rotation"

    def execute(self, context):
        cursor = context.scene.cursor

        if cursor.rotation_mode == 'QUATERNION':
            cursor.rotation_quaternion = (1,0,0,0)
        elif cursor.rotation_mode == 'AXIS_ANGLE':
            cursor.rotation_axis_angle = (0,0,1,0)
        else:
            cursor.rotation_euler = (0,0,0)
        return {'FINISHED'}


##############################
#   REGISTRATION
##############################


classes = (
    PIESPLUS_OT_origin_to_selection,
    PIESPLUS_OT_origin_to_bottom,
    PIESPLUS_OT_origin_to_com,
    PIESPLUS_OT_cursor_to_selected,
    PIESPLUS_OT_cursor_to_active,
    PIESPLUS_OT_cursor_to_active_orient,
    PIESPLUS_OT_origin_to_active_orient,
    PIESPLUS_OT_draw_vectors_with_fade,
    PIESPLUS_OT_reset_origin,
    PIESPLUS_OT_reset_cursor,
    PIESPLUS_OT_reset_cursor_rot
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
