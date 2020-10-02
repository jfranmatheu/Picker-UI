# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Picker",
    "author" : "J. Fran Matheu (@jfranmatheu)",
    "description" : "The most wanted power for rig and animation",
    "blender" : (2, 83, 0),
    "version" : (0, 1, 0),
    "location" : "3D Viewport > Sidebar (N) > 'Rig' tab",
    "warning" : "",
    "category" : "Interface"
}

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

    from bpy.types import WindowManager as wm, Scene as scn
    from bpy.props import PointerProperty
    from . ui_data import PK_UI_Properties
    from . pk_data import PK
    wm.ui_data = PointerProperty(type=PK_UI_Properties)
    scn.pickers = PointerProperty(type=PK)
    
    from bpy.utils import register_class
    from .ui.panels import register as register_ui
    register_ui(register_class)

def unregister():
    from .ui.panels import unregister as unregister_ui
    from bpy.utils import unregister_class
    unregister_ui(unregister_class)
    
    auto_load.unregister()

    from bpy.types import WindowManager as wm, Scene as scn
    del wm.ui_data
    del scn.pickers
