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
from .__init__ import *


class PIESPLUS_OT_active_tools(bpy.types.Operator):
    bl_idname = "pies_plus.active_tools"
    bl_label = "Active Tools"
    bl_description = "Changes the Active Tool / Gizmo to the corresponding selected option"
    bl_options = {'REGISTER', 'UNDO'}

    active_tools: EnumProperty(
        items=(('tool_transform', "Transform", ""),
               ('tool_move', "Move", ""),
               ('tool_rotate', "Rotate", ""),
               ('tool_scale', "Scale", ""),
               ('gizmo_transform', "Transform", ""),
               ('gizmo_move', "Move", ""),
               ('gizmo_rotate', "Rotate", ""),
               ('gizmo_scale', "Scale", ""),
               ('select_tweak', "Select", ""),
               ('select_circle', "Select Circle", ""),
               ('select_lasso', "Select Lasso", ""),
               ('select_box', "select Box", ""),
               ('cursor', "Cursor", "")),
               default='tool_transform')

    def execute(self, context):
        # Affect Tool
        if self.active_tools == 'tool_transform':
            bpy.ops.wm.tool_set_by_id(name="builtin.transform")

        elif self.active_tools == 'tool_move':
            bpy.ops.wm.tool_set_by_id(name="builtin.move")

        elif self.active_tools == 'tool_rotate':
            bpy.ops.wm.tool_set_by_id(name="builtin.rotate")

        elif self.active_tools == 'tool_scale':
            bpy.ops.wm.tool_set_by_id(name="builtin.scale")

        # Affect Gizmo
        elif self.active_tools == 'gizmo_transform':
            bpy.ops.view3d.transform_gizmo_set(type={'TRANSLATE', 'ROTATE', 'SCALE'})

        elif self.active_tools == 'gizmo_move':
            bpy.ops.view3d.transform_gizmo_set(type={'TRANSLATE'})

        elif self.active_tools == 'gizmo_rotate':
            bpy.ops.view3d.transform_gizmo_set(type={'ROTATE'})

        elif self.active_tools == 'gizmo_scale':
            bpy.ops.view3d.transform_gizmo_set(type={'SCALE'})

        # Selection Type
        elif self.active_tools == 'select_tweak':
            bpy.ops.wm.tool_set_by_id(name="builtin.select")

        elif self.active_tools == 'select_circle':
            bpy.ops.wm.tool_set_by_id(name="builtin.select_circle")

        elif self.active_tools == 'select_lasso':
            bpy.ops.wm.tool_set_by_id(name="builtin.select_lasso")

        elif self.active_tools == 'select_box':
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")

        else: # 3D Cursor
            bpy.ops.wm.tool_set_by_id(name="builtin.cursor")

        defaultToolPref = context.preferences.addons[__package__].preferences.defaultTool_Pref
        tools = context.workspace.tools
        current_active_tool = tools.from_space_view3d_mode(context.mode).idname

        if self.active_tools.startswith("gizmo"):
            if current_active_tool not in {'builtin.select', 'builtin.select_box', 'builtin.select_circle', 'builtin.select_lasso'}:
                if defaultToolPref == 'tweak_select':
                    bpy.ops.wm.tool_set_by_id(name="builtin.select")
                elif defaultToolPref == 'box_select':
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                elif defaultToolPref == 'circle_select':
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_circle")
                else: # Lasso
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_lasso")
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_active_tools)

def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_active_tools)