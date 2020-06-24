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
from bpy.types import Operator


class PIESPLUS_OT_proportional_smooth(Operator):
    bl_idname = "proportional.smooth"
    bl_label = "Smooth"
    bl_description = "Changes the proportional editing method to Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'SMOOTH'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_sphere(Operator):
    bl_idname = "proportional.sphere"
    bl_label = "Sphere"
    bl_description = "Changes the proportional editing method to Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'SPHERE'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_root(Operator):
    bl_idname = "proportional.root"
    bl_label = "Root"
    bl_description = "Changes the proportional editing method to Root"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'ROOT'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_sharp(Operator):
    bl_idname = "proportional.sharp"
    bl_label = "Sharp"
    bl_description = "Changes the proportional editing method to Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'SHARP'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_linear(Operator):
    bl_idname = "proportional.linear"
    bl_label = "Linear"
    bl_description = "Changes the proportional editing method to Linear"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'LINEAR'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_constant(Operator):
    bl_idname = "proportional.constant"
    bl_label = "Constant"
    bl_description = "Changes the proportional editing method to Constant"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'CONSTANT'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_random(Operator):
    bl_idname = "proportional.random"
    bl_label = "Random"
    bl_description = "Changes the proportional editing method to Random"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'RANDOM'
        return {'FINISHED'}


class PIESPLUS_OT_proportional_inverse_square(Operator):
    bl_idname = "proportional.inverse_square"
    bl_label = "Inverse Square"
    bl_description = "Changes the proportional editing method to Inverse Square"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        if context.mode == 'OBJECT':
            ts.use_proportional_edit_objects = True
        else:
            ts.use_proportional_edit = True
        ts.proportional_edit_falloff = 'INVERSE_SQUARE'
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_proportional_smooth,
           PIESPLUS_OT_proportional_sphere,
           PIESPLUS_OT_proportional_root,
           PIESPLUS_OT_proportional_sharp,
           PIESPLUS_OT_proportional_linear,
           PIESPLUS_OT_proportional_constant,
           PIESPLUS_OT_proportional_random,
           PIESPLUS_OT_proportional_inverse_square)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)