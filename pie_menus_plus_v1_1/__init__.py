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
    "version": (1, 1, 0),
    "blender": (2, 83, 0),
    "location": "View3D",
    "category": "3D View"}


import bpy
import rna_keymap_ui
from bpy.props import StringProperty, EnumProperty, BoolProperty, IntProperty
from bpy.types import Operator, AddonPreferences

from . import (ui,
               pie_modes,
               pie_snapping,
               pie_looptools,
               pie_active_tools,
               pie_origin_cursor,
               pie_apply_transforms,
               pie_selection,
               pie_shading,
               pie_proportional,
               pie_keyframing)


##################################
# Preferences                    
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
                                  ctrl=ctrl,
                                  shift=shift, alt=alt,
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
        kmi_names = [item[0] for item in cls._keymaps.values() if
                     item not in ['wm.call_menu', 'wm.call_menu_pie']]

        for km, kmi in cls._addon_keymaps:
            # remove addon keymap for menu and pie menu
            if hasattr(kmi.properties, 'name'):
                if kmi_values:
                    if kmi.properties.name in kmi_values:
                        km.keymap_items.remove(kmi)

            # remove addon_keymap for operators
            else:
                if kmi_names:
                    if kmi.idname in kmi_names:
                        km.keymap_items.remove(kmi)

        cls._addon_keymaps.clear()

    @staticmethod
    def get_hotkey_entry_item(name, kc, km, kmi_name, kmi_value, col):

        # for menus and pie_menu
        if kmi_value:
            for km_item in km.keymap_items:
                if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
                    col.context_pointer_set('keymap', km)
                    rna_keymap_ui.draw_kmi([], kc, km, km_item, col, 0)
                    return

            col.label(text=f"No hotkey entry found for {name}")
            col.operator(PIESPLUS_OT_Add_Hotkey.bl_idname,
                         text="Restore keymap",
                         icon='ADD').km_name = km.name

        # for operators
        else:
            if km.keymap_items.get(kmi_name):
                col.context_pointer_set('keymap', km)
                rna_keymap_ui.draw_kmi([], kc, km, km.keymap_items[kmi_name],
                                       col, 0)

            else:
                col.label(text=f"No hotkey entry found for {name}")
                col.operator(PIESPLUS_OT_Add_Hotkey.bl_idname,
                             text="Restore keymap",
                             icon='ADD').km_name = km.name

    @staticmethod
    def draw_keymap_items(wm, layout):
        kc = wm.keyconfigs.user

        row = layout.row()
        row.label(text="        Standard Keymaps:")

        for name, items in PIESPLUS_addon_keymaps._keymaps.items():
            if not name.endswith('(UV)'):
                kmi_name, kmi_value, km_name = items[:3]
                box = layout.box()
                split = box.split()
                col = split.column()
                km = kc.keymaps[km_name]
                PIESPLUS_addon_keymaps.get_hotkey_entry_item(name, kc, km, kmi_name, kmi_value, col)

        row = layout.row()
        row.label(text="        UV Keymaps:")

        for name, items in PIESPLUS_addon_keymaps._keymaps.items():
            if name.endswith('(UV)'):
                kmi_name, kmi_value, km_name = items[:3]
                box = layout.box()
                split = box.split()
                col = split.column()
                km = kc.keymaps[km_name]
                PIESPLUS_addon_keymaps.get_hotkey_entry_item(name, kc, km, kmi_name, kmi_value, col)


class PIESPLUS_OT_Add_Hotkey(Operator):
    bl_idname = "template.add_hotkey"
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


