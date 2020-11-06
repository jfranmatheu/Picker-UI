from enum import Enum
import bpy
from bpy.types import Operator
from mathutils import Vector
import bgl
from bgl import (
    glEnable, glDisable, GL_DEPTH_TEST, GL_BLEND, glDepthRange, glScissor, GL_SCISSOR_TEST,
    GL_COLOR_BUFFER_BIT
)
from .utils.event import Simulate as Event
'''
try:
    from . import keyboard as Event
except:
    import keyboard as Event
'''
from .functions import (
    point_inside_rect, point_inside_tri, _point_inside_tri, deselect_all_pose_bones, point_inside_circle
)
from .draw.fun import (
    _dr2dr,
    _dr2drt,
    _drai,
    _draoi,
    text_size,
    dr2dr, dr2drr, dr2drrt,
    dr2dtri, dr2drrf, dr2drf,
    dr2ds, dr2drc, dr2drrb,
    dr2drfsc,
    drt, drtbx, drtrbx, dr2dsbr,
    drtbxc, drtbxcwd, drtbxcrwd,
    drtc, drtcswd,
    drtcsoutwd, drtcsoutgwd,
    drtcsgwd,
    driao, dria, driac,
    dr2dl, dr2dls, dr2dps, dr2dp, dr2dcl, dr2dcls,
    dr2dc, dr2dcs, dr2dcaaswd
)
from .pk_ui_menu import PK_UI_MenuBar, PK_UI_Menu, PK_UI_MenuItem, MenuItemType, PK_UI_MenuSeparator
from .pk_ui_tool import PK_UI_ToolBar, PK_UI_Tool, MODAL_PASS, MODAL_RUN, MODAL_FINISHED
from .cursors import Cursor, CursorIcon
from .pk_character import PK_Mode
from .utils.colors import ColorsRGBA as Color


RECTANGLE = 0
CIRCLE = 1
ROUND_SQUARE = 2


''' Item types that can be on hover. '''
class HoverType(Enum):
    NONE = 0
    BUTTON = 1
    LAYER = 2
    MENU = 3
    TOP_RIGHT = 4
    SCENE = 5
    TOOL = 6

NONE = None
BOTTOM = 0
TOP = 1
LEFT = 2
RIGHT = 3

MIDDLE = 4


