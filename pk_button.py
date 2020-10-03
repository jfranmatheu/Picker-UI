import bpy
from bpy.types import PropertyGroup, Image, Panel
from bpy.props import *
from bpy import ops as OP
from enum import Enum
from os.path import exists, isfile


MASTER_VIEW = 0
SECONDARY_VIEW = 1

NON_MIRROR_LAYER = 0
MIRROR_LAYER = 1
LEFT    = 'L'
RIGHT   = 'R'

default_layers = [
    ("Arm.", MIRROR_LAYER, {'arm', 'shoulder'}, 'color_arm_'),
    ("Leg.", MIRROR_LAYER, {'leg', 'thig', 'shin', 'toe', 'foot', 'toe', 'heel'}, 'color_leg_'),
    ("Torso", NON_MIRROR_LAYER, {'spine', 'pelvis', 'breast'}, 'color_body'),
    ("Head", NON_MIRROR_LAYER, {'head', 'neck'}, 'color_head'),
    ("Hand", MIRROR_LAYER, {'hand', 'finger', 'thumb', 'palm', 'f_pincky', 'f_middle', 'f_index', 'f_ring'}, 'color_hand_'),
    #("Facial", NON_MIRROR_LAYER, {'face'}, 'color_facial')
]


class ButtonShape(Enum):
    RECTANGLE = 0,
    CIRCLE = 1,
    ROUND_SQUARE = 2

    def __call__(self):
        return self.value

def update_button_shape(self, context):
    if self.shape_type == 'RECT':
        self.shape = 0
    elif self.shape_type == 'CIRC':
        self.shape = 1
        # TODO: change height to match width.
        #       maybe button style data should be inside PK_Button.
    elif self.shape_type == 'ROUND_SQUARE':
        self.shape = 2

#def update_button_shading(self, context):
#    if self.shading_type == 'FLAT':

def update_shading(self, context):
    if self.shading=='IMG':
        if self.icon:
            self.icon.gl_load()
    elif self.icon:
        self.icon.gl_free()
        self.icon.buffers_free()

