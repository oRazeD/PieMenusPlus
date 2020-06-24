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
from bpy.props import EnumProperty


class PIESPLUS_OT_apply_clear_transforms(bpy.types.Operator):
    bl_idname = "pies_plus.apply_transforms"
    bl_label = "Apply Transforms"
    bl_description = "Applys / Clears transforms with the corresponding selected method"
    bl_options = {'REGISTER', 'UNDO'}

    apply_transforms: EnumProperty(items=(('apply_loc', "Apply Location", ""),
                                          ('apply_rot', "Apply Rotation", ""),
                                          ('apply_scale', "Apply Scale", ""),
                                          ('apply_rot_scale', "Apply Rot & Scale", ""),
                                          ('apply_all', "Apply All", ""),
                                          ('clear_all', "Clear All", "")))

    def execute(self, context):
        if self.apply_transforms == 'apply_loc':
            bpy.ops.object.transform_apply(rotation=False, scale=False)

        elif self.apply_transforms == 'apply_rot':
            bpy.ops.object.transform_apply(location=False, scale=False)

        elif self.apply_transforms == 'apply_scale':
            bpy.ops.object.transform_apply(location=False, rotation=False)

        elif self.apply_transforms == 'apply_rot_scale':
            bpy.ops.object.transform_apply(location=False)

        elif self.apply_transforms == 'apply_all':
            bpy.ops.object.transform_apply()

        else:
            for ob in context.selected_objects:
                ob.rotation_euler, ob.location, ob.scale = (0,0,0), (0,0,0), (1,1,1)
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_apply_clear_transforms)

def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_apply_clear_transforms)