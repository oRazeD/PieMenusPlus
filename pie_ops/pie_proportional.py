import bpy
from ..razeds_bpy_utils.utils.generic import OpInfo


class PIESPLUS_OT_change_proportional_falloff(OpInfo, bpy.types.Operator):
    bl_idname = "pies_plus.change_proportional_falloff"
    bl_label = "Change Proportional Falloff"
    bl_description = "Changes the proportional editing falloff to the selected type"

    falloff_type: bpy.props.EnumProperty(
        items=(
            ('SMOOTH', "Smooth", ""),
            ('SPHERE', "Sphere", ""),
            ('ROOT', "Root", ""),
            ('INVERSE_SQUARE', "Inverse Square", ""),
            ('SHARP', "Sharp", ""),
            ('LINEAR', "Linear", ""),
            ('CONSTANT', "Constant", ""),
            ('RANDOM', "Random", "")
        ),
        name='Falloff Type'
    )

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True

        ts.proportional_edit_falloff = self.falloff_type
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_change_proportional_falloff)


def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_change_proportional_falloff)


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