''' THIS OPERATOR WILL DRAW THE PICKER UI / WIDGET '''
class PK_OT_draw_picker(Operator):
    bl_idname = "pk.draw_picker"
    bl_label = ""
    bl_description = "Draw Picker"
    instance = None
    
    idx : bpy.props.IntProperty(default=-1)
    
    def refresh(self):
        self.ctx_area.tag_redraw()

    def toggle_ghost_mode(self, toggle: bool = False) -> bool:
        if toggle:
            self.ghost_mode = not self.ghost_mode
        return self.ghost_mode

    def toggle_edit_mode(self):
        self.picker.toggle_edit_mode()
        # We need to ensure buttons positions.
        self.ensure_buttons_positions()
        # RESET.
        if self.picker.mode == 0:
            self.using_tool = False
    
    def lock_ui(self, toggle: bool = False) -> bool:
        if toggle:
            self.picker.is_locked = not self.picker.is_locked
        return self.picker.is_locked

    def is_locked(self):
        #print(self.picker.is_locked)
        return self.picker.is_locked

    def move_picker(self, reg):
        size = self.picker.size
        p = self.mousePos - self.offset
        p[0] = 0 if p[0] < 0 else reg.width - size[0] if p[0] + size[0] > reg.width else p[0]
        p[1] = 0 if p[1] < 0 else reg.height - size[1] if p[1] + size[1] > reg.height else p[1]
        self.picker.pos = (int(p[0]), int(p[1])) # must be integer

    def scale_picker(self, reg):
        # New size is the difference. :-)
        # BUT, needs to be clamped to minimum values.
        # Luckily for us, Blender property does it for us this time. ;-)
        self.picker.size = (int(self.mousePos[0]-self.picker.pos[0]), int(self.mousePos[1]-self.picker.pos[1]))

        # We need to ensure buttons positions.
        self.ensure_buttons_positions()

    def ensure_buttons_positions(self):
        active_scene = self.picker.get_active_scene()
        active_view_idx = active_scene.active_view
        active_view = active_scene.get_active_view()

        if active_view.image:
            x, y, w, h = self.get_view_image_pos_size(active_view)
        else:
            w, h = self.get_scene_size(True)
        for b in self.picker.get_active_scene().buttons:
            d = b.get_data_from_view_index(active_view_idx)
            d.pos = [int(w * d.factor[0]), int(h * d.factor[1])]

    def ensure_active_button_relative_position(self):
        if not self.active_button:
            return
        #active_scene = self.picker.get_active_scene()
        #active_view_idx = active_scene.active_view
        #active_view = active_scene.get_active_view()
        #if active_view.image:
        #    x, y, w, h = self.get_view_image_pos_size(active_view)
        #else:
        w, h = self.get_scene_size(True)

        d = self.active_button.get_data_from_view_index(self.active_view_index)
        d.factor = [d.pos[0] / w, d.pos[1] / h]
        #print(list(d.pos))
        #print(list(d.factor))

    def get_scene_position(self, with_margins=False):
        if with_margins:
            return [self.picker.pos[0] + self.picker.theme.layerbar_width + 10, self.picker.pos[1] + self.picker.theme.statusbar_height + 10]
        else:
            return (self.picker.pos[0] + self.picker.theme.layerbar_width, self.picker.pos[1] + self.picker.theme.statusbar_height)

    def get_scene_size(self, with_margins=False):
        pk = self.picker
        if with_margins:
            # In EDIT MODE take into account the tool bar space.
            if pk.mode == 1:
                return [pk.size[0] - pk.theme.layerbar_width - 20 - pk.theme.toolbar_width, pk.size[1] - pk.theme.header_height() - pk.theme.statusbar_height - 35]
            else:
                return [pk.size[0] - pk.theme.layerbar_width - 20, pk.size[1] - pk.theme.header_height() - pk.theme.statusbar_height - 35]
        else:
            return (pk.size[0] - pk.theme.layerbar_width, pk.size[1] - pk.theme.header_height() - pk.theme.statusbar_height)

    def get_view_image_pos_size(self, view):
        scene_pos = self.get_scene_position(True)
        scene_size = self.get_scene_size(True)
        if not view.image:
            return scene_pos[0], scene_pos[1], scene_size[0], scene_size[1]
        s = view.image.size
        p = s[1] / s[0]
        if s[1] > s[0]:
            h = scene_size[1]
            w = h / p
            if w > scene_size[0]:
                x = scene_pos[0]
                w = scene_size[0]
                h = w * p
            else:
                off_x = scene_size[0] - w
                x = scene_pos[0] + abs(off_x / 2.0)
            y = scene_pos[1]
        else:
            w = scene_size[0]
            h = w * p
            if h > scene_size[1]:
                y = scene_pos[1]
                j = scene_size[1]
                w = h / p
            else:
                off_y = scene_size[1] - h
                y = scene_pos[1] + abs(off_y / 2.0)
            x = scene_pos[0]
        return x, y, w, h

    def check_layer_bar(self, event, mouse) -> (bool, bool):
        if self.picker.active_scene == -1:
            return False, False

        scene = self.picker.get_active_scene()
        active_view = scene.active_view

        if active_view == -1:
            return False, False

        view = scene.get_active_view()
        layers = view.layers

        size = [self.picker.theme.layerbar_width, self.picker.size[1] - self.picker.theme.header_height()]
        spacing = [3, 6] # TODO: NOT HARDCODED -> theme.layer_button_spacing
        offX = offY = spacing[0] # we want top spacing to be the same as side spacings (for first item)
        top = self.picker.pos[1] + size[1] # Top coords
        left = self.picker.pos[0] + offX # Left coords # o[0] - size[0] + offX
        width = size[0] - offX * 2 # New width is the total bar width minus the spacing in both sides
        size = [width, width] # Squared size
        offY += width # Add spacing for first item on the layer list/col # need to add width

        for l in layers:
            if point_inside_rect(mouse, [left, top - offY], size):
                self.on_hover_layer = (l, [left, top - offY], size)
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    return True, LEFT
                elif event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
                    return True, RIGHT
                elif event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
                    return True, MIDDLE
                return True, False
            offY += spacing[1] + width
        self.on_hover_layer = None
        return False, False

    def on_click_hovered_button(self, event):
        mouse = self.mousePos
        # ox, oy = self.get_scene_position(True)
        scene = self.picker.get_active_scene()
        active_view = scene.active_view

        if active_view == -1:
            return None

        ox, oy, ow, oh = self.get_view_image_pos_size(scene.get_active_view())

        if self.on_hover_button:
            b_data = self.on_hover_button.get_data_from_view_index(active_view)
            # Get real coordinates and size.
            xt, yt, w, h = b_data.get_real_pos_size()
            xt += ox
            yt += oy
            aug_size = [w + 8, h + 8]
            if point_inside_rect(mouse, [xt - 4, yt - 4], aug_size):
                sep = 2
                if point_inside_circle(mouse, (xt + int(w / 2), yt - sep), 4):
                    self.scaling_from = BOTTOM
                elif point_inside_circle(mouse, (xt + int(w / 2), yt + h + sep), 4):
                    self.scaling_from = TOP
                elif point_inside_circle(mouse, (xt - sep, yt + int(h / 2)), 4):
                    self.scaling_from = LEFT
                elif point_inside_circle(mouse, (xt + w + sep, yt + int(h / 2)), 4):
                    self.scaling_from = RIGHT
                else:
                    self.scaling_from = NONE
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.active_button = self.on_hover_button
                    print("Clicked button:", self.on_hover_button.name)
                    return b_data
                self.active_button = None
                return None

        for b in scene.buttons:
            b_data = b.get_data_from_view_index(active_view)
            # TODO: CHANGE THIS!
            if b.style.shape != RECTANGLE:
                b_data.size[1] = b_data.size[0]
            # Get real coordinates and size.
            x, y, w, h = b_data.get_real_pos_size()
            if point_inside_rect(mouse, [x + ox, y + oy], [w, h]):
                print("On hover button:", b.name)
                self.on_hover_button = b
                self.hover_type = HoverType.BUTTON
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.active_button = b
                    print("Clicked button:", b.name)
                    return b_data
                return None
        self.on_hover_button = None
        self.active_button = None
        return None

    def move_button(self):
        # ox, oy = self.get_scene_position(True)
        ow, oh = self.get_scene_size(True)
        #ox, oy, ow, oh = self.get(active_view)

        b_data = self.active_button.get_data_from_view_index(self.active_view_index)
        size = b_data.size

        # Get real coordinates and size.
        #xt, yt, w, h = b_data.get_real_pos_size()
        #xt += ox
        #yt += oy

        # transposed_mouse = self.mousePos - Vector((ox, oy))
        p = self.mousePos - self.offset
        p[0] = size[0] if p[0] - size[0] < 0 else ow - size[0] if p[0] + size[0] > ow else p[0]
        p[1] = size[1] if p[1] - size[1] < 0 else oh - size[1] if p[1] + size[1] > oh else p[1]
        b_data.pos = (int(p[0]), int(p[1])) # must be integer

    def scale_button(self, event):
        mx, my = self.mousePos
        side = self.scaling_from
        min_size = 5
        padding_top = 25
        ox, oy = self.get_scene_position(True)
        ow, oh = self.get_scene_size(True)
        b_data = self.active_button.get_data_from_view_index(self.active_view_index)

        if event.alt:
            if side in {LEFT, RIGHT}:
                local_mouse_pos = mx - ox
                if local_mouse_pos < 0:
                    return
                if local_mouse_pos > ox + ow:
                    return
                diff_pos = abs(int(self.initial_pos[0] - local_mouse_pos))
                if diff_pos == 0:
                    return
                if diff_pos <= min_size:
                    return
                if (self.initial_pos[0] - diff_pos) < 0:
                    return
                if (self.initial_pos[0] + diff_pos) > ow:
                    return
                b_data.size[0] = diff_pos
                if self.active_button.style.shape != RECTANGLE:
                    b_data.size[1] = b_data.size[0]
            elif side in {TOP, BOTTOM}:
                local_mouse_pos = my - oy
                if local_mouse_pos < 0:
                    return
                if local_mouse_pos > oy + oh:
                    return
                diff_pos = abs(int(self.initial_pos[1] - local_mouse_pos))
                if diff_pos == 0:
                    return
                if diff_pos <= min_size:
                    return
                if (self.initial_pos[1] - diff_pos) < 0:
                    return
                if (self.initial_pos[1] + diff_pos) > oh:
                    return
                b_data.size[1] = diff_pos
                if self.active_button.style.shape != RECTANGLE:
                    b_data.size[0] = b_data.size[1]
            return

        if side == LEFT:
            local_mouse_pos = mx - ox
            if local_mouse_pos < 0:
                return
            o_left_x = self.initial_pos[0] - self.initial_size[0]
            diff_pos = int((o_left_x - local_mouse_pos) / 2)
            if diff_pos == 0:
                return
            diff_pos = diff_pos if diff_pos % 2 == 0 else diff_pos + 1
            new_pos = self.initial_pos[0] - diff_pos
            new_size = self.initial_size[0] + diff_pos
            if new_size <= min_size:
                return
            else:
                b_data.pos[0] = new_pos
                b_data.size[0] = new_size
                if self.active_button.style.shape != RECTANGLE:
                    b_data.size[1] = b_data.size[0]
        elif side == RIGHT:
            local_mouse_pos = mx - ox
            if local_mouse_pos > ox + ow:
                return
            o_right_x = self.initial_pos[0] + self.initial_size[0]
            diff_pos = int((local_mouse_pos - o_right_x) / 2)
            if diff_pos == 0:
                return
            diff_pos = diff_pos if diff_pos % 2 == 0 else diff_pos + 1
            new_pos = self.initial_pos[0] + diff_pos
            new_size = self.initial_size[0] + diff_pos
            if new_size <= min_size:
                return
            else:
                b_data.pos[0] = new_pos
                b_data.size[0] = new_size
                if self.active_button.style.shape != RECTANGLE:
                    b_data.size[1] = b_data.size[0]
        elif side == BOTTOM:
            local_mouse_pos = my - oy
            if local_mouse_pos < 0:
                return
            o_bot_y = self.initial_pos[1] - self.initial_size[1]
            diff_pos = int((o_bot_y - local_mouse_pos) / 2)
            if diff_pos == 0:
                return
            diff_pos = diff_pos if diff_pos % 2 == 0 else diff_pos + 1
            new_pos = self.initial_pos[1] - diff_pos
            new_size = self.initial_size[1] + diff_pos
            if new_size <= min_size:
                return
            else:
                b_data.pos[1] = new_pos
                b_data.size[1] = new_size
                if self.active_button.style.shape != RECTANGLE:
                    b_data.size[0] = b_data.size[1]
        elif side == TOP:
            local_mouse_pos = my - oy
            if local_mouse_pos > oy + oh:
                return
            o_top_y = self.initial_pos[1] + self.initial_size[1]
            diff_pos = int((local_mouse_pos - o_top_y) / 2)
            if diff_pos == 0:
                return
            diff_pos = diff_pos if diff_pos % 2 == 0 else diff_pos + 1
            new_pos = self.initial_pos[1] + diff_pos
            new_size = self.initial_size[1] + diff_pos
            if new_size <= min_size:
                return
            else:
                b_data.pos[1] = new_pos
                b_data.size[1] = new_size
                if self.active_button.style.shape != RECTANGLE:
                    b_data.size[0] = b_data.size[1]


    def check_clicked_button(self, context, event, mouse) -> bool:
        # print("Clicked, searching button...")
        
        # ox, oy = self.get_scene_position(True)
        scene = self.picker.get_active_scene()
        if not scene:
            self.failed = True
            return False
        ox, oy, ow, oh = self.get_view_image_pos_size(scene.get_active_view())
        
        active_view = scene.active_view

        if active_view == -1:
            return False

        for b in scene.buttons:
            b_data = b.get_data_from_view_index(active_view)
            # TODO: CHANGE THIS!
            if b.style.shape != RECTANGLE:
                b_data.size[1] = b_data.size[0]
            # Get real coordinates and size.
            x, y, w, h = b_data.get_real_pos_size()
            if point_inside_rect(mouse, (x + ox, y + oy), (w, h)):
                self.active_button = b
                return self.select_bone(context, b, event.shift, event.alt)
        self.active_button = None
        return False

    def check_button(self, event):
        # print("Searching button...")
        mouse = self.mousePos
        scene = self.picker.get_active_scene()
        active_view = scene.active_view

        if active_view == -1:
            return None
        
        view = scene.get_active_view()
        
        if view.image:
            ox, oy, ow, oh = self.get_view_image_pos_size(view)
        else:
            ox, oy = self.get_scene_position(True)

        for b in scene.buttons:
            b_data = b.get_data_from_view_index(active_view)
            # TODO: CHANGE THIS!
            if b.style.shape != RECTANGLE:
                b_data.size[1] = b_data.size[0]
            # Get real coordinates and size.
            x, y, w, h = b_data.get_real_pos_size()
            if point_inside_rect(mouse, (x + ox, y + oy), (w, h)):
                #self.active_button = b
                return b
        # self.active_button = None
        return None

    def select_bone(self, context, button, additive=False, mirror=False) -> bool:
        arma = self.picker.arm_obj.data
        bone = arma.bones.get(button.name, None)
        if not bone:
            self.report({'WARNING'}, "Bone '%s' not found" % button.name)
            return False
        if not additive:
            deselect_all_pose_bones(context)
        bone.select = True # Select the target bone
        if mirror:
            if button.name[-1] in {'L', 'l'}:
                ending = 'R' if button.name.endswith('L') else 'r'
                bone = arma.bones.get(button.name[:-1] + ending, None)
            elif button.name[-1] in {'R', 'r'}:
                ending = 'L' if button.name.endswith('R') else 'l'
            else:
                ending = None
            if ending:
                bone = arma.bones.get(button.name[:-1] + ending, None)
                if bone:
                    bone.select = True
                
        arma.bones.active = bone # Make the target bone the active one
        if self.picker.use_button_direct_action:
            if button.action == 'MOVE':
                #bpy.ops.transform.translate(context, release_confirm=True) # devuelve finished es decir no tira el operador bien :(
                #keyboard.press_and_release('g')
                #Event.press_and_release(context, self.mousePos, 'G')
                bpy.ops.transform.translate('INVOKE_DEFAULT', orient_type='GLOBAL', release_confirm=True)
            elif button.action == 'ROTATE':
                #bpy.ops.transform.rotate(release_confirm=True)
                #keyboard.press_and_release('r')
                #Event.press_and_release(context, self.mousePos, 'R')
                bpy.ops.transform.rotate('INVOKE_DEFAULT', orient_type='GLOBAL', release_confirm=True)
            else: # SCALE
                #bpy.ops.transform.resize(release_confirm=True)
                #keyboard.press_and_release('s')
                #Event.press_and_release(context, self.mousePos, 'S')
                bpy.ops.transform.resize('INVOKE_DEFAULT', orient_type='GLOBAL', release_confirm=True)
        return True

    def modal(self, context, event):
        if context.workspace != self.ctx_workspace:
            self.finish()
            return {'CANCELLED'}
        elif bpy.context.scene != self.ctx_scene:
            return {'CANCELLED'}
        elif self.ctx_area != context.area:
            self.finish()
            return {'CANCELLED'}
        if context.mode != 'POSE':
            self.finish()
            return {'CANCELLED'}
        if not self.picker or self.picker.name == "" or self.failed:
            print("Name:", self.picker.name)
            print("HELLO ERROR")
            del self.picker
            self.finish()
            context.area.tag_redraw()
            return {'CANCELLED'}
        if self.signal:
            from . utils.signal import Signal
            if self.signal == Signal.GENERATE_IMAGE:
                self.prev_signal = self.signal
                self.signal = Signal.COMPLETE
                return {'RUNNING_MODAL'}
            elif self.signal == Signal.COMPLETE:
                if self.prev_signal == Signal.GENERATE_IMAGE:
                    self.is_hidden = False
                    self.refresh()
                self.prev_signal = NONE
                self.signal = NONE
            return {'RUNNING_MODAL'}
        #print(event.type, event.value)
        #print(bpy.context.window_manager.clipboard)

        # UI is locked due to some external event / operator.
        #if context.scene.pickers.block_ui:
        #    return {'PASS_THROUGH'}

        self.mousePos = Vector((event.mouse_region_x, event.mouse_region_y))

        # We are using some tool.
        if self.using_tool:
            signal = self.toolbar.modal_tool(self, event)
            if signal == MODAL_PASS:
                return {'PASS_THROUGH'}
            if signal == MODAL_FINISHED:
                self.using_tool = False
            return {'RUNNING_MODAL'}

        elif self.picker.mode == 0 and self.menu_bar.check(context.region, event, self.mousePos):
            return {'RUNNING_MODAL'}
        elif self.picker.mode == 1 and self.edit_menu_bar.check(context.region, event, self.mousePos):
            return {'RUNNING_MODAL'}

        # We are moving our picker UI.
        elif self.moving:
            if (event.type == 'LEFTMOUSE' and event.value == 'RELEASE') or event.value not in {'PRESS', 'MOUSEMOVE', 'NOTHING'}:
                #print(event.type, event.value)
                Cursor.set_icon(context, CursorIcon.DEFAULT)
                self.moving = False
                return {'PASS_THROUGH'}
            Cursor.set_icon(context, CursorIcon.HAND)
            self.move_picker(context.region)
            self.ctx_area.tag_redraw()

        # We are scaling our piker UI.
        elif self.scaling:
            if (event.type == 'LEFTMOUSE' and event.value == 'RELEASE') or event.value not in {'PRESS', 'MOUSEMOVE', 'NOTHING'}:
                Cursor.set_icon(context, CursorIcon.DEFAULT)
                self.scaling = False
                return {'PASS_THROUGH'}
            Cursor.set_icon(context, CursorIcon.MOVE_X)
            self.scale_picker(context.region)
            self.ctx_area.tag_redraw()

        # Detects if mouse is inside the picker UI
        elif point_inside_rect(self.mousePos, self.picker.pos, self.picker.size):
            self.ctx_area.tag_redraw()
            self.inside = True

            ''' 1o. Check WHERE the mouse is. '''
            # SCENE ?
            pk = self.picker
            scene_pos = (pk.pos[0] + pk.theme.layerbar_width, pk.pos[1])
            scene_size = (pk.size[0] - pk.theme.layerbar_width, pk.size[1] - pk.theme.header_height())

            if point_inside_rect(self.mousePos, scene_pos, scene_size):
                self.hover_type = HoverType.SCENE
                Cursor.set_icon(context, CursorIcon.DEFAULT)
                self.on_hover_layer = None
                # TODO: Check buttons for hovering effect. (timer)
            else:
                # Outside Scene. Make sure active button is null.
                self.active_button = None

                # LAYER BAR.
                on_hover, clicked = self.check_layer_bar(event, self.mousePos)
                if clicked:
                    if clicked == LEFT and self.on_hover_layer:
                        self.on_hover_layer[0].toggle()
                    elif clicked == RIGHT and self.on_hover_layer:
                        self.on_hover_layer[0].show_context_menu(context)
                    elif clicked == MIDDLE:
                        pass
                        # TODO: SCROLL
                    return {'RUNNING_MODAL'}
                elif on_hover:
                    # if clicked == MIDDLE:
                        # TODO: SCROLL
                    self.hover_type = HoverType.LAYER
                    return {'PASS_THROUGH'}

                if not self.is_locked():
                    # TOP_RIGHT ? (for scaling).
                    tr = [pk.pos[0] + pk.size[0], pk.pos[1] + pk.size[1]]
                    if point_inside_tri(
                            self.mousePos[0], self.mousePos[1],
                            tr[0], tr[1],
                            tr[0] - 12, tr[1],
                            tr[0], tr[1] - 12):
                        
                        self.hover_type = HoverType.TOP_RIGHT
                        Cursor.set_icon(context, CursorIcon.MOVE_X)
                    else:
                        Cursor.set_icon(context, CursorIcon.DEFAULT)
                        self.hover_type = HoverType.NONE
                else:
                    Cursor.set_icon(context, CursorIcon.DEFAULT)
                    self.hover_type = HoverType.NONE

            ''' 2o. Check WHICH event was triggered. '''
            # PICKER MODE
            if pk.mode == PK_Mode.OBJECT():
                # LEFT_MOUSE
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        if self.hover_type == HoverType.SCENE:
                            if self.check_clicked_button(context, event, self.mousePos):
                                #if self.picker.use_button_direct_action:
                                #    return {'PASS_THROUGH'}
                                return {'RUNNING_MODAL'}
                        if not self.is_locked():
                            if self.hover_type == HoverType.TOP_RIGHT:
                                self.scaling = True
                            else:
                                self.moving = True
                                self.offset = self.mousePos - Vector((pk.pos[0], pk.pos[1]))
                    return {'RUNNING_MODAL'}
                # EXIT 0/
                elif event.type == 'ESC':
                    self.finish(context)
                    return {'FINISHED'}
            # EDIT MODE
            else: # pk.mode == PK_Mode.EDIT()
                if self.hover_type.SCENE:
                    # TOOLBAR.
                    if self.toolbar.on_hover(context, self.mousePos):
                        if event.type == 'LEFTMOUSE':
                            if event.value == 'PRESS':
                                self.toolbar.on_click(self)
                            return {'RUNNING_MODAL'}
                        return {'PASS_THROUGH'}
                    # BUTTONS.
                    if event.type == 'RIGHTMOUSE':
                        if event.value == 'PRESS':
                            button = self.check_button(event)
                            if button:
                                print("Open Button Context Menu")
                                button.show_context_menu(context)
                        return {'RUNNING_MODAL'}
                    # TOOL
                    invoke = self.toolbar.invoke_tool(self, event)
                    if invoke:
                        self.using_tool = True
                        return {'RUNNING_MODAL'}
                # WIDGET.
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        if not self.is_locked():
                            if self.hover_type == HoverType.TOP_RIGHT:
                                self.scaling = True
                            else:
                                self.moving = True
                                self.offset = self.mousePos - Vector((pk.pos[0], pk.pos[1]))
                    return {'RUNNING_MODAL'}
                # EXIT EDIT MODE 0/
                elif event.type == 'ESC':
                    if event.value == 'RELEASE':
                        self.toggle_edit_mode()
                        self.active_button = None
                        self.moving = False
                        self.scaling = False
                        self.scaling_from = NONE
                        self.using_tool = False
                    return {'RUNNING_MODAL'}
        else:
            # Was inside ?
            if self.inside:
                # Ensure cursor is right one.
                Cursor.set_icon(context, CursorIcon.DEFAULT)
                self.inside = False
                self.on_hover_layer = None
                self.active_button = None

        return {'PASS_THROUGH'}

    def execute(self, context):
        ''' SOME USEFUL REFERENCES '''
        self.ctx_area = context.area # To detect area/space/editor changes
        self.ctx_scene = bpy.context.scene # To detect scene changes
        self.ctx_workspace = context.workspace # To detect workspace changes

        ''' SETUP PICKER VARIABLES '''
        self.ghost_mode = False
        if self.idx == -1:
            context.scene.pickers.active_index = len(context.scene.pickers.data) - 1
            if context.scene.pickers.active_index < 0:
                print("ERROR: Picker data not found")
                return {'CANCELLED'}
        else:
            context.scene.pickers.active_index = self.idx
        self.picker = context.scene.pickers.data[self.idx]
        if not self.picker:
            print("ERROR: Picker data is invalid or corrupted")
            return {'CANCELLED'}
        if self.picker.active_scene != -1:
            scene = self.picker.scenes[self.picker.active_scene]
            if scene.active_view != -1:
                print("VIEW DETECTED")
                view = scene.main_view if scene.active_view == 0 else scene.secondary_view
                self.load_view_image(view) # scene.views[scene.active_view]

        self.scene_pos = (self.picker.pos[0] + self.picker.theme.layerbar_width, self.picker.pos[1])
        self.scene_size = (self.picker.size[0] - self.picker.theme.layerbar_width, self.picker.size[1] - self.picker.theme.header_height())
        self.active_view_index = 0

        ''' SETUP MODAL VARIABLES '''
        self.triggers = []
        self.signal = NONE
        self.prev_signal = NONE
        self.signal_args = ()
        self.is_hidden = False
        self.failed = False
        self.override_buttons = False
        self.using_tool = False
        self.temp_button_props = {}
        self.on_hover_layer = None
        self.on_hover_button = None
        self.active_button = None
        self.scaling_from = NONE
        self.initial_pos = [0, 0]
        self.initial_size = [0, 0]
        self.firstPos = Vector((0, 0))
        self.mousePos = Vector((0, 0))
        self.inside = False
        self.moving = False
        self.scaling = False
        self.hover_type = HoverType.NONE

        global context_area
        context_area = self.ctx_area

        ''' SETUP MENU_BAR '''
        OP = MenuItemType.OPS
        PPT = MenuItemType.PPT
        SEP = MenuItemType.SEP

        menu_bar = PK_UI_MenuBar(self.picker)
        # TODO: add poll function to know if button is enabled or disabled.
        m_picker = PK_UI_Menu("Picker ", menu_bar)
        m_picker.add_item(PK_UI_MenuItem("Toggle Edit Mode", OP, self.toggle_edit_mode))
        m_picker.add_item(PK_UI_MenuSeparator())
        m_picker.add_item(PK_UI_MenuItem("Lock UI", PPT, self.lock_ui))
        m_picker.add_item(PK_UI_MenuSeparator())
        m_picker.add_item(PK_UI_MenuItem("Close", OP, self.finish))

        m_scene = PK_UI_Menu("Scene", menu_bar)
        m_scene.add_item(PK_UI_MenuItem("New", OP, bpy.ops.pk.create_scene, 'INVOKE_DEFAULT'))
        m_scene.add_item(PK_UI_MenuItem("Remove Active", OP, bpy.ops.pk.remove_scene))
        m_scene.add_item(PK_UI_MenuSeparator())
        m_scene.add_item(PK_UI_MenuItem("Switch Scene", OP, bpy.ops.pk.change_scene_selector, 'INVOKE_DEFAULT'))

        m_view = PK_UI_Menu("View", menu_bar)
        m_view.add_item(PK_UI_MenuItem("Switch View", OP, bpy.ops.pk.switch_view))
        m_view.add_item(PK_UI_MenuSeparator())
        m_view.add_item(PK_UI_MenuItem("Generate Image", OP, self.generate_image_safe, 'INVOKE_DEFAULT'))
        m_view.add_item(PK_UI_MenuSeparator())
        m_view.add_item(PK_UI_MenuItem("Clear", OP, bpy.ops.pk.clear_view, 'INVOKE_DEFAULT'))

        m_layer = PK_UI_Menu("Layer", menu_bar)
        m_layer.add_item(PK_UI_MenuItem("New", OP, bpy.ops.pk.create_layer, 'INVOKE_DEFAULT'))
        m_layer.add_item(PK_UI_MenuItem("Remove", OP, bpy.ops.pk.remove_layer, 'INVOKE_DEFAULT'))

        m_button = PK_UI_Menu("Button", menu_bar)
        m_button.add_item(PK_UI_MenuItem("Add Selected Bones", OP, bpy.ops.pk.layer_add_selected_buttons, 'INVOKE_DEFAULT')) # pk.create_picker_button))
        # m_button.add_item(PK_UI_MenuItem("Remove", OP, bpy.ops.pk.remove_picker_button))
        m_button.add_item(PK_UI_MenuSeparator())
        m_button.add_item(PK_UI_MenuItem("Direct action", PPT, self.picker.get_set_use_button_direct_action))

        self.menu_bar = menu_bar

        ###

        edit_menu_bar = PK_UI_MenuBar(self.picker)

        m_picker = PK_UI_Menu("Picker ", edit_menu_bar)
        m_picker.add_item(PK_UI_MenuItem("Toggle Edit Mode", OP, self.toggle_edit_mode))
        m_picker.add_item(PK_UI_MenuSeparator())
        m_picker.add_item(PK_UI_MenuItem("Close", OP, self.finish))

        m_edit = PK_UI_Menu("Edit", edit_menu_bar)
        m_edit.add_item(PK_UI_MenuItem("Ghost Mode", PPT, self.toggle_ghost_mode))

        # m_selection = PK_UI_Menu("Selection", edit_menu_bar)
        # m_selection.add_item(PK_UI_MenuItem("Remove selected buttons", OP, self.toggle_ghost_mode))

        self.edit_menu_bar = edit_menu_bar

        ''' SETUP TOOLBAR '''
        from .tool_selection import Tool_SelectTweak, Tool_SelectBox # Templates.
        from .tool_zdepth import Tool_ZDepth
        from .tool_magicpicker import Tool_MagicPicker
        toolbar = PK_UI_ToolBar(self.picker)

        tool_1 = Tool_SelectTweak(toolbar)
        toolbar.set_default(tool_1)
        Tool_SelectBox(toolbar)

        toolbar.add_separator()

        Tool_MagicPicker(toolbar)

        toolbar.add_separator()

        Tool_ZDepth(toolbar)

        toolbar.add_separator()

        #tool_move = PK_UI_Tool("Move", toolbar)
        #tool_rotate = PK_UI_Tool("Rotate", toolbar)

        self.toolbar = toolbar
        
        self.ensure_buttons_positions()

        ''' SETUP HANDLERS '''
        if not context.window_manager.modal_handler_add(self):
            return {'FINISHED'}
        args = (self, context)
        self._handler = context.space_data.draw_handler_add(draw_picker_callback_px, args, 'WINDOW', 'POST_PIXEL')
        context.area.tag_redraw()
        PK_OT_draw_picker.instance = self
        return {'RUNNING_MODAL'}

    def finish(self, context=None):
        PK_OT_draw_picker.instance = None
        try:
            if hasattr(self, '_handler'):
                if context:
                    context.space_data.draw_handler_remove(self._handler, 'WINDOW')
                    context.area.tag_redraw()
                else:
                    bpy.types.SpaceView3D.draw_handler_remove(self._handler, 'WINDOW')
                del self._handler
        except Exception as e:
            print(e)

    def load_view_image(self, view):
        if view.image:
            print("Loading picker image...")
            view.image.gl_load()
    
    def generate_image_safe(self, *args):
        from .utils.signal import Signal
        self.is_hidden = True
        self.refresh()
        bpy.ops.pk.view_generate_image(*args)
        self.signal = Signal.GENERATE_IMAGE
        # self.signal_args = args


