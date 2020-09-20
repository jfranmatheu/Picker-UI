from enum import Enum
from os.path import dirname, join, realpath, exists, isfile

import bpy

icons = join(dirname(realpath(__file__)), 'icons')


class PK_UI_Icon(Enum):
    TOOL_SELECTION_TWEAK = 'tool_selection_tweak'
    TOOL_SELECTION_BOX = 'tool_selection_box'


    def __call__(self):
        icon_path = join(icons, self.value + '.png')
        if not exists(icon_path) or not isfile(icon_path):
            return None
        return bpy.data.images.load(icon_path, check_existing=True)
