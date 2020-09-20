from bpy.types import PropertyGroup, Object
from bpy.props import (
    StringProperty, IntVectorProperty, FloatProperty, BoolProperty,
    IntProperty, PointerProperty, CollectionProperty
)
from uuid import uuid4
from .pk_scene import PK_Scene
from .pk_theme import PK_Theme
from enum import Enum


class PK_Mode(Enum):
    OBJECT = 0
    EDIT = 1

    def __call__(self):
        return self.value


class PK_Character(PropertyGroup):
    uuid : StringProperty(default="", name="UUID", description="Unic Identifier of your picker")
    name : StringProperty(default="My Picker", name="Picker Name", description="Name of your picker")

    pos : IntVectorProperty(default=(0, 0), size=2, min=0, name="Position")
    size : IntVectorProperty(default=(282, 375), size=2, min=280, max=1024, name="Size")
    scale : FloatProperty(default=1, min=0.5, max=2, name="Scale")

    scenes : CollectionProperty(type=PK_Scene, name="Scene")
    active_scene : IntProperty(default=-1, name="Active Scene")

    theme : PointerProperty(type=PK_Theme, name="Theme")
    arm_obj : PointerProperty(type=Object, name="Armature Object")

    mode : IntProperty(default=PK_Mode.OBJECT(), min=0, max=1, name="Mode")

    ''' Here is our serialization path to export our picker. '''
    database_path : StringProperty(default="", subtype='FILE_PATH', name="Database Path")

    use_button_direct_action : BoolProperty (
        default=True, name="Direct action button",
        description="Trigger action {Move, Rotate, Scale} directly instead of just selecting bone"
    )


    def get_active_scene(self):
        return self.scenes[self.active_scene] if self.active_scene != -1 else None

    def generate_uuid(self):
        self.uuid = str(uuid4())

    def get_active_view(self):
        return self.get_active_scene().get_active_view()

    def get_set_use_button_direct_action(self, toggle=False):
        if toggle:
            self.use_button_direct_action = not self.use_button_direct_action
        return self.use_button_direct_action

    def toggle_edit_mode(self):
        self.mode = PK_Mode.EDIT() if self.mode == PK_Mode.OBJECT() else PK_Mode.OBJECT()