def draw_picker_callback_px(self, context):
    if self.ctx_area != context.area:
        return
    if not self.picker:
        return
    if self.is_hidden:
        return

    ''' INTERESTING VARS '''
    pk = self.picker
    theme = pk.theme
    statusbar_height = theme.statusbar_height

    o = pk.pos
    behind = theme.draw_behind_objects

    if behind:
        glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    ''' START BY DRAWING THE BACKGROUND '''
    # TODO: Change picker position to scene position or something more deep like area or so.
    # _dr2dr(o[0], o[1], pk.size, theme.pk_bg_color)
    if pk.mode == PK_Mode.OBJECT():
        dr2drr(o[0], o[1], pk.size, theme.pk_bg_color)


    ''' DRAW SCENE. '''
    if pk.active_scene != -1:
        scene = pk.scenes[pk.active_scene]
        active_view = scene.active_view
        if active_view != -1:
            #view = scene.views[scene.active_view]
            #side = view.is_side_view
            view = scene.main_view if active_view == 0 else scene.secondary_view
            layers = view.layers
            self.active_view_index = active_view
        else:
            print("ERROR: No view detected!")
        buttons = scene.buttons
    else:
        print("WAR: Picker has no Scene!")
        # Draw Layer Bar.
        size = [theme.layerbar_width, pk.size[1] - statusbar_height - theme.header_height()] #]
        _dr2dr(o[0], o[1] + statusbar_height, size, theme.layerbar_bg_color)

        # Draw Menu Bar.
        self.menu_bar.draw()

        if behind:
            glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        return

    # Real scene transform.
    self.scene_pos = (o[0] + theme.layerbar_width + 10, o[1] + statusbar_height + 10)
    if pk.mode == 1:
        self.scene_size = (pk.size[0] - theme.layerbar_width - 20 - theme.toolbar_width, pk.size[1] - theme.header_height() - statusbar_height - 35)
    else:
        self.scene_size = (pk.size[0] - theme.layerbar_width - 20, pk.size[1] - theme.header_height() - statusbar_height - 35)

    # frame name points
    width = 90
    left = [self.scene_pos[0] + int(self.scene_size[0] / 2) - int(width / 2), self.scene_pos[1] + self.scene_size[1]]
    right = [self.scene_pos[0] + int(self.scene_size[0] / 2) + int(width / 2), self.scene_pos[1] + self.scene_size[1]]

    # Draw scene frame representing margins.
    dr2dls((.4, .4, .4, .2),
                  # B  # D
                  # A  # C
                  [self.scene_pos[0], self.scene_pos[1]], [self.scene_pos[0], self.scene_pos[1] + self.scene_size[1]], # A-B
                  [self.scene_pos[0], self.scene_pos[1]], [self.scene_pos[0] + self.scene_size[0], self.scene_pos[1]], # A-C
                  #[self.scene_pos[0], self.scene_pos[1] + self.scene_size[1]], [self.scene_pos[0] + self.scene_size[0], self.scene_pos[1] + self.scene_size[1]], # B-D
                  [self.scene_pos[0] + self.scene_size[0], self.scene_pos[1]], [self.scene_pos[0] + self.scene_size[0], self.scene_pos[1] + self.scene_size[1]], # C-D
                  # TOP
                  [self.scene_pos[0], self.scene_pos[1] + self.scene_size[1]], left, # B - Left
                  [self.scene_pos[0] + self.scene_size[0], self.scene_pos[1] + self.scene_size[1]], right # D - Right
                )
    dr2drrf(left[0], left[1]-10, width, 20, 6, (.4, .4, .4, .2))
    drt(left[0]+10, left[1]-3, self.picker.name, 11, 0, .5, .5, .5, .5, True)

    # Draw picker view image.
    if view.image:
        s = view.image.size
        p = s[1] / s[0]
        if s[1] > s[0]:
            h = self.scene_size[1]
            w = h / p
            if w > self.scene_size[0]:
                x = self.scene_pos[0]
                w = self.scene_size[0]
                h = w * p
            else:
                off_x = self.scene_size[0] - w
                x = self.scene_pos[0] + abs(off_x / 2.0)
            y = self.scene_pos[1]
        else:
            w = self.scene_size[0]
            h = w * p
            if h > self.scene_size[1]:
                y = self.scene_pos[1]
                j = self.scene_size[1]
                w = h / p
            else:
                off_y = self.scene_size[1] - h
                y = self.scene_pos[1] + abs(off_y / 2.0)
            x = self.scene_pos[0]

        # New 'scene' area coordinates based on view image.
        ox = int(x)
        oy = int(y)

        driao(view.image, x, y, w, h, view.image_opacity)

    else:
        # No image, coordinates from scene itself.
        ox, oy = self.scene_pos

    # Fondo anaranjado en edit mode.
    if self.picker.mode == 1:
        dr2dr(self.scene_pos[0] - 10, self.scene_pos[1] - 10, self.scene_size[0] + 20 + theme.toolbar_width, self.scene_size[1] + 35, (.8, .4, .2, .05))

    ''' CONTINUE WITH BUTTONS '''
    text_size = theme.button_text_size
    if not self.override_buttons:
        draw_buttons(active_view, layers, buttons, ox, oy, text_size)

    ''' SCENE EDIT MODE '''
    if self.picker.mode == 1:
        drt(self.scene_pos[0], self.scene_pos[1] + self.scene_size[1] + 5, "[ Edit Mode ]", 12)
        self.toolbar.tool_draw(self, ox, oy)
    else:
        if self.active_button:
            style = self.active_button.style
            data = self.active_button.get_data_from_view_index(active_view)
            shading = style.shading
            if style.shape == RECTANGLE:
                drtbxcrwd (
                    data.pos[0] + ox, data.pos[1] + oy,
                    data.size, data.rotation, style.color_on_hover,
                    self.active_button.text, style.text_color_on_hover, text_size, True, data.depth
                )
            else: # CIRCLE
                if shading == 'FLAT':
                    if style.use_outline:
                        if style.outline_blur:
                            drtcsoutgwd (
                                data.pos[0] + ox, data.pos[1] + oy,
                                data.size[0], style.color_on_hover, style.outline_color,
                                style.outline_factor, style.outline_blur,
                                self.active_button.text, style.text_color_on_hover, text_size
                            )
                        else:
                            drtcsoutwd (
                                data.pos[0] + ox, data.pos[1] + oy,
                                data.size[0], style.color_on_hover,
                                style.outline_color, style.outline_factor,
                                self.active_button.text, style.text_color_on_hover, text_size
                            )
                    else:
                        drtcswd (
                            data.pos[0] + ox, data.pos[1] + oy, data.size[0], style.color_on_hover,
                            self.active_button.text, style.text_color_on_hover, text_size, True
                        )
                elif shading == 'GRAD':
                    drtcsgwd (
                        data.pos[0] + ox, data.pos[1] + oy,
                        data.size[0], style.color_on_hover,
                        style.second_color, style.gradient_type, style.gradient_factor, style.gradient_rotation,
                        self.active_button.text, style.text_color_on_hover, text_size
                    )
                elif shading == 'IMG':
                    pass

    ''' DRAW LAYERS '''
    # Draw Layer Bar.
    size = [theme.layerbar_width, pk.size[1] - theme.header_height()]
    _dr2dr(o[0], o[1] + statusbar_height, size, theme.layerbar_bg_color)

    glEnable(GL_SCISSOR_TEST)
    #glClearColor(0, 0, 0, 0)
    #glClear(GL_COLOR_BUFFER_BIT | GL_SCISSOR_BIT)
    glScissor(o[0], o[1] + statusbar_height, size[0], size[1])

    tsize = theme.layerbar_text_size
    co, co_act = theme.layerbar_button_color, theme.layerbar_button_color_active
    tco, tco_act = theme.layerbar_text_color, theme.layerbar_text_color_active
    spacing = [3, 6] # TODO: NOT HARDCODED -> theme.layer_button_spacing
    offX = offY = spacing[0] # we want top spacing to be the same as side spacings (for first item)
    top = o[1] + size[1] # Top coords
    left = o[0] + offX # Left coords # o[0] - size[0] + offX
    width = size[0] - offX * 2 # New width is the total bar width minus the spacing in both sides
    size = [width, width] # Squared size
    offY += width # Add spacing for first item on the layer list/col # need to add width

    for l in layers:
        drtbx(left, top - offY, size, co_act if l.is_active else co, l.text[0].upper(), tco_act if l.is_active else tco, tsize*2, True)
        #dr2dr(left, top - offY, size[0], size[1], co_act if l.is_active else co)
        offY += spacing[1] + width

    if self.hover_type == HoverType.LAYER and self.on_hover_layer:
        tail_pos = self.on_hover_layer[1]
        tail_pos[1] += int(self.on_hover_layer[2][1] / 2)
        drtbx(self.on_hover_layer[1][0], self.on_hover_layer[1][1] - int(self.on_hover_layer[2][1] / 2), self.on_hover_layer[2], (.8, .6, .2, 1), self.on_hover_layer[0].text[0].upper(), (1, 1, 1, 1), tsize*2, True)
        #dr2dr(self.on_hover_layer[1][0], self.on_hover_layer[1][1] - int(self.on_hover_layer[2][1] / 2), self.on_hover_layer[2][0], self.on_hover_layer[2][1], (.8, .6, .2, 1))
        glDisable(GL_SCISSOR_TEST)
        dr2dsbr(tail_pos, [11, 4], (0, 0, 0, .8), self.on_hover_layer[0].text, tsize, (1, 1, 1, 1))

        # Draw on hover layer buttons.
        if self.on_hover_layer[0].is_active:
            # color = Color.Tomato()
            for indice in self.on_hover_layer[0].button_indices:
                if indice == -1:
                    break
                b = buttons[indice]
                data = b.get_data_from_view_index(active_view)
                if b.style.shape == RECTANGLE:
                    #dr2drfsc (
                    #    data.pos[0] + ox, data.pos[1] + oy,
                    #    data.size[0], data.size[1], 1.3, color
                    #)
                    dr2drc (
                        data.pos[0] + ox, data.pos[1] + oy,
                        data.size, (1, 0, 0, 1)
                    )
                else: # CIRCLE
                    #dr2dcls (
                    #    (data.pos[0] + ox, data.pos[1] + oy),
                    #    data.size[0], 32, 1.3, color
                    #)
                    dr2dcs (
                        data.pos[0] + ox, data.pos[1] + oy,
                        data.size[0], (1, 0, 0, 1)
                    )
    else:
        glDisable(GL_SCISSOR_TEST)

    # Draw Status Bar.
    dr2drrb(o[0], o[1], (pk.size[0], statusbar_height), theme.statusbar_bg_color)

    # Draw Menu Bar.
    if pk.mode == PK_Mode.OBJECT():
        self.menu_bar.draw()
    else: # Edit Mode
        self.edit_menu_bar.draw()

    ''' DRAW TOOL BAR : EDIT MODE '''
    if pk.mode == 1:
        self.toolbar.draw()
        
    # Draw scale mark.
    tr = [o[0] + pk.size[0] - 3, o[1] + pk.size[1] - 3]
    dr2dtri(
        (tr[0], tr[1]),
        (tr[0] - 6, tr[1]),
        (tr[0], tr[1] - 6),
        (.9, .9, .9, 1)
    )

    if behind:
        glDisable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)


