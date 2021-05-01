import bpy, bmesh
from bpy.types import Operator
from bpy.props import EnumProperty
from .generic_utils import OpInfo


class PIESPLUS_OT_origin_to_selection(OpInfo, Operator):
    bl_idname = "pies_plus.origin_to_selection"
    bl_label = "Origin to Selection"
    bl_description = "[BATCH] Sets the Active Objects Origin to the current selection"

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
    bl_description = "[BATCH] Sets the Active Objects Origin to the bottom of the mesh"

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
    bl_description = "[BATCH] Resets the Origin to the respective selected axis"

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
    bl_description = "[BATCH] Sends the 3D Cursor to the center of mass"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        return{'FINISHED'}


class PIESPLUS_OT_reset_cursor(OpInfo, Operator):
    bl_idname = "pies_plus.reset_cursor"
    bl_label = "Cursor Reset"
    bl_description = "Resets the 3D Cursor to the respective selected axis"

    cursor_reset_axis: EnumProperty(items=(('cursor_all', "All", ""),
                                           ('cursor_x', "X", ""),
                                           ('cursor_y', "Y", ""),
                                           ('cursor_z', "Z", "")), name = 'Reset Axis')

    def execute(self, context):
        cursor = context.scene.cursor

        if self.cursor_reset_axis == 'cursor_all':
            cursor.location = (0, 0, 0)
        elif self.cursor_reset_axis == 'cursor_x':
            cursor.location[0] = 0
        elif self.cursor_reset_axis == 'cursor_y':
            cursor.location[1] = 0
        else:
            cursor.location[2] = 0

        if context.preferences.addons[__package__].preferences.resetRot_Pref:
            bpy.ops.pies_plus.reset_cursor_rot()
        return{'FINISHED'}


class PIESPLUS_OT_reset_cursor_rot(OpInfo, Operator):
    bl_idname = "pies_plus.reset_cursor_rot"
    bl_label = "Reset Cursor Rot"
    bl_description = "Reset the 3D Cursor's Rotation"

    def execute(self, context):
        cursor = context.scene.cursor

        if cursor.rotation_mode == 'QUATERNION':
            cursor.rotation_quaternion[0] = 1
            cursor.rotation_quaternion[1] = 0
            cursor.rotation_quaternion[2] = 0
            cursor.rotation_quaternion[3] = 0

        elif cursor.rotation_mode == 'AXIS_ANGLE':
            cursor.rotation_axis_angle[0] = 0
            cursor.rotation_axis_angle[1] = 0
            cursor.rotation_axis_angle[2] = 1
            cursor.rotation_axis_angle[3] = 0

        else:
            cursor.rotation_euler = (0,0,0)
        return {'FINISHED'}


class PIESPLUS_OT_edit_origin(Operator):
    bl_idname = "pies_plus.edit_origin"
    bl_label = "Edit Origin"
    bl_description = "Manually edit the origin or cursor with a translate modal"
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
                context.object.modifiers["Subdivision"].show_viewport = True

            for ob in self.mirror_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Mirror"].show_viewport = True

            # Refresh original selection & Active Object
            for o in self.savedSelection:
                ob = context.scene.objects.get(o)
                ob.select_set(True)

            if self.edit_type == 'origin':
                # If the experimental mode is on, remove the loose vertices on the mesh
                if context.preferences.addons[__package__].preferences.faceCenterSnap_Pref:
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
                if(mod.type == "SUBSURF"):
                    if ob.modifiers["Subdivision"].show_viewport:
                        ob.modifiers["Subdivision"].show_viewport = False
                        self.subsurf_check_list.append(ob.name)
                if(mod.type == "MIRROR"):
                    if ob.modifiers["Mirror"].show_viewport:
                        ob.modifiers["Mirror"].show_viewport = False
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
            if context.preferences.addons[__package__].preferences.faceCenterSnap_Pref:
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