class PIESPLUS_MT_addon_prefs(AddonPreferences):
    bl_idname = __name__

    Tabs : EnumProperty(items = (('info', "Information", "Information about the addon"),
                                 ('keymaps', "Keymaps", "Keymapping"),
                                 ('settings', "Settings", "Settings")))

    gizmoSwitch_Pref : EnumProperty(items = (('tool', "Tool", "Changes the tool"),
                                             ('gizmo', "Gizmo", "Changes the gizmo instead of the tool (preferred workflow, will set your tool to tweak if using a different tool that isn't box, lasso or circle select)")))

    wireframeType_Pref : EnumProperty(items = (('viewport_shading', "Viewport Shading", "Uses the standard wireframe shading mode"),
                                               ('overlay', "Overlay", "Uses the alternate wireframe method that overlays a wireframe over all meshes (similar functionality to Max or Maya)")))

    defaultTool_Pref : EnumProperty(items = (('tweak_select', "Tweak", "Tweak"),
                                             ('box_select', "Box", "Box Select"),
                                             ('circle_select', "Circle", "Circle Select"),
                                             ('lasso_select', "Lasso", "Lasso Select")))

    keepSharp_Pref : BoolProperty(description = "Toggles whether the FWN Modifier accounts for Sharps on each mesh", default=True)

    weightValue_Pref : IntProperty(name="Weight", default=100, min=1, max=100)
        
    smoothAngle_Pref : IntProperty(name="Smooth Angle", default=60, min=0, max=180, description = "Tip: You don't actually need to turn on Auto Smoothing normally with the button, if you use the slider it will take care of all the prerequisites for turning on Auto Smoothing")

    autoSnap_Pref : BoolProperty(description = "Automatically turns snapping on when you change snapping pie settings", default=True)

    resetRot_Pref : BoolProperty(description = "Decide whether the 3D Cursors rotation resets when you reset per axis", default=True)

    editOriginActivate_Pref : BoolProperty(description = "Edit Origin & 3D Cursor allows you to move the Actives origin (or 3D Cursor) with a modal. This used to be on by default but the undo system can be a bit unreliable. The tool is safe to use, avoid undos if you can <3")

    faceCenterSnap_Pref : BoolProperty(description = "Allows snapping directly to the center of any face on the object being edited (WARNING: This operation can be very slow in bigger scenes)")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "Tabs", expand=True)

        # Information

        if self.Tabs == 'info':
            row = layout.row()
            row.separator()

            flow = layout.grid_flow()
            box = flow.box()

            box.label(text="Pie Menus Plus is an add-on structured around creating a fully functioning pie menu")
            box.label(text="ecosystem that extends usability beyond what the built-in pie menus are capable of.")

            row = layout.row()
            row.label(text="        Support:")

            flow = layout.grid_flow()
            box = flow.box()

            box.label(text="Pie Menus Plus was developed in Blender Version 2.82.7 and while most operations have")
            box.label(text="been created carefully to work with earlier versions of Blender 2.80 it is still possible that")
            box.label(text="I missed some things that wont work in earlier versions. I am supporting versions earlier")
            box.label(text="than 2.82.7 down to 2.80 so if you ever have problems with any of the tools provided")
            box.label(text="you can contact me via email @ ethan.simon.3d@gmail.com or via Discord")
            box.label(text="@ razed#2764 (add me first).")

        # Keymapping

        if self.Tabs == 'keymaps':
            row = layout.row()
            row.separator()

            wm = context.window_manager
            
            PIESPLUS_addon_keymaps.draw_keymap_items(wm, layout)

        # Settings

        if self.Tabs == 'settings':
            row = layout.row()
            row.separator()
            row = layout.row()

            row.label(text="        Gizmo / Tool Settings:")
            box = layout.box()
            row = box.row()
            row.label(text="Gizmo change method:")
            row.prop(self, "gizmoSwitch_Pref", expand=True)
            row = box.row()
            row.scale_x = 2
            row.label(text="Default Selection Tool:")
            row.prop(self, "defaultTool_Pref", expand=True)

            row = layout.row()
            row.separator()
            row = layout.row()

            row.label(text="        Wireframe Settings:")
            box = layout.box()
            row = box.row()
            row.label(text="Wireframe method:")
            row.prop(self, "wireframeType_Pref", expand=True)

            row = layout.row()
            row.separator()
            row = layout.row()

            row.label(text="        Snapping Settings:")
            box = layout.box()
            row = box.row()
            row.prop(self, "autoSnap_Pref", text="Auto enable snapping when snap type changed")

            row = layout.row()
            row.separator()
            row = layout.row()

            row.label(text="        Origin / Cursor Change Settings:")
            box = layout.box()
            if bpy.app.version >= (2, 81, 0):
                row = box.row()
                row.prop(self, "editOriginActivate_Pref", text="Enable Edit Origin & 3D Cursor Tool (README)")
                if self.editOriginActivate_Pref:
                    row = box.row()
                    row.prop(self, "faceCenterSnap_Pref", text="[EXPERIMENTAL] Edit Origin snapping to center of faces (Slow in big scenes)")
            row = box.row()
            row.separator()
            row = box.row()
            row.prop(self, "resetRot_Pref", text="Reset 3D Cursor rotation when resetting location")

            row = layout.row()
            row.separator()
            row = layout.row()

            row.label(text="        Quick Face-Weighted Normals Settings:")
            box = layout.box()
            row = box.row()
            row.label(text="Weight:")
            row.scale_x = 2
            row.prop(self, "weightValue_Pref")
            row = box.row()
            row.label(text="Smooth Angle:")
            row.scale_x = 2
            row.prop(self, "smoothAngle_Pref")
            row = box.row()
            row.prop(self, "keepSharp_Pref", text="Keep Sharps")

            row = layout.row()
            row.separator()
            row = layout.row()

            row.label(text="        General Pie Settings:")

            view = context.preferences.view
            flow = layout.grid_flow()
            box = flow.box()
            box.scale_y = .97

            box.label(text="Dev Note: I personally recommend 0 for Animation Timeout and 125+")
            box.label(text="for Radius, but I have not changed any of your User Preferences.")

            box.prop(view, "pie_animation_timeout")
            box.prop(view, "pie_tap_timeout")
            box.prop(view, "pie_initial_timeout")
            box.prop(view, "pie_menu_radius")
            box.prop(view, "pie_menu_threshold")
            box.prop(view, "pie_menu_confirm")


