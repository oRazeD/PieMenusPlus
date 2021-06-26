import bpy, rna_keymap_ui
from bpy.props import StringProperty, EnumProperty, BoolProperty, IntProperty, PointerProperty
from .addon_updater import Updater as updater
from .__init__ import bl_info


##################################
# Operators
##################################


class PIESPLUS_OT_check_for_update(bpy.types.Operator):
    bl_idname = "updater_pies_plus.check_for_update"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        updater.check_for_update_now()
        return{'FINISHED'}


##################################
# Property Group
##################################


class PIESPLUS_property_group(bpy.types.PropertyGroup):
    def update_smoothAngle(self, context):
        if context.selected_objects:
            bpy.ops.pies_plus.auto_smooth()

    def update_uvSyncSelection(self, context):
        context.scene.tool_settings.use_uv_select_sync = self.uvSyncSelection

        if context.preferences.addons[__package__].preferences.preserve_uv_selection_pref:
            if not context.scene.tool_settings.use_uv_select_sync:
                old_area_type = context.area.type
                    
                context.area.type = 'VIEW_3D'

                bpy.ops.mesh.select_all(action='SELECT')

                context.area.type = old_area_type

    smoothAngle: IntProperty(
        name="Smooth Angle",
        default=60,
        min=0,
        max=180,
        update=update_smoothAngle
    )
        
    uvSyncSelection: BoolProperty(
        name="UV Sync Selection",
        update=update_uvSyncSelection
    )

    dropdownDelete: BoolProperty()
    dropdownSelection: BoolProperty()
    dropdownProportional: BoolProperty()
    dropdownSnapping: BoolProperty()
    dropdownSelectMode: BoolProperty()
    dropdownTools: BoolProperty()
    dropdownAnimation: BoolProperty()
    dropdownShading: BoolProperty()
    dropdownOrigin: BoolProperty()
    dropdownTransform: BoolProperty()
    dropdownLT: BoolProperty()
    dropdownBT: BoolProperty()
    dropdownSave: BoolProperty()
    dropdownAlign: BoolProperty()


##################################
# Keymapping
##################################


