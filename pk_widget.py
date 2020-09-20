from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty, CollectionProperty, BoolProperty,
    PointerProperty, FloatProperty, IntVectorProperty, IntProperty
)


class PK_Widget(PropertyGroup):
    name : StringProperty(default='Widget_', name="Name")
    abs_pos : IntVectorProperty(size=2, default=(0,0), min=0, name="Absolute Position")
    rel_pos : IntVectorProperty(size=2, default=(0,0), min=0, max=1, name="Relative Position")
    aspect_ratio : IntVectorProperty(size=2, default=(1,1), min=1, name="Aspect Ratio")
    scale : FloatProperty(default=1, min=0.5, max=2, name="Scale")
