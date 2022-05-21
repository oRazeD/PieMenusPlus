import bpy, bmesh
from bpy.types import Operator
from bpy.props import EnumProperty
from .generic_utils import OpInfo


class PIESPLUS_OT_origin_to_selection(OpInfo, Operator):
    bl_idname = "pies_plus.origin_to_selection"
    bl_label = "Origin to Selection"
    bl_description = "Sets the Active Objects Origin to the current selection"

    def execute(self, context):
        modeCallback = context.object.mode

        saved_location = context.scene.cursor.location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        context.scene.cursor.location = saved_location

        bpy.ops.object.mode_set(mode=modeCallback)
        return {'FINISHED'}


class PIESPLUS_OT_origin_to_bottom(OpInfo, Operator):
    bl_idname = "pies_plus.origin_to_bottom"
    bl_label = "Origin to Bottom"
    bl_description = "Sets the Active Objects Origin to the bottom of the mesh"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        for ob in context.selected_objects:
            vertices = ob.data.vertices
            minZ = min((vertex.co.z for vertex in vertices))
            
            for vertex in ob.data.vertices:
                vertex.co.z -= minZ

            ob.location.z += minZ
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
        modeCallback = context.object.mode

        bpy.ops.object.mode_set(mode='OBJECT')

        for ob in context.selected_objects:
            self.create_pivot(context, ob)

        bpy.ops.object.mode_set(mode=modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_origin_to_com(OpInfo, Operator):
    bl_idname = "pies_plus.origin_to_com"
    bl_label = "Origin to Mass"
    bl_description = "Snap 3D Cursor to the center of mass"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        return{'FINISHED'}


class EdgeAlign: # Mix-in class
    '''Helper properties, ui and functions for operators with Edge Align capabilities'''
    def get_active_geo_rotation(self, context, bm: bmesh.types.BMesh=None) -> str:
        '''Get and set the normal direction of the 3D Cursor based on the active geo'''
        return_msg = None
        cursor = context.scene.cursor
        ob = context.object

        if bm is None:
            bm = bmesh.from_edit_mesh(ob.data)
            bm.faces.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
        
        active_geo = bm.select_history.active
        if active_geo is None:
            return_msg = "Could not find the active geo to copy rotation"
            return return_msg

        _loc, rot, _scl = ob.matrix_world.decompose()
        rot_matrix = rot.to_matrix().to_4x4()

        if isinstance(active_geo, bmesh.types.BMFace):
            direction_vec = rot_matrix @ active_geo.normal
        else: # Edge
            if self.edge_rot_type == 'face_1_angle':
                if len(active_geo.link_faces):
                    direction_vec = rot_matrix @ active_geo.link_faces[0].normal
                else:
                    return_msg = "There is no face to sample from, using edge angle as fallback"
            elif self.edge_rot_type == 'face_2_angle':
                if len(active_geo.link_faces) > 1:
                    direction_vec = rot_matrix @ active_geo.link_faces[1].normal
                else:
                    return_msg = "There is no second face to sample from, using edge angle as fallback"
            elif self.edge_rot_type == 'average_face_angle':
                if len(active_geo.link_faces) > 1:
                    direction_vec = rot_matrix @ ((active_geo.link_faces[0].normal + active_geo.link_faces[1].normal) / 2)
                else:
                    return_msg = "There isn't 2 faces to average from, using edge angle as fallback"

            if self.edge_rot_type == 'edge_angle' or return_msg is not None: # Also use as fallback
                direction_vec = rot_matrix @ (active_geo.verts[0].co - active_geo.verts[1].co) 

        normal_quat = direction_vec.to_track_quat('Z', 'Y')
        normal_euler = normal_quat.to_euler('XYZ')
        normal_axis = normal_quat.to_axis_angle()

        if cursor.rotation_mode == 'QUATERNION':
            cursor.rotation_quaternion = normal_quat
        elif cursor.rotation_mode == 'AXIS_ANGLE':
            cursor.rotation_axis_angle[0] = normal_axis[1]
            cursor.rotation_axis_angle[1] = normal_axis[0][0]
            cursor.rotation_axis_angle[2] = normal_axis[0][1]
            cursor.rotation_axis_angle[3] = normal_axis[0][2]
        else:
            cursor.rotation_euler = normal_euler
        return return_msg

    def draw(self, context):
        layout = self.layout

        if 'FACE' in self.bm.select_mode:
            self.selection_type = 'face'
        elif 'EDGE' in self.bm.select_mode:
            self.selection_type = 'edge'
        elif 'VERT' in self.bm.select_mode:
            self.selection_type = 'vertex'

        row = layout.row()
        row.enabled = False
        row.prop(self, 'selection_type', expand=True)

        if self.selection_type in {'edge', 'face'}:
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
        default=False
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
        description='Different methods of getting the rotation angle to copy from',
        name='Copy Type'
    )


