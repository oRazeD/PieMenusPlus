import bpy
from bpy.types import Operator
from bpy.props import EnumProperty


class PIESPLUS_OT_object_mode(Operator):
    bl_idname = "pies_plus.object_mode"
    bl_label = "Object Mode"
    bl_description = "Changes the Context Mode to Object Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}


class PIESPLUS_OT_texture_paint(Operator):
    bl_idname = "pies_plus.texture_paint"
    bl_label = "Texture Paint"
    bl_description = "Changes the Context Mode to Texture Paint Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


class PIESPLUS_OT_weight_paint(Operator):
    bl_idname = "pies_plus.weight_paint"
    bl_label = "Weight Paint"
    bl_description = "Changes the Context Mode to Weight Paint Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.paint.weight_paint_toggle()
        return {'FINISHED'}


class PIESPLUS_OT_vertex_paint(Operator):
    bl_idname = "pies_plus.vertex_paint"
    bl_label = "Vertex Paint"
    bl_description = "Changes the Context Mode to Vertex Paint Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.paint.vertex_paint_toggle()
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
    bl_label = "UV Sel Change"
    bl_description = "Changes the UV selection mode to the selected mode"
    bl_options = {'REGISTER', 'UNDO'}

    sel_choice: EnumProperty(items=(('sel_vert', "Vertex", ""),
                                    ('sel_edge', "Edge", ""),
                                    ('sel_face', "Face", ""),
                                    ('sel_island', "Island", "")),
                                    default='sel_vert')

    def execute(self, context):
        if self.sel_choice == 'sel_vert':
            context.scene.tool_settings.uv_select_mode = 'VERTEX'
        elif self.sel_choice == 'sel_edge':
            context.scene.tool_settings.uv_select_mode = 'EDGE'
        elif self.sel_choice == 'sel_face':
            context.scene.tool_settings.uv_select_mode = 'FACE'
        else: # Island
            context.scene.tool_settings.uv_select_mode = 'ISLAND'
        return {'FINISHED'}


class PIESPLUS_OT_overlays(Operator):
    bl_idname = "pies_plus.overlay"
    bl_label = "Overlay Toggle"
    bl_description = "Toggles the viewport Overlays"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.space_data.overlay.show_overlays:
            context.space_data.overlay.show_overlays = True
        else:
            context.space_data.overlay.show_overlays = False
        return {'FINISHED'}


class PIESPLUS_OT_xray(Operator):
    bl_idname = "pies_plus.xray"
    bl_label = "X-Ray Toggle"
    bl_description = "Toggles the viewport X-Ray"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.space_data.shading.type == 'SOLID' or context.space_data.shading.type == 'WIREFRAME':
            bpy.ops.view3d.toggle_xray()
        else:
            self.report({'INFO'}, "X-Ray not available in current mode")
        return {'FINISHED'}


class PIESPLUS_OT_auto_active(Operator):
    bl_idname = "pies_plus.auto_active"
    bl_label = "Auto-Select Active"
    bl_description = "Automatically selects the Active Object from one of the currently selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.selected_objects:
            context.view_layer.objects.active = ob
            break
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_object_mode,
           PIESPLUS_OT_texture_paint,
           PIESPLUS_OT_weight_paint,
           PIESPLUS_OT_vertex_paint,
           PIESPLUS_OT_particle_edit,
           PIESPLUS_OT_vertex,
           PIESPLUS_OT_edge,
           PIESPLUS_OT_face,
           PIESPLUS_OT_UV_sel_change,
           PIESPLUS_OT_overlays,
           PIESPLUS_OT_xray,
           PIESPLUS_OT_auto_active)

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