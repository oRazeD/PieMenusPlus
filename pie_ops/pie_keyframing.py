import bpy
from utils import OpInfo


class PIESPLUS_OT_keyframing(OpInfo, bpy.types.Operator):
    bl_idname = "pies_plus.keyframing"
    bl_label = "Keyframing"
    bl_description = "Keyframes to the corresponding selected option"

    key_choice: bpy.props.EnumProperty(
        items=(
            ('key_loc', "Location", ""),
            ('key_rot', "Rotation", ""),
            ('key_scale', "Scale", ""),
            ('key_locrot', "LocRot", ""),
            ('key_locrotscale', "LocRotScale", ""),
            ('key_locscale', "LocScale", ""),
            ('key_rotscale', "RotScale", ""),
            ('key_vis_loc', "Visual Location", ""),
            ('key_vis_rot', "Visual Rotation", ""),
            ('key_vis_scale', "Visual Scale", ""),
            ('key_vis_locrot', "Visual LocRot", ""),
            ('key_vis_locrotscale',"Visual LocRotScale", ""),
            ('key_vis_locscale', "Visual LocScale", ""),
            ('key_vis_rotscale', "Visual RotScale", ""),
            ('key_del_loc', "Delta Location", ""),
            ('key_del_rot', "Delta Rotation", ""),
            ('key_del_scale', "Delta Scale", ""),
            ('key_available', "Available", ""),
            ('key_bendy_bones', "BBone Shape", ""),
            ('key_whole_char', "Whole Character", ""),
            ('key_whole_char_sel', "Whole Character Selected", "")
        ),
        default='key_loc',
        name='Keyframe Type'
    )

    def execute(self, context):
        # Non-visual
        if self.key_choice == 'key_loc':
            bpy.ops.anim.keyframe_insert_menu(type='Location')
        elif self.key_choice == 'key_rot':
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        elif self.key_choice == 'key_scale':
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        elif self.key_choice == 'key_locrot':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
        elif self.key_choice == 'key_locrotscale':
            bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        elif self.key_choice == 'key_locscale':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocScale')
        elif self.key_choice == 'key_rotscale':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_RotScale')

        # Visual
        elif self.key_choice == 'key_vis_loc':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLoc')
        elif self.key_choice == 'key_vis_rot':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualRot')
        elif self.key_choice == 'key_vis_scale':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualScaling')
        elif self.key_choice == 'key_vis_locrot':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
        elif self.key_choice == 'key_vis_locrotscale':
            bpy.ops.anim.keyframe_insert_menu(
                type='BUILTIN_KSI_VisualLocRotScale')
        elif self.key_choice == 'key_vis_locscale':
            bpy.ops.anim.keyframe_insert_menu(
                type='BUILTIN_KSI_VisualLocScale')
        elif self.key_choice == 'key_vis_rotscale':
            bpy.ops.anim.keyframe_insert_menu(
                type='BUILTIN_KSI_VisualRotScale')

        # Delta
        elif self.key_choice == 'key_del_loc':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_DeltaLocation')
        elif self.key_choice == 'key_del_rot':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_DeltaRotation')
        elif self.key_choice == 'key_del_scale':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_DeltaScale')

        # Others
        elif self.key_choice == 'key_available':
            try:
                bpy.ops.anim.keyframe_insert_menu(type='Available')
            except:
                self.report({'ERROR'}, "No suitable context info for active keying set")
        elif self.key_choice == 'key_bendy_bones':
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_BendyBones')
        elif self.key_choice == 'key_whole_char':
            bpy.ops.anim.keyframe_insert_menu(type='WholeCharacter')
        elif self.key_choice == 'key_whole_char_sel':
            bpy.ops.anim.keyframe_insert_menu(type='WholeCharacterSelected')
        return {'FINISHED'}


##############################
#   REGISTRATION
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_keyframing)


def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_keyframing)


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
