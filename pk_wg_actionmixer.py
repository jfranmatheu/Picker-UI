from bpy.props import (
    StringProperty, CollectionProperty, BoolProperty,
    PointerProperty, FloatProperty, IntVectorProperty, IntProperty
)
from bpy.types import PropertyGroup

from .pk_widget import PK_Widget

class PK_Property(PropertyGroup):
    prop_path : StringProperty()
    prop_id : StringProperty()
    min_value : FloatProperty()
    max_value : FloatProperty()


class PK_Widget_ActionMixer(PK_Widget):
    control_factor : IntVectorProperty(size=2, default=(0, 0), min=-1, max=1, name="Control Factor")
    action_left : PointerProperty(type=PK_Property)
    action_right : PointerProperty(type=PK_Property)
    action_top : PointerProperty(type=PK_Property)
    action_bottom : PointerProperty(type=PK_Property)
