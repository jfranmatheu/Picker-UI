from enum import Enum

from blf import (
    dimensions as text_dim,
    size as text_size
)
from mathutils import Vector

from .functions import point_inside_rect
from .utils.shapes import Rect, RectSimple
from .draw.polygon import Draw_2D_Rectangle_Rounded_Top, Draw_2D_Rectangle, Draw_2D_Rectangle_Rounded_Bottom, Draw_2D_Rectangle_Rounded
from .draw.text import Draw_Text, Draw_Text_Box
from .draw.toggle import Draw_Checkbox, Draw_Checkbox_Simple
from .draw.primitives import Draw_2D_Line


class MenuItemType(Enum):
    OPS = 0 # operator
    PPT = 1 # property
    SEP = 2 # separator


class PK_UI_MenuItem: # TODO: rename it!
    def __init__(self, name: str, type: MenuItemType, function, *args, **kwargs: dict):
        self.name = name
        self.type = type
        if type == MenuItemType.PPT:
            self.value = function()
        self.function = function
        self.args = args # tuple / list
        self.kwargs = kwargs # dict
        #if kwargs.get('close_on_click', None):
        #    self.close_on_click = kwargs['close_on_click']
        #else:
        #    self.close_on_click = False
        print(self.args, self.kwargs)

    def __call__(self):
        if self.function:
            if self.is_property():
                self.function(True)
                self.value = not self.value
            else:
                self.function(*self.args, **self.kwargs)
        return self.type == MenuItemType.OPS
        # Function that actually changes the property value.
        # ATM only supports boolean properties.
        #    self.set_property_value()
            # To function call when updating property value.
        #    if self.update:
        #        self.update(*self.args)

    def is_separator(self):
        return self.type == MenuItemType.SEP

    def is_property(self):
        return self.type == MenuItemType.PPT

    def get_width(self, size):
        text_size(2, size, 72)
        off = 30 if self.is_property() else 10
        return text_dim(2, self.name)[0] + off + 15


class PK_UI_MenuSeparator(PK_UI_MenuItem): # TODO: rename it!
    def __init__(self):
        super().__init__('', MenuItemType.SEP, None)


class PK_UI_Menu:

    def __init__(self, title: str = 'Menu', parent=None):
        self.parent = parent
        parent.add_menu(self)

        # Dropdown menu.
        self.item_height = 16
        self.spacing = 4
        self.width = 50
        self.margin_top = 4
        self.margin_bottom = 8
        self.is_active = False
        self.text_size = 10
        self.items = []

        # Title setup.
        self.title = title
        self.on_hover_item = None

        if parent and title:
            text_size(0, self.parent.text_size, 72)
            self.title_width = text_dim(0, title)[0]
        else:
            self.title_width = 10

    def add_item(self, item: PK_UI_MenuItem = None):
        if item:
            self.items.append(item)
            w = item.get_width(self.text_size)
            if w > self.width:
                self.width = w

    def draw(self, menu_pos):
        theme = self.parent.picker.theme
        checkbox_bg = Vector((list(theme.menubar_drop_color_active))) * .65
        n = len(self.items)
        x0 = menu_pos[0]
        height = self.item_height * n + self.spacing * (n - 1) + self.margin_top
        y0 = menu_pos[1] - height
        # Draw_2D_Rectangle(x0, y0 - self.margin_bottom, self.width, height + self.margin_bottom, theme.menubar_drop_bg_color)
        Draw_2D_Rectangle_Rounded_Bottom(x0, y0 - self.margin_bottom, [self.width, height + self.margin_bottom], theme.menubar_drop_bg_color, 5)
        text_indent_x = x0 + 10
        for item in reversed(self.items):
            if item.is_separator():
                y = y0 + int(self.item_height/2 - self.spacing/2)
                Draw_2D_Line((x0, y), (x0+self.width, y), (1, 1, 1, .4))
            else:
                if item == self.on_hover_item:
                    Draw_2D_Rectangle(x0+1, y0 - self.spacing, self.width-2, self.item_height + self.spacing, theme.menubar_drop_color_active)
                if item.is_property():
                    Draw_Text(text_indent_x + self.item_height, y0+3, item.name, self.text_size, 0, 1, 1, 1, 1, True)
                    # Draw_Checkbox(x0 + 6, y0, [self.item_height-2, self.item_height-2], item.value, checkbox_bg, item == self.on_hover_item)
                    Draw_Checkbox_Simple(x0+6, y0+1, self.item_height-6, self.item_height-6, item.value, (1, 1, 1, 1), (.1,.1,.1,1))
                else:
                    Draw_Text(text_indent_x, y0+3, item.name, self.text_size, 0, 1, 1, 1, 1, True)
            y0 += self.item_height + self.spacing

    # TODO: add menu_size
    def check(self, menu_pos, event, mouse):
        # print("Menu Pos:", menu_pos)
        n = len(self.items)
        x0 = menu_pos[0]
        height = self.item_height * n + self.spacing * (n - 1) + self.margin_top
        y0 = menu_pos[1] - height
        pos = [x0, y0 - self.margin_bottom - 4]
        size = [self.width, height + self.margin_bottom + 8]
        if not point_inside_rect(mouse, pos, size):
            self.is_active = False
            self.on_hover_item = None
            return False, False

        if not self.is_on_hover(menu_pos, mouse):
            return True, False

        if event.type == 'LEFTMOUSE' and event.value in {'CLICK', 'PRESS'}:
            close = self.on_click() # close on start ?
            self.is_active = False
            self.on_hover_item = None
            if close:
                return False, False
            return True, True

        return True, False

    def is_on_hover(self, menu_pos, mouse):
        my = mouse[1]
        y1 = menu_pos[1] - self.margin_top
        for item in self.items:
            y0 = y1 - self.item_height
            if my < y1 and my > y0:
                if item.is_separator():
                    self.on_hover_item = None
                    return False
                self.on_hover_item = item
                return True
            y1 = y0 - self.spacing
        self.on_hover_item = None
        return False

    def on_click(self):
        if self.on_hover_item:
            return self.on_hover_item()
        return False

    def set_style(self, style: dict = {}):
        for key in style.keys:
            if key and hasattr(self, key):
                setattr(self, key, style[key])


