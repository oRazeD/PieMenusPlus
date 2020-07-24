import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from bpy_extras import view3d_utils
import bmesh
from ctypes import *
from time import sleep


class PIESPLUS_OT_origin_to_selection(Operator):
    bl_idname = "pies_plus.origin_to_selection"
    bl_label = "Origin To Selection"
    bl_description = "[BATCH] Sets the Active Objects Origin to the current selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        modeCallback = context.object.mode

        saved_location = context.scene.cursor.location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        context.scene.cursor.location = saved_location

        bpy.ops.object.mode_set(mode=modeCallback)
        return {'FINISHED'}


class PIESPLUS_OT_origin_to_bottom(Operator):
    bl_idname = "pies_plus.origin_to_bottom"
    bl_label = "Origin to Bottom"
    bl_description = "[BATCH] Sets the Active Objects Origin to the bottom of the mesh"
    bl_options = {'REGISTER', 'UNDO'}

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


class PIESPLUS_OT_reset_origin(Operator):
    bl_idname = "pies_plus.reset_origin"
    bl_label = "Origin Reset"
    bl_description = "[BATCH] Resets the Origin to the respective selected axis"
    bl_options = {'REGISTER', 'UNDO'}

    origin_reset_axis: EnumProperty(items=(('origin_all', "All", ""),
                                           ('origin_x', "X", ""),
                                           ('origin_y', "Y", ""),
                                           ('origin_z', "Z", "")))

    def create_pivot(self, context, obj):
        if self.origin_reset_axis == 'origin_all':
            bpy.ops.object.empty_add(type='ARROWS', location = (0, 0, 0))
        else:
            bpy.ops.object.empty_add(type='ARROWS', location = obj.location)
        pivot = context.active_object
        pivot.name = obj.name + ".OriginHelper"
        if self.origin_reset_axis == 'origin_x':
            pivot.location[0] = 0
        elif self.origin_reset_axis == 'origin_y':
            pivot.location[1] = 0
        else:
            pivot.location[2] = 0
        obj = bpy.data.objects[pivot.name[:-13]]
        piv_loc = pivot.location
        cl = context.scene.cursor.location
        piv = (cl[0],cl[1],cl[2])
        context.scene.cursor.location = piv_loc
        context.view_layer.objects.active = obj
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        context.scene.cursor.location = (piv[0],piv[1],piv[2])
        bpy.data.objects[obj.name].select_set(False)
        bpy.data.objects[pivot.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[obj.name].select_set(True)
        context.view_layer.objects.active = obj

    def execute(self, context):
        modeCallback = context.object.mode

        bpy.ops.object.mode_set(mode='OBJECT')

        for obj in context.selected_objects:
            self.create_pivot(context, obj)

        bpy.ops.object.mode_set(mode=modeCallback)
        return{'FINISHED'}

class PIESPLUS_OT_origin_to_com(Operator):
    bl_idname = "pies_plus.origin_to_com"
    bl_label = "Origin to Center of Mass"
    bl_description = "[BATCH] Sends the origin to the center of mass"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        return{'FINISHED'}

class PIESPLUS_OT_reset_cursor(Operator):
    bl_idname = "pies_plus.reset_cursor"
    bl_label = "Origin Reset"
    bl_description = "Resets the 3D Cursor to the respective selected axis"
    bl_options = {'REGISTER', 'UNDO'}

    cursor_reset_axis: EnumProperty(items=(('cursor_all', "All", ""),
                                           ('cursor_x', "X", ""),
                                           ('cursor_y', "Y", ""),
                                           ('cursor_z', "Z", "")))

    def execute(self, context):
        if self.cursor_reset_axis == 'cursor_all':
            context.scene.cursor.location = (0,0,0)

        elif self.cursor_reset_axis == 'cursor_x':
            context.scene.cursor.location[0] = 0

        elif self.cursor_reset_axis == 'cursor_y':
            context.scene.cursor.location[1] = 0

        else:
            context.scene.cursor.location[2] = 0

        if context.preferences.addons[__package__].preferences.resetRot_Pref:
            context.scene.cursor.rotation_euler = (0,0,0)
        return{'FINISHED'}


class PIESPLUS_OT_reset_cursor_rot(Operator):
    bl_idname = "view3d.reset_cursor_rot"
    bl_label = "Reset Cursor Rot"
    bl_description = "Resets the 3D Cursor's rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.cursor.rotation_euler = (0,0,0)
        return{'FINISHED'}


class PIESPLUS_OT_edit_origin(Operator):
    """Manually edit the origin

While this tool is stable usability wise, lack of control with the undo system
means this breaks if you undo/redo into an edit origin state. Included is a 
safety undo in your history should the operation break"""
    bl_idname = "pies_plus.edit_origin"
    bl_label = "Edit Origin"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        ts = context.scene.tool_settings

        if event.type in {'LEFTMOUSE', 'RET', 'RIGHTMOUSE', 'ESC'} or self.redoOp:
            # If the experimental mode is on, remove the loose vertices on the mesh
            if context.preferences.addons[__package__].preferences.faceCenterSnap_Pref and not self.redoOp:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete_loose()

                self.redoOp = True
                return {'PASS_THROUGH'}
            else:
                # Refresh snapping options
                ts.snap_elements = self.savedSnapSettings
                ts.use_snap_backface_culling = self.savedBackface
                ts.use_snap_align_rotation = self.savedAlignSettings

                # Select Active here because later causes crashing...???
                context.view_layer.objects.active = self.savedActive
                bpy.data.objects[self.savedActive.name].select_set(True)

                # Only works on Windows (TO-DO - Find an alternative that works for Mac)
                if event.type in {'LEFTMOUSE', 'RET'}:
                    #windll.user32.keybd_event(0x0D, 0, 0, 0)
                    #sleep(0.01)
                    #windll.user32.keybd_event(0x0D, 0, 2, 0)
                    #sleep(0.01)

                    self.piv = (self.cursor_loc[0], self.cursor_loc[1], self.cursor_loc[2])
                    context.scene.cursor.location = self.piv_loc

                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                    context.scene.cursor.location = (self.piv[0],self.piv[1],self.piv[2])
                else:
                    windll.user32.keybd_event(0x1B, 0, 0, 0)
                    sleep(0.01)
                    windll.user32.keybd_event(0x1B, 0, 2, 0)
                    sleep(0.01)

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

                context.view_layer.objects.active = self.savedActive

                # Refresh Context Mode
                bpy.ops.object.mode_set(mode=self.modeCallback)
                return {'CANCELLED'}
        return {'PASS_THROUGH'}
        
    def invoke(self, context, event):
        # Safety check for if user searches the operation
        if not context.active_object:
            self.report({'ERROR'}, "No Active Object selected")
            return{'FINISHED'}

        ts = context.scene.tool_settings

        self.savedBackface = ts.use_snap_backface_culling
        self.savedSnapSettings = ts.snap_elements
        self.savedAlignSettings = ts.use_snap_align_rotation
        self.savedSelection = context.view_layer.objects.selected.keys()
        self.modeCallback = context.object.mode

        self.redoOp = False

        # Save the Active Object & Make sure it is selected
        self.savedActive = context.view_layer.objects.active
        context.active_object.select_set(True)

        # BMesh (Add vertices to face centers)
        if context.preferences.addons[__package__].preferences.faceCenterSnap_Pref:
            mesh = context.object.data
            verts = []

            for poly in mesh.polygons:
                verts.append((poly.center[0],poly.center[1],poly.center[2]))

            bm = bmesh.new()

            bpy.ops.object.mode_set(mode='EDIT') # Convert the current mesh to a bmesh (must be in edit mode)
            bm.from_mesh(mesh)
            bpy.ops.object.mode_set(mode='OBJECT')

            for v in verts:
                bm.verts.new(v) # Add a new vert

            bm.to_mesh(mesh) # Make the bmesh the object's mesh
            bm.free() # Always do this when finished

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

        # Create new empty & scale (would rather it be super small than super large)
        bpy.ops.object.empty_add(location = self.savedActive.location)
        context.object.scale = (.05, .05, .05)

        # Save Active Object pivot to a variable
        self.pivot = context.active_object

        # Set the variables name to the obj
        self.pivot.name = self.savedActive.name + ".OriginHelper"

        # Magic
        self.piv_loc = self.pivot.location
        self.cursor_loc = context.scene.cursor.location

        # Enable wireframe
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    self.savedWireframe = space.overlay.show_wireframes
                    space.overlay.show_wireframes = True
                    break

        # Change snap settings & enable editable origin
        ts.use_snap_backface_culling = True
        ts.use_snap_align_rotation = False
        ts.snap_elements = {'VERTEX', 'EDGE', 'FACE', 'EDGE_MIDPOINT'}

        # Translate modal
        bpy.ops.transform.translate('INVOKE_DEFAULT', snap=True)

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PIESPLUS_OT_edit_cursor(Operator):
    """Manually edit the 3D Cursor"""
    bl_idname = "pies_plus.edit_cursor"
    bl_label = "Edit Cursor"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        ts = context.scene.tool_settings

        if self.finished or self.cancelled:
            ts.snap_elements = self.savedSnapSettings
            ts.use_snap_backface_culling = self.savedBackface
            ts.use_snap_align_rotation = self.savedAlignSettings
            ts.use_snap = self.savedUsingSnap

            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        space.overlay.show_wireframes = self.savedWireframe
                        break

            for ob in self.subsurf_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Subdivision"].show_viewport = True

            for ob in self.mirror_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Mirror"].show_viewport = True

            for o in self.savedSelection:
                ob = context.scene.objects.get(o)
                ob.select_set(True)

            bpy.ops.object.mode_set(mode=self.modeCallback)

            if self.finished:
                return {'FINISHED'}

        # We need to pass_through once on completion so that the built-in translate finishes before we do
        if event.type in {'LEFTMOUSE'}:
            ts.snap_elements = self.savedSnapSettings
            ts.use_snap_backface_culling = self.savedBackface
            ts.use_snap_align_rotation = self.savedAlignSettings
            ts.use_snap = False #self.savedUsingSnap

            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        space.overlay.show_wireframes = self.savedWireframe
                        break

            for ob in self.subsurf_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Subdivision"].show_viewport = True

            for ob in self.mirror_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Mirror"].show_viewport = True

            for o in self.savedSelection:
                ob = context.scene.objects.get(o)
                ob.select_set(True)

            bpy.ops.object.mode_set(mode=self.modeCallback)
            return {'CANCELLED'}
        
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            ts.snap_elements = self.savedSnapSettings
            ts.use_snap_backface_culling = self.savedBackface
            ts.use_snap_align_rotation = self.savedAlignSettings
            ts.use_snap = False #self.savedUsingSnap

            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        space.overlay.show_wireframes = self.savedWireframe
                        break

            for ob in self.subsurf_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Subdivision"].show_viewport = True

            for ob in self.mirror_check_list:
                context.view_layer.objects.active = bpy.data.objects[ob]
                context.object.modifiers["Mirror"].show_viewport = True

            for o in self.savedSelection:
                ob = context.scene.objects.get(o)
                ob.select_set(True)
            
            # Only works for Windows
            windll.user32.keybd_event(0x1B, 0, 0, 0)
            
            bpy.ops.object.mode_set(mode=self.modeCallback)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
        
    def invoke(self, context, event):
        # Safety check for if user searches the operation
        if not context.active_object:
            self.report({'ERROR'}, "No Active Object selected")
            return{'FINISHED'}

        ts = context.scene.tool_settings

        # Safety undo push to undo possible errors
        bpy.ops.ed.undo_push(message="Safety push, go here to revert unwanted changes!")
                    
        self.savedBackface = ts.use_snap_backface_culling
        self.savedSnapSettings = ts.snap_elements
        self.savedAlignSettings = ts.use_snap_align_rotation
        self.savedUsingSnap = ts.use_snap
        self.savedSelection = context.view_layer.objects.selected.keys()

        # Save & set the Context Mode
        self.modeCallback = context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Make sure Active Object is selected
        context.active_object.select_set(True)

        # Lists for saving which objects had subsurf/mirror enabled and which didn't
        self.subsurf_check_list = []
        self.mirror_check_list = []

        # Deselect objects that aren't the Active, Toggle modifiers if turned on & save to list
        for ob in context.view_layer.objects:
            for mod in ob.modifiers:
                if(mod.type == "SUBSURF"):
                    if ob.modifiers["Subdivision"].show_viewport:
                        ob.modifiers["Subdivision"].show_viewport = False
                        if ob.select_get():
                            self.subsurf_check_list.append(ob.name)
                if(mod.type == "MIRROR"):
                    if ob.modifiers["Mirror"].show_viewport:
                        ob.modifiers["Mirror"].show_viewport = False
                        if ob.select_get():
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
        
        # Reset 3D Cursor rotation
        context.scene.cursor.rotation_euler = (0,0,0)

        # Change snap settings & enable editable origin
        ts.use_snap_backface_culling = True
        ts.use_snap_align_rotation = True
        #ts.use_snap = False

        ts.snap_elements = {'VERTEX', 'FACE', 'EDGE_MIDPOINT'}

        # Translate modal
        bpy.ops.transform.translate('INVOKE_DEFAULT', cursor_transform=True, snap=True)

        #ts.use_snap = True

        # Finished/cancelled checks for the modal
        self.finished = False
        self.cancelled = False

        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_origin_to_selection,
           PIESPLUS_OT_origin_to_bottom,
           PIESPLUS_OT_origin_to_com,
           PIESPLUS_OT_reset_origin,
           PIESPLUS_OT_reset_cursor,
           PIESPLUS_OT_reset_cursor_rot,
           PIESPLUS_OT_edit_origin,
           PIESPLUS_OT_edit_cursor)

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