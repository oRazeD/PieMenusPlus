import bpy
from bpy.types import Operator
from ..razeds_bpy_utils.utils.generic import OpInfo


class PIESPLUS_OT_separate(OpInfo, Operator):
    bl_idname = "pies_plus.separate"
    bl_label = "Separate"
    bl_description = "Separate selected geometry into a new mesh"

    type: bpy.props.EnumProperty(
        items=( # Following source code conventions, ugh
            ('SELECTED', "Selection", ""),
            ('MATERIAL', "By Material", ""),
            ('LOOSE', "By Loose Parts", "")
        ),
        name='Type'
    )

    remove_mods: bpy.props.BoolProperty(default=False, name='Remove Modifiers')

    def execute(self, context):
        if self.remove_mods:
            saved_ob_list = context.selected_objects.copy()

        bpy.ops.mesh.separate(type=self.type)

        if not self.remove_mods:
            return{'FINISHED'}

        for ob in context.selected_objects:
            if ob not in saved_ob_list:
                for mod in ob.modifiers:
                    ob.modifiers.remove(mod)
        return{'FINISHED'}


class PIESPLUS_MT_separate(bpy.types.Menu):
    bl_idname = "PIESPLUS_MT_separate"
    bl_label = "Separate"

    def draw(self, context):
        layout = self.layout
        layout.operator_enum("pies_plus.separate", "type")


##############################
#   REGISTRATION    
##############################


classes = (
    PIESPLUS_OT_separate,
    PIESPLUS_MT_separate
)

addon_keymaps = []
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