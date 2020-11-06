from bpy.types import PropertyGroup, Image
from bpy.props import FloatVectorProperty, IntProperty, BoolProperty, FloatProperty


class PK_Theme(PropertyGroup):
    # COLORS
    pk_bg_color              : FloatVectorProperty(default=(0, 0, 0, .6),    size=4, min=0, max=1, subtype='COLOR', name="Background Color")
    pk_text_color            : FloatVectorProperty(default=(1, 1, 1, .8),    size=4, min=0, max=1, subtype='COLOR', name="Text Color")
    
    wndheader_bg_color       : FloatVectorProperty(default=(0, 0, 0, .6),    size=4, min=0, max=1, subtype='COLOR', name="Header Background Color")
    wndheader_text_color     : FloatVectorProperty(default=(1, 1, 1, .8),    size=4, min=0, max=1, subtype='COLOR', name="Header Text Color") 
    
    menubar_bg_color         : FloatVectorProperty(default=(.01, .01, .01, 1), size=4, min=0, max=1, subtype='COLOR', name="MenuBar Background Color")
    menubar_color_active     : FloatVectorProperty(default=(.1, .2, .4, 1), size=4, min=0, max=1, subtype='COLOR', name="Active MenuBar Menu Background Color")
    menubar_drop_bg_color    : FloatVectorProperty(default=[.01, .01, .01, .9], size=4, min=0, max=1, subtype='COLOR', name="MenuBar Dropdown Background Color")
    menubar_drop_color_active: FloatVectorProperty(default=(.1, .2, .4, 1), size=4, min=0, max=1, subtype='COLOR', name="Active MenuBar Dropdown Item Background Color")
    menubar_text_color       : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="MenuBar Text Color")

    layerbar_bg_color        : FloatVectorProperty(default=(.1, .1, .1, 1), size=4, min=0, max=1, subtype='COLOR', name="Background Color")
    layerbar_button_color    : FloatVectorProperty(default=(.2, .3, .7, 1), size=4, min=0, max=1, subtype='COLOR', name="Layer Button Color")
    layerbar_button_color_active   : FloatVectorProperty(default=(.4, .5, .9, 1), size=4, min=0, max=1, subtype='COLOR', name="Active Layer Button Color")
    layerbar_text_color      : FloatVectorProperty(default=(0, 0, 0, 1),     size=4, min=0, max=1, subtype='COLOR', name="Text Color")
    layerbar_text_color_active     : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="Active Text Color")

    statusbar_bg_color       : FloatVectorProperty(default=(.01, .01, .01, 1), size=4, min=0, max=1, subtype='COLOR', name="StatusBar Background Color")
    statusbar_text_color     : FloatVectorProperty(default=(1, 1, 1, 1),     size=4, min=0, max=1, subtype='COLOR', name="StatusBar Text Color")

    toolbar_bg_color         : FloatVectorProperty(default=(.016, .016, .016, 1), size=4, min=0, max=1, subtype='COLOR', name="ToolBar Background Color")
    toolbar_line_color       : FloatVectorProperty(default=(.2, .2, .2, 1), size=4, min=0, max=1, subtype='COLOR', name="ToolBar Line Color")
    toolbar_hovered_tool_color: FloatVectorProperty(default=(.24, .24, .24, 1), size=4, min=0, max=1, subtype='COLOR', name="ToolBar OnHover Tool Color")
    toolbar_active_tool_color: FloatVectorProperty(default=(.34, .5, .76, 1), size=4, min=0, max=1, subtype='COLOR', name="ToolBar Active Tool Color")


    # DIMENSIONS
    wndheader_height         : IntProperty(default=25, name="Window Header Height")
    layerbar_width           : IntProperty(default=32, name="Layer Bar Width")
    menubar_height           : IntProperty(default=25, name="MenuBar Height")
    statusbar_height         : IntProperty(default=16, name="StatusBar Height")
    toolbar_width            : IntProperty(default=32, name="Tool Bar Width")

    # TODO: move this to px unit, so scale to dimensions (only 1 so it's squared ATM)
    # scale : FloatProperty(default=0.1, min=0.0, max=1.0, name="Thumbnail Scale") # Preview to change facial/body

    # TEXT SIZE
    pk_text_size        : IntProperty(default=14, min=8, max=24, name="Picker Area Text Size")
    menubar_text_size    : IntProperty(default=11, min=8, max=24, name="MenuBar Text Size")
    layerbar_text_size  : IntProperty(default=10, min=8, max=24, name="LayerBar Text Size")
    layerbar_text_size  : IntProperty(default=9, min=8, max=24, name="StatusBar Text Size")
    button_text_size    : IntProperty(default=12, min=8, max=24, name="Picker Buttons Text Size")

    # OTHER
    draw_behind_objects : BoolProperty(default=False, name="Draw Behind Objects")
    
    def header_height(self):
        return self.menubar_height + self.wndheader_height