class PIESPLUS_addon_keymaps:
    _addon_keymaps = []
    _keymaps = {}

    @classmethod
    def new_keymap(cls, name, kmi_name, kmi_value=None, km_name='3D View',
                   space_type="VIEW_3D", region_type="WINDOW",
                   event_type=None, event_value=None, ctrl=False, shift=False,
                   alt=False, key_modifier="NONE"):

        cls._keymaps.update({name: [kmi_name, kmi_value, km_name, space_type,
                                    region_type, event_type, event_value,
                                    ctrl, shift, alt, key_modifier]})

    @classmethod
    def add_hotkey(cls, kc, keymap_name):
        items = cls._keymaps.get(keymap_name)
        if not items:
            return

        kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
        event_type, event_value, ctrl, shift, alt, key_modifier = items[5:]
        km = kc.keymaps.new(name=km_name, space_type=space_type,
                            region_type=region_type)

        kmi = km.keymap_items.new(kmi_name, event_type, event_value,
                                  ctrl=ctrl, shift=shift, alt=alt,
                                  key_modifier=key_modifier)

        if kmi_value:
            kmi.properties.name = kmi_value

        kmi.active = True

        cls._addon_keymaps.append((km, kmi))

    @staticmethod
    def register_keymaps():
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon

        if not kc:
            return

        for keymap_name in PIESPLUS_addon_keymaps._keymaps.keys():
            PIESPLUS_addon_keymaps.add_hotkey(kc, keymap_name)

    @classmethod
    def unregister_keymaps(cls):
        kmi_values = [item[1] for item in cls._keymaps.values() if item]

        for km, kmi in cls._addon_keymaps:
            if hasattr(kmi.properties, 'name'):
                if kmi_values:
                    if kmi.properties.name in kmi_values:
                        km.keymap_items.remove(kmi)

        cls._addon_keymaps.clear()

    @staticmethod
    def get_hotkey_entry_item(name, kc, km, kmi_name, kmi_value, col):
        for km_item in km.keymap_items:
            if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
                col.context_pointer_set('keymap', km)
                rna_keymap_ui.draw_kmi([], kc, km, km_item, col, 0)
                return

        col.label(text=f"No hotkey entry found for {name}")
        col.operator(PIESPLUS_OT_add_hotkey.bl_idname, text="Restore keymap", icon='ADD').km_name = km.name

    @staticmethod
    def draw_keymap_items(wm, layout):
        pies_plus = bpy.context.scene.pies_plus

        deleteUsed = False
        selectionUsed = False
        proportionalUsed = False
        snappingUsed = False
        selectModeUsed = False
        animationUsed = False
        toolsUsed = False
        shadingUsed = False
        transformUsed = False
        originUsed = False
        ltUsed = False
        btUsed = False
        saveUsed = False
        alignUsed = False

        for name, items in PIESPLUS_addon_keymaps._keymaps.items():
            drawKeymap = False

            # Tools
            if name.endswith('Tools'):
                if not toolsUsed:
                    toolsUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownTools', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownTools else "RIGHTARROW")
                    row.label(text="Active Tool Pies")
                    row.label(text="Context: [3D View, Sculpt]")

                if pies_plus.dropdownTools:
                    drawKeymap = True

            # Align
            elif name.startswith('Align'):
                if not alignUsed:
                    alignUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownAlign', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownAlign else "RIGHTARROW")
                    row.label(text="Align Pies")
                    row.label(text="Context: [Mesh]")

                if pies_plus.dropdownAlign:
                    drawKeymap = True

            # Animation
            elif name.startswith('Animation'):
                if not animationUsed:
                    animationUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownAnimation', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownAnimation else "RIGHTARROW")
                    row.label(text="Anim Playback & Keyframing Pies")
                    row.label(text="Context: [3D View]")

                if pies_plus.dropdownAnimation:
                    drawKeymap = True
            
            # Bool Tool
            elif name.startswith('Bool Tool'):
                if not btUsed:
                    btUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownBT', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownBT else "RIGHTARROW")
                    row.label(text="Bool Tool Pies")
                    row.label(text="Context: [Object]")

                if pies_plus.dropdownBT:
                    drawKeymap = True

            # Delete
            elif name.startswith('Delete'):
                if not deleteUsed:
                    deleteUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownDelete', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownDelete else "RIGHTARROW")
                    row.label(text="Delete Pies")
                    row.label(text="Context: [Mesh, Curve]")

                if pies_plus.dropdownDelete:
                    drawKeymap = True


            # LoopTools
            elif name.startswith('LoopTools'):
                if not ltUsed:
                    ltUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownLT', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownLT else "RIGHTARROW")
                    row.label(text="LoopTools Pies")
                    row.label(text="Context: [Mesh]")

                if pies_plus.dropdownLT:
                    drawKeymap = True

            # Origin / Cursor
            elif name.startswith('Origin'):
                if not originUsed:
                    originUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownOrigin', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownOrigin else "RIGHTARROW")
                    row.label(text="Origin / Cursor Pies")
                    row.label(text="Context: [3D View]")

                if pies_plus.dropdownOrigin:
                    drawKeymap = True

            # Proportional
            elif name.startswith('Proportional'):
                if not proportionalUsed:
                    proportionalUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownProportional', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownProportional else "RIGHTARROW")
                    row.label(text="Proportional Pies")
                    row.label(text="Context: [Object, Mesh]")

                if pies_plus.dropdownProportional:
                    drawKeymap = True

            # Save
            elif name.startswith('Save'):
                if not saveUsed:
                    saveUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownSave', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownSave else "RIGHTARROW")
                    row.label(text="Save Pies")
                    row.label(text="Context: [3D View]")

                if pies_plus.dropdownSave:
                    drawKeymap = True

            # Select Mode
            elif name.startswith('Select Mode'):
                if not selectModeUsed:
                    selectModeUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownSelectMode', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownSelectMode else "RIGHTARROW")
                    row.label(text="Select Mode Pies")
                    row.label(text="Context: [3D View, UV Editor]")

                if pies_plus.dropdownSelectMode:
                    drawKeymap = True

            # Selection
            elif name.startswith('Selection'):
                if not selectionUsed:
                    selectionUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownSelection', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownSelection else "RIGHTARROW")
                    row.label(text="Selection Pies")
                    row.label(text="Context: [Object, Mesh]")

                if pies_plus.dropdownSelection:
                    drawKeymap = True

            # Shading
            elif name.startswith('Shading'):
                if not shadingUsed:
                    shadingUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownShading', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownShading else "RIGHTARROW")
                    row.label(text="Shading Pies")
                    row.label(text="Context: [3D View]")

                if pies_plus.dropdownShading:
                    drawKeymap = True

            # Snapping
            elif name.startswith('Snapping'):
                if not snappingUsed:
                    snappingUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownSnapping', icon_only=True, emboss=False,
                             icon="DOWNARROW_HLT" if pies_plus.dropdownSnapping else "RIGHTARROW")
                    row.label(text="Snapping Pies")
                    row.label(text="Context: [3D View, UV Editor]")

                if pies_plus.dropdownSnapping:
                    drawKeymap = True

            # Transforms
            elif name.startswith('Transforms'):
                if not transformUsed:
                    transformUsed = True

                    box = layout.box()
                    row = box.row()
                    row.prop(pies_plus, 'dropdownTransform', icon_only=True, emboss=False, icon="DOWNARROW_HLT" if pies_plus.dropdownTransform else "RIGHTARROW")
                    row.label(text="Transform Pies")
                    row.label(text="Context: [Object]")

                if pies_plus.dropdownTransform:
                    drawKeymap = True

            if drawKeymap:
                kc = wm.keyconfigs.user

                kmi_name, kmi_value, km_name = items[:3]
                split = box.split()
                col = split.column()
                km = kc.keymaps[km_name]
                PIESPLUS_addon_keymaps.get_hotkey_entry_item(name, kc, km, kmi_name, kmi_value, col)


