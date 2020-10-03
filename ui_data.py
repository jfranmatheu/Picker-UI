from bpy.types import PropertyGroup, Object, Armature, Image
from bpy.props import *


class PK_UI_Properties(PropertyGroup):
    picker_name : StringProperty(default="New Picker", name="Picker Name", description="Identifier for your picker")
    
    armature_object : PointerProperty(type=Object, name="Armature Object")
    armature : PointerProperty(type=Armature, name="Armature") # TODO: Change to dyn enum (armatures in active scene).
    
    generate_picker_image : BoolProperty(default=True, name="Generate Picker Images")
    picker_image : PointerProperty(type=Image, name="Picker Image")
    add_selected_bones : BoolProperty(default=True, name="Add selected bones")
    
    view : EnumProperty (
        items=(
            ('FRONT',       "Front",        "Create front view"),
            ('RIGHT',       "Right",        "Create right view"),
            ('LEFT',        "Left",         "Create left view"),
            #('BACK',        "Back",         "Create back view"),
            #('TOP',         "Top",          "Create top view"),
        ), default='FRONT',
        name="View",
        description="Select view you want to generate"
    )
    
    '''
    scene_name : StringProperty(default="New Scene", name="Scene Name", description="Identifier for your scene")
    view_name : StringProperty(default="New View", name="View Name", description="Identifier for your view")
    
    
    layer_name : StringProperty(default="New Layer", name="Layer Name", description="Identifier for your view")
    layer_text : StringProperty(default="Layer", name="Layer Text", description="Text for your layer")
    only_selected_pose_bones : BoolProperty(default=False, name="Only Selected Pose Bones")
    
    button_text : StringProperty(default="Text", name="Button Text", description="Text for your button")

    generate_default_layers : BoolProperty(
        default=True,
        name="Generate Default Layers?",
        description="Automatically will generate a bunch of useful layers for you (hands, arms, legs, body, face...)"
    )
    
    generate_facial : BoolProperty(default=True, name="Generate Facial Picker")

    # Views to create.
    facial_views : EnumProperty (
        items=(
            ('FRONT',       "Front",        "Create front view"),
            ('FRONT_RIGHT', "Front+Right",  "Create front and right views"),
            ('FRONT_LEFT',  "Front+Left",   "Create front and left views"),
            ('RIGHT',       "Right",        "Create right view"),
            ('LEFT',        "Left",         "Create left view"),
        ), default='FRONT_RIGHT',
        name="Facial Views",
        description="Select views you want to generate"
    )

    picker_facial_image : PointerProperty(type=Image, name="Facial Image")
    
    color_arm_l         : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Left Arm")
    color_arm_r         : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Right Arm")
    color_leg_l         : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Left Leg")
    color_leg_r         : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Right Leg")
    color_hand_l        : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Left Hand")
    color_hand_r        : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Right Hand")
    #color_spine         : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Spine Color")
    color_body          : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Body")
    color_head          : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Head")
    '''
