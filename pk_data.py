from bpy.types import PropertyGroup, Image, Text, Object
from bpy.props import *
from .pk_character import PK_Character


''' ELEMENTS OF A PICKER '''
# We have buttons -> position, size, color, name/identifier, text, reference to specific layers?
# We have different views -> front, back, left, right, 3/4... ATM limite it to front and right.
# Each view have their buttons, maybe are the same? If so, we have to add diferent positions to each button por each view...
# Picker has different layers for visibility (bone layers) -> position, icon, name/text, .... Can be a hidden menu or tabs like
# Also, should be some master toggle to activate all again, each one is a toggle with states: active/inactive,
# this way multiple layers can be stocked together. With Ctrl+Click should isolate the clicked layer.
# Edition should be really easy as toggle a lock icon on/off that activate/deactivate this function.


''' This way we can have multiple pickers in our project. '''
class PK(PropertyGroup):
    data : CollectionProperty(type=PK_Character, name="Picker Character")
    active_index : IntProperty(default=-1, name="Active Piker Index")
    enabled_pickers = []
    lock_ui : BoolProperty(default=False)

    def active_picker(self):
        return self.data[self.active_index] if self.active_index != -1 else None

    def active_scene(self):
        pk = self.active_picker()
        if not pk:
            return None
        return pk.get_active_scene()

    def active_view(self):
        active_scene = self.active_scene()
        if not active_scene:
            return None
        return active_scene.get_active_view()
