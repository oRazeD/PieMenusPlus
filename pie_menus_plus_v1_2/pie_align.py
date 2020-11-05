from bpy.types import Operator
from bpy.props import EnumProperty
from bpy_extras import view3d_utils
import mathutils
import bpy
import bmesh


class PIESPLUS_OT_quick_world_align(Operator):
    bl_idname = "pies_plus.quick_world_align"
    bl_label = "Quick World Align"
    bl_description = "Quickly aligns your selection automatically based on the closest distance within your selections bounding box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bm = bmesh.new()
        ob = context.active_object
        bm = bmesh.from_edit_mesh(ob.data)

        points = []
        for v in bm.verts:
            if v.select:
                obMat = ob.matrix_world
                points.append(obMat @ v.co)

        # Takes a list of points, returns a tuple containing the corner points
        # containting the minimum and maximum values in x, y, z directions
        xMin, yMin, zMin = float( 'inf'), float( 'inf'), float( 'inf')
        xMax, yMax, zMax = float('-inf'), float('-inf'), float('-inf')

        for p in points:
            if (p.x < xMin):
                xMin = p.x
            if (p.y < yMin):
                yMin = p.y
            if (p.z < zMin):
                zMin = p.z
            if (p.x > xMax):
                xMax = p.x
            if (p.y > yMax):
                yMax = p.y
            if (p.z > zMax):
                zMax = p.z

        xDist = xMin - xMax
        yDist = yMin - yMax
        zDist = zMin - zMax

        if not xDist and not yDist or not xDist and not zDist or not yDist and not zDist:
            return{'FINISHED'}

        savedTransPivot = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

        if xDist < 0:
            xDist *= -1
        if yDist < 0:
            yDist *= -1
        if zDist < 0:
            zDist *= -1

        axisDistsEdge = [xDist, yDist, zDist]
        axisDistsFace = [xDist, yDist, zDist]

        try:
            axisDistsEdge.pop(axisDistsEdge.index(0))
        except:
            print('There are no values with 0')

        minDistanceEdge = axisDistsEdge.index(min(axisDistsEdge))
        minDistanceFace = axisDistsFace.index(min(axisDistsFace))

        faceMode = context.scene.tool_settings.mesh_select_mode[2]

        if faceMode and axisDistsFace[minDistanceFace] == xDist and xDist > 0.0 or not faceMode and axisDistsEdge[minDistanceEdge] == xDist and xDist > 0.0:
            bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', constraint_axis=(True, False, False))
        elif faceMode and axisDistsFace[minDistanceFace] == yDist and yDist > 0.0 or not faceMode and axisDistsEdge[minDistanceEdge] == yDist and yDist > 0.0:
            bpy.ops.transform.resize(value=(1, 0, 1), orient_type='GLOBAL', constraint_axis=(False, True, False))
        elif faceMode and axisDistsFace[minDistanceFace] == zDist and zDist > 0.0 or not faceMode and axisDistsEdge[minDistanceEdge] == zDist and zDist > 0.0:
            bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', constraint_axis=(False, False, True))

        context.scene.tool_settings.transform_pivot_point = savedTransPivot
        return{'FINISHED'}


class PIESPLUS_OT_world_align(Operator):
    bl_idname = "pies_plus.world_align"
    bl_label = "World Align"
    bl_description = "Aligns the selection to world based on the selected operator"
    bl_options = {'REGISTER', 'UNDO'}

    align_axis: EnumProperty(items=(('align_x', "X", ""),
                                    ('align_y', "Y", ""),
                                    ('align_z', "Z", "")), name = 'Align Axis')

    def execute(self, context):
        savedTransPivot = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

        if self.align_axis == 'align_x':
            bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', constraint_axis=(True, False, False))
        elif self.align_axis == 'align_y':
            bpy.ops.transform.resize(value=(1, 0, 1), orient_type='GLOBAL', constraint_axis=(False, True, False))
        else:
            bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', constraint_axis=(False, False, True))

        context.scene.tool_settings.transform_pivot_point = savedTransPivot
        return{'FINISHED'}


class PIESPLUS_OT_normal_z_align(Operator):
    bl_idname = "pies_plus.normal_z_align"
    bl_label = "Normal Align"
    bl_description = "Aligns the selected geometry to the z coordinate of the normal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        savedTransPivot = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

        bpy.ops.transform.resize(value=(1, 1, 0), orient_type='NORMAL', constraint_axis=(True, True, True))

        context.scene.tool_settings.transform_pivot_point = savedTransPivot
        return{'FINISHED'}


class PIESPLUS_OT_active_face_align(Operator):
    bl_idname = "pies_plus.active_face_align"
    bl_label = "Align to Active Face"
    bl_description = "Aligns the selected geometry to the active face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        savedTransPivot = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'

        bpy.ops.transform.resize(value=(1, 1, 0), orient_type='NORMAL', constraint_axis=(True, True, True))

        context.scene.tool_settings.transform_pivot_point = savedTransPivot
        return{'FINISHED'}


class PIESPLUS_OT_active_vert_align(Operator):
    bl_idname = "pies_plus.active_vert_align"
    bl_label = "Align to Active Vert"
    bl_description = "Aligns the vertex selection to the active vertex based on the selected operator"
    bl_options = {'REGISTER', 'UNDO'}

    align_axis: EnumProperty(items=(('align_x', "X", ""),
                                    ('align_y', "Y", ""),
                                    ('align_z', "Z", "")), name = 'Align Axis')

    def execute(self, context):
        savedTransPivot = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'

        if self.align_axis == 'align_x':
            bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', constraint_axis=(True, False, False))
        elif self.align_axis == 'align_y':
            bpy.ops.transform.resize(value=(1, 0, 1), orient_type='GLOBAL', constraint_axis=(False, True, False))
        else:
            bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', constraint_axis=(False, False, True))

        context.scene.tool_settings.transform_pivot_point = savedTransPivot
        return{'FINISHED'}


class PIESPLUS_OT_local_align(Operator):
    bl_idname = "pies_plus.local_align"
    bl_label = "Local Align"
    bl_description = "Aligns the selection to the local axis based on the selected operator"
    bl_options = {'REGISTER', 'UNDO'}

    align_axis: EnumProperty(items=(('align_x', "X", ""),
                                    ('align_y', "Y", ""),
                                    ('align_z', "Z", "")), name = 'Align Axis')

    def execute(self, context):
        savedTransPivot = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

        if self.align_axis == 'align_x':
            bpy.ops.transform.resize(value=(0, 1, 1), orient_type='LOCAL', constraint_axis=(True, False, False))
        elif self.align_axis == 'align_y':
            bpy.ops.transform.resize(value=(1, 0, 1), orient_type='LOCAL', constraint_axis=(False, True, False))
        else:
            bpy.ops.transform.resize(value=(1, 1, 0), orient_type='LOCAL', constraint_axis=(False, False, True))

        context.scene.tool_settings.transform_pivot_point = savedTransPivot
        return{'FINISHED'}


##############################
#   REGISTRATION    
##############################


classes = (PIESPLUS_OT_quick_world_align,
           PIESPLUS_OT_world_align,
           PIESPLUS_OT_normal_z_align,
           PIESPLUS_OT_active_face_align,
           PIESPLUS_OT_active_vert_align,
           PIESPLUS_OT_local_align)

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