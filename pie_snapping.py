import bpy
from bpy.props import EnumProperty


class PIESPLUS_OT_snapping(bpy.types.Operator):
    bl_idname = "pies_plus.snap"
    bl_label = "Snapping"
    bl_description = "Changes the snapping setting to the corresponding selected option"
    bl_options = {'REGISTER', 'UNDO'}

    snap_elements : EnumProperty(
        items=(('vertex', "Vertex", ""),
               ('edge', "Edge", ""),
               ('face', "Face", ""),
               ('increment', "Increment", ""),
               ('volume', "Volume", ""),
               ('edge_center', "Edge Center", ""),
               ('edge_perp', "Edge Perpendicular", ""),
               ('uv_increment', "UV Increment", ""),
               ('uv_vertex', "UV Vertex", "")),
               default='vertex', name = 'Snap Element')

    def execute(self, context):
        ts = context.scene.tool_settings

        pies_plus = context.preferences.addons[__package__].preferences

        # Snap Elements
        if self.snap_elements == 'vertex':
            ts.snap_elements = {'VERTEX'}
        elif self.snap_elements == 'edge':
            ts.snap_elements = {'EDGE'}
        elif self.snap_elements == 'face':
            ts.snap_elements = {'FACE'}
        elif self.snap_elements == 'increment':
            ts.snap_elements = {'INCREMENT'}
            if pies_plus.autoAbsoluteGridSnap_Pref:
                ts.use_snap_grid_absolute = True
        elif self.snap_elements == 'volume':
            ts.snap_elements = {'VOLUME'}
        elif self.snap_elements == 'edge_center':
            ts.snap_elements = {'EDGE_MIDPOINT'}
        elif self.snap_elements == 'edge_perp':
            ts.snap_elements = {'EDGE_PERPENDICULAR'}

        # UV
        elif self.snap_elements == 'uv_increment':
            ts.snap_uv_element = 'INCREMENT'
        elif self.snap_elements == 'uv_vertex':
            ts.snap_uv_element = 'VERTEX'

        if pies_plus.autoSnap_Pref:
            ts.use_snap = True
        return {'FINISHED'}


##############################
#   REGISTRATION    
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_snapping)

def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_snapping)
    

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