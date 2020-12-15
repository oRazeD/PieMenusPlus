import bpy
from bpy.types import Operator


class PIESPLUS_OT_edit_mode(Operator):
    bl_idname = "pies_plus.edit_mode"
    bl_label = "Object Mode"
    bl_description = "Changes the Context Mode to Object Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.view_layer.objects.active = context.selected_objects[0]

        bpy.ops.object.mode_set(mode="EDIT")
        return {'FINISHED'}


class PIESPLUS_OT_particle_edit(Operator):
    bl_idname = "pies_plus.particle_edit"
    bl_label = "Particle Edit"
    bl_description = "Changes the Context Mode to Particle Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.particle.particle_edit_toggle()
        return {'FINISHED'}


class PIESPLUS_OT_vertex(Operator):
    """Changes the selection mode to Vertex Select.

        Specials:
    SHIFT - Extend"""
    bl_idname = "pies_plus.vertex"
    bl_label = "Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(use_extend=event.shift, type='VERT')
        return {'FINISHED'}


class PIESPLUS_OT_edge(Operator):
    """Changes the selection mode to Edge Select.

        Specials:
    SHIFT - Extend"""
    bl_idname = "pies_plus.edge"
    bl_label = "Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(use_extend=event.shift, type='EDGE')
        return {'FINISHED'}


class PIESPLUS_OT_face(Operator):
    """Changes the selection mode to Face Select.

        Specials:
    SHIFT - Extend"""
    bl_idname = "pies_plus.face"
    bl_label = "Face"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(use_extend=event.shift, type='FACE')
        return {'FINISHED'}


class PIESPLUS_OT_UV_sel_change(Operator):
    bl_idname = "pies_plus.uv_sel_change"
    bl_label = "UV Selection Change"
    bl_description = "Changes the UV selection mode to whatever option is selected"
    bl_options = {'REGISTER'}

    sel_choice: bpy.props.EnumProperty(items=(('vertex', "Vertex", ""),
                                              ('edge', "Edge", ""),
                                              ('face', "Face", ""),
                                              ('island', "Island", "")),
                                              default='vertex', name = 'Selection Choice')

    def execute(self, context):
        context.scene.tool_settings.uv_select_mode = self.sel_choice.upper()
        return {'FINISHED'}


class PIESPLUS_OT_overlays(Operator):
    bl_idname = "pies_plus.overlay"
    bl_label = "Overlay Toggle"
    bl_description = "Toggles the viewport Overlays"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.space_data.overlay.show_overlays = not context.space_data.overlay.show_overlays
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_edit_mode,
           PIESPLUS_OT_particle_edit,
           PIESPLUS_OT_vertex,
           PIESPLUS_OT_edge,
           PIESPLUS_OT_face,
           PIESPLUS_OT_UV_sel_change,
           PIESPLUS_OT_overlays)

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