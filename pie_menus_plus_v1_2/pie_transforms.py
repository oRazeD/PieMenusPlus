import bpy
from bpy.props import EnumProperty


class PIESPLUS_OT_transforms(bpy.types.Operator):
    bl_idname = "pies_plus.transforms"
    bl_label = "Apply / Clear Transforms"
    bl_description = "Applys / Clears transforms based on the selected method"
    bl_options = {'REGISTER', 'UNDO'}

    tranforms_type: EnumProperty(items=(('apply_loc', "Apply Location", ""),
                                          ('apply_rot', "Apply Rotation", ""),
                                          ('apply_scale', "Apply Scale", ""),
                                          ('apply_rot_scale', "Apply Rot & Scale", ""),
                                          ('apply_all', "Apply All", ""),
                                          ('clear_all', "Clear All", "")), name = 'Transform Type')

    def execute(self, context):
        if self.tranforms_type == 'apply_loc':
            bpy.ops.object.transform_apply(rotation=False, scale=False)

        elif self.tranforms_type == 'apply_rot':
            bpy.ops.object.transform_apply(location=False, scale=False)

        elif self.tranforms_type == 'apply_scale':
            bpy.ops.object.transform_apply(location=False, rotation=False)

        elif self.tranforms_type == 'apply_rot_scale':
            bpy.ops.object.transform_apply(location=False)

        elif self.tranforms_type == 'apply_all':
            bpy.ops.object.transform_apply()

        else:
            for ob in context.selected_objects:
                ob.rotation_euler, ob.location, ob.scale = (0,0,0), (0,0,0), (1,1,1)
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_transforms)

def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_transforms)


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