class PK_UI_MenuBar:

    def __init__(self, picker):
        self.picker = picker
        self.menus = []
        self.active_menu = None
        self.pos = [self.picker.pos[0], self.picker.pos[1] + self.picker.size[1] - self.picker.theme.menubar_height]
        self.size = [self.picker.size[0], self.picker.theme.menubar_height]
        self.on_hover_menu = None
        self.active_menu_rect = RectSimple()

        # Hardcoded attributes.
        self.spacing = 20
        self.margin_left = 15
        self.text_size = self.picker.theme.menubar_text_size

    def add_menu(self, menu: PK_UI_Menu = None):
        if menu:
            self.menus.append(menu)
            if self is not menu.parent:
                menu.parent = self
        else:
            raise TypeError

    def get_pos(self):
        return self.picker.pos[0], self.picker.pos[1] + self.picker.size[1] - self.picker.theme.menubar_height

    def get_size(self):
        return self.picker.size[0], self.picker.theme.menubar_height

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

    def draw(self):
        theme = self.picker.theme
        tsize = theme.menubar_text_size
        tco = theme.menubar_text_color
        x0, y0 = self.get_pos()
        w, h = self.get_size()
        self.size = [w, h]
        self.pos = [x0, y0]

        Draw_2D_Rectangle_Rounded_Top(x0, y0, self.size, theme.menubar_bg_color)

        x0 += self.margin_left

        for menu in self.menus:
            if menu == self.active_menu:
                Draw_2D_Rectangle(x0-8, y0+2, menu.title_width+16, h-4, theme.menubar_color_active)
                menu.draw([x0-8, y0])
            elif menu == self.on_hover_menu:
                Draw_2D_Rectangle(x0-8, y0+2, menu.title_width+16, h-4, theme.menubar_color_active)
                # menu.draw([x0-8, y0]) # NOTE: If want to draw on hover instead.
            Draw_Text(x0, y0 + 8, menu.title, tsize, 0, *tco, True)
            x0 += menu.title_width + self.spacing

    def check(self, event, mouse):
        if self.active_menu:
            # Check if mouse is outside menu to set active_menu to NULL.
            on_hover, clicked = self.active_menu.check(self.get_menu_position(self.active_menu), event, mouse)
            if clicked:
                return True
            if not on_hover:
                if not point_inside_rect(mouse, self.pos, self.size):
                    self.active_menu = None
                self.on_hover_menu = None

            else:
                # NOTE: So events inside menu items are not pass through to picker...
                if point_inside_rect(mouse, self.pos, self.size):
                    return True
            # Check if mouse is still inside active menu.
            if point_inside_rect(mouse, self.active_menu_rect.pos, self.active_menu_rect.size):
                return False # UNDO

            #print("- Mouse:", mouse)
            #print("- Rect-Pos:", self.active_menu_rect.pos)
            #print("- Rect-Size:", self.active_menu_rect.size)

        if not point_inside_rect(mouse, self.pos, self.size):
            if self.on_hover_menu:
                self.on_hover_menu = None
                self.active_menu = None
            return False

        # Reaching this point means user is sliding mouse to another menu.
        if self.active_menu:
            if self.is_on_hover(mouse):
                self.active_menu = self.on_hover_menu
            return False

        if not self.is_on_hover(mouse):
            self.active_menu = None
            return False

        if event.type == 'LEFTMOUSE' and event.value in {'CLICK', 'PRESS'}:
            self.on_click()
            return True
        return False

    def get_menu_position(self, target_menu: PK_UI_Menu = None):
        ox = self.picker.pos[0]
        x0 = self.margin_left + ox
        for menu in self.menus:
            if menu == target_menu:
                return [x0, self.pos[1]]
            x0 += menu.title_width + self.spacing
        return [0, 0]

    def is_on_hover(self, mouse):
        ox = self.picker.pos[0]
        x0 = self.margin_left + ox
        mx = mouse[0]
        for menu in self.menus:
            x1 = x0 + menu.title_width
            if mx > x0 - 8 and mx < x1 + 8:
                self.on_hover_menu = menu
                self.active_menu_rect.set_pos(x0 - 8, self.pos[1])
                self.active_menu_rect.set_size(menu.title_width + 16, self.size[1])
                return True
            x0 = x1 + self.spacing
        self.on_hover_menu = None
        return False

    def on_click(self):
        if self.on_hover_menu:
            self.active_menu = self.on_hover_menu

    def set_style(self, style: dict = {}):
        for key in style.keys:
            if key and hasattr(self, key):
                setattr(self, key, style[key])
