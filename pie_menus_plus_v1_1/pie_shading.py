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
from .__init__ import *
from bpy.types import Operator


    # Smoothing Stuff

def update_autoSmoothNormals(self, context):
    bpy.ops.object.mode_set(mode="OBJECT")
    
    if not context.selected_objects:
        context.active_object.select_set(True)

    if context.object.data.use_auto_smooth:
        context.object.data.use_auto_smooth = False
        bpy.ops.object.shade_flat()
    elif not context.object.data.use_auto_smooth:
        context.object.data.use_auto_smooth = True
        bpy.ops.object.shade_smooth()

bpy.types.Object.useAutoSmooth = bpy.props.BoolProperty(name="Auto Smoothing", default=False, update=update_autoSmoothNormals)

def update_autoSmoothAngle(self, context):
    context.object.data.auto_smooth_angle = context.object.smoothAngle * 3.14159 / 180
    context.object.useAutoSmooth = True
    context.object.data.use_auto_smooth = True
    bpy.ops.object.shade_smooth()

bpy.types.Object.smoothAngle = bpy.props.IntProperty(name="Smooth Angle", default=30, min=0, max=180, update=update_autoSmoothAngle)


    # Operators

class PIESPLUS_OT_solid_shading(Operator):
    bl_idname = "pies_plus.solid"
    bl_label = "Solid"
    bl_description = "Sets the viewport shading type to Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.space_data.shading.type = 'SOLID'
        return {'FINISHED'}


class PIESPLUS_OT_wire_shading(Operator):
    bl_idname = "pies_plus.wireframe"
    bl_label = "Wireframe"
    bl_description = "Sets the viewport shading type to Wireframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.preferences.addons[__package__].preferences.wireframeType_Pref == 'overlay':
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.overlay.show_wireframes:
                            space.overlay.show_wireframes = False
                        else:
                            space.overlay.show_wireframes = True
                        break
        else:
            context.space_data.shading.type = 'WIREFRAME'
        return {'FINISHED'}


class PIESPLUS_OT_wire_shading_per_obj(Operator):
    bl_idname = "pies_plus.wireframe_per_obj"
    bl_label = "Wireframe Toggle (per obj)"
    bl_description = "Turns on/off Wireframes for each selected object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.selected_objects:
            if not context.object.show_wire:
                ob.show_wire = True
            else:
                ob.show_wire = False
        return {'FINISHED'}


class PIESPLUS_OT_mat_preview_shading(Operator):
    bl_idname = "pies_plus.mat_preview"
    bl_label = "Material Preview"
    bl_description = "Sets the viewport shading type to Material Preview"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.space_data.shading.type = 'MATERIAL'
        return {'FINISHED'}


class PIESPLUS_OT_rendered_shading(Operator):
    bl_idname = "pies_plus.rendered"
    bl_label = "Rendered"
    bl_description = "Sets the viewport shading type to Rendered"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.space_data.shading.type = 'RENDERED'
        return {'FINISHED'}

class PIESPLUS_OT_recalc_normals(Operator):
    """    [BATCH] Recalculates the Active(s) Normals (individual faces in Edit Mode if selected)

    ALT  -  Invert"""
    bl_idname = 'pies_plus.recalc_normals'
    bl_label = "Recalculate Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        modeCallback = context.object.mode

        if context.mode == 'EDIT_MESH':
            context.view_layer.objects.active.select_set(True)
            for ob in context.selected_objects:
                ob.update_from_editmode()
                selected_polys = [x for x in ob.data.polygons if x.select]
                if selected_polys:
                    bpy.ops.mesh.select_mode(type='FACE')
                    bpy.ops.mesh.normals_make_consistent(inside=event.alt)
                    self.report({'INFO'}, "Recalculated Normals on Selected Faces")
                    return{'FINISHED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=event.alt)
        bpy.ops.mesh.select_all(action='DESELECT')
        self.report({'INFO'}, "Recalculated Normals on All Faces")

        bpy.ops.object.mode_set(mode = modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_shade_smooth(Operator):
    bl_idname = "pies_plus.shade_smooth"
    bl_label = "Shade Smooth"
    bl_description = "[BATCH] Changes the shading of the Active Object to smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        modeCallback = context.object.mode

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_smooth()

        bpy.ops.object.mode_set(mode = modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_shade_flat(Operator):
    bl_idname = "pies_plus.shade_flat"
    bl_label = "Shade Flat"
    bl_description = "[BATCH] Changes the shading of the Active Object to flat"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        modeCallback = context.object.mode

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_flat()

        bpy.ops.object.mode_set(mode = modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_auto_fwn(Operator):
    bl_idname = "pies_plus.auto_fwn"
    bl_label = "Add Weighted Normals"
    bl_description = "[BATCH] Automates assigning the Weighted Normals modifier to all selected meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        userPrefs = context.preferences.addons[__package__].preferences

        activeCallback = context.view_layer.objects.active

        modeCallback = context.object.mode
        
        bpy.ops.object.mode_set(mode='OBJECT')

        for ob in context.selected_objects:
            if ob.type == 'MESH':
                context.view_layer.objects.active = ob

                bpy.ops.object.shade_smooth()
                ob.data.use_auto_smooth = True
                context.object.smoothAngle = userPrefs.smoothAngle_Pref
                
                for mod in ob.modifiers:
                    if mod.type == 'WEIGHTED_NORMAL':
                        break
                else:
                    ob.modifiers.new('Weighted Normal', 'WEIGHTED_NORMAL')
                    ob.modifiers["Weighted Normal"].weight = userPrefs.weightValue_Pref
                    ob.modifiers["Weighted Normal"].keep_sharp = userPrefs.keepSharp_Pref

        context.view_layer.objects.active = activeCallback
        
        bpy.ops.object.mode_set(mode = modeCallback)
        
        self.report({'INFO'}, "Automatically FWN'd selection")
        return{'FINISHED'}


class PIESPLUS_OT_remove_custom_normals(Operator):
    bl_idname = "pies_plus.remove_custom_normals"
    bl_label = "Clear Custom Normals"
    bl_description = "Removes custom normals on all selected objects (useful for meshes imported with smoothing groups)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.selected_objects:
            
            activeCallback = context.view_layer.objects.active.name
            
            context.view_layer.objects.active = ob
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            
            context.view_layer.objects.active = bpy.data.objects[activeCallback]
        return{'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_solid_shading,
           PIESPLUS_OT_wire_shading_per_obj,
           PIESPLUS_OT_wire_shading,
           PIESPLUS_OT_mat_preview_shading,
           PIESPLUS_OT_rendered_shading,
           PIESPLUS_OT_recalc_normals,
           PIESPLUS_OT_shade_smooth,
           PIESPLUS_OT_shade_flat,
           PIESPLUS_OT_auto_fwn,
           PIESPLUS_OT_remove_custom_normals)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)