class PIESPLUS_OT_cursor_to_selected(OpInfo, EdgeAlign, Operator):
    bl_idname = "pies_plus.cursor_to_selection"
    bl_label = "Cursor to Selection"
    bl_description = "Snap 3D Cursor to the middle of the selected items"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()

        if context.mode == 'EDIT_MESH':
            self.bm = bmesh.from_edit_mesh(context.object.data)

            if self.copy_active_selections_rot:
                return_msg = self.get_active_geo_rotation(context)

                if return_msg is not None:
                    self.report({'WARNING'}, return_msg)
        return{'FINISHED'}


class PIESPLUS_OT_cursor_to_active(OpInfo, EdgeAlign, Operator):
    bl_idname = "pies_plus.cursor_to_active"
    bl_label = "Cursor to Active"
    bl_description = "Snap 3D Cursor to active item"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_active()

        if context.mode == 'EDIT_MESH':
            self.bm = bmesh.from_edit_mesh(context.object.data)



            if self.copy_active_selections_rot:
                return_msg = self.get_active_geo_rotation(context)

                if return_msg is not None:
                    self.report({'WARNING'}, return_msg)
        return{'FINISHED'}


class PIESPLUS_OT_cursor_to_active_orient(OpInfo, EdgeAlign, Operator):
    bl_idname = "pies_plus.cursor_to_active_orient"
    bl_label = "Cursor to Orient"
    bl_description = "Align only rotation of the 3D Cursor to the active edge or face"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        self.bm = bmesh.from_edit_mesh(context.object.data)

        if 'VERT' in self.bm.select_mode:
            self.report({'ERROR'}, 'This operator does not work on vertices')
            return{'CANCELLED'}

        self.copy_active_selections_rot = True
        
        return_msg = self.get_active_geo_rotation(context)

        if return_msg is not None:
            self.report({'WARNING'}, return_msg)
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

        if context.preferences.addons[__package__].preferences.reset_3d_cursor_rot_pref:
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


