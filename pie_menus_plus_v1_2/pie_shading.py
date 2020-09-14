import bpy
from bpy.types import Operator


class PIESPLUS_OT_auto_smooth(Operator):
    bl_idname = "pies_plus.auto_smooth"
    bl_label = " Auto Smooth+"
    bl_description = "[BATCH] Automation for setting up meshes with Auto Smooth Normals. Also turns on Shade Smooth as it is a prerequisite for ASN"
    bl_options = {'UNDO'}

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report({'ERROR'}, "Nothing is selected & there is no Active Object")
            return{'FINISHED'}

        if context.active_object:
            modeCallback = context.object.mode

            bpy.ops.object.mode_set(mode="OBJECT")

        for ob in context.selected_objects:
            if ob.type == 'MESH':
                ob.data.use_auto_smooth = True

                ob.data.auto_smooth_angle = context.scene.pies_plus.smoothAngle * 3.14159 / 180
            
        bpy.ops.object.shade_smooth()

        if 'modeCallback' in locals():
            bpy.ops.object.mode_set(mode = modeCallback)
        return {'FINISHED'}


class PIESPLUS_OT_remove_auto_smooth(Operator):
    bl_idname = "pies_plus.remove_auto_smooth"
    bl_label = ""
    bl_description = "[Batch] An 'undo' for Quick Smooth, sets to Shade Flat as well"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report({'ERROR'}, "Nothing is selected & there is no Active Object")
            return{'FINISHED'}

        if context.active_object:
            modeCallback = context.object.mode

            bpy.ops.object.mode_set(mode="OBJECT")

        for ob in context.selected_objects:
            if ob.type == 'MESH':
                ob.data.use_auto_smooth = False

        if context.preferences.addons[__package__].preferences.autoSmoothShadeFlat_Pref:
            bpy.ops.object.shade_flat()

        if 'modeCallback' in locals():
            bpy.ops.object.mode_set(mode = modeCallback)
        return {'FINISHED'}


class PIESPLUS_OT_wire_per_obj(Operator):
    bl_idname = "pies_plus.wire_per_obj"
    bl_label = "Wireframe (per obj)"
    bl_description = "Toggle per-object wireframes for all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.selected_objects:
            ob.show_wire = not ob.show_wire
        return {'FINISHED'}


class PIESPLUS_OT_remove_wire_per_obj(Operator):
    bl_idname = "pies_plus.remove_wire_per_obj"
    bl_label = ""
    bl_description = "Remove per-object wireframes from all selected objects"
    bl_options = {'UNDO'}

    def execute(self, context):
        for ob in context.selected_objects:
            ob.show_wire = False
        return {'FINISHED'}


class PIESPLUS_OT_recalc_normals(Operator):
    """    [BATCH] Recalculates the Active(s) Normals (individual faces in Edit Mode if selected)

        Specials:
    ALT  -  Invert"""
    bl_idname = 'pies_plus.recalc_normals'
    bl_label = "Recalculate Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if not context.selected_objects and not context.active_object:
            self.report({'ERROR'}, "Nothing is selected & there is no Active Object")
            return{'FINISHED'}

        if context.active_object:
            if context.object.type != 'MESH':
                self.report({'ERROR'}, "The Active Object is not a mesh")
                return{'FINISHED'}
        else:
            for ob in context.selected_objects:
                context.view_layer.objects.active = ob
                break

        modeCallback = context.object.mode

        if context.mode == 'EDIT_MESH':
            context.view_layer.objects.active.select_set(True)
            for ob in context.selected_objects:
                if ob.type == 'MESH':
                    ob.update_from_editmode()

                    selected_polys = [x for x in ob.data.polygons if x.select]
                    if selected_polys:
                        bpy.ops.mesh.select_mode(type='FACE')
                        bpy.ops.mesh.normals_make_consistent(inside=event.alt)
                        self.report({'INFO'}, "Recalculated Normals on selected faces")
                        return{'FINISHED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=event.alt)
        bpy.ops.mesh.select_all(action='DESELECT')
        self.report({'INFO'}, "Recalculated Normals on all faces")

        if 'modeCallback' in locals():
            bpy.ops.object.mode_set(mode = modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_shade_smooth(Operator):
    bl_idname = "pies_plus.shade_smooth"
    bl_label = "Shade Smooth"
    bl_description = "[BATCH] Changes the shading of the selected objects to smooth"
    bl_options = {'UNDO'}

    def execute(self,context):
        if context.active_object:
            modeCallback = context.object.mode

            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_smooth()

        if 'activeCallback' in locals():
            bpy.ops.object.mode_set(mode = modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_shade_flat(Operator):
    bl_idname = "pies_plus.shade_flat"
    bl_label = "Shade Flat"
    bl_description = "[BATCH] Changes the shading of the selected objects to flat"
    bl_options = {'UNDO'}

    def execute(self,context):
        if context.active_object:
            modeCallback = context.object.mode

            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_flat()

        if 'activeCallback' in locals():
            bpy.ops.object.mode_set(mode = modeCallback)
        return{'FINISHED'}


class PIESPLUS_OT_auto_fwn(Operator):
    bl_idname = "pies_plus.auto_fwn"
    bl_label = "Quick Weighted Normals"
    bl_description = "[BATCH] Automates assigning the Weighted Normals modifier to all selected meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report({'ERROR'}, "Nothing is selected & there is no Active Object")
            return{'FINISHED'}

        pies_plus_prefs = context.preferences.addons[__package__].preferences

        if context.active_object:
            activeCallback = context.view_layer.objects.active

            modeCallback = context.object.mode
        
            bpy.ops.object.mode_set(mode='OBJECT')

        for ob in context.selected_objects:
            if ob.type == 'MESH':
                context.view_layer.objects.active = ob

                bpy.ops.object.shade_smooth()
                ob.data.use_auto_smooth = True
                ob.data.auto_smooth_angle = pies_plus_prefs.smoothAngle_Pref
                
                for mod in ob.modifiers:
                    if mod.type == 'WEIGHTED_NORMAL':
                        break
                else:
                    ob.modifiers.new('Weighted Normal', 'WEIGHTED_NORMAL')
                    ob.modifiers["Weighted Normal"].weight = pies_plus_prefs.weightValue_Pref
                    ob.modifiers["Weighted Normal"].keep_sharp = pies_plus_prefs.keepSharp_Pref
                    ob.modifiers["Weighted Normal"].face_influence = pies_plus_prefs.faceInf_Pref

        if 'activeCallback' in locals():
            context.view_layer.objects.active = activeCallback
            
            bpy.ops.object.mode_set(mode = modeCallback)
        
        self.report({'INFO'}, "Automatically Face Weighted selection")
        return{'FINISHED'}


class PIESPLUS_OT_remove_custom_normals(Operator):
    bl_idname = "pies_plus.remove_custom_normals"
    bl_label = "Clear Custom Normals"
    bl_description = "Removes custom normals on all selected objects (useful for meshes imported with smoothing groups)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report({'ERROR'}, "Nothing is selected & there is no Active Object")
            return{'FINISHED'}

        if context.active_object:
            activeCallback = context.view_layer.objects.active.name

        for ob in context.selected_objects:
            context.view_layer.objects.active = ob
            bpy.ops.mesh.customdata_custom_splitnormals_clear()

        if 'activeCallback' in locals():
            context.view_layer.objects.active = bpy.data.objects[activeCallback]
        return{'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_auto_smooth,
           PIESPLUS_OT_remove_auto_smooth,
           PIESPLUS_OT_wire_per_obj,
           PIESPLUS_OT_remove_wire_per_obj,
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