''' THIS INFO IS FOR EACH SCENE '''
class PK_Button_Style(PropertyGroup):
    shading : EnumProperty (
        items=(
            ('FLAT', "Flat", "Flat Shading Style", 'SHADING_SOLID', 0),
            ('GRAD', "Gradient", "Gradient Shading Style", 'SHADING_RENDERED', 1),
            ('IMG', "Image", "Image Shading Style", 'SHADING_TEXTURE', 2)
        ),
        default='FLAT',
        name="Shading",
        update=update_shading
    )
    shape_type : EnumProperty (
        items=(
            ('RECT', "Rectangle", "Rectangular Shape", 'SEQ_STRIP_DUPLICATE', 0),
            ('CIRC', "Circle", "Circular Shape", 'RADIOBUT_ON', 1),
            ('ROUND_SQUARE', "Rounded Square", "Rounded Square Shape", 'SNAP_FACE', 2)
        ),
        default='RECT',
        update=update_button_shape,
        name="Shape"
    )
    shape : IntProperty(default=0, name="Shape", min=0)
    color : FloatVectorProperty(default=(0, 1, 1, .6), size=4, min=0, max=1, subtype='COLOR', name="Color") # (.6, .2, .32, .8)
    text_color : FloatVectorProperty(default=(1, 1, 1, 1), size=4, min=0, max=1, subtype='COLOR', name="Text Color")
    color_on_hover : FloatVectorProperty(default=(1, 1, 0, 1), size=4, min=0, max=1, subtype='COLOR', name="OnHover Color")
    text_color_on_hover : FloatVectorProperty(default=(0, 0, 0, 1), size=4, min=0, max=1, subtype='COLOR', name="OnHover Text Color")

    # FLAT Shading.
    use_outline : BoolProperty(default=False, name="Use Outline") # icon: ANTIALIASED
    outline_color : FloatVectorProperty(default=(0, 0, 0, 1), size=4, min=0, max=1, subtype='COLOR', name="Outline Color")
    outline_factor : FloatProperty(default=0.2, min=0, max=1, name="Outline Factor")
    outline_blur : BoolProperty(default=False, name="Blur Outline")
    
    # CIRCLE SQUARED SHAPE.
    sharpness_factor : FloatProperty(default=0, min=.1, max=.9, name="Sharpness Factor")

    # GRAD Shading.
    # use_gradient : BoolProperty(default=False, name="Use Gradient") # icon: NODE_TEXTURE
    gradient_type : EnumProperty (
        items=(
            ('RADIAL', "Radial", "Radial gradient"),
            ('LINEAR', "Linear", "Linear gradient"),
            ('REFLECT', "Reflect", "Reflected gradient"),
            ('DIAMOND', "Diamond", "Diamond gradient")
        ),
        default='RADIAL',
        # update=update_button_shape,
        name="Gradient Type"
    )
    second_color : FloatVectorProperty(default=(0, 0, 0, 1), size=4, min=0, max=1, subtype='COLOR',
                                       name="Second Color", description="Secondary color used by gradient")
    gradient_factor : FloatProperty(default=0, min=-1, max=1, name="Gradient Factor")
    gradient_rotation : IntProperty(default=0, min=-180, max=180, step=5, name="Gradient Rotation")
    

    def load_icon(self, context):
        if self.use_icon and self.icon:
            self.icon.gl_load()
        elif self.icon:
            self.icon.gl_free()
            self.icon.buffers_free()

    use_icon : BoolProperty(default=False, name="Use Icon", update=load_icon)
    icon : PointerProperty(type=Image, name="Icon")
    icon_scale : FloatProperty(default=0.7, min=.1, max=.9, name="Icon Scale")
    icon_tint : FloatVectorProperty(default=(1, 1, 1, 1), size=4, min=0, max=1, subtype='COLOR', name="Icon Tint")

    def update_icon(self, context):
        if not exists(self.icon_path) or not isfile(self.icon_path):
            self.use_icon = False
            return
        icon = bpy.data.images.load(self.icon_path, check_existing=True)

        size = icon.size
        if size[0] < 16 or size[1] < 16:
            self.use_icon = False
            return
        if abs(1 - size[0] / size[1]) > 0.05:
            self.use_icon = False
            return

        self.icon = icon
        self.load_icon(context)

    icon_path : StringProperty(default="", subtype='FILE_PATH', name="Icon Path", update=update_icon)


''' THIS INFO IS FOR EACH VIEW '''
class PK_Button_Data(PropertyGroup):
    pos : IntVectorProperty(default=(0, 0), size=2, min=0, name="Position")
    size : IntVectorProperty(default=(20, 20), size=2, min=0, name="Size")
    factor : FloatVectorProperty(default=(0, 0), size=2, min=0, max=1, name="Factor")

    rotation : IntProperty(default=0, min=-90, max=90, step=5, name="Rotation")
    depth : FloatProperty(default=0, min=0, max=100, step=1, name="Depth")

    ''' To avoid a triple loop (as we may want to add a button to multiple layers),
        We need to store the layer users this button has (int).
        As well as the active layer users (int).
        When it's 0, active is False, otherwise is True.
    '''
    layer : IntProperty(default=-1, min=-1, max=128, name="Layer Index")
    layer_users : IntProperty(default=0, min=0, name="Layer Users")
    active_layer_users : IntProperty(default=0, min=0, name="Active Layer Users")
    # The button/BONE is selected
    is_selected : BoolProperty(default=False,name="Is Selected")
    # The button is active in active_view
    is_active : BoolProperty(default=False, name="Is Active") # NOTE: NO MORE NEEDED BY USING ACTIVE VIEW LAYER BUTTON INDICES.
    # The button is visible due to layers
    is_visible : BoolProperty(default=False, name="Is Visible") # NOTE: NO MORE NEEDED BY USING ACTIVE VIEW LAYER BUTTON INDICES.

    # Conditions to be drawn
    def can_draw_it(self):
        return self.is_active and self.is_visible

    def init_default(self):
        self.layer_users = 0
        self.active_layer_users = 0
        self.is_active = True
        self.is_visible = False
        self.is_selected = False

    def get_real_pos_size(self):
        return self.pos[0] - self.size[0], self.pos[1] - self.size[1], self.size[0] * 2, self.size[1] * 2

    def reset(self):
        self.is_active = False
        self.is_visible = False
        self.layer = -1
        self.pos = (0, 0)
        self.size = (0, 0)

