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
import os
from .pie_shading import *
from .__init__ import *
from bpy.types import Menu


##############################
#   PIE MENUS
##############################


########################################################################################################################
# CONTEXT MODES - TAB
########################################################################################################################


class PIESPLUS_MT_modes(Menu):
    bl_idname = "PIESPLUS_MT_modes"
    bl_label = "Select Mode Pie"

    def draw(self, context):
        ts = context.tool_settings

        try:
            obType = context.object.type
        except:
            print("")

        layout = self.layout
        pie = layout.menu_pie()

        if not context.active_object:
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            pie.separator()
            # 7 - TOP - LEFT
            pie.operator("pies_plus.xray", icon='XRAY')
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.overlay", icon='OVERLAY')
            # 1 - BOTTOM - LEFT
            if context.selected_objects:
                pie.operator("pies_plus.auto_active")
                pie.label(text = "          WARNING: No Active Object selected")
            else:
                pie.separator()
                pie.label(text = "          WARNING: No objects selected")
            # 3 - BOTTOM - RIGHT
            pie.prop(ts, "use_mesh_automerge", text="Auto Merge")
    
        elif obType == 'MESH':
            # 4 - LEFT
            pie.operator("pies_plus.vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator("pies_plus.face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator("pies_plus.edge", icon='EDGESEL')
            # 8 - TOP
            pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            pie.operator("pies_plus.xray", icon='XRAY')
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.overlay", icon='OVERLAY')
            # 1 - BOTTOM - LEFT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 12.5

            box = col.box().column()
            box.scale_y = 1.25

            box.operator("sculpt.sculptmode_toggle", text="Sculpt Mode", icon='SCULPTMODE_HLT')
            box.operator("pies_plus.weight_paint", text="Weight Paint", icon='WPAINT_HLT')
            box.operator("pies_plus.texture_paint", text="Texture Paint", icon='TPAINT_HLT')
            box.operator("pies_plus.vertex_paint", text="Vertex Paint", icon='VPAINT_HLT')
            box.operator("particle.particle_edit_toggle", text="Particle Edit", icon='PARTICLEMODE')
            # 3 - BOTTOM - RIGHT
            pie.prop(ts, "use_mesh_automerge", text="Auto Merge")
        
        elif obType == 'CAMERA':
            # 4 - LEFT
            pie.prop(context.space_data, "lock_cursor", text="Lock Camera to Cursor", icon='PIVOT_CURSOR')
            # 6 - RIGHT
            pie.prop(context.space_data, "lock_camera", text="Lock Camera to View", icon='OBJECT_DATAMODE')
            # 2 - BOTTOM
            pie.operator("ui.eyedropper_depth", text="DOF Distance", icon='EYEDROPPER')
            # 8 - TOP
            pie.operator("view3d.view_camera", icon='VIEW_CAMERA')
            # 7 - TOP - LEFT
            pie.operator("pies_plus.xray", icon='XRAY')
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.overlay", icon='OVERLAY')

        else:
            # 4 - LEFT
            if obType == 'GPENCIL':
                pie.operator("gpencil.sculptmode_toggle", text="Sculpt Mode", icon='SCULPTMODE_HLT')
            else:
                pie.separator()
            # 6 - RIGHT
            if obType == 'ARMATURE':
                pie.operator("object.posemode_toggle", text="Pose Mode", icon='POSE_HLT')
            elif obType == 'GPENCIL':
                pie.operator("gpencil.paintmode_toggle", text="Draw Mode", icon='GREASEPENCIL')
            else:
                pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            if obType in {'CURVE', 'FONT', 'SURFACE', 'META', 'LATTICE', 'ARMATURE'}:
                pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            elif obType == 'GPENCIL':
                pie.operator("gpencil.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            else:
                pie.separator()
            # 7 - TOP - LEFT
            pie.operator("pies_plus.xray", icon='XRAY')
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.overlay", icon='OVERLAY')
            # 1 - BOTTOM - LEFT
            if obType == 'GPENCIL':
                pie.operator("gpencil.weightmode_toggle", text="Weight Paint", icon='WPAINT_HLT')
            else:
                pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.prop(ts, "use_mesh_automerge", text="Auto Merge")


class PIESPLUS_MT_UV_modes(Menu):
    bl_idname = "PIESPLUS_MT_UV_modes"
    bl_label = "Select Mode Pie (UV)"

    def draw(self, context):
        ts = context.tool_settings

        layout = self.layout
        pie = layout.menu_pie()

        if ts.use_uv_select_sync:
            # 4 - LEFT
            pie.operator("pies_plus.vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator("pies_plus.face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator("pies_plus.edge", icon='EDGESEL')
            # 8 - TOP
            pie.prop(ts, "use_uv_select_sync", icon='UV_SYNC_SELECT')
        else:
            #4 - LEFT
            pie.operator("pies_plus.uv_sel_change", text='Vertex', icon='VERTEXSEL').sel_choice = 'sel_vert'
            # 6 - RIGHT
            pie.operator("pies_plus.uv_sel_change", text='Face', icon='FACESEL').sel_choice = 'sel_face'
            # 2 - BOTTOM
            pie.operator("pies_plus.uv_sel_change", text='Edge', icon='EDGESEL').sel_choice = 'sel_edge'
            # 8 - TOP
            pie.prop(ts, "use_uv_select_sync", icon='UV_SYNC_SELECT')
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.uv_sel_change", text='Island', icon='UV_ISLANDSEL').sel_choice = 'sel_island'


########################################################################################################################
# ACTIVE TOOLS - W
########################################################################################################################


class PIESPLUS_MT_active_tools(Menu):
    bl_idname = "PIESPLUS_MT_active_tools"
    bl_label = "Active Tools Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        addon_Prefs = context.preferences.addons[__package__].preferences

        if addon_Prefs.gizmoSwitch_Pref == 'tool':
            #4 - LEFT
            pie.operator("pies_plus.active_tools", text="Move", icon='ORIENTATION_GLOBAL').active_tools = 'tool_move'
            #6 - RIGHT
            pie.operator("pies_plus.active_tools", text="Rotate", icon='DRIVER_ROTATIONAL_DIFFERENCE').active_tools = 'tool_rotate'
            #2 - BOTTOM
            pie.operator("pies_plus.active_tools", text="Scale", icon='SNAP_FACE').active_tools = 'tool_scale'
            #8 - TOP
            if addon_Prefs.defaultTool_Pref == 'tweak_select':
                pie.operator("pies_plus.active_tools", text="Tweak", icon='RESTRICT_SELECT_OFF').active_tools = 'select_tweak'
            elif addon_Prefs.defaultTool_Pref == 'box_select':
                pie.operator("pies_plus.active_tools", text="Box", icon='SELECT_SET').active_tools = 'select_box'
            elif addon_Prefs.defaultTool_Pref == 'circle_select':
                pie.operator("pies_plus.active_tools", text="Circle", icon='MESH_CIRCLE').active_tools = 'select_circle'
            else:
                pie.operator("pies_plus.active_tools", text="Lasso", icon='GP_ONLY_SELECTED').active_tools = 'select_lasso'
            #7 - TOP - LEFT
            pie.operator("pies_plus.active_tools", text="All", icon='GIZMO').active_tools = 'tool_transform'
        else: # Gizmo
            #4 - LEFT
            pie.operator("pies_plus.active_tools", text="Move", icon='ORIENTATION_GLOBAL').active_tools = 'gizmo_move'
            #6 - RIGHT
            pie.operator("pies_plus.active_tools", text="Rotate", icon='DRIVER_ROTATIONAL_DIFFERENCE').active_tools = 'gizmo_rotate'
            #2 - BOTTOM
            pie.operator("pies_plus.active_tools", text="Scale", icon='SNAP_FACE').active_tools = 'gizmo_scale'
            #8 - TOP
            if addon_Prefs.defaultTool_Pref == 'tweak_select':
                pie.operator("pies_plus.active_tools", text="Tweak", icon='RESTRICT_SELECT_OFF').active_tools = 'select_tweak'
            elif addon_Prefs.defaultTool_Pref == 'box_select':
                pie.operator("pies_plus.active_tools", text="Box", icon='SELECT_SET').active_tools = 'select_box'
            elif addon_Prefs.defaultTool_Pref == 'circle_select':
                pie.operator("pies_plus.active_tools", text="Circle", icon='MESH_CIRCLE').active_tools = 'select_circle'
            else:
                pie.operator("pies_plus.active_tools", text="Lasso", icon='GP_ONLY_SELECTED').active_tools = 'select_lasso'
            #7 - TOP - LEFT
            pie.operator("pies_plus.active_tools", text="All", icon='GIZMO').active_tools = 'gizmo_transform'
        #9 - TOP - RIGHT
        pie.operator("pies_plus.active_tools", text="Cursor", icon='PIVOT_CURSOR').active_tools = 'cursor'
        # 1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 6.5

        box = col.box().column()
        box.scale_y = 1.25

        if addon_Prefs.defaultTool_Pref == 'tweak_select':
            box.operator("pies_plus.active_tools", text="Box", icon='SELECT_SET').active_tools = 'select_box'
            box.operator("pies_plus.active_tools", text="Circle", icon='MESH_CIRCLE').active_tools = 'select_circle'
            box.operator("pies_plus.active_tools", text="Lasso", icon='GP_ONLY_SELECTED').active_tools = 'select_lasso'
        else:
            box.operator("pies_plus.active_tools", text="Tweak", icon='RESTRICT_SELECT_OFF').active_tools = 'select_tweak'
            if addon_Prefs.defaultTool_Pref == 'box_select':
                box.operator("pies_plus.active_tools", text="Circle", icon='MESH_CIRCLE').active_tools = 'select_circle'
                box.operator("pies_plus.active_tools", text="Lasso", icon='GP_ONLY_SELECTED').active_tools = 'select_lasso'
            elif addon_Prefs.defaultTool_Pref == 'circle_select':
                box.operator("pies_plus.active_tools", text="Box", icon='SELECT_SET').active_tools = 'select_box'
                box.operator("pies_plus.active_tools", text="Lasso", icon='GP_ONLY_SELECTED').active_tools = 'select_lasso'
            else:
                box.operator("pies_plus.active_tools", text="Box", icon='SELECT_SET').active_tools = 'select_box'
                box.operator("pies_plus.active_tools", text="Circle", icon='MESH_CIRCLE').active_tools = 'select_circle'


########################################################################################################################
# SNAPPING - SHIFT + TAB
########################################################################################################################


class PIESPLUS_MT_snapping(Menu):
    bl_idname = "PIESPLUS_MT_snapping"
    bl_label = "Snapping Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("pies_plus.snap", text="Snap Vertex", icon='SNAP_VERTEX').snap_elements='vertex'
        # 6 - RIGHT
        pie.operator("pies_plus.snap", text="Snap Face", icon='SNAP_FACE').snap_elements = 'face'
        # # 2 - BOTTOM
        pie.operator("pies_plus.snap", text="Snap Edge", icon='SNAP_EDGE').snap_elements = 'edge'
        # # 8 - TOP
        pie.prop(context.tool_settings, "use_snap", text="Snap Toggle")
        # # 7 - TOP - LEFT
        pie.operator("pies_plus.snap", text="Snap Volume", icon='SNAP_VOLUME').snap_elements = 'volume'
        # # 9 - TOP - RIGHT
        pie.operator("pies_plus.snap", text="Snap Increment", icon='SNAP_INCREMENT').snap_elements = 'increment'
        # 1 - BOTTOM - LEFT
        if bpy.app.version >= (2, 81, 0):
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 3.5

            box = col.box().column()
            box.scale_y = 1.25

            box.operator("pies_plus.snap", text="Snap Edge Center", icon='SNAP_MIDPOINT').snap_elements = 'edge_center'
            box.operator("pies_plus.snap", text="Snap Edge Perp", icon='SNAP_PERPENDICULAR').snap_elements = 'edge_perp'
        else:
            pie.separator()
        # 3 - BOTTOM - RIGHT
        pie.popover(panel="VIEW3D_PT_snapping", text="More...")


class PIESPLUS_MT_UV_snapping(Menu):
    bl_idname = "PIESPLUS_MT_UV_snapping"
    bl_label = "Snapping Pie (UV)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("pies_plus.snap", text="Snap Vertex", icon='SNAP_VERTEX').snap_elements='uv_vertex'
        # 6 - RIGHT
        pie.operator("pies_plus.snap", text="Snap Increment", icon='SNAP_INCREMENT').snap_elements = 'uv_increment'
        # # 2 - BOTTOM
        pie.separator()
        # # 8 - TOP
        pie.prop(context.tool_settings, "use_snap", text="Snap Toggle")
        # # 7 - TOP - LEFT
        pie.separator()
        # # 9 - TOP - RIGHT
        pie.separator()
        # 1 - BOTTOM - LEFT
        pie.separator()
        # 3 - BOTTOM - RIGHT
        pie.popover(panel="IMAGE_PT_snapping", text="More...")


########################################################################################################################
# LOOPTOOLS - SHIFT + W
########################################################################################################################


class PIESPLUS_MT_looptools(Menu):
    bl_idname = "PIESPLUS_MT_looptools"
    bl_label = "LoopTools Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        for modID in context.preferences.addons.keys():
            if modID == 'mesh_looptools':
                # 4 - LEFT
                pie.operator("pies_plus.looptools", text="Relax").lt_func = 'lt_relax'
                # 6 - RIGHT
                pie.operator("pies_plus.looptools", text="Space").lt_func = 'lt_space'
                # # 2 - BOTTOM
                pie.operator("pies_plus.looptools", text="Flatten").lt_func = 'lt_flatten'
                # # 8 - TOP
                pie.operator("pies_plus.looptools", text="Circle").lt_func='lt_circle'
                # # 7 - TOP - LEFT
                pie.operator("pies_plus.looptools", text="Loft").lt_func = 'lt_loft'
                # # 9 - TOP - RIGHT
                pie.operator("pies_plus.looptools", text="GStretch").lt_func = 'lt_gstretch'
                # 1 - BOTTOM - LEFT
                pie.operator("pies_plus.looptools", text="Curve").lt_func = 'lt_curve'
                # 3 - BOTTOM - RIGHT
                pie.operator("pies_plus.looptools", text="Bridge").lt_func = 'lt_bridge'
                break
        else:
            pie.label(text="          WARNING: You do not have LoopTools enabled")


########################################################################################################################
# APPLY TRANSFORMS - CTRL + A
########################################################################################################################


class PIESPLUS_MT_apply_clear_transforms(Menu):
    bl_idname = "PIESPLUS_MT_apply_clear_transforms"
    bl_label = "Apply Transforms Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if not context.active_object:
            if context.selected_objects:
                pie.label(text = "          WARNING: No Active Object selected")
            else:
                pie.label(text = "          WARNING: No objects selected")

        else:
            #4 - LEFT
            pie.operator("pies_plus.apply_transforms", text="Clear All", icon='EMPTY_AXIS').apply_transforms = 'clear_all'
            #6 - RIGHT
            pie.operator("pies_plus.apply_transforms", text="Apply Scale", icon='FILE_TICK').apply_transforms = 'apply_scale'
            #2 - BOTTOM
            pie.operator("pies_plus.apply_transforms", text="Apply All", icon='FILE_TICK').apply_transforms = 'apply_all'
            #8 - TOP
            pie.operator("pies_plus.apply_transforms", text="Apply Rot & Scale", icon='FILE_TICK').apply_transforms = 'apply_rot_scale'
            #7 - TOP - LEFT
            pie.operator("pies_plus.apply_transforms", text="Apply Location", icon='FILE_TICK').apply_transforms = 'apply_loc'
            #9 - TOP - RIGHT
            pie.operator("pies_plus.apply_transforms", text="Apply Rotation", icon='FILE_TICK').apply_transforms = 'apply_rot'
            #1 - BOTTOM - LEFT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 6

            box = col.box().column()
            box.scale_y = 1.25    

            box.operator("object.location_clear", icon='EMPTY_AXIS')
            box.operator("object.rotation_clear", icon='EMPTY_AXIS')
            box.operator("object.scale_clear", icon='EMPTY_AXIS')
            # 3 - BOTTOM - RIGHT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 6

            box = col.box().column()
            box.scale_y = 1.25     

            box.operator("object.visual_transform_apply", text="Apply Visual Transforms", icon='FILE_TICK')
            box.operator("object.convert", text="Convert to Mesh", icon='OUTLINER_OB_MESH').target = 'MESH'
            box.operator("object.duplicates_make_real", text="Make Duplicates Real", icon='USER')


########################################################################################################################
# CURSOR / ORIGIN - SHIFT + S
########################################################################################################################


class PIESPLUS_MT_origin_pivot(Menu):
    bl_idname = "PIESPLUS_MT_origin_pivot"
    bl_label = "Origin / Cursor Change Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if not context.active_object:
            if context.selected_objects:
                pie.label(text = "          WARNING: No Active Object selected")
            else:
                pie.label(text = "          WARNING: No objects selected")

        if context.active_object:
            # 4 - LEFT
            pie.operator("object.origin_set", text="Origin to Cursor", icon='PIVOT_CURSOR').type = 'ORIGIN_CURSOR'
            # 6 - RIGHT
            pie.operator("view3d.snap_cursor_to_selected", text="Cursor to Selection", icon='PIVOT_CURSOR')
            # 2 - BOTTOM
            pie.operator("pies_plus.origin_to_selection", icon='PIVOT_BOUNDBOX')
            # 8 - TOP
            if context.preferences.addons[__package__].preferences.editOriginActivate_Pref:
                pie.operator("pies_plus.edit_origin", icon='OBJECT_ORIGIN')
            else:
                pie.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor",icon='RESTRICT_SELECT_OFF').use_offset = True
            # 7 - TOP - LEFT
            pie.operator("object.origin_set", text="Origin to Geo", icon='PIVOT_BOUNDBOX').type = 'ORIGIN_GEOMETRY'
            # 9 - TOP - RIGHT
            pie.operator("view3d.snap_cursor_to_active", text="Cursor to Active", icon='PIVOT_CURSOR')
        else:
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            pie.separator()
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
        # 1 - BOTTOM - LEFT
        if context.active_object:
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 13

            box = col.box().column(align=True)

            row = box.row()
            row.scale_y = 1.25
            row.operator("pies_plus.reset_origin", text='Origin to 0,0,0', icon='PIVOT_BOUNDBOX').origin_reset_axis = 'origin_all'
            row = box.row(align=True)
            row.scale_y = 1.1
            row.operator("pies_plus.reset_origin", text='X').origin_reset_axis = 'origin_x'
            row.operator("pies_plus.reset_origin", text='Y').origin_reset_axis = 'origin_y'
            row.operator("pies_plus.reset_origin", text='Z').origin_reset_axis = 'origin_z'

            box = col.box().column()
            box.scale_y = 1.25

            box.operator("object.origin_set", text="Geometry to Origin", icon='PIVOT_BOUNDBOX').type = 'GEOMETRY_ORIGIN'
            box.operator("pies_plus.origin_to_com", icon='PIVOT_BOUNDBOX')
            box.operator("pies_plus.origin_to_bottom", icon='PIVOT_BOUNDBOX')
        else:
            if context.selected_objects:
                pie.operator("pies_plus.auto_active")
            else:
                pie.separator()
        # 3 - BOTTOM - RIGHT
        col = pie.column()

        gap = col.column()
        gap.separator()
        if context.preferences.addons[__package__].preferences.editOriginActivate_Pref:
            gap.scale_y = 13
        else:
            gap.scale_y = 7

        box = col.box().column(align=True)
        row = box.row()
        row.scale_y = 1.25
        row.operator("pies_plus.reset_cursor", text='Cursor to 0,0,0', icon='PIVOT_CURSOR').cursor_reset_axis = 'cursor_all'
        row = box.row(align=True)
        row.scale_y = 1.1
        row.operator("pies_plus.reset_cursor", text='X').cursor_reset_axis = 'cursor_x'
        row.operator("pies_plus.reset_cursor", text='Y').cursor_reset_axis = 'cursor_y'
        row.operator("pies_plus.reset_cursor", text='Z').cursor_reset_axis = 'cursor_z'

        box = col.box().column()
        box.scale_y = 1.25
        box.operator("view3d.reset_cursor_rot", icon='PIVOT_CURSOR')
        if context.preferences.addons[__package__].preferences.editOriginActivate_Pref:
            box.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor",icon='RESTRICT_SELECT_OFF').use_offset = True
            box.operator("pies_plus.edit_cursor", icon='PIVOT_CURSOR')


########################################################################################################################
# DELETE - X
########################################################################################################################


class PIESPLUS_MT_delete(Menu):
    bl_idname = "PIESPLUS_MT_delete"
    bl_label = "Delete Pie (Edit Mode)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.operator("mesh.delete", text="Delete Vertices", icon='VERTEXSEL').type='VERT'
        #6 - RIGHT
        pie.operator("mesh.delete", text="Delete Faces", icon='FACESEL').type='FACE'
        #2 - BOTTOM
        pie.operator("mesh.delete", text="Delete Edges", icon='EDGESEL').type='EDGE'
        #8 - TOP
        pie.operator("mesh.dissolve_edges", text="Dissolve Edges", icon='SNAP_EDGE')
        #7 - TOP - LEFT
        pie.operator("mesh.dissolve_verts", text="Dissolve Vertices", icon='SNAP_VERTEX')
        #9 - TOP - RIGHT
        pie.operator("mesh.remove_doubles", text="Merge by Distance", icon= 'AUTOMERGE_ON')
        #1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 9.5

        box = col.box().column()
        box.scale_y=1.25
        box.operator("mesh.dissolve_limited", text="Limited Dissolve", icon= 'STICKY_UVS_LOC')
        box.operator("mesh.dissolve_faces", text="Dissolve Faces", icon='SNAP_FACE')
        box.operator("mesh.delete", text="Only Edge & Faces", icon='SNAP_FACE').type='EDGE_FACE'
        box.operator("mesh.delete", text="Only Faces", icon='FACESEL').type='ONLY_FACE'
        #3 - BOTTOM - RIGHT
        pie.operator("mesh.edge_collapse", text="Edge Collapse", icon='UV_EDGESEL')


########################################################################################################################
# SELECTION - A
########################################################################################################################


class PIESPLUS_MT_selection_object_mode(Menu):
    bl_idname = "PIESPLUS_MT_selection_object_mode"
    bl_label = "Selection Pie (Object Mode)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.separator()
        #6 - RIGHT
        pie.separator()
        #2 - BOTTOM
        pie.operator("object.select_all", text="Invert Selection", icon='SELECT_DIFFERENCE').action='INVERT'
        #8 - TOP
        pie.operator("pies_plus.mesh_selection", icon='RESTRICT_SELECT_OFF')
        #7 - TOP - LEFT
        pie.operator("pies_plus.frame_selected_all", icon='VIS_SEL_10')
        #9 - TOP - RIGHT
        pie.operator("view3d.localview", text="Isolate Toggle", icon='CAMERA_DATA')
        #1 - BOTTOM - LEFT

        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 9.5

        box = col.box().column()
        box.scale_y=1.25
        box.operator("object.select_random", text="Select Random", icon='GROUP_VERTEX')
        box.operator("object.select_by_type", text="Select By Type...", icon='SNAP_VOLUME')
        box.operator("object.select_grouped", text="Select Grouped...", icon='GROUP_VERTEX')
        box.operator("object.select_linked", text="Select Linked...", icon='CONSTRAINT_BONE')
        #1 - BOTTOM - LEFT
        pie.operator("object.join", text="Merge Selection", icon='OBJECT_DATA')


class PIESPLUS_MT_selection_edit_mode(Menu):
    bl_idname = "PIESPLUS_MT_selection_edit_mode"
    bl_label = "Selection Pie (Edit Mode)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.separator()
        #6 - RIGHT
        pie.operator("mesh.select_nth", text="Checker Select", icon='PARTICLE_POINT')
        #2 - BOTTOM
        pie.operator("mesh.select_all", text="Invert Selection", icon='SELECT_DIFFERENCE').action='INVERT'
        #8 - TOP
        pie.operator("pies_plus.mesh_selection", icon='RESTRICT_SELECT_OFF')
        #7 - TOP - LEFT
        pie.operator("mesh.loop_multi_select", text="Ring Select", icon='ZOOM_PREVIOUS').ring=True
        #9 - TOP - RIGHT
        pie.operator("mesh.loop_multi_select", text="Loop Select", icon='ZOOM_PREVIOUS').ring=False
        #1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 12.5

        box = col.box().column()
        box.scale_y=1.25
        box.operator("mesh.select_random", text="Select Random", icon='GROUP_VERTEX')
        box.operator("mesh.region_to_loop", text="Select Boundary Loop", icon='MESH_PLANE')
        box.operator("pies_plus.select_loop_inner_region", icon='FACESEL')
        box.operator("mesh.select_similar", text="Select Similar...", icon='PIVOT_INDIVIDUAL')
        row = box.row(align=True)
        row.scale_x = .875
        row.label(text="Select:")
        row.operator("pies_plus.select_marked_sharp", text="Sharps").markedChoice = 'marked_sharp'
        row.operator("pies_plus.select_marked_sharp", text="Seams").markedChoice = 'marked_seam'
        #3 - BOTTOM - RIGHT
        pie.operator("mesh.select_linked", text="Select Linked All", icon='STICKY_UVS_LOC').delimit=set()


########################################################################################################################
# SHADING - Z
########################################################################################################################


class PIESPLUS_MT_shading(Menu):
    bl_idname = "PIESPLUS_MT_shading"
    bl_label = "Shading Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
 
        # 4 - LEFT
        pie.operator("pies_plus.solid", icon='SHADING_SOLID')
        # 6 - RIGHT
        if context.selected_objects:
            if context.active_object:
                if context.object.type == 'MESH':
                    if context.active_object.data.polygons[0].use_smooth:
                        pie.operator("pies_plus.shade_flat")
                    else:
                        pie.operator("pies_plus.shade_smooth")
                else:
                    pie.separator()
            else:
                pie.separator()
                pie.label(text = "          WARNING: No Active Object selected")
        else:
            pie.separator()
            pie.label(text = "          WARNING: No objects selected")
        # 2 - BOTTOM
        pie.operator("pies_plus.wireframe", icon='SHADING_WIRE')
        # 8 - TOP
        pie.operator("pies_plus.mat_preview", icon='MATERIAL_DATA')
        # 7 - TOP - LEFT
        pie.operator("pies_plus.xray", icon='XRAY')
        # 9 - TOP - RIGHT
        pie.operator("pies_plus.overlay", icon='OVERLAY')
        #1 - BOTTOM - LEFT
        if context.active_object and context.object.type == 'MESH':
            col = pie.column()

            gap = col.column()
            gap.separator()
            if context.selected_objects:
                gap.scale_y = 16.5
            else:
                gap.scale_y = 2.5

            box = col.box().column(align=True)
            box.scale_y=1.1

            box.prop(context.active_object,"useAutoSmooth")
            box.prop(context.active_object,"smoothAngle")
            if context.selected_objects:
                box = col.box().column()
                box.scale_y=1.25
                box.operator("pies_plus.recalc_normals", icon='NORMALS_FACE')
                box.operator("pies_plus.auto_fwn", icon='MOD_NORMALEDIT')
                box.operator("pies_plus.remove_custom_normals", icon='X')

                box = col.box().column()
                box.scale_y=1.25
                box.operator("pies_plus.wireframe_per_obj", icon='MOD_WIREFRAME')

        elif context.selected_objects and not context.active_object:
            pie.operator("pies_plus.auto_active")

        else:
            pie.separator()
        #3 - BOTTOM - RIGHT
        pie.operator("pies_plus.rendered", icon='SHADING_RENDERED')


########################################################################################################################
# ANIMATION - SHIFT + SPACE
########################################################################################################################


class PIESPLUS_MT_animation(Menu):
    bl_idname = "PIESPLUS_MT_animation"
    bl_label = "Animation Pie"

    def draw(self, context):
        toolsettings = context.tool_settings
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        # 6 - RIGHT
        pie.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True
        # 2 - BOTTOM
        pie.prop(toolsettings, "use_keyframe_insert_auto", text="Auto Key", icon='REC')
        # 8 - TOP
        if not context.screen.is_animation_playing:
            pie.operator("screen.animation_play", text="Play", icon='PLAY')
        else:
            pie.operator("screen.animation_play", text="Stop", icon='PAUSE')
        # 7 - TOP - LEFT
        pie.operator("screen.keyframe_jump", text="Previous FR", icon='PREV_KEYFRAME').next = False
        # 9 - TOP - RIGHT
        pie.operator("screen.keyframe_jump", text="Next FR", icon='NEXT_KEYFRAME').next = True
        # 1 - BOTTOM - LEFT
        pie.operator("screen.animation_play", text="Reverse", icon='PLAY_REVERSE').reverse = True
        # 3 - BOTTOM - RIGHT
        pie.menu("VIEW3D_MT_object_animation", text="Keyframe...", icon="KEYINGSET")


########################################################################################################################
# KEYFRAMING - CTRL + SPACE
########################################################################################################################


class PIESPLUS_MT_keyframing(Menu):
    bl_idname = "PIESPLUS_MT_keyframing"
    bl_label = "Keyframing Pie"

    def draw(self, context):
        toolsettings = context.tool_settings
        layout = self.layout
        pie = layout.menu_pie()

        if not context.selected_objects:
            if context.active_object:
                if context.mode == "POSE" and not context.selected_pose_bones:
                    pie.label(text = "          WARNING: No bones selected")
                    # 4 - LEFT
                    pie.separator()
                    # 6 - RIGHT
                    pie.separator()
                    # 2 - BOTTOM
                    pie.separator()
                    # 8 - TOP
                    pie.separator()
                    # 7 - TOP - LEFT
                    pie.operator("pies_plus.keyframing", text="Whole Character").key_choice = 'key_whole_char'
                    # 9 - TOP - RIGHT
                    pie.operator("pies_plus.keyframing", text="Whole Selected").key_choice = 'key_whole_char_sel'
                else:
                    pie.label(text = "          WARNING: No objects selected")
            else:
                pie.label(text = "          WARNING: No objects selected")

        elif context.mode not in {'POSE', 'OBJECT'}:
            pie.label(text = "          WARNING: You are not in the appropriate Context Mode")
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            if context.object.type in {'MESH','CURVE', 'FONT', 'SURFACE', 'META', 'LATTICE', 'ARMATURE'}:
                pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            else:
                pie.separator()
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            if context.object.type == "ARMATURE":
                pie.operator("object.posemode_toggle", text="Pose Mode", icon='POSE_HLT')

        elif context.mode == "POSE" and not context.selected_pose_bones:
            pie.label(text = "          WARNING: No bones selected")
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            pie.separator()
            # 7 - TOP - LEFT
            pie.operator("pies_plus.keyframing", text="Whole Character").key_choice = 'key_whole_char'
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.keyframing", text="Whole Selected").key_choice = 'key_whole_char_sel'
        else:
            # 4 - LEFT
            pie.operator("pies_plus.keyframing", text="Visual LocRot").key_choice = 'key_vis_locrot'
            # 6 - RIGHT
            pie.operator("pies_plus.keyframing", text="LocRot").key_choice = 'key_locrot'
            # 2 - BOTTOM
            pie.prop(toolsettings, "use_keyframe_insert_auto", text="Auto Key")
            # 8 - TOP
            pie.operator("pies_plus.keyframing", text="Rotation").key_choice = 'key_rot'
            # 7 - TOP - LEFT
            pie.operator("pies_plus.keyframing", text="Location").key_choice = 'key_loc'
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.keyframing", text="Scale").key_choice = 'key_scale'
            # 1 - BOTTOM - LEFT
            col = pie.column()

            gap = col.column()
            gap.separator()
            if context.mode == "POSE":
                gap.scale_y = 25.5
            else:
                gap.scale_y = 15.5

            box = col.box().column()
            box.scale_y=1.25
            box.operator("pies_plus.keyframing", text="Visual Location").key_choice = 'key_vis_loc'
            box.operator("pies_plus.keyframing", text="Visual Rotation").key_choice = 'key_vis_rot'
            box.operator("pies_plus.keyframing", text="Visual Scaling").key_choice = 'key_vis_scale'
            box.operator("pies_plus.keyframing", text="Visual LocRotScale").key_choice = 'key_vis_locrotscale'
            box.operator("pies_plus.keyframing", text="Visual LocScale").key_choice = 'key_vis_locscale'
            box.operator("pies_plus.keyframing", text="Visual RotScale").key_choice = 'key_vis_rotscale'
            
            if context.mode == "POSE":
                gap = col.column()

                box = col.box().column()
                box.scale_y=1.25
                box.operator("pies_plus.keyframing", text="BBone Shape").key_choice = 'key_bendy_bones'
                box.operator("pies_plus.keyframing", text="Whole Character").key_choice = 'key_whole_char'
                box.operator("pies_plus.keyframing", text="Whole Selected").key_choice = 'key_whole_char_sel'
            # 3 - BOTTOM - RIGHT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 20.5

            box = col.box().column()
            box.scale_y=1.25
            box.operator("pies_plus.keyframing", text="Available").key_choice = 'key_available'

            gap = col.column()

            box = col.box().column()
            box.scale_y=1.25
            box.operator("pies_plus.keyframing", text="LocRotScale").key_choice = 'key_locrotscale'
            box.operator("pies_plus.keyframing", text="LocScale").key_choice = 'key_locscale'
            box.operator("pies_plus.keyframing", text="RotScale").key_choice = 'key_rotscale'
            
            gap = col.column()

            box = col.box().column()
            box.scale_y=1.25
            box.operator("pies_plus.keyframing", text="Delta Location").key_choice = 'key_del_loc'
            box.operator("pies_plus.keyframing", text="Delta Rotation").key_choice = 'key_del_rot'
            box.operator("pies_plus.keyframing", text="Delta Scale").key_choice = 'key_del_scale'


########################################################################################################################
# PROPORTIONAL EDITING - O
########################################################################################################################


class PIESPLUS_MT_proportional_edit_mode(Menu):
    bl_idname = "PIESPLUS_MT_proportional_edit_mode"
    bl_label = "Proportional Pie (Edit Mode)"

    def draw(self, context):
        ts = context.tool_settings

        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("proportional.smooth", icon='SMOOTHCURVE')
        # 6 - RIGHT
        pie.operator("proportional.sphere", icon='SPHERECURVE')
        # 2 - BOTTOM
        pie.operator("proportional.inverse_square", icon='INVERSESQUARECURVE')
        # 8 - TOP
        pie.prop(ts, "use_proportional_edit", text="Proportional Toggle", icon='PROP_ON')
        # 7 - TOP - LEFT
        pie.prop(ts, "use_proportional_connected", icon='PROP_CON')
        # 9 - TOP - RIGHT
        pie.prop(ts, "use_proportional_projected", icon='PROP_PROJECTED')
        # 1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 9.5

        box = col.box().column()
        box.scale_y=1.25
        box.operator("proportional.constant", icon='NOCURVE')
        box.operator("proportional.random", icon='RNDCURVE')
        box.operator("proportional.sharp", icon='SHARPCURVE')
        box.operator("proportional.linear", icon='LINCURVE')
        # 3 - BOTTOM - RIGHT
        pie.operator("proportional.root", icon='ROOTCURVE')


class PIESPLUS_MT_proportional_object_mode(Menu):
    bl_idname = "PIESPLUS_MT_proportional_object_mode"
    bl_label = "Proportional Pie (Object Mode)"

    def draw(self, context):
        ts = context.tool_settings

        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("proportional.smooth", icon='SMOOTHCURVE')
        # 6 - RIGHT
        pie.operator("proportional.sphere", icon='SPHERECURVE')
        # 2 - BOTTOM
        pie.operator("proportional.inverse_square", icon='INVERSESQUARECURVE')
        # 8 - TOP
        pie.prop(ts, "use_proportional_edit_objects", text="Proportional Toggle")
        # 7 - TOP - LEFT
        pie.operator("proportional.sharp", icon='SHARPCURVE')
        # 9 - TOP - RIGHT
        pie.operator("proportional.linear", icon='LINCURVE')
        # 1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 6

        box = col.box().column()
        box.scale_y=1.25
        box.operator("proportional.constant", icon='NOCURVE')
        box.operator("proportional.random", icon='RNDCURVE')
        # 3 - BOTTOM - RIGHT
        pie.operator("proportional.root", icon='ROOTCURVE')


########################################################################################################################
# SCULPT (Sculpt Mode) - S
########################################################################################################################


class PIESPLUS_MT_sculpt(Menu):
    bl_idname = "PIESPLUS_MT_sculpt"
    bl_label = "Sculpt Pie (Sculpt Mode)"

    def draw(self, context):
        if bpy.app.version >= (2, 81, 0):
            global brush_icons
        layout = self.layout
        pie = layout.menu_pie()
        layout.scale_y = 1.2

        if bpy.app.version >= (2, 81, 0):
            # 4 - LEFT
            pie.operator("paint.brush_select", text="    Crease", icon_value=brush_icons["crease"]).sculpt_tool = 'CREASE'
            # 6 - RIGHT
            pie.operator("paint.brush_select", text="    Blob", icon_value=brush_icons["blob"]).sculpt_tool = 'BLOB'
            # 2 - BOTTOM
            pie.menu("PIESPLUS_MT_sculpt_more", text="    More...")
            # 8 - TOP
            pie.operator("paint.brush_select", text="    Draw", icon_value=brush_icons["draw"]).sculpt_tool = 'DRAW'
            # 7 - TOP - LEFT
            pie.operator("paint.brush_select", text="    Clay", icon_value=brush_icons["clay"]).sculpt_tool = 'CLAY'
            # 9 - TOP - RIGHT
            pie.operator("paint.brush_select", text="    Clay Strips", icon_value=brush_icons["clay_strips"]).sculpt_tool = 'CLAY_STRIPS'
            # 1 - BOTTOM - LEFT
            pie.operator("paint.brush_select", text="    Inflate / Deflate", icon_value=brush_icons["inflate"]).sculpt_tool = 'INFLATE'
            # 3 - BOTTOM - RIGHT
            pie.menu("PIESPLUS_MT_sculpt_grab", text="    Grab...", icon_value=brush_icons["grab"])
        else:
            # 4 - LEFT
            pie.operator("paint.brush_select", text="    Crease").sculpt_tool = 'CREASE'
            # 6 - RIGHT
            pie.operator("paint.brush_select", text="    Blob").sculpt_tool = 'BLOB'
            # 2 - BOTTOM
            pie.menu("PIESPLUS_MT_sculpt_more", text="    More...")
            # 8 - TOP
            pie.operator("paint.brush_select", text="    Draw").sculpt_tool = 'DRAW'
            # 7 - TOP - LEFT
            pie.operator("paint.brush_select", text="    Clay").sculpt_tool = 'CLAY'
            # 9 - TOP - RIGHT
            pie.operator("paint.brush_select", text="    Clay Strips").sculpt_tool = 'CLAY_STRIPS'
            # 1 - BOTTOM - LEFT
            pie.operator("paint.brush_select", text="    Inflate / Deflate").sculpt_tool = 'INFLATE'
            # 3 - BOTTOM - RIGHT
            pie.menu("PIESPLUS_MT_sculpt_grab", text="    Grab...")


class PIESPLUS_MT_sculpt_more(Menu):
    bl_idname = "PIESPLUS_MT_sculpt_more"
    bl_label = ""

    def draw(self, context):
        if bpy.app.version >= (2, 81, 0):
            global brush_icons
        layout = self.layout
        layout.scale_y = 1.2

        if bpy.app.version >= (2, 81, 0):
            layout.operator("paint.brush_select", text='    Smooth', icon_value=brush_icons["smooth"]).sculpt_tool = 'SMOOTH'
            layout.operator("paint.brush_select", text='    Flatten', icon_value=brush_icons["flatten"]).sculpt_tool = 'FLATTEN'
            layout.operator("paint.brush_select", text='    Scrape / Peaks', icon_value=brush_icons["scrape"]).sculpt_tool = 'SCRAPE'
            layout.operator("paint.brush_select", text='    Fill / Deepen', icon_value=brush_icons["fill"]).sculpt_tool = 'FILL'
            if bpy.app.version >= (2, 83, 0):
                layout.operator("paint.brush_select", text='    Clay Thumb', icon_value=brush_icons["clay_thumb"]).sculpt_tool = 'CLAY_THUMB'
                layout.operator("paint.brush_select", text='    Cloth', icon_value=brush_icons["cloth"]).sculpt_tool = 'CLOTH'
                layout.operator("paint.brush_select", text='    Face Sets', icon_value=brush_icons["draw_face_sets"]).sculpt_tool = 'DRAW_FACE_SETS'
            layout.operator("paint.brush_select", text='    Layer', icon_value=brush_icons["layer"]).sculpt_tool = 'LAYER'
            layout.operator("paint.brush_select", text='    Mask', icon_value=brush_icons["mask"]).sculpt_tool = 'MASK'
        else:
            layout.operator("paint.brush_select", text='    Smooth').sculpt_tool = 'SMOOTH'
            layout.operator("paint.brush_select", text='    Flatten').sculpt_tool = 'FLATTEN'
            layout.operator("paint.brush_select", text='    Scrape / Peaks').sculpt_tool = 'SCRAPE'
            layout.operator("paint.brush_select", text='    Fill / Deepen').sculpt_tool = 'FILL'
            layout.operator("paint.brush_select", text='    Layer').sculpt_tool = 'LAYER'
            layout.operator("paint.brush_select", text='    Mask').sculpt_tool = 'MASK'


class PIESPLUS_MT_sculpt_grab(Menu):
    bl_idname = "PIESPLUS_MT_sculpt_grab"
    bl_label = ""

    def draw(self, context):
        if bpy.app.version >= (2, 81, 0):
            global brush_icons
        layout = self.layout
        layout.scale_y = 1.2

        if bpy.app.version >= (2, 81, 0):
            layout.operator("paint.brush_select", text='    Grab', icon_value=brush_icons["grab"]).sculpt_tool = 'GRAB'
            layout.operator("paint.brush_select", text='    Pinch / Magnify', icon_value=brush_icons["pinch"]).sculpt_tool = 'PINCH'
            layout.operator("paint.brush_select", text='    Elastic Deform', icon_value=brush_icons["elastic_deform"]).sculpt_tool = 'ELASTIC_DEFORM'
            layout.operator("paint.brush_select", text='    Snake Hook', icon_value=brush_icons["snake_hook"]).sculpt_tool = 'SNAKE_HOOK'
            layout.operator("paint.brush_select", text='    Thumb', icon_value=brush_icons["thumb"]).sculpt_tool = 'THUMB'
            layout.operator("paint.brush_select", text='    Pose', icon_value=brush_icons["pose"]).sculpt_tool = 'POSE'
            layout.operator("paint.brush_select", text='    Nudge', icon_value=brush_icons["nudge"]).sculpt_tool = 'NUDGE'
            layout.operator("paint.brush_select", text='    Rotate', icon_value=brush_icons["rotate"]).sculpt_tool = 'ROTATE'
        else:
            layout.operator("paint.brush_select", text='    Grab').sculpt_tool = 'GRAB'
            layout.operator("paint.brush_select", text='    Pinch / Magnify').sculpt_tool = 'PINCH'
            layout.operator("paint.brush_select", text='    Snake Hook').sculpt_tool = 'SNAKE_HOOK'
            layout.operator("paint.brush_select", text='    Thumb').sculpt_tool = 'THUMB'
            layout.operator("paint.brush_select", text='    Nudge').sculpt_tool = 'NUDGE'
            layout.operator("paint.brush_select", text='    Rotate').sculpt_tool = 'ROTATE'


########################################################################################################################
# TRANSFORM ORIENTATIONS - ALT + W (V1.2)
########################################################################################################################


#bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
#(popover VIEW3D_PT_transform_orientations)


##############################
#   REGISTRATION    
##############################


    # Icons
brush_icons = {}

def create_icons():
    if bpy.app.version >= (2, 81, 0):
        global brush_icons
        icons_directory = bpy.utils.system_resource('DATAFILES', "icons")

        brushes = ["crease", "blob", "smooth", "draw", "clay", "clay_strips", "inflate", "grab", "nudge", "thumb",
                "snake_hook", "rotate", "flatten", "scrape", "fill", "pinch", "layer", "mask", "pose", "elastic_deform"]
            
        if bpy.app.version >= (2, 83, 0):
            brushes += ["cloth", "clay_thumb", "draw_face_sets"]

        for brush in brushes:
            filename = os.path.join(icons_directory, f"brush.sculpt.{brush}.dat")
            icon_value = bpy.app.icons.new_triangles_from_file(filename)
            brush_icons[brush] = icon_value
    else:
        print("Brush icons are not currently supported in versions of blender lower than 2.81")

def release_icons():
    if bpy.app.version >= (2, 81, 0):
        global brush_icons
        for value in brush_icons.values():
            bpy.app.icons.release(value)

    # Classes
classes = (PIESPLUS_MT_modes,
           PIESPLUS_MT_UV_modes,
           PIESPLUS_MT_snapping,
           PIESPLUS_MT_UV_snapping,
           PIESPLUS_MT_active_tools,
           PIESPLUS_MT_looptools,
           PIESPLUS_MT_origin_pivot,
           PIESPLUS_MT_apply_clear_transforms,
           PIESPLUS_MT_delete,
           PIESPLUS_MT_selection_object_mode,
           PIESPLUS_MT_selection_edit_mode,
           PIESPLUS_MT_shading,
           PIESPLUS_MT_animation,
           PIESPLUS_MT_keyframing,
           PIESPLUS_MT_proportional_edit_mode,
           PIESPLUS_MT_proportional_object_mode,
           PIESPLUS_MT_sculpt,
           PIESPLUS_MT_sculpt_grab,
           PIESPLUS_MT_sculpt_more)

def register():
    create_icons()

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    release_icons()

    for cls in classes:
        bpy.utils.unregister_class(cls)