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


bl_info = {
    "name": "Pie Menus Plus",
    "description": "Additional / Improved Pie Menus for Blender 2.8+",
    "author": "Ethan Simon-Law",
    "version": (1, 1, 5),
    "blender": (2, 83, 0),
    "location": "View3D",
    "category": "3D View"}


import importlib
import bpy


module_names = ("ui",
                "prefs",
                "pie_modes",
                "pie_snapping",
                "pie_looptools",
                "pie_active_tools",
                "pie_origin_cursor",
                "pie_apply_transforms",
                "pie_selection",
                "pie_shading",
                "pie_proportional",
                "pie_keyframing")
modules = []

for module_name in module_names:
    if module_name in locals():
        modules.append(importlib.reload(locals()[module_name]))
    else:
        modules.append(importlib.import_module(
            "." + module_name, package=__package__))


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
