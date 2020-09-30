import bpy

from .draw.polygon import (
    dr2drr_2, dr2dr, dr2dt, dr2drUniform
)
from .draw.primitives import (
    dr2dl
)
from .draw.text import (
    drtbx, drtrbx, drt
)
from .draw.gpu_shaders import shader_2d_color_unif
from .draw.image import dria
from .pk_ui_icon import PK_UI_Icon
from .functions import point_inside_rect
from .utils.shapes import RectSimple
from blf import size as text_size, dimensions as text_dim
from .utils.colors import ColorsRGBA as Color


MODAL_PASS = 0
MODAL_RUN = 1
MODAL_FINISHED = 2


class PK_UI_ToolTip:
    def __init__(self, parent=None, tooltip: str = ""):
        self.tooltip = tooltip.splitlines() if isinstance(tooltip, str) else [str(tooltip)]
        self.is_active = False
        self.expand = False
        self._timer = None
        self.tool = parent

    def activate(self, context=None):
        if self.is_active:
            if self._timer:
                self.expand = True
        else:
            self.is_active = True
            return 0.6

    def start_timer(self, context=None):
        # This one invoke the function in time.
        if not bpy.app.timers.is_registered(self.activate):
            bpy.app.timers.register(self.activate, first_interval=.6)
        else:
            bpy.app.timers.unregister(self.activate)
            bpy.app.timers.register(self.activate, first_interval=.6)
        # This other one provoke-refresh so we can see the tooltip poping-up.
        if not self._timer:
            if not context:
                context = bpy.context
            self._timer = context.window_manager.event_timer_add(0.7, window=context.window)

    def stop_timer(self, context=None):
        if bpy.app.timers.is_registered(self.activate):
            bpy.app.timers.unregister(self.activate)
        if self._timer:
            if not context:
                context = bpy.context
            context.window_manager.event_timer_remove(self._timer)
            #context.area.tag_redraw()
            self._timer = None
        self.is_active = False
        self.expand = False

    def draw(self, parent, pos):
        if not self.is_active:
            return
        # _x, _y, _size, _color, _text, text_size, _text_color
        if not self.expand:
            drtrbx(
                pos[0] + 10, pos[1], parent.text_dim, (.1, .1, .1, .9), parent.name, 11, (1, 1, 1, 1), shader_2d_color_unif
            )
        else:
            off_y = 20
            height = len(self.tooltip) * 15 + 35
            y = pos[1] - height + 10 + off_y
            dr2drr_2(
                pos[0] + 10, y, 170, height, (.1, .1, .1, .9), 2, 6, shader_2d_color_unif
            )
            y = y + height - 20
            drt(pos[0] + 20, y, parent.name, 11, 0, 1, 1, 1, 1, True)
            y = y - 20
            for line in self.tooltip:
                drt(pos[0] + 20, y, line, 10, 0, 1, 1, 1, 1)
                y -= 15


class PK_UI_Tool:
    def __init__(self, name: str = "", parent=None):
        self.name = name
        text_size(0, 12, 72)
        dim = text_dim(0, name)
        self.text_dim = (dim[0] + 10, dim[1] + 10)
        self.tooltip = None
        #self.is_separator = False
        self.parent = parent
        if parent:
            parent.add_tool(self)
        self.hover = False
        self.icon = None
        self.icon_char = ''

    def set_icon(self, icon: PK_UI_Icon):
        if not icon or not isinstance(icon, PK_UI_Icon):
            return
        self.icon = icon()
        if self.icon:
            self.icon.gl_load()

    def set_char_as_icon(self, char: str = '?'):
        self.icon_char = char

    def set_tooltip(self, tooltip: str = ""):
        self.tooltip = PK_UI_ToolTip(self, tooltip)
        self.parent._add_timer(self.tooltip)

    def on_hover(self, context=None):
        if not self.hover:
            self.on_hover_enter()

    def on_hover_enter(self, context=None):
        self.hover = True
        if self.tooltip:
            self.tooltip.start_timer(context)

    def on_hover_exit(self, context=None):
        self.hover = False
        if self.tooltip:
            self.tooltip.stop_timer(context)

    def draw(self, x, y, size):
        if self.icon:
            dria(
                self.icon, x, y, size, size
            )
        elif self.icon_char:
            drt(x+4, y+4, self.icon_char, 20, 0, 1, 1, 1, 1, True)
        if self.tooltip:
            self.tooltip.draw(self, (x + size, y))
        #else:
        #    dr2dr(
        #        x, y, size, size, (.4, .4, .4, 1.0)
        #    )

    def init(self, op):
        pass

    def exit(self, op):
        pass

    def invoke(self, op, event) -> bool:
        return False

    def modal(self, op, event) -> int:
        return MODAL_PASS

    def draw_callback(self, op, *args, **kwargs):
        pass