class PK_Button(PropertyGroup):
    name : StringProperty(default="Button", name="Name", description="Button Bone Name")
    index : IntProperty(default=0, min=0, name="Index")
    text : StringProperty(default="Button", name="Text")
    action : EnumProperty(
        items=(
            ('MOVE', 'Move', "Move bone"),
            ('ROTATE', 'Rotate', "Rotate bone"),
            ('SCALE', 'Scale', "Scale bone")
        ),
        default='MOVE', name="Action"
    )
    master : PointerProperty(type=PK_Button_Data, name="Button Data in Master View")
    secondary : PointerProperty(type=PK_Button_Data, name="Button Data in Secondary View")
    style : PointerProperty(type=PK_Button_Style, name="Button Style")

    def get_data_from_view_index(self, view_index):
        if view_index == MASTER_VIEW:
            return self.master
        elif view_index == SECONDARY_VIEW:
            return self.secondary
        else:
            return None

    def has_layer(self, view_index):
        data = self.get_data_from_view_index()
        return data.layer != -1

    def set_layer(self, view_index, new_layer):
        data = self.get_data_from_view_index()
        data.layer = new_layer

    def get_layer(self, view_index):
        data = self.get_data_from_view_index()
        return data.layer

    def show_context_menu(self, context):
        active_picker = context.scene.pickers.active_picker()
        if not active_picker:
            print("ERROR: Active Picker")
            return
        active_scene = active_picker.get_active_scene()
        if not active_scene:
            print("ERROR: Active Scene")
            return
        ok = False
        for index, b in enumerate(active_scene.buttons):
            if b == self:
                ok = True
                print(index)
                active_scene.active_button = index
                #active_button[0] = index
                break
        if ok:
            # context.scene.widgets.active = [self.w_index, self.b_index, -1]
            OP.wm.call_panel(name="PK_PT_button_context_menu", keep_open=True)
        return

    def remove(self, scene, from_active_view=True):
        if from_active_view:
            active_view = scene.get_active_view()
            data = self.get_data_from_view_index(scene.active_view)
            # Remove from layer.
            if data.layer != -1:
                active_view.layers[data.layer].remove_button(self)
            # Reset Button Data.
            data.reset()
            # Remove from view.
            active_view.remove_button(self)
            other_view = MASTER_VIEW if scene.active_view == SECONDARY_VIEW else SECONDARY_VIEW
            data = self.get_data_from_view_index(other_view)
            if not data.is_active:
                # self.reset_data(other_view)
                # scene.other_view().remove_button(self)
                # Remove from scene.
                scene.remove_button(self, True)
        else:
            # Remove from scene.
            scene.remove_button(self)