##################################
# REGISTRATION                       
##################################


classes = (ui,
           pie_modes,
           pie_snapping,
           pie_looptools,
           pie_active_tools,
           pie_origin_cursor,
           pie_apply_transforms,
           pie_selection,
           pie_shading,
           pie_proportional,
           pie_keyframing)

def register():
    for cls in classes:
        cls.register()

    bpy.utils.register_class(PIESPLUS_MT_addon_prefs)
    bpy.utils.register_class(PIESPLUS_OT_Add_Hotkey)

    # Assign Standard Keymaps

    PIESPLUS_addon_keymaps.new_keymap('Select Mode Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_modes',
                                      'Object Non-modal', 'EMPTY', 'WINDOW',
                                      'TAB', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Delete Pie (Edit Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_delete',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'X', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Shading Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_shading',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'Z', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Origin / Cursor Change Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_origin_pivot',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'S', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Apply / Clear Transforms Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_apply_clear_transforms',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'A', 'PRESS', True, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Active Tools Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_active_tools',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'W', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Snapping Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_snapping',
                                      '3D View', 'VIEW_3D', 'WINDOW',
                                      'TAB', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Animation Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_animation',
                                      'Object Non-modal', 'EMPTY', 'WINDOW',
                                      'SPACE', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Keyframing Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_keyframing',
                                      'Object Non-modal', 'EMPTY', 'WINDOW',
                                      'SPACE', 'PRESS', True, False, False)
        
    PIESPLUS_addon_keymaps.new_keymap('LoopTools Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_looptools',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'Q', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.new_keymap('Sculpt Pie (Sculpt Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_sculpt',
                                      'Sculpt', 'EMPTY', 'WINDOW',
                                      'W', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Selection Pie (Object Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_selection_object_mode',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'A', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Selection Pie (Edit Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_selection_edit_mode',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'A', 'PRESS', False, False, False)
                                
    PIESPLUS_addon_keymaps.new_keymap('Proportional Editing Pie (Object Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_proportional_object_mode',
                                      'Object Mode', 'EMPTY', 'WINDOW',
                                      'O', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Proportional Editing Pie (Edit Mode)', 'wm.call_menu_pie', 'PIESPLUS_MT_proportional_edit_mode',
                                      'Mesh', 'EMPTY', 'WINDOW',
                                      'O', 'PRESS', False, False, False)

#    PIESPLUS_addon_keymaps.new_keymap('Transform Orientations Pie', 'wm.call_menu_pie', 'PIESPLUS_MT_shading',
#                                      '3D View', 'VIEW_3D', 'WINDOW',
#                                      'W', 'PRESS', False, False, True)

    # Assign UV Keymaps

    PIESPLUS_addon_keymaps.new_keymap('Select Mode Pie (UV)', 'wm.call_menu_pie', 'PIESPLUS_MT_UV_modes',
                                      'UV Editor', 'EMPTY', 'WINDOW',
                                      'TAB', 'PRESS', False, False, False)

    PIESPLUS_addon_keymaps.new_keymap('Snapping Pie (UV)', 'wm.call_menu_pie', 'PIESPLUS_MT_UV_snapping',
                                      'UV Editor', 'EMPTY', 'WINDOW',
                                      'TAB', 'PRESS', False, True, False)

    PIESPLUS_addon_keymaps.register_keymaps() # Keymap Setup

def unregister():
    for cls in classes:
        cls.unregister()

    bpy.utils.unregister_class(PIESPLUS_MT_addon_prefs)
    bpy.utils.unregister_class(PIESPLUS_OT_Add_Hotkey)

    PIESPLUS_addon_keymaps.unregister_keymaps() # Keymap Cleanup