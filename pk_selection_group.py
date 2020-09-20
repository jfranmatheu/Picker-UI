from .pk_button import PK_Button
from .pk_layer import LAYER_MAX_BUTTONS, SCENE_MAX_BUTTONS
from bpy.props import IntVectorProperty, CollectionProperty


class PK_Button_SelectionGroup(PK_Button):
    # button_indices : IntVectorProperty(default=[-1]*LAYER_MAX_BUTTONS, min=-1, max=SCENE_MAX_BUTTONS)
    buttons = []

    def __init__(self):
        self.buttons = []