class PIESPLUS_OT_edit_origin(Operator):
    bl_idname = "pies_plus.edit_origin"
    bl_label = "Edit Origin"
    bl_description = "Transform the origin or 3D Cursor"
    bl_options = {'REGISTER'}

    edit_type: EnumProperty(
        items=(
            ('origin', "Origin", ""),
            ('cursor', "Cursor", "")
        ),
        name='Edit Type'
    )

    def modal(self, context, event):
        if self.finished:
            return {'CANCELLED'}

        if event.type in {'LEFTMOUSE', 'RET', 'RIGHTMOUSE', 'ESC'}:
            # Refresh snapping options
            if bpy.app.version >= (2, 82, 0):
                self.ts.use_snap_backface_culling = self.savedBackface

            self.ts.snap_elements = self.savedSnapSettings
            self.ts.use_snap_align_rotation = self.savedAlignSettings

            context.view_layer.objects.active = self.savedActive
            bpy.data.objects[self.savedActive.name].select_set(True)

            if self.edit_type == 'origin':
                if event.type in {'LEFTMOUSE', 'RET'}:
                    self.piv = (self.cursor_loc[0], self.cursor_loc[1], self.cursor_loc[2])
                    context.scene.cursor.location = self.piv_loc

                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                    context.scene.cursor.location = (self.piv[0], self.piv[1], self.piv[2])

                # Deselect the Active Object rather than having to loop through every selected object later
                bpy.data.objects[self.savedActive.name].select_set(False)

                # Delete the pivot
                bpy.data.objects.remove(bpy.data.objects[self.pivot.name], do_unlink=True)

            # Refresh wireframe settings
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        space.overlay.show_wireframes = self.savedWireframe
                        break

            # Refresh modifier visibility
            for ob in self.subsurf_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]

                for mod in bpy.data.objects[ob].modifiers:
                    if mod.type == "SUBSURF":
                        mod.show_viewport = True

            for ob in self.mirror_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]

                for mod in bpy.data.objects[ob].modifiers:
                    if mod.type == "MIRROR":
                        mod.show_viewport = True

            # Refresh original selection & Active Object
            for o in self.savedSelection:
                ob = context.scene.objects.get(o)
                ob.select_set(True)

            if self.edit_type == 'origin':
                # If the experimental mode is on, remove the loose vertices on the mesh
                if context.preferences.addons[__package__].preferences.face_center_snap_pref:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.delete_loose()
            
            context.view_layer.objects.active = self.savedActive

            # Refresh Context Mode
            bpy.ops.object.mode_set(mode=self.modeCallback)

            self.finished = True
            return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}
        
    def invoke(self, context, event):
        # Safety check for if user searches the operation
        if not context.active_object:
            self.report({'ERROR'}, "No Active Object selected")
            return{'FINISHED'}

        self.finished = False
        self.ts = context.scene.tool_settings

        if bpy.app.version >= (2, 82, 0):
            self.savedBackface = self.ts.use_snap_backface_culling

            self.ts.use_snap_backface_culling = True

        self.savedSnapSettings = self.ts.snap_elements
        self.savedAlignSettings = self.ts.use_snap_align_rotation
        self.savedSelection = context.view_layer.objects.selected.keys()
        self.modeCallback = context.object.mode

        # Save the Active Object & Make sure it is selected
        self.savedActive = context.view_layer.objects.active
        context.active_object.select_set(True)

        # Save & set the Context Mode
        self.modeCallback = context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Lists for saving which objects had subsurf/mirror enabled and which didn't
        self.subsurf_check_list = []
        self.mirror_check_list = []

        # Deselect objects that aren't the Active, Toggle modifiers if turned on & save to list
        for ob in context.view_layer.objects:
            for mod in ob.modifiers:
                if mod.type == "SUBSURF":
                    if mod.show_viewport:
                        mod.show_viewport = False
                        self.subsurf_check_list.append(ob.name)
                if mod.type == "MIRROR":
                    if mod.show_viewport:
                        mod.show_viewport = False
                        self.mirror_check_list.append(ob.name)

            if ob != context.active_object:
                ob.select_set(False)
            
        # Enable wireframe
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    self.savedWireframe = space.overlay.show_wireframes
                    space.overlay.show_wireframes = True
                    break

        if self.edit_type == 'origin':
            # BMesh (Add vertices to face centers)
            if context.preferences.addons[__package__].preferences.face_center_snap_pref:
                mesh = context.object.data
                verts = []

                for poly in mesh.polygons:
                    verts.append((poly.center[0], poly.center[1], poly.center[2]))

                bm = bmesh.new()

                bpy.ops.object.mode_set(mode='EDIT') # Convert the current mesh to a bmesh (must be in edit mode)
                bm.from_mesh(mesh)
                bpy.ops.object.mode_set(mode='OBJECT')

                for v in verts:
                    bm.verts.new(v) # Add a new vert

                bm.to_mesh(mesh) # Make the bmesh the object's mesh
                bm.free() # Always do this when finished

            # Create new empty
            bpy.ops.object.empty_add(location = self.savedActive.location)

            # Scale down the object(would rather it be super small than super large)
            context.object.scale = (.00001, .00001, .00001)

            # Save Active Object pivot to a variable
            self.pivot = context.active_object

            # Set the variables name to the ob
            self.pivot.name = self.savedActive.name + ".OriginHelper"

            # Save the location of the newly made empty
            self.piv_loc = self.pivot.location

            # Save the 3D Cursor location
            self.cursor_loc = context.scene.cursor.location

            # Change snap settings & enable editable origin
            self.ts.use_snap_align_rotation = False

            if bpy.app.version >= (2, 81, 0):
                self.ts.snap_elements = {'VERTEX', 'EDGE', 'FACE', 'EDGE_MIDPOINT'}
            else:
                self.ts.snap_elements = {'VERTEX', 'EDGE', 'FACE'}

            # Translate modal
            bpy.ops.transform.translate('INVOKE_DEFAULT')
        else:
            # Reset 3D Cursor rotation
            context.scene.cursor.rotation_euler = (0, 0, 0)

            # Change snap settings & enable editable origin
            self.ts.use_snap_align_rotation = True

            if bpy.app.version >= (2, 81, 0):
                self.ts.snap_elements = {'VERTEX', 'FACE', 'EDGE_MIDPOINT'}
            else:
                self.ts.snap_elements = {'VERTEX', 'FACE'}

            # Translate modal
            bpy.ops.transform.translate('INVOKE_DEFAULT', cursor_transform=True)

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


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
    PIESPLUS_OT_reset_origin,
    PIESPLUS_OT_reset_cursor,
    PIESPLUS_OT_reset_cursor_rot,
    PIESPLUS_OT_edit_origin
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