class PIESPLUS_OT_add_hotkey(bpy.types.Operator):
    bl_idname = "pies_plus.add_hotkey"
    bl_label = "Add Hotkeys"
    bl_options = {'REGISTER', 'INTERNAL'}

    km_name: StringProperty()

    def execute(self, context):
        context.preferences.active_section = 'KEYMAP'
        wm = context.window_manager
        kc = wm.keyconfigs.addon
        km = kc.keymaps.get(self.km_name)
        if km:
            km.restore_to_default()
            context.preferences.is_dirty = True
        context.preferences.active_section = 'ADDONS'
        return {'FINISHED'}


##################################
# Preferences
##################################


class PIESPLUS_MT_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    tabs: EnumProperty(
        items=(
            ('general', "General", "Information & Settings"),
            ('keymaps', "Keymaps", "Keymap Customizing")
        )
    )

    # Select Tool Prefs

    default_tool_pref: EnumProperty(
        items=(
            ('builtin.select', "Tweak", "Tweak"),
            ('builtin.select_box', "Box", "Box Select"),
            ('builtin.select_circle', "Circle", "Circle Select"),
            ('builtin.select_lasso', "Lasso", "Lasso Select")
        )
    )

    # Shading Prefs
    
    auto_smooth_flat_pref: BoolProperty(
        description="Automatically set objects that have Auto Smooth+ removed to Shade Flat"
    )

    # Quick FWN Prefs

    fwn_keep_sharps_pref: BoolProperty(
        description="Toggles whether the FWN Modifier accounts for Sharps on each mesh",
        default=True
    )
    
    fwn_weight_value_pref: IntProperty(
        name="Weight",
        default=100,
        min=1,
        max=100
    )
    
    fwn_face_influence_pref: BoolProperty(
        description="Use influence of face for FWN"
    )

    # Snapping Prefs
    
    auto_enable_snap_pref: BoolProperty(
        description="Automatically enables snapping when you change any settings within the pie",
        default=True
    )

    # Origin / Cursor Prefs
    
    auto_enable_abs_grid_snap_pref: BoolProperty(
        description="Automatically enables Absolute Grid Snap when you switch to incremental snapping within the pie"
    )
    
    reset_3d_cursor_rot_pref: BoolProperty(
        description="Automatically reset 3D Cursor rotation when resetting the translation within the pie", 
        default=True
    )

    # Edit Origin Prefs
    
    face_center_snap_pref: BoolProperty(
        description="Allows for snapping directly to the center of any face on the object being edited (WARNING: This operation can be very slow in bigger scenes)"
    )

    # Selection Prefs
    
    invert_selection_pref: BoolProperty(
        description="Only deselect all objects if all object are selected (versus deselecting if any selection is made)"
    )

    # Context Mode Prefs
       
    simple_context_mode_pref: BoolProperty(
        description="A simple version of the context mode pie, which removes xray and overlay toggle (in case you keep using it on accident)"
    )

    preserve_uv_selection_pref: BoolProperty(
        description="Selects all faces when you leave UV Sync so you don't need to select the mesh again as you would normally"
    )

    sculptors_haven_pref: BoolProperty(
        description="Move the sculpt mode button to the main array of context mode operators, so that you can quickly switch between the modes"
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        if updater.update_ready == None:
            row.label(text = "Checking for an update...")

            updater.check_for_update_now()

        elif updater.update_ready:
            row.alert = True
            row.label(text = "There is a Pie Menus Plus update available! Go grab it on Gumroad/Github :D")

        elif not updater.update_ready:
            row.label(text = "You have the latest version of Pie Menus Plus! There are no new versions available.")
            row.operator("updater_pies_plus.check_for_update", text = "", icon = "FILE_REFRESH")

        row.operator("wm.url_open", text="", icon = 'URL').url = "https://gumroad.com/l/piesplus"

        row = layout.row()
        row.prop(self, "tabs", expand=True)

        # Information
        if self.tabs == 'general':
            col = layout.column(align = True)
            col.label(text="        Active Tools Pie Settings:")
            box = col.box()
            row = box.row()
            row.scale_x = 2
            row.label(text="Default Selection Tool:")
            row.prop(self, "default_tool_pref", expand=True)

            col = layout.column(align = True)
            col.label(text="        Origin / Cursor Pie Settings:")
            box = col.box()
            box.prop(self, "face_center_snap_pref", text="[EXPERIMENTAL] Edit Origin Tool Snapping to Center of Faces (Slow in Big Scenes)")
            box.prop(self, "reset_3d_cursor_rot_pref", text="Reset 3D Cursor Rotation when Resetting Location")

            col = layout.column(align = True)
            col.label(text="        Select Mode Pie Settings:")
            box = col.box()
            box.prop(self, "preserve_uv_selection_pref", text="Select Entire Mesh in 3D View when Exiting UV Sync Mode")
            box.prop(self, "simple_context_mode_pref", text="Use Simple Select Mode Pie")
            box.prop(self, "sculptors_haven_pref", text="Add Sculpt Mode Button to Main Pie")
            
            col = layout.column(align = True)
            col.label(text="        Selection Pie Settings:")
            box = col.box()
            box.prop(self, "invert_selection_pref", text="Invert Selection Toggle")

            col = layout.column(align = True)
            col.label(text="        Shading Pie Settings:")
            box = col.box()
            box.prop(self, "auto_smooth_flat_pref", text="Shade Objects Flat when Auto Smooth+ is Removed")
            box = col.box()
            box.label(text = "Quick Weighted Normals:")
            row = box.row()
            row.label(text="Face Weight")
            row.scale_x = 2
            row.prop(self, "fwn_weight_value_pref")
            row = box.row()
            row.prop(self, "fwn_keep_sharps_pref", text="Keep Sharps")
            row.prop(self, "fwn_face_influence_pref", text="Face Influence")

            col = layout.column(align = True)
            col.label(text="        Snapping Pie Settings:")
            box = col.box()
            box.prop(self, "auto_enable_snap_pref", text="Enable Snapping when Changing Snap Pie Settings")
            box.prop(self, "auto_enable_abs_grid_snap_pref", text="Enable Absolute Grid Snap when Turning on Incremental Snapping")

            col = layout.column(align = True)
            col.label(text="    General Settings:")
            box = col.box()

            view = context.preferences.view

            col = box.column()
            col.label(text = "Animation Timeout Recommended: 0  -  Removes Animations")
            col.prop(view, "pie_animation_timeout")
            col.label(text = "Radius Recommended: 125  -  Fixes UI Clipping")
            col.prop(view, "pie_menu_radius")
            col.separator(factor = 1.5)
            col.prop(view, "pie_tap_timeout")
            col.prop(view, "pie_initial_timeout")
            col.prop(view, "pie_menu_threshold")
            col.prop(view, "pie_menu_confirm")

        # Keymapping
        if self.tabs == 'keymaps':
            wm = context.window_manager
            PIESPLUS_addon_keymaps.draw_keymap_items(wm, layout)


##################################
# REGISTRATION
##################################


classes = (
    PIESPLUS_MT_addon_prefs,
    PIESPLUS_OT_add_hotkey,
    PIESPLUS_property_group,
    PIESPLUS_OT_check_for_update
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Set the updaters repo
    updater.user = "oRazeD"
    updater.repo = "piemenusplus"
    updater.current_version = bl_info["version"]

    # Initial check for repo updates
    updater.check_for_update_now()

    if updater.update_ready:
        print("There is a Pie Menus Plus update available! Go grab it on Gumroad/Github :D")

    bpy.types.Scene.pies_plus = PointerProperty(type = PIESPLUS_property_group)

    # Assign Standard Keymaps
    PIESPLUS_addon_keymaps.new_keymap('Active Tools', 'wm.call_menu_pie', 'PIESPLUS_MT_active_tools',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'W', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Sculpt Tools', 'wm.call_menu_pie', 'PIESPLUS_MT_sculpt',
                                      'Sculpt', 'EMPTY', 'WINDOW',
                                      'W', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Align Pie (Object Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_align',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'X', 'PRESS', False, False, True)

    PIESPLUS_addon_keymaps.new_keymap('Animation Playback', 'wm.call_menu_pie', 'PIESPLUS_MT_animation',
                                      'Object Non-modal', 'EMPTY', 'WINDOW',
                                      'SPACE', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Animation Keyframing', 'wm.call_menu_pie', 'PIESPLUS_MT_keyframing',
                                      'Object Non-modal', 'EMPTY', 'WINDOW',
                                      'SPACE', 'PRESS', False, False, True)

    PIESPLUS_addon_keymaps.new_keymap('Bool Tool Pie (Object Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_booltool',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'C', 'PRESS', False, False, True)

    PIESPLUS_addon_keymaps.new_keymap('Delete Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_delete',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'X', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Delete Pie (Curve)', 'wm.call_menu_pie', 'PIESPLUS_MT_delete_curve',
                                      'Curve', 'EMPTY', 'WINDOW',
                                      'X', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('LoopTools Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_looptools',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'Q', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Origin / Cursor Change Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_origin_pivot',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'S', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Proportional Editing Pie (Object Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_proportional_object_mode',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'O', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Proportional Editing Pie (Edit Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_proportional_edit_mode',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'O', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Save Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_save',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'S', 'PRESS', True, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Select Mode Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_modes',
                                      'Object Non-modal', 'EMPTY', 'WINDOW',
                                      'TAB', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Select Mode Pie (UV)', 'wm.call_menu_pie', 'PIESPLUS_MT_UV_modes',
                                      'UV Editor', 'EMPTY', 'WINDOW',
                                      'TAB', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Selection Pie (Object Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_selection_object_mode',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'A', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Selection Pie (Edit Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_selection_edit_mode',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'A', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Shading Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_shading',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'Z', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Snapping Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_snapping',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'TAB', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Snapping Pie (UV)', 'wm.call_menu_pie', 'PIESPLUS_MT_UV_snapping',
                                      'UV Editor', 'EMPTY', 'WINDOW',
                                      'TAB', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Transforms Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_transforms',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'A', 'PRESS', True, False, False)

    PIESPLUS_addon_keymaps.register_keymaps()  # Keymap Setup


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.pies_plus

    PIESPLUS_addon_keymaps.unregister_keymaps()  # Keymap Cleanup


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
