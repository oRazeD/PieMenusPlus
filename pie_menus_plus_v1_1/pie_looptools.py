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


class PIESPLUS_OT_looptools(bpy.types.Operator):
    bl_idname = "pies_plus.looptools"
    bl_label = "LoopTools"
    bl_description = "Runs the corresponding selected LoopTools operation"
    bl_options = {'REGISTER', 'UNDO'}

    lt_func: EnumProperty(items=(('lt_bridge', "Bridge", ""),
               ('lt_circle', "Circle", ""),
               ('lt_curve', "Curve", ""),
               ('lt_flatten', "Flatten", ""),
               ('lt_gstretch', "GStretch", ""),
               ('lt_loft', "Loft", ""),
               ('lt_relax', "Relax", ""),
               ('lt_space', "Space", "")),
               default='lt_bridge')

    def execute(self, context):
        if self.lt_func == 'lt_bridge':
            bpy.ops.mesh.looptools_bridge('INVOKE_DEFAULT')
        elif self.lt_func == 'lt_circle':
            bpy.ops.mesh.looptools_circle('INVOKE_DEFAULT')
        elif self.lt_func == 'lt_curve':
            bpy.ops.mesh.looptools_curve('INVOKE_DEFAULT')
        elif self.lt_func == 'lt_flatten':
            bpy.ops.mesh.looptools_flatten('INVOKE_DEFAULT')
        elif self.lt_func == 'lt_gstretch':
            bpy.ops.mesh.looptools_gstretch('INVOKE_DEFAULT')
        elif self.lt_func == 'lt_loft':
            bpy.ops.mesh.looptools_loft('INVOKE_DEFAULT')
        elif self.lt_func == 'lt_relax':
            bpy.ops.mesh.looptools_relax('INVOKE_DEFAULT')
        else: # Space
            bpy.ops.mesh.looptools_space('INVOKE_DEFAULT')
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_looptools)

def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_looptools)