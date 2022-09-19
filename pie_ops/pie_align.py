import bpy
from bpy.types import Operator
from ..razeds_bpy_utils.utils.generic import OpInfo
from ..razeds_bpy_utils.utils.bmesh import BMeshFromEditMode


X_PLANE = (0, 1, 1)
Y_PLANE = (1, 0, 1)
Z_PLANE = (1, 1, 0)

X_AXIS = (True, False, False)
Y_AXIS = (False, True, False)
Z_AXIS = (False, False, True)
ALL_AXES = (True, True, True)


def align_to_axis(pivot_point: str, value: tuple, orient_type: str, constraint_axis: tuple) -> None:
    """Align the selected geometry to a given axis plane

    Parameters
    ----------
    pivot_point : str
    value : tuple
    orient_type : str
    constraint_axis : tuple
    """
    tool_settings = bpy.context.scene.tool_settings

    saved_trans_pivot = tool_settings.transform_pivot_point
    tool_settings.transform_pivot_point = pivot_point

    bpy.ops.transform.resize(value=value, orient_type=orient_type, constraint_axis=constraint_axis)

    tool_settings.transform_pivot_point = saved_trans_pivot


class AxisAlignHelper: # Mix-in Class
    align_axis: bpy.props.EnumProperty(
        items=(
            ('align_x', "X", ""),
            ('align_y', "Y", ""),
            ('align_z', "Z", "")
        ),
        name='Align Axis'
    )


class PIESPLUS_OT_quick_world_align(OpInfo, Operator):
    bl_idname = "pies_plus.quick_world_align"
    bl_label = "Quick World Align"
    bl_description = "Quickly aligns your selection automatically based on the closest distance within your selections bounding box"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        xMin, yMin, zMin = float( 'inf'), float( 'inf'), float( 'inf')
        xMax, yMax, zMax = float('-inf'), float('-inf'), float('-inf')

        ob = context.object
        with BMeshFromEditMode(ob, False) as bmesh:
            v_cos = [ob.matrix_world @ v.co for v in bmesh.bm.verts if v.select]

        for co in v_cos:
            if co.x < xMin:
                xMin = co.x
            if co.y < yMin:
                yMin = co.y
            if co.z < zMin:
                zMin = co.z
            if co.x > xMax:
                xMax = co.x
            if co.y > yMax:
                yMax = co.y
            if co.z > zMax:
                zMax = co.z

        xDist = abs(xMin - xMax)
        yDist = abs(yMin - yMax)
        zDist = abs(zMin - zMax)

        axis_dist = [xDist, yDist, zDist]

        if axis_dist.count(0) >= 2:
            self.report({'WARNING'}, "No axis to auto-align")
            return{'FINISHED'}

        try:
            axis_dist.pop(axis_dist.index(0))
        except ValueError: # No values with 0
            pass

        if min(axis_dist) == xDist:
            plane_value, axis_lock = X_PLANE, X_AXIS
        elif min(axis_dist) == yDist:
            plane_value, axis_lock = Y_PLANE, Y_AXIS
        elif min(axis_dist) == zDist:
            plane_value, axis_lock = Z_PLANE, Z_AXIS
        
        align_to_axis('BOUNDING_BOX_CENTER', plane_value, 'GLOBAL', axis_lock)
        return{'FINISHED'}


class PIESPLUS_OT_world_align(OpInfo, AxisAlignHelper, Operator):
    bl_idname = "pies_plus.world_align"
    bl_label = "World Align"
    bl_description = "Aligns the selection to world based on the selected operator"

    def execute(self, context):
        if self.align_axis == 'align_x':
            align_to_axis('BOUNDING_BOX_CENTER', X_PLANE, 'GLOBAL', X_AXIS)
        elif self.align_axis == 'align_y':
            align_to_axis('BOUNDING_BOX_CENTER', Y_PLANE, 'GLOBAL', Y_AXIS)
        else:
            align_to_axis('BOUNDING_BOX_CENTER', Z_PLANE, 'GLOBAL', Z_AXIS)
        return{'FINISHED'}


class PIESPLUS_OT_normal_z_align(OpInfo, Operator):
    bl_idname = "pies_plus.normal_z_align"
    bl_label = "Normal Align"
    bl_description = "Aligns the selected geometry to the z coordinate of the normal"

    def execute(self, context):
        align_to_axis('BOUNDING_BOX_CENTER', Z_PLANE, 'NORMAL', ALL_AXES)
        return{'FINISHED'}


class PIESPLUS_OT_active_face_align(OpInfo, Operator):
    bl_idname = "pies_plus.active_face_align"
    bl_label = "Align to Active Face"
    bl_description = "Aligns the selected geometry to the active face"

    def execute(self, context):
        align_to_axis('ACTIVE_ELEMENT', Z_PLANE, 'NORMAL', ALL_AXES)
        return{'FINISHED'}


class PIESPLUS_OT_active_vert_align(OpInfo, AxisAlignHelper, Operator):
    bl_idname = "pies_plus.active_vert_align"
    bl_label = "Align to Active Vert"
    bl_description = "Aligns the vertex selection to the active vertex based on the selected operator"

    def execute(self, context):
        if self.align_axis == 'align_x':
            align_to_axis('ACTIVE_ELEMENT', X_PLANE, 'GLOBAL', X_AXIS)
        elif self.align_axis == 'align_y':
            align_to_axis('ACTIVE_ELEMENT', Y_PLANE, 'GLOBAL', Y_AXIS)
        else:
            align_to_axis('ACTIVE_ELEMENT', Z_PLANE, 'GLOBAL', Z_AXIS)
        return{'FINISHED'}


class PIESPLUS_OT_local_align(OpInfo, AxisAlignHelper, Operator):
    bl_idname = "pies_plus.local_align"
    bl_label = "Local Align"
    bl_description = "Aligns the selection to the local axis based on the selected operator"

    def execute(self, context):
        if self.align_axis == 'align_x':
            align_to_axis('BOUNDING_BOX_CENTER', X_PLANE, 'LOCAL', X_AXIS)
        elif self.align_axis == 'align_y':
            align_to_axis('BOUNDING_BOX_CENTER', Y_PLANE, 'LOCAL', Y_AXIS)
        else:
            align_to_axis('BOUNDING_BOX_CENTER', Z_PLANE, 'LOCAL', Z_AXIS)
        return{'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (
    PIESPLUS_OT_quick_world_align,
    PIESPLUS_OT_world_align,
    PIESPLUS_OT_normal_z_align,
    PIESPLUS_OT_active_face_align,
    PIESPLUS_OT_active_vert_align,
    PIESPLUS_OT_local_align
)


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