''' Now it uses 'None' to say this is a space in between. '''
#class PK_UI_Tool_Separator(PK_UI_Tool):
#    def __init__(self, parent=None):
#        super().__init__('', parent)
#        self.is_separator = True


class PK_UI_ToolSet:
    def __init__(self, name: str = "", parent=None):
        self.name = name
        self.parent = parent # toolbar
        self.default = None # tool
        self.tools = [] # tool
        self.on_hover_item = None

        # Dropdown tool.
        self.item_height = 16
        self.spacing = 4
        self.width = 50
        self.margin_top = 4
        self.margin_bottom = 8
        self.is_active = False
        self.text_size = 10

    def add_tool(self, tool: PK_UI_Tool = None, set_default=False):
        if not tool or not isinstance(tool, PK_UI_Tool):
            return
        self.tools.append(tool)
        if set_default:
            self.default = tool

    def set_default(self, tool: PK_UI_Tool = None):
        if not tool or not isinstance(tool, PK_UI_Tool) or tool not in self.tools:
            return
        self.default = tool

    def on_hover_exit(self, context=None):
        self.default.on_hover_exit()

    # ToolSet Pop-up.
    def draw(self, x, y, size):
        dr2dr(
            x, y, size, size
        )

    def init(self, op):
        self.default.init(op)

    def exit(self, op):
        self.default.exit(op)

    def invoke(self, op, event) -> bool:
        return self.default.invoke(op, event)

    def modal(self, op, event) -> int:
        return self.default.modal(op, event)

    def draw_callback(self, op, *args, **kwargs):
        self.default.modal(op, args, kwargs)


