'''
Copyright (C) 2017 MACHIN3, machin3.io, support@machin3.io

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


bl_info = {
    "name": "MACHIN3tools",
    "author": "MACHIN3",
    "version": (0, 2),
    "blender": (2, 78, 0),
    "location": "",
    "description": "A collection of blender python scripts.",
    "warning": "",
    "wiki_url": "https://github.com/machin3io/MACHIN3tools",
    "category": "Mesh"}


import bpy
from bpy.props import BoolProperty
from . import developer_utils as du
from . import M3utils as m3

modules = du.setup_addon_modules(__path__, __name__, "bpy" in locals())


class MACHIN3Settings(bpy.types.PropertyGroup):
    debugmode = BoolProperty(name="Debug Mode", default=False)


class MACHIN3Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    M3path = __path__[0]

    activate_ShadingSwitch = BoolProperty(name="Shading Switch", default=False)
    activate_RedMode = BoolProperty(name="Red Mode", default=False)
    activate_CenterCube = BoolProperty(name="Center Cube", default=False)
    activate_CleansUpGood = BoolProperty(name="Cleans Up Good", default=False)
    activate_ClippingToggle = BoolProperty(name="Clipping Plane Toggle", default=False)
    activate_Focus = BoolProperty(name="Focus", default=False)
    # activate_ThemeSwitch = BoolProperty(name="Theme Switch", default=False)
    activate_Mirror = BoolProperty(name="Mirror", default=False)
    activate_StarConnect = BoolProperty(name="Star Connect", default=False)
    activate_SmartConnect = BoolProperty(name="Smart Connect", default=False)

    CleansUpgGood_objectmodeshortcut = False  # set to True, if the keyboard shortcut should work in OBJECT mode as well, otherwise it's just EDIT mode. Call the script from the spacebar menu in object mode in that case.

    def draw(self, context):
        layout=self.layout

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        col = layout.column()

        col.label("Activating modules requires saving user preferences and re-starting Blender.")
        col.separator()

        # SHADING SWITCH

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ShadingSwitch", toggle=True)
        row.label("Switches between Material and Solid shading modes. Also re-assigns Z key for wireframe switching and Shift + Z for render switching accordingly.")
        du.show_keymap(self.activate_ShadingSwitch, kc, "3D View", "machin3.shading_switch", col)

        # RED MODE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_RedMode", toggle=True)
        row.label("In SOLID mode: switch to red matcap and back. In MATERIAL mode: switch turn bevels of WStep materials red and.")
        du.show_keymap(self.activate_RedMode, kc, "3D View", "machin3.red_mode", col)

        # Center Cube

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CenterCube", toggle=True)
        row.label("If nothing is selected, places a cube at the cursor location, with any of X/Y/Z zeroed out, enters edit mode, selects all and initiates the scale tool. If objects are selected, it zeroes out any of X/Y/Z.")
        du.show_keymap(self.activate_CenterCube, kc, "Object Mode", "machin3.center_cube", col)

        # Cleans Up Good

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleansUpGood", toggle=True)
        row.label("Removes doubles, dissolves degenerates, deletes loose vertices and edges, recalculates normals, dissolves 2-edged vertices, selects non-manifold geometry. Works in edit mode and object mode(incl. on multiple objects).")
        du.show_keymap(self.activate_CleansUpGood, kc, "Mesh", "machin3.clean_up", col)

        # CLIPPING TOGGLE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ClippingToggle", toggle=True)
        row.label("Toggle through different clipping plane settings")
        du.show_keymap(self.activate_ClippingToggle, kc, "3D View", "machin3.clipping_toggle", col)

        # FOCUS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Focus", toggle=True)
        row.label("Disables all Mirror modifiers of the selected objects, then enters local view. Renables mirror modifers again, when exiting localview.")
        du.show_keymap(self.activate_Focus, kc, "Object Mode", "machin3.focus", col)

        # THEME SWITCH

        # row = col.split(percentage=0.2)
        # row.prop(self, "activate_ThemeSwitch")
        # row.label("Switchs Theme. Optionally switches Matcap at the same time")

        # MIRROR

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Mirror", toggle=True)
        row.label("Mirrors selected objects across the active object, allows mirroring of multiple objects at once and supports DECALmachine.")
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_x", col)
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_y", col)
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_z", col)

        # STAR CONNECT

        row = col.split(percentage=0.2)
        row.prop(self, "activate_StarConnect", toggle=True)
        row.label("In Vert mode, connects all selected verts to the last one of the selection, in Face mode it creates a center star vert")
        du.show_keymap(self.activate_StarConnect, kc, "Mesh", "machin3.star_connect", col)

        # SMART CONNECT

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SmartConnect", toggle=True)
        row.label("In Vert mode connects vert path, in edge mode is turns the edge.")
        du.show_keymap(self.activate_SmartConnect, kc, "Mesh", "machin3.smart_connect", col)


MACHIN3_keymaps = []


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.machin3 = bpy.props.PointerProperty(type=MACHIN3Settings)

    wm = bpy.context.window_manager

    # SHADING SWITCH

    if m3.M3_prefs().activate_ShadingSwitch:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.shading_switch", 'BUTTON5MOUSE', 'PRESS', shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # RED MODE

    if m3.M3_prefs().activate_RedMode:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.red_mode", 'BUTTON5MOUSE', 'PRESS', alt=True)
        MACHIN3_keymaps.append((km, kmi))

    # CENTER CUBE

    if m3.M3_prefs().activate_CenterCube:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.center_cube", 'C', 'PRESS', shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # CLEANS UP GOOD

    if m3.M3_prefs().activate_CleansUpGood:
        if m3.M3_prefs().CleansUpgGood_objectmodeshortcut:
            km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        else:
            km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.clean_up", "THREE", "PRESS")
        MACHIN3_keymaps.append((km, kmi))

    # CLIPPING PLANE TOGGLE

    if m3.M3_prefs().activate_ClippingToggle:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.clipping_toggle", "BUTTON5MOUSE", "PRESS")

    # FOCUS

    if m3.M3_prefs().activate_Focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.focus", "F", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))

    # THEME SWITCH

    # if m3.M3_prefs().activate_ThemeSwitch:
        # km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        # kmi = km.keymap_items.new("machin3.theme_switch", "BUTTON5MOUSE", "PRESS", ctrl=True)

    # MIRROR

    if m3.M3_prefs().activate_Focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.mirror_x", "X", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))
        kmi = km.keymap_items.new("machin3.mirror_y", "Y", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))
        kmi = km.keymap_items.new("machin3.mirror_z", "Z", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # STAR CONNECT

    if m3.M3_prefs().activate_StarConnect:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.star_connect", "TWO", "PRESS", shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # SMART CONNECT

    if m3.M3_prefs().activate_SmartConnect:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_connect", "TWO", "PRESS")
        MACHIN3_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_module(__name__)

    for km, kmi in MACHIN3_keymaps:
        km.keymap_items.remove(kmi)

    MACHIN3_keymaps.clear()