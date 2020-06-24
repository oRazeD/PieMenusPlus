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


import bpy
from bpy.types import Operator
from bpy.props import EnumProperty


class PIESPLUS_OT_view_selection(Operator):
    bl_idname = 'pies_plus.frame_selected_all'
    bl_label = "Frame Selected / All"
    bl_description = "Frames the selection if one exists, otherwise frames the entire scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.selected_objects:
            bpy.ops.view3d.view_selected()
        else:
            bpy.ops.view3d.view_all()
        return {'FINISHED'}


class PIESPLUS_OT_mesh_selection(Operator):
    """Selects or Deselects all visible objects in the scene.

        Specials:
    SHIFT - Select All
    CTRL  - Deselect All
    ALT    - Invert"""
    bl_idname = 'pies_plus.mesh_selection'
    bl_label = "Select / Deselect All"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if event.shift:
            if context.active_object:
                if context.object.mode == 'EDIT':
                    bpy.ops.mesh.select_all(action='SELECT')
                    return {'FINISHED'}
            bpy.ops.object.select_all(action='SELECT')

        elif event.ctrl:
            if context.active_object:
                if context.object.mode == 'EDIT':
                    bpy.ops.mesh.select_all(action='DESELECT')
                    return {'FINISHED'}
            bpy.ops.object.select_all(action='DESELECT')

        elif event.alt:
            if context.active_object:
                if context.object.mode == 'EDIT':
                    bpy.ops.mesh.select_all(action='INVERT')
                    return {'FINISHED'}
            bpy.ops.object.select_all(action='INVERT')

        else:
            if context.active_object:
                if context.object.mode == 'EDIT':
                    bpy.ops.mesh.select_all(action='TOGGLE')
                    return {'FINISHED'}
            bpy.ops.object.select_all(action='TOGGLE')
        return {'FINISHED'}


class PIESPLUS_OT_select_loop_inner_region(Operator):
    """Converts a loop selection to a filled face selection.

        Specials:
    ALT - Invert"""
    bl_idname = 'pies_plus.select_loop_inner_region'
    bl_label = "Select Loop Inner Region"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.mesh.loop_to_region(select_bigger=event.alt)
        bpy.ops.mesh.select_mode(type='FACE')
        return {'FINISHED'}

class PIESPLUS_OT_select_marked(Operator):
    bl_idname = 'pies_plus.select_marked_sharp'
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    markedChoice: EnumProperty(items=(('marked_sharp', "Sharps", ""),
                                      ('marked_seam', "Seams", "")),
                                      default='marked_sharp')

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh = context.object.data

        for edge in mesh.edges:
            if self.markedChoice == 'marked_sharp':
                if edge.use_edge_sharp:
                    edge.select = True
            else: # Seam
                if edge.use_seam:
                    edge.select = True

        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_view_selection,
           PIESPLUS_OT_mesh_selection,
           PIESPLUS_OT_select_loop_inner_region,
           PIESPLUS_OT_select_marked)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)