class PK_Button_ContextMenu(Panel):
    bl_idname = "PK_PT_button_context_menu"
    bl_label = "Button Properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "NONE"

    def draw(self, context):
        active_picker = context.scene.pickers.active_picker()
        if not active_picker:
            print("ERROR: Active Picker")
            return
        active_scene = active_picker.get_active_scene()
        if not active_scene:
            print("ERROR: Active Scene")
            return
        button = active_scene.get_active_button()
        #if active_button[0] == -1:
        #    return
        #button = active_scene.buttons[active_button[0]]
        if not button:
            print("ERROR: Active Button")
            return

        data = button.get_data_from_view_index(active_scene.active_view)

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.separator()
        layout.label(text=button.name, icon='BONE_DATA') # SEQ_STRIP_DUPLICATE

        #layout.separator()
        main = layout.column(align=True)

        main.prop(button, "text", text="Text")
        main.prop(button, "action", text="Action", icon='STYLUS_PRESSURE')

        main.separator()

        style = button.style
        color = main.box().column(align=True)
        color.label(text="Button Style:", icon='PROPERTIES')
        color.row().prop(style, "shape_type", text="Shape")
        color.separator()
        color.prop(style, "color", text="Color")
        color.prop(style, "color_on_hover", text="Color OnHover")

        color.separator()
        if style.shape_type == 'ROUND_SQUARE':
            color.prop(style, 'sharpness_factor', text='Sharpness Factor', slider=True)
            self.draw_settings(main, data)
            return

        color.row().prop(style, 'shading', text="Shading", icon='COLOR')
        color.separator()

        if style.shading == 'FLAT':
            color.prop(style, 'use_outline', text="Use Outline", icon='SELECT_SET')
            box = color.box().column(align=True)
            box.enabled = style.use_outline
            box.prop(style, 'outline_color', text='Color')
            if style.shape_type == 'CIRC':
                box.prop(style, 'outline_factor', text='Factor', slider=True)
                box.prop(style, 'outline_blur', text='Blur')

        elif style.shading == 'GRAD':
            if style.shape_type == 'CIRC':
                # color.separator()
                # color.prop(style, 'use_gradient', text="Use Gradient", icon='NODE_TEXTURE')
                box = color.box().column(align=True)
                # box.enabled = style.use_gradient and not style.use_outline
                box.prop(style, 'gradient_type', text='Type')
                box.prop(style, 'second_color', text='Second Color')
                box.prop(style, 'gradient_factor', text='Factor', slider=True)
                if style.gradient_type != 'RADIAL':
                    box.prop(style, 'gradient_rotation', text='Angle', slider=True)

        elif style.shading == 'IMG':
            box = color.box().column(align=True)
            # box.prop(style, 'icon', text='Image')
            box.prop(style, 'icon_path', text='Image Path')
            box.prop(style, 'icon_scale', text='Image Scale')

        if not style.shading == 'IMG':
            color.separator()
            color.prop(style, 'use_icon', text="Use Icon", icon='OUTLINER_OB_IMAGE')
            if style.use_icon:
                box = color.box().column(align=True)
                # box.enabled = style.use_icon
                # box.prop(style, 'icon', text='Icon')
                box.prop(style, 'icon_path', text='Icon Path')
                box.prop(style, 'icon_scale', text='Icon Scale')

            text = main.box().column(align=True)
            text.label(text="Text Style:", icon='FONTPREVIEW')
            text.prop(style, "text_color", text="Color")
            text.prop(style, "text_color_on_hover", text="Color OnHover")
            #text.prop(b, "text_use_shadow", text="Use Shadow")
            
        self.draw_settings(main, data)

    
    def draw_settings(self, layout, data):
        layout.separator()

        #settings = layout.box().column(align=True)
        #settings.label(text="Settings:", icon='SETTINGS')
        #settings.prop(data, "depth", text="Depth", slider=True, icon='IMAGE_ZDEPTH')

        exp = layout.box().column(align=True)
        exp.label(text="Experimental:", icon='EXPERIMENTAL')
        exp.prop(data, "depth", text="Depth", slider=True, icon='IMAGE_ZDEPTH')
        exp.prop(data, 'rotation', text="Rotation", slider=True, icon='ORIENTATION_GIMBAL')

        #manage = main.box()
        #remove = manage.operator('dui.widget_remove_button', text="Remove Button")
        #remove.w_index = active[0]
        #remove.b_index = active[1]
        #remove.from_floating = True