def draw_buttons(active_view, layers, buttons, ox, oy, text_size):
    # OLD METHOD (by iter scene buttons and check visibility properties):
    #for b in buttons:
    #    if data.can_draw_it():

    # NEW METHOD (by iter active view layer button indices, way more convenient):
    for layer in layers:
        if layer.is_active:
            for indice in layer.button_indices:
                if indice == -1:
                    break
                try:
                    b = buttons[indice]
                    draw_button(ox, oy, b, b.get_data_from_view_index(active_view), b.style, text_size)
                except:
                    print("Button %i in %s is not valid" % (indice, layer.name))

def draw_button(ox, oy, b, data, style, text_size):
    xt = data.pos[0] + ox
    yt = data.pos[1] + oy
    # Draw button.
    if style.shape == RECTANGLE:
        drtbxcrwd (
            xt, yt,
            data.size, data.rotation, style.color,
            b.text, style.text_color, text_size, True, data.depth
        )
        if style.use_icon and style.icon:
            s = min(data.size[0], data.size[1]) * style.icon_scale
            driac(style.icon, xt, yt, s, s)
    elif style.shape == CIRCLE: # CIRCLE
        shading = style.shading
        if shading == 'FLAT':
            if style.use_outline:
                if style.outline_blur:
                    drtcsoutgwd (
                        xt, yt,
                        data.size[0], style.color, style.outline_color,
                        1-style.outline_factor, style.outline_blur,
                        b.text, style.text_color, text_size, True, data.depth
                    )
                else:
                    drtcsoutwd (
                        xt, yt,
                        data.size[0], style.color,
                        style.outline_color, 1-style.outline_factor,
                        b.text, style.text_color, text_size, True, data.depth
                    )
            else:
                drtcswd (
                    xt, yt,
                    data.size[0], style.color,
                    b.text, style.text_color, text_size
                )
            # Icon.
            if style.use_icon and style.icon:
                s = data.size[0] * style.icon_scale
                driac(style.icon, xt, yt, s, s)
        elif shading == 'GRAD':
            drtcsgwd (
                xt, yt,
                data.size[0], style.color,
                style.second_color, style.gradient_type, style.gradient_factor, style.gradient_rotation,
                b.text, style.text_color, text_size, True, data.depth
            )
            # Icon.
            if style.use_icon and style.icon:
                s = data.size[0] * style.icon_scale
                driac(style.icon, xt, yt, s, s)
        elif shading == 'IMG':
            if style.icon:
                driac(style.icon, xt, yt, data.size[0], data.size[1])

    elif style.shape == ROUND_SQUARE:
        dr2dcaaswd(
            xt, yt, data.size[0],
            0.008, style.sharpness_factor, 1.0,
            style.color, data.depth
        )
    else:
        print("WHAT IS THIS BUTTON?")