class PK_UI_ToolBar:

    def __init__(self, picker):
        self.picker = picker
        self.tools = []
        self.active_tool = None
        self.timers = []
        self.num_tools = 0
        self.num_spacers = 0
        self.num_cats = 0
        self.cats = []
        self.pos = [0, 0]
        self.size = [0, 0]
        self.on_hover_tool = None
        # self.on_hover_tool_rect = RectSimple()
        self.prev_spacer = False
        self.is_inside = False

        # Hardcoded attributes.
        self.inner_margins = 5
        self.padding_picker = 5
        self.spacer_height = 10
        self.padding_top = 25
        self.padding_right = 5

    def _add_timer(self, ui_timer):
        self.timers.append(ui_timer)

    def stop_all_timers(self, context=None):
        for timer in self.timers:
            if timer.is_active:
                if timer.tool != self.on_hover_tool:
                    print("STOP ALL:", timer.tool)
                    timer.stop_timer()
            timer.tool.hover = False
        if context:
            context.area.tag_redraw()

    def add_tool(self, tool: PK_UI_Tool = None):
        print(tool)
        if tool:
            if self.num_tools == 0 or self.prev_spacer: #self.tools[-1] == None:
                self.cats.append([self.num_tools]*2)
                self.prev_spacer = False
            else:
                self.cats[self.num_cats][1] = self.num_tools
            self.tools.append(tool)
            self.num_tools += 1
            if self is not tool.parent:
                tool.parent = self
        else:
            self.cats[self.num_cats][1] = self.num_tools
            # self.tools.append(None)
            self.prev_spacer = True
            self.num_spacers += 1
            self.num_cats += 1

    def add_separator(self):
        self.add_tool(None)

    def set_default(self, tool):
        if tool in self.tools:
            self.active_tool = tool

    def get_pos(self):
        # OUTSIDE
        # return self.picker.pos[0] + self.picker.size[0] + self.padding_picker, self.picker.pos[1] + self.picker.size[1] - self.picker.theme.menubar_height
        # INSIDE
        return self.picker.pos[0] + self.picker.size[0] - self.picker.theme.toolbar_width - self.padding_right, self.picker.pos[1] + self.picker.size[1] - self.picker.theme.menubar_height - self.padding_top

    def get_size(self):
        w = self.picker.theme.toolbar_width
        return w, w * self.num_tools + self.spacer_height * self.num_spacers

    def get_cat_height(self, index: int = 0) -> int:
        i, f = self.cats[index]
        return (f - i + 1) * self.picker.theme.toolbar_width

    def get_pos_size(self):
        return self.get_pos(), self.get_size()

    def get_rect(self):
        x0, y0 = self.get_pos()
        x1, y1 = self.get_size()
        x1 += x0
        y1 += y0
        return [x0, y0, x1, y1]

    def get_bounds(self):
        x0, y0 = self.get_pos()
        w, h = self.get_size()
        return Rect(x0, y0, w, h, True).get_bounds()

    def on_hover(self, context, mouse) -> bool:
        x, y = self.get_pos()
        size = self.get_size()
        y -= size[1]
        on_hover = point_inside_rect(mouse, (x, y), size)
        if on_hover:
            #print('TOOLBAR: in on_hover')
            self.check_tool(context, mouse)
            self.is_inside = True
            return True
        else:
            #print('TOOLBAR: NOT in on_hover')
            if self.is_inside and self.on_hover_tool:
                #self.on_hover_tool.on_hover_exit()
                self.on_hover_tool = None
                self.stop_all_timers(context)
        return False

    def check_tool(self, context, mouse):
        x, y = self.get_pos()
        w, h = self.get_size()

        theme = self.picker.theme
        tools = self.tools
        tool_w = tool_h = w
        tool_x = x
        tool_y = y - tool_h

        for i, cat in enumerate(self.cats):
            init_tool, final_tool = cat
            num_cat_tools = (final_tool - init_tool)# + 1) # +1 to include 0 index.
            cat_h = num_cat_tools * tool_h

            for k in range(init_tool, final_tool):
                if point_inside_rect(mouse, (tool_x, tool_y), (tool_w, tool_h)):
                    #print('TOOLBAR: tool in on_hover')
                    if self.on_hover_tool != tools[k]:
                        self.on_hover_tool = tools[k]
                        #self.on_hover_tool.on_hover_exit()
                        self.stop_all_timers(context)
                        self.tools[k].on_hover()
                    #print(tools[k].name)
                    # self.tools[k].on_hover = True
                    return True
                tool_y -= tool_h

            # Offset 'y' based on cat height and spacer.
            y -= (cat_h + self.spacer_height)
            tool_y = y - tool_h
        if self.on_hover_tool:
            self.on_hover_tool = None
            self.stop_all_timers(context)
        return False

    def on_click(self, op):
        if self.on_hover_tool:
            if isinstance(self.on_hover_tool, PK_UI_ToolSet):
                pass
            if self.active_tool != self.on_hover_tool:
                self.active_tool.exit(op)
                self.on_hover_tool.on_hover_exit()
                self.active_tool = self.on_hover_tool
                self.active_tool.init(op)

    def invoke_tool(self, op, event) -> bool:
        return self.active_tool.invoke(op, event)

    def modal_tool(self, op, event) -> int:
        return self.active_tool.modal(op, event)

    def tool_draw(self, op, *args, **kwargs):
        self.active_tool.draw_callback(op, args, kwargs)

    def on_mouse_exit(self):
        if self.on_hover_tool:
            self.on_hover_tool.on_hover_exit()
            self.on_hover_tool = None

    def draw(self):
        x, y = self.get_pos()
        w, h = self.get_size()

        dr2dr(
            x, y-h, w, h, (0, 0, 0, .2)
        )

        theme = self.picker.theme
        tools = self.tools
        width = self.picker.theme.toolbar_width
        tool_x = x + self.inner_margins
        tool_w = int(width - self.inner_margins * 2.0)
        tool_y = y - (tool_w + self.inner_margins)

        batch_lines = []

        # DRAW BACKGROUND
        co = theme.toolbar_bg_color

        for i, cat in enumerate(self.cats):
            # Get proper category height.
            # cat_h = self.get_cat_height(i)
            # print(cat)
            init_tool, final_tool = cat
            num_cat_tools = (final_tool - init_tool)# + 1 # +1 to include 0 index.
            cat_h = num_cat_tools * width
            # print(num_cat_tools)

            # Draw cat background.
            dr2drr_2(
                x, y-cat_h, w, cat_h, co, 2, 3
            )

            # Draw each tool from cat.
            for k in range(init_tool, final_tool):
                tool = self.tools[k]

                if tool == self.active_tool:
                    dr2drUniform(x, tool_y-self.inner_margins, w, w, theme.toolbar_active_tool_color)
                elif tool == self.on_hover_tool:
                    dr2drUniform(x, tool_y-self.inner_margins, w, w, theme.toolbar_hovered_tool_color)

                # print(tool)
                tool.draw(tool_x, tool_y, tool_w)

                # Puede dibujarse línea intermedia?
                if num_cat_tools > 1 and k != final_tool:
                    line_y = tool_y - self.inner_margins
                    batch_lines.append((x, line_y))
                    batch_lines.append((x + width, line_y))

                # Calc next tool 'y' pos.
                #tool_y -= (self.inner_margins * 2.0 + width)
                tool_y -= (tool_w + self.inner_margins * 2.0)

            # Offset 'y' based on cat height and spacer.
            y -= (cat_h + self.spacer_height)
            tool_y = y - (tool_w + self.inner_margins)

        # Draw Batched Lines.
        if batch_lines:
            dr2dl(
                theme.toolbar_line_color, *batch_lines
            )
