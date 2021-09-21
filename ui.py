import bpy, os, re, math
from bpy.types import Menu


########################################################################################################################
# CONTEXT MODES - TAB
########################################################################################################################


class PIESPLUS_MT_modes(Menu):
    bl_idname = "PIESPLUS_MT_modes"
    bl_label = "Select Mode"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # Get Active type if one exists
        if context.object:
            ob_type = context.object.type

        pies_plus_prefs = context.preferences.addons[__package__].preferences

        if not context.object:
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            if context.selected_objects:
                pie.operator("pies_plus.edit_mode", text="Edit / Object", icon='OBJECT_DATAMODE')
            else:
                pie.separator()
            # 7 - TOP - LEFT
            if not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("view3d.toggle_xray", text = 'X-Ray Toggle', icon = 'XRAY')
            else:
                pie.separator()
            # 9 - TOP - RIGHT
            if not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("pies_plus.overlay", icon='OVERLAY')
            else:
                pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()

        elif ob_type == 'MESH':
            # 4 - LEFT
            pie.operator("pies_plus.vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator("pies_plus.face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator("pies_plus.edge", icon='EDGESEL')
            # 8 - TOP
            if context.mode == 'EDIT_MESH' or context.mode == 'OBJECT':
                pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            else:
                pie.operator("object.mode_set", text="Edit / Object", icon='OBJECT_DATAMODE').mode = "OBJECT"
            # 7 - TOP - LEFT
            if not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("view3d.toggle_xray", text = 'X-Ray Toggle', icon = 'XRAY')
            else:
                pie.separator()
            # 9 - TOP - RIGHT
            if pies_plus_prefs.sculptors_haven_pref:
                pie.operator("object.mode_set", text="Sculpt Mode", icon='SCULPTMODE_HLT').mode = "SCULPT"
            elif not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("pies_plus.overlay", icon='OVERLAY')
            else:
                pie.separator()
            # 1 - BOTTOM - LEFT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 12.5

            box = col.box().column()
            box.scale_y = 1.2

            box.operator("object.mode_set", text="Sculpt Mode", icon='SCULPTMODE_HLT').mode = "SCULPT"
            box.operator("object.mode_set", text="Weight Paint", icon='WPAINT_HLT').mode = "WEIGHT_PAINT"
            box.operator("object.mode_set", text="Texture Paint", icon='TPAINT_HLT').mode = "TEXTURE_PAINT"
            box.operator("object.mode_set", text="Vertex Paint", icon='VPAINT_HLT').mode = "VERTEX_PAINT"
            box.operator("pies_plus.particle_edit", text="Particle Edit", icon='PARTICLEMODE')

        elif ob_type == 'CAMERA':
            # 4 - LEFT
            pie.prop(context.space_data, "lock_cursor", text="Lock Camera to Cursor", icon='PIVOT_CURSOR')
            # 6 - RIGHT
            pie.prop(context.space_data, "lock_camera", text="Lock Camera to View", icon='OBJECT_DATAMODE')
            # 2 - BOTTOM
            pie.operator("ui.eyedropper_depth", text="DOF Distance", icon='EYEDROPPER')
            # 8 - TOP
            pie.operator("view3d.view_camera", icon='VIEW_CAMERA')
            # 7 - TOP - LEFT
            if not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("view3d.toggle_xray", text = 'X-Ray Toggle', icon = 'XRAY')
            else:
                pie.separator()
            # 9 - TOP - RIGHT
            if not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("pies_plus.overlay", icon='OVERLAY')
            else:
                pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()

        else:
            # 4 - LEFT
            if ob_type == 'GPENCIL':
                pie.operator("gpencil.sculptmode_toggle", text="Sculpt Mode", icon='SCULPTMODE_HLT')
            else:
                pie.separator()
            # 6 - RIGHT
            if ob_type == 'ARMATURE':
                pie.operator("object.posemode_toggle", text="Pose Mode", icon='POSE_HLT')
            elif ob_type == 'GPENCIL':
                pie.operator("gpencil.paintmode_toggle", text="Draw Mode", icon='GREASEPENCIL')
            else:
                pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            if ob_type == 'ARMATURE':
                if context.mode == 'POSE':
                    pie.operator("object.posemode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
                else:
                    pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            elif ob_type in {'CURVE', 'FONT', 'SURFACE', 'META', 'LATTICE'}:
                pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            elif ob_type == 'GPENCIL':
                pie.operator("gpencil.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            else:
                pie.separator()
            # 7 - TOP - LEFT
            if not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("view3d.toggle_xray", text = 'X-Ray Toggle', icon = 'XRAY')
            else:
                pie.separator()
            # 9 - TOP - RIGHT
            if pies_plus_prefs.sculptors_haven_pref:
                pie.operator("object.mode_set", text="Sculpt Mode", icon='SCULPTMODE_HLT').mode = "SCULPT"
            elif not pies_plus_prefs.simple_context_mode_pref:
                pie.operator("pies_plus.overlay", icon='OVERLAY')
            else:
                pie.separator()
            # 1 - BOTTOM - LEFT
            if ob_type == 'GPENCIL':
                pie.operator("gpencil.weightmode_toggle", text="Weight Paint", icon='WPAINT_HLT')
            else:
                pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.prop(context.tool_settings, "use_mesh_automerge", text="Auto Merge")


class PIESPLUS_MT_UV_modes(Menu):
    bl_idname = "PIESPLUS_MT_UV_modes"
    bl_label = "Select Mode (UV)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if context.tool_settings.use_uv_select_sync:
            # 4 - LEFT
            pie.operator("pies_plus.vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator("pies_plus.face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator("pies_plus.edge", icon='EDGESEL')
            # 8 - TOP
            pie.prop(context.scene.pies_plus, "uvSyncSelection", icon='UV_SYNC_SELECT')
        else:
            #4 - LEFT
            pie.operator("pies_plus.uv_sel_change", text='Vertex', icon='VERTEXSEL').sel_choice = 'vertex'
            # 6 - RIGHT
            pie.operator("pies_plus.uv_sel_change", text='Face', icon='FACESEL').sel_choice = 'face'
            # 2 - BOTTOM
            pie.operator("pies_plus.uv_sel_change", text='Edge', icon='EDGESEL').sel_choice = 'edge'
            # 8 - TOP
            pie.prop(context.scene.pies_plus, "uvSyncSelection", icon='UV_SYNC_SELECT')
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.operator("pies_plus.uv_sel_change", text='Island', icon='UV_ISLANDSEL').sel_choice = 'island'


########################################################################################################################
# ACTIVE TOOLS - W
########################################################################################################################


class PIESPLUS_MT_active_tools(Menu):
    bl_idname = "PIESPLUS_MT_active_tools"
    bl_label = "Active Tools"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pies_plus_prefs = context.preferences.addons[__package__].preferences
        
        #4 - LEFT
        pie.operator("wm.tool_set_by_id", text="Move", icon='ORIENTATION_GLOBAL').name = 'builtin.move'
        #6 - RIGHT
        pie.operator("wm.tool_set_by_id", text="Rotate", icon='DRIVER_ROTATIONAL_DIFFERENCE').name = 'builtin.rotate'
        #2 - BOTTOM
        pie.operator("wm.tool_set_by_id", text="Scale", icon='SNAP_FACE').name = 'builtin.scale'
        #8 - TOP
        if pies_plus_prefs.default_tool_pref == 'builtin.select':
            pie.operator("wm.tool_set_by_id", text="Tweak", icon='RESTRICT_SELECT_OFF').name = 'builtin.select'
        elif pies_plus_prefs.default_tool_pref == 'builtin.select_box':
            pie.operator("wm.tool_set_by_id", text="Box", icon='SELECT_SET').name = 'builtin.select_box'
        elif pies_plus_prefs.default_tool_pref == 'builtin.select_circle':
            pie.operator("wm.tool_set_by_id", text="Circle", icon='MESH_CIRCLE').name = 'builtin.select_circle'
        elif pies_plus_prefs.default_tool_pref == 'builtin.select_lasso':
            pie.operator("wm.tool_set_by_id", text="Lasso", icon='GP_ONLY_SELECTED').name = 'builtin.select_lasso'
        #7 - TOP - LEFT
        pie.operator("wm.tool_set_by_id", text="All", icon='GIZMO').name = 'builtin.transform'
        #9 - TOP - RIGHT
        if pies_plus_prefs.default_tool_pref == 'builtin.select_box':
            pie.operator("wm.tool_set_by_id", text="Tweak", icon='RESTRICT_SELECT_OFF').name = 'builtin.select'
        else:
            pie.operator("wm.tool_set_by_id", text="Box", icon='SELECT_SET').name = 'builtin.select_box'
        # 1 - BOTTOM - LEFT
        if pies_plus_prefs.default_tool_pref == 'builtin.select_circle':
            pie.operator("wm.tool_set_by_id", text="Tweak", icon='RESTRICT_SELECT_OFF').name = 'builtin.select'
        else:
            pie.operator("wm.tool_set_by_id", text="Circle", icon='MESH_CIRCLE').name = 'builtin.select_circle'
        # 3 - BOTTOM - RIGHT
        if pies_plus_prefs.default_tool_pref == 'builtin.select_lasso':
            pie.operator("wm.tool_set_by_id", text="Tweak", icon='RESTRICT_SELECT_OFF').name = 'builtin.select'
        else:
            pie.operator("wm.tool_set_by_id", text="Lasso", icon='GP_ONLY_SELECTED').name = 'builtin.select_lasso'


########################################################################################################################
# SNAPPING - SHIFT + TAB
########################################################################################################################


class PIESPLUS_MT_snapping(Menu):
    bl_idname = "PIESPLUS_MT_snapping"
    bl_label = "Snapping"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("pies_plus.snap", text="Vertex", icon='SNAP_VERTEX').snap_elements = 'vertex'
        # 6 - RIGHT
        pie.operator("pies_plus.snap", text="Increment", icon='SNAP_INCREMENT').snap_elements = 'increment'
        # # 2 - BOTTOM
        pie.operator("pies_plus.snap", text="Edge", icon='SNAP_EDGE').snap_elements = 'edge'
        # # 8 - TOP
        pie.prop(context.tool_settings, "use_snap", text="Snap Toggle")
        # # 7 - TOP - LEFT
        pie.operator("pies_plus.snap", text="Volume", icon='SNAP_VOLUME').snap_elements = 'volume'
        # # 9 - TOP - RIGHT
        pie.operator("pies_plus.snap", text="Face", icon='SNAP_FACE').snap_elements = 'face'
        # 1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()

        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
            gap.scale_y = 3.5

            box = col.box().column()
            box.scale_y = 1.2

            box.operator("pies_plus.snap", text="Edge Center", icon='SNAP_MIDPOINT').snap_elements = 'edge_center'
            box.operator("pies_plus.snap", text="Edge Perpendicular", icon='SNAP_PERPENDICULAR').snap_elements = 'edge_perp'
        # 3 - BOTTOM - RIGHT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 12.5
        
        box = col.box().column(align = True)
        box.scale_y = 1.2
        box.scale_x = .9

        ts = context.tool_settings

        box.label(text="Snap With", icon='SNAP_FACE_CENTER')

        split = box.split(align = True)
        split.prop_enum(ts, "snap_target", 'CLOSEST')
        split.prop_enum(ts, "snap_target", 'CENTER')
        split = box.split(align = True)
        split.prop_enum(ts, "snap_target", 'MEDIAN')
        split.prop_enum(ts, "snap_target", 'ACTIVE')

        box = col.box().column()
        box.scale_y = 1.2

        box.label(text="Affect", icon='MOD_TIME')

        row = box.row(align = True)
        row.prop(ts, "use_snap_translate", text='Move')
        row.prop(ts, "use_snap_rotate", text='Rot')
        row.prop(ts, "use_snap_scale", text='Scale')


class PIESPLUS_MT_UV_snapping(Menu):
    bl_idname = "PIESPLUS_MT_UV_snapping"
    bl_label = "Snapping (UV)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("pies_plus.snap", text="Vertex", icon='SNAP_VERTEX').snap_elements = 'uv_vertex'
        # 6 - RIGHT
        pie.operator("pies_plus.snap", text="Increment", icon='SNAP_INCREMENT').snap_elements = 'uv_increment'
        # # 2 - BOTTOM
        pie.separator()
        # # 8 - TOP
        pie.prop(context.tool_settings, "use_snap", text="Snap Toggle")
        # # 7 - TOP - LEFT
        pie.separator()
        # # 9 - TOP - RIGHT
        pie.separator()
        # 1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()

        gap.scale_y = 6.5

        box = col.box().column()
        box.scale_y = 1.2
        box.scale_x = .9

        ts = context.tool_settings

        box.label(text="Snap With:")

        row = box.row(align = True)
        row.prop_enum(ts, "snap_target", 'CLOSEST')
        row.prop_enum(ts, "snap_target", 'CENTER')
        row = box.row(align = True)
        row.prop_enum(ts, "snap_target", 'MEDIAN')
        row.prop_enum(ts, "snap_target", 'ACTIVE')
        # 3 - BOTTOM - RIGHT
        pie.popover(panel="IMAGE_PT_snapping", text="Snap Panel...")


########################################################################################################################
# LOOPTOOLS - SHIFT + Q
########################################################################################################################


class PIESPLUS_MT_looptools(Menu):
    bl_idname = "PIESPLUS_MT_looptools"
    bl_label = "LoopTools"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if 'mesh_looptools' in context.preferences.addons.keys():
            # 4 - LEFT
            pie.operator("mesh.looptools_relax")
            # 6 - RIGHT
            pie.operator("mesh.looptools_space")
            # # 2 - BOTTOM
            pie.operator("mesh.looptools_flatten")
            # # 8 - TOP
            pie.operator("mesh.looptools_circle")
            # # 7 - TOP - LEFT
            pie.operator("mesh.looptools_bridge", text="Loft").loft = True
            # # 9 - TOP - RIGHT
            pie.operator("mesh.looptools_gstretch")
            # 1 - BOTTOM - LEFT
            pie.operator("mesh.looptools_curve")
            # 3 - BOTTOM - RIGHT
            pie.operator("mesh.looptools_bridge", text="Bridge")
        else:
            pie.label(text="          WARNING: You must have LoopTools enabled")


########################################################################################################################
# BOOLTOOL - ALT + C
########################################################################################################################


class PIESPLUS_MT_booltool(Menu):
    bl_idname = "PIESPLUS_MT_booltool"
    bl_label = "Bool Tool"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if len(context.selected_objects) < 2:
            pie.label(text="          WARNING: You must have at least 2 objects selected")

        elif not context.active_object:
            pie.label(text="          WARNING: You must have an Active Object selected")

        elif 'object_boolean_tools' in context.preferences.addons.keys():
            # 4 - LEFT
            pie.operator("object.booltool_auto_slice", text='Auto Slice', icon='SELECT_DIFFERENCE')
            # 6 - RIGHT
            pie.operator("btool.boolean_slice", text='Mod Slice', icon='SELECT_DIFFERENCE')
            # # 2 - BOTTOM
            pie.operator("object.booltool_auto_difference", text='Auto Difference', icon='SELECT_SUBTRACT')
            # # 8 - TOP
            pie.operator("btool.boolean_diff", text='Mod Difference', icon='SELECT_SUBTRACT')
            # # 7 - TOP - LEFT
            pie.operator("btool.boolean_inters", text='Mod Intersect', icon='SELECT_INTERSECT')
            # # 9 - TOP - RIGHT
            pie.operator("btool.boolean_union", text='Mod Union', icon='SELECT_EXTEND')
            # 1 - BOTTOM - LEFT
            pie.operator("object.booltool_auto_union", text='Auto Union', icon='SELECT_EXTEND')
            # 3 - BOTTOM - RIGHT
            pie.operator("object.booltool_auto_intersect", text='Auto Intersect', icon='SELECT_INTERSECT')

        else:
            pie.label(text="          WARNING: You must have Bool Tool enabled")


########################################################################################################################
# TRANSFORMS - CTRL + A
########################################################################################################################


class PIESPLUS_MT_transforms(Menu):
    bl_idname = "PIESPLUS_MT_transforms"
    bl_label = "Transforms & Relations"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if context.selected_objects:
            #4 - LEFT
            pie.operator("pies_plus.transforms", text="Clear All", icon='EMPTY_AXIS').tranforms_type = 'clear_all'
            #6 - RIGHT
            pie.operator("pies_plus.transforms", text="Apply Scale", icon='FILE_TICK').tranforms_type = 'apply_scale'
            #2 - BOTTOM
            pie.operator("pies_plus.transforms", text="Apply All", icon='FILE_TICK').tranforms_type = 'apply_all'
            #8 - TOP
            pie.operator("pies_plus.transforms", text="Apply Rot & Scale", icon='FILE_TICK').tranforms_type = 'apply_rot_scale'
            #7 - TOP - LEFT
            pie.operator("pies_plus.transforms", text="Apply Location", icon='FILE_TICK').tranforms_type = 'apply_loc'
            #9 - TOP - RIGHT
            pie.operator("pies_plus.transforms", text="Apply Rotation", icon='FILE_TICK').tranforms_type = 'apply_rot'
            #1 - BOTTOM - LEFT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 13

            box = col.box().column()
            box.scale_y = 1.2
            box.scale_x = .875

            box.label(text="Clear Transforms", icon='EMPTY_AXIS')

            row = box.row(align = True)
            row.operator("object.location_clear", text='Loc')
            row.operator("object.rotation_clear", text='Rot')
            row.operator("object.scale_clear", text='Scale')

            box = col.box().column()
            box.scale_y = 1.2
            box.scale_x = .875
            
            box.label(text="Apply to Deltas", icon='TRANSFORM_ORIGINS')

            box.operator("object.transforms_to_deltas", text="All Tforms to Deltas")

            row = box.row(align = True)
            row.operator("object.transforms_to_deltas", text="Loc").mode = 'LOC'
            row.operator("object.transforms_to_deltas", text="Rot").mode = 'ROT'
            row.operator("object.transforms_to_deltas", text="Scale").mode = 'SCALE'
            
            # 3 - BOTTOM - RIGHT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 10

            box = col.box().column()
            box.scale_y = 1.2

            box.operator("object.convert", text="Convert to...", icon='FILE_REFRESH')

            make_single_mesh = box.operator("object.make_single_user", text="Make Single User...", icon='USER')
            make_single_mesh.object = True
            make_single_mesh.obdata = True
            make_single_mesh.material = False
            make_single_mesh.animation = False

            box.operator("object.make_override_library", text="Make Library Override...", icon='LIBRARY_DATA_OVERRIDE')

            box = col.box().column()
            box.scale_y = 1.2
            box.operator("object.visual_transform_apply", text="Apply Visual Transforms", icon='FILE_TICK')
        else:
            pie.label(text="          WARNING: You must have an object selected")


########################################################################################################################
# CURSOR / ORIGIN - SHIFT + S
########################################################################################################################


class PIESPLUS_MT_origin_pivot(Menu):
    bl_idname = "PIESPLUS_MT_origin_pivot"
    bl_label = "Origin / Cursor"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if context.object:
            # 4 - LEFT
            pie.operator("object.origin_set", text="Origin to Cursor", icon='PIVOT_BOUNDBOX').type = 'ORIGIN_CURSOR'
            # 6 - RIGHT
            pie.operator("view3d.snap_cursor_to_selected", text="Cursor to Selection", icon='PIVOT_CURSOR')
            # 2 - BOTTOM
            pie.operator("pies_plus.origin_to_selection", icon='PIVOT_BOUNDBOX')
            # 8 - TOP
            pie.operator("view3d.snap_selected_to_cursor", text="Sel to Cursor (O)", icon='RESTRICT_SELECT_OFF').use_offset = True
            # 7 - TOP - LEFT
            pie.operator("object.origin_set", text="Origin to Geo", icon='PIVOT_BOUNDBOX').type = 'ORIGIN_GEOMETRY'
            # 9 - TOP - RIGHT
            pie.operator("view3d.snap_cursor_to_active", text="Cursor to Active", icon='PIVOT_CURSOR')
            # 1 - BOTTOM - LEFT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 15.7

            box = col.box().column(align=True)
            
            row = box.row(align=True) # Row to affect scaling
            row.scale_y = 1.2
            row.operator("pies_plus.reset_origin", text='Origin to 0,0,0', icon='PIVOT_BOUNDBOX').origin_reset_axis = 'origin_all'
            row = box.row(align=True)
            row.scale_y = 1
            row.operator("pies_plus.reset_origin", text='X').origin_reset_axis = 'origin_x'
            row.operator("pies_plus.reset_origin", text='Y').origin_reset_axis = 'origin_y'
            row.operator("pies_plus.reset_origin", text='Z').origin_reset_axis = 'origin_z'

            box = col.box().column()
            box.scale_y = 1.2

            box.operator("pies_plus.edit_origin", icon='OBJECT_ORIGIN').edit_type = 'origin'
            box.operator("object.origin_set", text="Geo to Origin", icon='PIVOT_BOUNDBOX').type = 'GEOMETRY_ORIGIN'
            box.operator("pies_plus.origin_to_com", icon='PIVOT_BOUNDBOX')
            box.operator("pies_plus.origin_to_bottom", icon='PIVOT_BOUNDBOX')
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
            pie.separator()

        # 3 - BOTTOM - RIGHT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 12.7

        box = col.box().column(align=True)
        row = box.row(align=True)
        row.scale_y = 1.2
        row.operator("pies_plus.reset_cursor", text='Cursor to 0,0,0', icon='PIVOT_CURSOR').cursor_reset_axis = 'cursor_all'
        row = box.row(align=True)
        row.scale_y = 1
        row.operator("pies_plus.reset_cursor", text='X').cursor_reset_axis = 'cursor_x'
        row.operator("pies_plus.reset_cursor", text='Y').cursor_reset_axis = 'cursor_y'
        row.operator("pies_plus.reset_cursor", text='Z').cursor_reset_axis = 'cursor_z'

        box = col.box().column()
        box.scale_y = 1.2
        box.operator("pies_plus.edit_origin", text = 'Edit Cursor', icon='OBJECT_ORIGIN').edit_type = 'cursor'
        box.operator("pies_plus.reset_cursor_rot", icon='PIVOT_CURSOR')
        box.operator("view3d.snap_selected_to_cursor", text="Sel to Cursor", icon='RESTRICT_SELECT_OFF').use_offset = False


########################################################################################################################
# DELETE - X
########################################################################################################################


class PIESPLUS_MT_delete(Menu):
    bl_idname = "PIESPLUS_MT_delete"
    bl_label = "Delete"

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.mode == 'EDIT'

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.operator("mesh.delete", text="Delete Vertices", icon='VERTEXSEL').type = 'VERT'
        #6 - RIGHT
        pie.operator("mesh.delete", text="Delete Faces", icon='FACESEL').type = 'FACE'
        #2 - BOTTOM
        pie.operator("mesh.delete", text="Delete Edges", icon='EDGESEL').type = 'EDGE'
        #8 - TOP
        pie.operator("mesh.dissolve_edges", text="Dissolve Edges", icon='SNAP_EDGE')
        #7 - TOP - LEFT
        pie.operator("mesh.dissolve_verts", text="Dissolve Vertices", icon='SNAP_VERTEX')
        #9 - TOP - RIGHT
        pie.operator("mesh.dissolve_limited", text="Limited Dissolve", icon='STICKY_UVS_LOC')
        #1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 17

        box = col.box().column()
        box.scale_y = 1.2

        box.operator("mesh.remove_doubles", text="Merge by Distance", icon='AUTOMERGE_ON')

        box2 = col.box().column()
        box2.scale_y = 1.25

        box2.operator("mesh.delete_loose", text="Delete Loose", icon='STICKY_UVS_VERT')

        box2 = col.box().column()
        box2.scale_y = 1.25

        box2.operator("mesh.dissolve_faces", text="Dissolve Faces", icon='SNAP_FACE')
        box2.operator("mesh.delete", text="Only Edge & Faces", icon='SNAP_FACE').type = 'EDGE_FACE'
        box2.operator("mesh.delete", text="Only Faces", icon='FACESEL').type = 'ONLY_FACE'
        box2.operator("mesh.dissolve_edges", text="Dissolve Edges (No V)", icon='SNAP_EDGE').use_verts = False
        #3 - BOTTOM - RIGHT
        pie.operator("mesh.edge_collapse", text="Edge Collapse", icon='UV_EDGESEL')


class PIESPLUS_MT_delete_curve(Menu):
    bl_idname = "PIESPLUS_MT_delete_curve"
    bl_label = "Delete (Curve)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.operator("curve.delete", text="Delete Vertices").type = 'VERT'
        #6 - RIGHT
        pie.operator("curve.delete", text="Delete Segments").type = 'SEGMENT'
        #2 - BOTTOM
        pie.operator("curve.dissolve_verts", text="Dissolve Vertices")


########################################################################################################################
# SELECTION - A
########################################################################################################################


class PIESPLUS_MT_selection_object_mode(Menu):
    bl_idname = "PIESPLUS_MT_selection_object_mode"
    bl_label = "Object Selection & Views"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.separator()
        #6 - RIGHT
        pie.operator("view3d.view_camera", icon='VIEW_CAMERA')
        #2 - BOTTOM
        pie.operator("object.select_all", text="Invert Selection", icon='SELECT_DIFFERENCE').action = 'INVERT'
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
        box.scale_y = 1.2
        box.operator("object.select_random", text="Select Random", icon='GROUP_VERTEX')
        box.operator("object.select_by_type", text="Select By Type...", icon='SNAP_VOLUME')
        box.operator("object.select_grouped", text="Select Grouped...", icon='GROUP_VERTEX')
        row = box.row(align=True)
        row.operator("object.select_linked", text="Select Linked...", icon='CONSTRAINT_BONE')
        row.operator("pies_plus.make_links", text="", icon='PLUS')
        #1 - BOTTOM - LEFT
        pie.operator("object.join", text="Merge To Active", icon='OBJECT_DATA')


class PIESPLUS_MT_selection_edit_mode(Menu):
    bl_idname = "PIESPLUS_MT_selection_edit_mode"
    bl_label = "Mesh Selection"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        #4 - LEFT
        pie.operator("mesh.faces_select_linked_flat",
                     text="Select Linked Flat", icon='VIEW_ORTHO')
        #6 - RIGHT
        pie.operator("mesh.select_linked", text="Select Linked All",
                     icon='STICKY_UVS_LOC').delimit = set()
        #2 - BOTTOM
        pie.operator("mesh.select_all", text="Invert Selection",
                     icon='SELECT_DIFFERENCE').action = 'INVERT'
        #8 - TOP
        pie.operator("pies_plus.mesh_selection", icon='RESTRICT_SELECT_OFF')
        #7 - TOP - LEFT
        pie.operator("pies_plus.ring_sel", text="Ring Select", icon='META_CUBE')
        #9 - TOP - RIGHT
        pie.operator("pies_plus.loop_sel", text="Loop Select", icon='META_BALL')
        #1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 15.5

        box = col.box().column()
        box.scale_y = 1.2
        box.operator("mesh.select_random", text="Select Random", icon='GROUP_VERTEX')
        box.operator("mesh.region_to_loop", text="Select Boundary Loop", icon='MESH_PLANE')
        box.operator("pies_plus.select_loop_inner_region", icon='SNAP_FACE_CENTER')
        box.operator("mesh.select_similar", text="Select Similar...", icon='PIVOT_INDIVIDUAL')
        box.operator("mesh.edges_select_sharp", text="Select by Edge Angle", icon='MOD_EDGESPLIT')
        row = box.row(align=True)
        row.scale_x = .7
        row.label(text="Select:")
        row.operator("pies_plus.select_seamed", text="Seams")
        row.operator("pies_plus.select_sharped", text="Sharps")
        #3 - BOTTOM - RIGHT
        pie.operator("mesh.select_nth", text="Checker Deselect", icon='PARTICLE_POINT')


########################################################################################################################
# SHADING - Z
########################################################################################################################


class PIESPLUS_MT_shading(Menu):
    bl_idname = "PIESPLUS_MT_shading"
    bl_label = "Shading & Overlays"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        space = context.space_data

        # 4 - LEFT
        pie.prop_enum(space.shading, "type", 'WIREFRAME')
        # 6 - RIGHT
        pie.prop_enum(space.shading, "type", 'SOLID')
        # 2 - BOTTOM
        if context.scene.render.engine in ('CYCLES', 'BLENDER_EEVEE'):
            pie.prop_enum(space.shading, "type", 'MATERIAL')
        else:
            pie.separator()   
        # 8 - TOP
        pie.prop_enum(space.shading, "type", 'RENDERED')
        # 7 - TOP - LEFT
        pie.operator("view3d.toggle_xray", text = 'X-Ray Toggle', icon = 'XRAY')
        # 9 - TOP - RIGHT
        pie.operator("pies_plus.overlay", icon='OVERLAY')
        #1 - BOTTOM - LEFT
        col = pie.column()

        col.scale_x = .96 # Override for X axis scaling

        gap = col.column()
        gap.separator()
        gap.scale_y = 19.5

        box = col.box().column()
        box.scale_y = 1.2

        split = box.split(factor=.55, align = True)

        split_left = split.row(align = True)
        split_left.scale_x = .1
        split_left.operator("pies_plus.auto_smooth")

        split_right = split.row(align= True)
        split_right.prop(context.scene.pies_plus, "smoothAngle", text = "")
        split_right.operator("pies_plus.remove_auto_smooth", icon = 'REMOVE')

        row = box.row(align = True)
        row.scale_y = .95
        row.label(text = "Shade:")
        row.operator("pies_plus.shade_smooth", text = "Smooth")
        row.operator("pies_plus.shade_flat", text = "Flat")

        box = col.box().column()
        box.scale_y = 1.2
        box.operator("pies_plus.recalc_normals", icon='NORMALS_FACE')
        box.operator("pies_plus.auto_fwn", icon='NORMALS_VERTEX_FACE')
        box.operator("pies_plus.remove_custom_normals", icon='X')

        box = col.box().column()
        box.scale_y = 1.2
        row = box.row()
        row.prop(space.overlay, "show_face_orientation", text = 'Face Orientation Overlay')
        row = box.row(align = True)
        row.operator("pies_plus.wire_per_obj", icon='MOD_WIREFRAME')
        row.operator("pies_plus.remove_wire_per_obj", icon='REMOVE')
        # 3 - BOTTOM - RIGHT
        pie.prop(space.overlay, "show_wireframes", text = 'Wire Overlay', icon = 'MOD_WIREFRAME')


########################################################################################################################
# ANIMATION - SHIFT + SPACE
########################################################################################################################


class PIESPLUS_MT_animation(Menu):
    bl_idname = "PIESPLUS_MT_animation"
    bl_label = "Animation (Playback)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        # 6 - RIGHT
        pie.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True
        # 2 - BOTTOM
        pie.prop(context.tool_settings, "use_keyframe_insert_auto", text="Auto Key", icon='REC')
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
# KEYFRAMING - ALT + SPACE
########################################################################################################################


class PIESPLUS_MT_keyframing(Menu):
    bl_idname = "PIESPLUS_MT_keyframing"
    bl_label = "Keyframing"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        if not context.selected_objects:
            if context.object:
                if context.mode == "POSE" and not context.selected_pose_bones:
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

        elif context.mode not in {'POSE', 'OBJECT'}:
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            if context.object.type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'META', 'LATTICE', 'ARMATURE'}:
                pie.operator("object.editmode_toggle", text="Edit / Object", icon='OBJECT_DATAMODE')
            else:
                pie.separator()
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            if context.object.type == "ARMATURE":
                pie.operator("object.posemode_toggle", text="Pose Mode", icon='POSE_HLT')

        elif context.mode == "POSE" and not context.selected_pose_bones:
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
            pie.prop(context.tool_settings, "use_keyframe_insert_auto", text="Auto Key")
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
            box.scale_y = 1.2
            box.operator("pies_plus.keyframing", text="Visual Location").key_choice = 'key_vis_loc'
            box.operator("pies_plus.keyframing", text="Visual Rotation").key_choice = 'key_vis_rot'
            box.operator("pies_plus.keyframing", text="Visual Scaling").key_choice = 'key_vis_scale'
            box.operator("pies_plus.keyframing", text="Visual LocRotScale").key_choice = 'key_vis_locrotscale'
            box.operator("pies_plus.keyframing", text="Visual LocScale").key_choice = 'key_vis_locscale'
            box.operator("pies_plus.keyframing", text="Visual RotScale").key_choice = 'key_vis_rotscale'

            if context.mode == "POSE":
                gap = col.column()

                box = col.box().column()
                box.scale_y = 1.2
                box.operator("pies_plus.keyframing", text="BBone Shape").key_choice = 'key_bendy_bones'
                box.operator("pies_plus.keyframing", text="Whole Character").key_choice = 'key_whole_char'
                box.operator("pies_plus.keyframing", text="Whole Selected").key_choice = 'key_whole_char_sel'
            # 3 - BOTTOM - RIGHT
            col = pie.column()

            gap = col.column()
            gap.separator()
            gap.scale_y = 20.5

            box = col.box().column()
            box.scale_y = 1.2
            box.operator("pies_plus.keyframing", text="Available").key_choice = 'key_available'

            gap = col.column()

            box = col.box().column()
            box.scale_y = 1.2
            box.operator("pies_plus.keyframing", text="LocRotScale").key_choice = 'key_locrotscale'
            box.operator("pies_plus.keyframing", text="LocScale").key_choice = 'key_locscale'
            box.operator("pies_plus.keyframing", text="RotScale").key_choice = 'key_rotscale'

            gap = col.column()

            box = col.box().column()
            box.scale_y = 1.2
            box.operator("pies_plus.keyframing", text="Delta Location").key_choice = 'key_del_loc'
            box.operator("pies_plus.keyframing", text="Delta Rotation").key_choice = 'key_del_rot'
            box.operator("pies_plus.keyframing", text="Delta Scale").key_choice = 'key_del_scale'


########################################################################################################################
# PROPORTIONAL EDITING - ALT + O
########################################################################################################################


class PIESPLUS_MT_proportional_edit_mode(Menu):
    bl_idname = "PIESPLUS_MT_proportional_edit_mode"
    bl_label = "Proportional (Edit Mode)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        ts = context.tool_settings

        # 4 - LEFT
        pie.operator("pies_plus.change_proportional_falloff", text='Smooth', icon='SMOOTHCURVE').falloff_type = 'SMOOTH'
        # 6 - RIGHT
        pie.operator("pies_plus.change_proportional_falloff", text='Sphere', icon='SPHERECURVE').falloff_type = 'SPHERE'
        # 2 - BOTTOM
        pie.operator("pies_plus.change_proportional_falloff", text='Inverse Square', icon='INVERSESQUARECURVE').falloff_type = 'INVERSE_SQUARE'
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
        box.scale_y = 1.2
        box.operator("pies_plus.change_proportional_falloff", text='Constant', icon='NOCURVE').falloff_type = 'CONSTANT'
        box.operator("pies_plus.change_proportional_falloff", text='Random', icon='RNDCURVE').falloff_type = 'RANDOM'
        box.operator("pies_plus.change_proportional_falloff", text='Sharp', icon='SHARPCURVE').falloff_type = 'SHARP'
        box.operator("pies_plus.change_proportional_falloff", text='Linear', icon='LINCURVE').falloff_type = 'LINEAR'
        # 3 - BOTTOM - RIGHT
        pie.operator("pies_plus.change_proportional_falloff", text='Root', icon='ROOTCURVE').falloff_type = 'ROOT'


class PIESPLUS_MT_proportional_object_mode(Menu):
    bl_idname = "PIESPLUS_MT_proportional_object_mode"
    bl_label = "Proportional (Object Mode)"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("pies_plus.change_proportional_falloff", text='Smooth', icon='SMOOTHCURVE').falloff_type = 'SMOOTH'
        # 6 - RIGHT
        pie.operator("pies_plus.change_proportional_falloff", text='Sphere', icon='SPHERECURVE').falloff_type = 'SPHERE'
        # 2 - BOTTOM
        pie.operator("pies_plus.change_proportional_falloff", text='Inverse Square', icon='INVERSESQUARECURVE').falloff_type = 'INVERSE_SQUARE'
        # 8 - TOP
        pie.prop(context.tool_settings, "use_proportional_edit_objects", text="Proportional Toggle")
        # 7 - TOP - LEFT
        pie.operator("pies_plus.change_proportional_falloff", text='Sharp', icon='SHARPCURVE').falloff_type = 'SHARP'
        # 9 - TOP - RIGHT
        pie.operator("pies_plus.change_proportional_falloff", text='Linear', icon='LINCURVE').falloff_type = 'LINEAR'
        # 1 - BOTTOM - LEFT
        col = pie.column()

        gap = col.column()
        gap.separator()
        gap.scale_y = 6

        box = col.box().column()
        box.scale_y = 1.2
        box.operator("pies_plus.change_proportional_falloff", text='Constant', icon='NOCURVE').falloff_type = 'CONSTANT'
        box.operator("pies_plus.change_proportional_falloff", text='Random', icon='RNDCURVE').falloff_type = 'RANDOM'
        # 3 - BOTTOM - RIGHT
        pie.operator("pies_plus.change_proportional_falloff", text='Root', icon='ROOTCURVE').falloff_type = 'ROOT'


########################################################################################################################
# SCULPT TOOLS - W
########################################################################################################################


class PIESPLUS_MT_sculpt(Menu):
    bl_idname = "PIESPLUS_MT_sculpt"
    bl_label = "Sculpt Tools"

    def draw(self, context):
        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
            global brush_icons

        layout = self.layout
        pie = layout.menu_pie()
        layout.scale_y = 1.2

        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
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
        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
            global brush_icons

        layout = self.layout
        layout.scale_y = 1.2

        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
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
        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
            global brush_icons

        layout = self.layout
        layout.scale_y = 1.2

        if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
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
# SAVE - S
########################################################################################################################


class PIESPLUS_MT_save(Menu):
    bl_idname = "PIESPLUS_MT_save"
    bl_label = "Save"

    def get_save_increment_number(self, context):
        # Get file name and dir path
        dir_path = os.path.dirname(bpy.data.filepath)
        file_name = os.path.basename(bpy.data.filepath)[:-6]

        # Look for other files in the same folder with the same base name & set the increment number
        list_of_blends = []
        
        for file in os.listdir(dir_path):
            if file.endswith(".blend") and '_' in file:
                delimiters = ".blend", "_"
                regex_pattern = '|'.join(map(re.escape, delimiters))

                # Split the string & convert to a number
                try:
                    increment_number = int(re.split(regex_pattern, file)[-2])
                    
                    list_of_blends.append(increment_number)
                except ValueError:
                    pass

        if list_of_blends:
            list_of_blends_max = max(list_of_blends) + 1

            digits = int(math.log10(list_of_blends_max)) + 1

            fill_digit_gaps = "0" * (3 - digits)

            increment_number = "_" + fill_digit_gaps + str(list_of_blends_max)
        else:
            increment_number = "_001"

        # Return the final to-be output path
        final_path = os.path.join(dir_path, file_name.split('_')[0] + increment_number + '.blend')
        return final_path, increment_number

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("wm.open_mainfile", text="Open...", icon='FILEBROWSER')
        # 6 - RIGHT
        pie.operator("wm.save_as_mainfile", text="Save As...", icon='FILE_TICK')
        # 2 - BOTTOM
        pie.operator("wm.read_homefile", text="New", icon='FILE_NEW')
        # 8 - TOP
        pie.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
        # 7 - TOP - LEFT
        pie.separator()
        # 9 - TOP - RIGHT
        pie.separator()
        # 1 - BOTTOM - LEFT
        col = pie.column()

        col.scale_x = .925 # Override for X axis scaling

        gap = col.column()
        gap.separator()
        gap.scale_y = 11.8

        box = col.box().column()
        box.scale_y = 1.2

        if bpy.data.is_saved:
            default_operator_context = layout.operator_context
            layout.operator_context = 'EXEC_DEFAULT'

            final_path, increment_number = self.get_save_increment_number(context)

            save_increment = box.operator("wm.save_as_mainfile", text=f"Save Increment  ({increment_number})", icon='FILE_TICK')
            save_increment.filepath = final_path
            save_increment.copy = True

            layout.operator_context = default_operator_context
        else:
            box.enabled = False
            box.operator("wm.save_as_mainfile", text="Save Increment  (not saved)", icon='FILE_TICK')

        box = col.box().column()
        box.scale_y = 1.2
        split = box.split(align = True)
        split.operator("wm.call_menu", text="Open Recent...").name = "TOPBAR_MT_file_open_recent"
        split.operator("pies_plus.open_last", text="Open Last", icon='LOOP_BACK')

        split = box.split(align = True)
        split.operator("wm.recover_auto_save", text="Auto Save... ")
        split.operator("wm.recover_last_session", text='Rec Last', icon='RECOVER_LAST')

        box = col.box().column()
        box.scale_y = 1.2
        split = box.split(factor = .475, align = True)
        split.operator("wm.link", text="Link...", icon='LINK_BLEND')
        split.operator("wm.append", text="Append...", icon='APPEND_BLEND')
        # 3 - BOTTOM - RIGHT
        col = pie.column()

        col.scale_x = .95 # Override for X axis scaling

        gap = col.column()
        gap.separator()
        gap.scale_y = 10

        box = col.box().column()
        box2 = box.box()
        box2.scale_y = 1.3
        box2.menu("TOPBAR_MT_file_export", icon='EXPORT', text="Export                   -->")

        box = col.box().column()
        box2 = box.box()
        box2.scale_y = 1.3
        box2.menu("TOPBAR_MT_file_import", icon='IMPORT', text="Import                   -->")

        split = box.split(align = True)
        split.scale_y = 1.1
        split.label(text = 'Batch:')

        split.operator("pies_plus.batch_import", text='FBX').import_type = 'fbx'
        split.operator("pies_plus.batch_import", text='OBJ').import_type = 'obj'


########################################################################################################################
# ALIGN - SHIFT + X
########################################################################################################################


class PIESPLUS_MT_align(Menu):
    bl_idname = "PIESPLUS_MT_align"
    bl_label = "Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("pies_plus.world_align", text = "Align Global X", icon = 'AXIS_FRONT').align_axis = 'align_x'
        # 6 - RIGHT
        pie.operator("pies_plus.world_align", text = "Align Global Y", icon = 'AXIS_SIDE').align_axis = 'align_y'
        # 2 - BOTTOM
        pie.operator("pies_plus.world_align", text = "Align Global Z", icon = 'AXIS_TOP').align_axis = 'align_z'
        # 8 - TOP
        pie.operator("pies_plus.quick_world_align", icon = 'EMPTY_DATA')
        # 7 - TOP - LEFT
        pie.operator("pies_plus.active_face_align", icon = 'PIVOT_ACTIVE')
        # 9 - TOP - RIGHT
        pie.operator("pies_plus.normal_z_align", icon = 'ORIENTATION_NORMAL')
        # 1 - BOTTOM - LEFT
        col = pie.column()

        col.scale_x = .975 # Override for X axis scaling

        gap = col.column()
        gap.separator()
        gap.scale_y = 9.8

        box = col.box().column(align=True)

        row = box.row()
        row.scale_y = 1.25
        row.label(text = "Align to Local Axis", icon = 'ORIENTATION_LOCAL')
        row = box.row(align=True)
        row.scale_y = 1.2
        row.operator("pies_plus.local_align", text = "X").align_axis = 'align_x'
        row.operator("pies_plus.local_align", text = "Y").align_axis = 'align_y'
        row.operator("pies_plus.local_align", text = "Z").align_axis = 'align_z'

        box = col.box().column(align=True)

        row = box.row()
        row.scale_y = 1.25
        row.label(text = "Align to Active Vert", icon = 'PIVOT_ACTIVE')
        row = box.row(align=True)
        row.scale_y = 1.2
        row.operator("pies_plus.active_vert_align", text='X').align_axis = 'align_x'
        row.operator("pies_plus.active_vert_align", text='Y').align_axis = 'align_y'
        row.operator("pies_plus.active_vert_align", text='Z').align_axis = 'align_z'
        # 3 - BOTTOM - RIGHT
        pie.separator()


##############################
#   REGISTRATION
##############################


brush_icons = {}

def create_icons():
    global brush_icons

    icons_directory = bpy.utils.system_resource('DATAFILES', "icons")

    brushes = [
        "crease", "blob", "smooth", "draw", "clay", "clay_strips", "inflate", "grab", "nudge", "thumb",
        "snake_hook", "rotate", "flatten", "scrape", "fill", "pinch", "layer", "mask", "pose", "elastic_deform"
    ]

    if bpy.app.version >= (2, 83, 0):
        brushes += ["cloth", "clay_thumb", "draw_face_sets"]

    for brush in brushes:
        filename = os.path.join(icons_directory, f"brush.sculpt.{brush}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[brush] = icon_value

def release_icons():
    global brush_icons

    for value in brush_icons.values():
        bpy.app.icons.release(value)


classes = (
    PIESPLUS_MT_modes,
    PIESPLUS_MT_UV_modes,
    PIESPLUS_MT_snapping,
    PIESPLUS_MT_UV_snapping,
    PIESPLUS_MT_active_tools,
    PIESPLUS_MT_looptools,
    PIESPLUS_MT_booltool,
    PIESPLUS_MT_origin_pivot,
    PIESPLUS_MT_transforms,
    PIESPLUS_MT_delete,
    PIESPLUS_MT_delete_curve,
    PIESPLUS_MT_selection_object_mode,
    PIESPLUS_MT_selection_edit_mode,
    PIESPLUS_MT_shading,
    PIESPLUS_MT_animation,
    PIESPLUS_MT_keyframing,
    PIESPLUS_MT_proportional_edit_mode,
    PIESPLUS_MT_proportional_object_mode,
    PIESPLUS_MT_sculpt,
    PIESPLUS_MT_sculpt_grab,
    PIESPLUS_MT_sculpt_more,
    PIESPLUS_MT_save,
    PIESPLUS_MT_align
)


def register():
    if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
        create_icons()

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    if bpy.app.version >= (2, 81, 0) and bpy.app.version < (3, 0, 0):
        release_icons()

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
