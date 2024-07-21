import bpy
from bpy.types import Operator

from ..utils import OpInfo, get_addon_preferences


class PIESPLUS_OT_auto_smooth(Operator):
    """Automation for setting up meshes with
    Auto Smooth Normals. Also turns on Shade Smooth"""
    bl_idname = "pies_plus.auto_smooth"
    bl_label = " Auto Smooth"
    bl_description = ""
    bl_options = {'UNDO'}

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report(
                {'ERROR'}, "Nothing is selected & there is no Active Object"
            )
            return{'FINISHED'}

        if context.active_object:
            saved_mode = context.object.mode
            bpy.ops.object.mode_set(mode="OBJECT")

        angle = context.scene.pies_plus.smoothAngle * 3.14159 / 180
        bpy.ops.object.shade_auto_smooth(use_auto_smooth=True, angle=angle)

        if 'saved_mode' in locals():
            bpy.ops.object.mode_set(mode = saved_mode)
        return {'FINISHED'}


class PIESPLUS_OT_wire_per_obj(OpInfo, Operator):
    bl_idname = "pies_plus.wire_per_obj"
    bl_label = "Wire Overlay Per Object"
    bl_description = "Toggle per-object wireframes for all selected objects"

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


class PIESPLUS_OT_recalc_normals(OpInfo, Operator):
    """Recalculates Active Object vertex normals (selected faces if in Edit Mode)

        Specials:
    ALT  -  Inside"""
    bl_idname = 'pies_plus.recalc_normals'
    bl_label = "Recalculate Normals"

    calc_inverse: bpy.props.BoolProperty(default=False, name='Inside', description='Calculate the inverse')

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def invoke(self, context, event):
        self.calc_inverse = event.alt
        return self.execute(context)

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.mesh.normals_make_consistent(inside=self.calc_inverse)
            self.report({'INFO'}, "Recalculated vertex normals on selected faces")
            return{'FINISHED'}

        saved_mode = context.object.mode

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=self.calc_inverse)
        bpy.ops.mesh.select_all(action='DESELECT')
        self.report({'INFO'}, "Recalculated vertex normals on all faces")

        if 'saved_mode' in locals():
            bpy.ops.object.mode_set(mode = saved_mode)
        return{'FINISHED'}


class PIESPLUS_OT_shade_smooth(Operator):
    bl_idname = "pies_plus.shade_smooth"
    bl_label = "Shade Smooth"
    bl_description = "Changes the shading of the selected objects to smooth"
    bl_options = {'UNDO'}

    def execute(self,context):
        if context.active_object:
            saved_mode = context.object.mode

            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_smooth()

        if 'saved_active' in locals():
            bpy.ops.object.mode_set(mode = saved_mode)
        return{'FINISHED'}


class PIESPLUS_OT_shade_flat(Operator):
    bl_idname = "pies_plus.shade_flat"
    bl_label = "Shade Flat"
    bl_description = "Changes the shading of the selected objects to flat"
    bl_options = {'UNDO'}

    def execute(self,context):
        if context.active_object:
            saved_mode = context.object.mode

            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_flat()

        if 'saved_active' in locals():
            bpy.ops.object.mode_set(mode = saved_mode)
        return{'FINISHED'}


class PIESPLUS_OT_auto_fwn(OpInfo, Operator):
    bl_idname = "pies_plus.auto_fwn"
    bl_label = "Quick Weighted Normals"
    bl_description = "Automates assigning the Weighted Normals modifier to all selected meshes"

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report(
                {'ERROR'}, "Nothing is selected & there is no Active Object"
            )
            return{'FINISHED'}

        pies_plus_prefs = get_addon_preferences()

        if context.active_object:
            saved_active = context.view_layer.objects.active
            saved_mode = context.object.mode
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.shade_auto_smooth(True, 3.14159)

        for ob in context.selected_objects:
            if ob.type != 'MESH':
                continue
            context.view_layer.objects.active = ob
            for mod in ob.modifiers:
                if mod.type == 'WEIGHTED_NORMAL':
                    break
            else:
                ob.modifiers.new('Weighted Normal', 'WEIGHTED_NORMAL')
                ob.modifiers["Weighted Normal"].weight = \
                    pies_plus_prefs.fwn_weight_value_pref
                ob.modifiers["Weighted Normal"].keep_sharp = \
                    pies_plus_prefs.fwn_keep_sharps_pref
                if bpy.app.version >= (2, 91, 0):
                    ob.modifiers["Weighted Normal"].use_face_influence = \
                        pies_plus_prefs.fwn_face_influence_pref
                else:
                    ob.modifiers["Weighted Normal"].face_influence = \
                        pies_plus_prefs.fwn_face_influence_pref

        if 'saved_active' in locals():
            context.view_layer.objects.active = saved_active

            bpy.ops.object.mode_set(mode = saved_mode)

        self.report({'INFO'}, "Automatically Face Weighted selection")
        return{'FINISHED'}


class PIESPLUS_OT_remove_custom_normals(OpInfo, Operator):
    bl_idname = "pies_plus.remove_custom_normals"
    bl_label = "Clear Custom Normals"
    bl_description = "Removes custom normals on all selected objects (useful for meshes imported with smoothing groups)"

    def execute(self, context):
        if not context.selected_objects and not context.active_object:
            self.report({'ERROR'}, "Nothing is selected & there is no Active Object")
            return{'FINISHED'}

        if context.active_object:
            saved_active = context.view_layer.objects.active.name

        for ob in context.selected_objects:
            if ob.type == 'MESH':
                context.view_layer.objects.active = ob
                bpy.ops.mesh.customdata_custom_splitnormals_clear()

        if 'saved_active' in locals():
            context.view_layer.objects.active = bpy.data.objects[saved_active]
        return{'FINISHED'}


##############################
#   REGISTRATION
##############################


classes = (
    PIESPLUS_OT_auto_smooth,
    PIESPLUS_OT_wire_per_obj,
    PIESPLUS_OT_remove_wire_per_obj,
    PIESPLUS_OT_recalc_normals,
    PIESPLUS_OT_shade_smooth,
    PIESPLUS_OT_shade_flat,
    PIESPLUS_OT_auto_fwn,
    PIESPLUS_OT_remove_custom_normals
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
