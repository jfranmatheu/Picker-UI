from mathutils import Vector

from .pk_character import PK_Character
from .pk_ui_icon import PK_UI_Icon
from .pk_ui_tool import PK_UI_Tool
from .utils.colors import ColorsRGBA as Color
from .draw.fun import  (
    dr2drc, dr2ds, dr2drf, dr2drfsc,
    dr2dc, dr2dcs, dr2dcaaswd,
    drtbxc, drtbxcwd, drt,
    drtbxcrwd,
    drtc, drtcswd, drtcsgwd,
    drtcsoutwd, drtcsoutgwd,
    dr2dcl, dr2dp, dr2dps, dr2dcls,
    dr2fldot, dr2fldotmul
)
from .draw_picker import RECTANGLE, CIRCLE, ROUND_SQUARE, NONE, TOP, BOTTOM, LEFT, RIGHT
from .pk_ui_tool import MODAL_PASS, MODAL_RUN, MODAL_FINISHED
from .functions import point_inside_rect


class Tool_SelectTweak(PK_UI_Tool):
    def __init__(self, parent: PK_Character = None):
        super().__init__('Tweak', parent)
        #self.set_tooltip('Select and activate items. \nUse it to quickly move and scale')
        self.set_icon(PK_UI_Icon.TOOL_SELECTION_TWEAK)

    def invoke(self, op, event) -> bool:
        # CHECK IF WE CLICKED ACTUAL HOVERED BUTTON.
        b_data = op.on_click_hovered_button(event)
        if b_data:
            op.initial_pos = [b_data.pos[0], b_data.pos[1]] # pos == center
            if op.scaling_from != None:
                print("Start Scaling Button...")
                op.scaling = True
                op.initial_size = [b_data.size[0], b_data.size[1]] # size == 'radius'
            else:
                print("Start Moving Button...")
                op.moving = True
                op.offset = op.mousePos - Vector((b_data.pos[0], b_data.pos[1]))
                # Make button transparent and save color to temp dict.
                op.temp_button_props['color'] = tuple(op.active_button.style.color)
                op.temp_button_props['text_color'] = tuple(op.active_button.style.text_color)
                op.active_button.style.color = Color.TRANSPARENT()
                op.active_button.style.text_color = Color.TRANSPARENT()
            return True
        return False

    def cancel(self, op):
        self.back_up(op)
        d = op.active_button.get_data_from_view_index(op.active_view_index)
        if op.scaling:
            d.pos = op.initial_pos
            d.size = op.initial_size
            op.scaling = False
        elif op.moving:
            d.pos = op.initial_pos
            op.moving = False
        op.active_button = None
    
    def back_up(self, op):
        # Back-Up properties data if available.
        if op.temp_button_props:
            style = op.active_button.style
            for key in op.temp_button_props.keys():
                if hasattr(style, key):
                    setattr(style, key, op.temp_button_props[key])
            op.temp_button_props.clear()

    def modal(self, op, event) -> int:
        # We are using out tool.
        if op.active_button: # self.hover_type == HoverType.BUTTON
            if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
                self.cancel(op)
                return MODAL_FINISHED
            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                if op.moving or op.scaling:
                    self.back_up(op)
                    d = op.active_button.get_data_from_view_index(op.active_view_index)
                    fx, fy = d.factor
                    x, y = d.pos

                    # print("Original Pos:", list(op.initial_pos))
                    # print("Original Factor:", list(d.factor))
                    d.factor = [
                        fx * x / op.initial_pos[0] if op.initial_pos[0] != 0 else 0,
                        fy * y / op.initial_pos[1] if op.initial_pos[1] != 0 else 0
                    ]
                    # print("New Pos:", list(d.pos))
                    # print("New Factor:", list(d.factor))

                    op.moving = False
                    op.scaling = False
                    print("Stop Moving/Scaling Button...")
                return MODAL_FINISHED
            elif op.moving:
                op.move_button()
                op.ctx_area.tag_redraw()
            elif op.scaling:
                op.scale_button(event)
                op.ctx_area.tag_redraw()
        return MODAL_PASS

    def draw_callback(self, op, *args, **kwargs):
        # Draw Active Button. (if available aka when clicking on some)
        if op.on_hover_button:
            #print("ARGS:", args)
            _args = args[0]
            text_size = op.picker.theme.button_text_size
            ox = _args[0]
            oy = _args[1]
            data = op.on_hover_button.get_data_from_view_index(op.active_view_index)
            xt = data.pos[0] + ox
            yt = data.pos[1] + oy
            w, h = data.size
            style = op.on_hover_button.style
            shape = style.shape

            # TODO: GHOST MODE
            if op.ghost_mode:
                if op.moving or op.scaling:
                    if shape == RECTANGLE:
                        dr2drc(xt, yt, data.size, (1, 1, 1, .07))
                    elif shape == CIRCLE:
                        #w2 = w/2
                        dr2dcs(xt, yt, w, (1, 1, 1, .07))
                        dr2dcls((xt, yt), w, 32, 1.3, (1, 1, 1, 1))
                    else:
                        dr2dcaaswd(
                            xt, yt, w,
                            0.008, .8, 1.0,
                            (1, 1, 1, .2), 1.0
                        )
                        dr2drfsc(
                            xt, yt, w, w, 2, (1, 1, 1, .07)
                        )
                    dr2ds((xt, yt), 2, (1, 1, 1, 1))
                else:
                    if shape == RECTANGLE:
                        dr2drc(xt, yt, data.size, (1, 1, 1, .2))
                    elif shape == CIRCLE:
                        #w2 = w/2
                        dr2dcs(xt, yt, w, (1, 1, 1, .2))
                        dr2dcls((xt, yt), w, 32, 1.3, (1, 1, 1, 1))
                    else:
                        dr2dcaaswd(
                            xt, yt, w,
                            0.008, style.sharpness_factor, 1.0,
                            style.color_on_hover, 1.0
                        )
                        dr2drfsc(
                            xt, yt, w, w, 2, (1, 1, 1, 1)
                        )
                    dr2ds((xt, yt), 1, (1, 1, 1, 1))
            else:
                shading = style.shading
                if shape == RECTANGLE:
                    drtbxcrwd (
                        xt, yt, data.size, data.rotation, style.color_on_hover,
                        op.on_hover_button.text, style.text_color_on_hover, text_size, True, data.depth
                    )
                elif style.shape == CIRCLE:
                    if shading == 'FLAT':
                        if style.use_outline:
                            if style.outline_blur:
                                drtcsoutgwd (
                                    xt, yt,
                                    w, style.color_on_hover, style.outline_color,
                                    1-style.outline_factor, style.outline_blur,
                                    op.on_hover_button.text, style.text_color_on_hover, text_size, True, data.depth
                                )
                            else:
                                drtcsoutwd (
                                    xt, yt,
                                    w, style.color_on_hover,
                                    style.outline_color, 1-style.outline_factor,
                                    op.on_hover_button.text, style.text_color_on_hover, text_size, True, data.depth
                                )
                        else:
                            drtcswd (
                                xt, yt, w, style.color_on_hover,
                                op.on_hover_button.text, style.text_color_on_hover, text_size, True, data.depth
                            )
                    elif shading == 'GRAD':
                        drtcsgwd (
                            xt, yt,
                            w, style.color_on_hover,
                            style.second_color, style.gradient_type, style.gradient_factor, style.gradient_rotation,
                            op.on_hover_button.text, style.text_color_on_hover, text_size, True, data.depth
                        )
                    elif shading == 'IMG':
                        pass
                elif style.shape == ROUND_SQUARE:
                    dr2dcaaswd(
                        xt, yt, w,
                        0.008, style.sharpness_factor, 1.0,
                        style.color_on_hover, data.depth
                    )
                    dr2drfsc(
                        xt, yt, w, w, 2, (1, 1, 1, .07)
                    )

            # Get real coordinates and size.
            # x, y, w, h = data.get_real_pos_size()
            xt -= w
            yt -= h
            w *= 2
            h *= 2

            # Draw frame and control points for scaling.
            if shape == RECTANGLE:
                dr2drf(xt, yt, w, h, (1, 1, 1, 1))
            elif shape == CIRCLE:
                w2 = w/2
                dr2dcls((xt+w2, yt+w2), w2, 32, 1.3, (1, 1, 1, 1))
            #else:
            #    dr2drfsc(
            #        xt, yt, w, w, 2, (1, 1, 1, 1)
            #    )

            if op.scaling_from != NONE:
                sep = 2
                b = (xt + int(w / 2), yt - sep)
                t = (xt + int(w / 2), yt + h + sep)
                l = (xt - sep, yt + int(h / 2))
                r = (xt + w + sep, yt + int(h / 2))

                if not op.scaling:
                    dr2dps((0, 0, 0, 1), b, t, l, r)

                if op.scaling_from == BOTTOM:
                    dr2dp(b, Color.Cyan())
                elif op.scaling_from == TOP:
                    dr2dp(t, Color.Cyan())
                elif op.scaling_from == LEFT:
                    dr2dp(l, Color.Cyan())
                elif op.scaling_from == RIGHT:
                    dr2dp(r, Color.Cyan())

            elif not op.moving:
                sep = 2
                b = (xt + int(w / 2), yt - sep)
                t = (xt + int(w / 2), yt + h + sep)
                l = (xt - sep, yt + int(h / 2))
                r = (xt + w + sep, yt + int(h / 2))

                dr2dps((0, 0, 0, 1), b, t, l, r)



class Tool_SelectBox(PK_UI_Tool):
    def __init__(self, parent: PK_Character = None):
        super().__init__('Select Box', parent)
        #self.set_tooltip('Select items using box selection')
        self.set_icon(PK_UI_Icon.TOOL_SELECTION_BOX)

        # self.clicked_button = None
        self.selected_buttons = []
        self.box_origin = Vector((0, 0))
        self.box_size = [0, 0]
        self.boxing = False
        self.moving = False
        self.shift = False

    def get_buttons_in_box(self, op):
        self.selected_buttons.clear()

        active_scene = op.picker.get_active_scene()
        if not active_scene:
            return

        active_view = active_scene.active_view
        if active_view == -1:
            return
        
        '''
        ox, oy = op.get_scene_position(True)
        for b in active_scene.buttons:
            b_data = b.get_data_from_view_index(active_view)
            # Get real coordinates and size.
            # x, y, w, h = b_data.get_real_pos_size()
            if point_inside_rect([b_data.pos[0] + ox, b_data.pos[1] + oy], self.box_origin, self.box_size):
                self.selected_buttons.append(b)
        '''
        ox, oy, ow, oh = op.get_view_image_pos_size(active_scene.get_active_view())

        for b in active_scene.buttons:
            # TODO: check if buttons is active and visible...
            x, y, w, h = b.get_data_from_view_index(active_view).get_real_pos_size()
            if point_inside_rect((x + ox, y + oy), self.box_origin, self.box_size):
                self.selected_buttons.append(b)

    def invoke(self, op, event) -> bool:
        if event.type in {'X', 'DEL'}:
            if event.value == 'PRESS':
                if self.selected_buttons:
                    #print(list(self.selected_buttons))
                    self.selected_buttons.sort(key=lambda x: x.index, reverse=True)
                    #print("** SORTED LIST **")
                    #print(list(self.selected_buttons))
                    active_scene = op.picker.get_active_scene()
                    print("BoxSelectTool::remove_selected_buttons")
                    for b in self.selected_buttons:
                        print("*** REMOVE BUTTON: %s - %i ***" % (b.name, b.index))
                        b.remove(active_scene)
                    self.selected_buttons.clear()
            return False
        self.shift = event.shift
        if event.type == 'LEFTMOUSE':
            #clicked_button = op.check_button(event)
            #if event.value == 'CLICK':
            #    self.moving = False
            #    self.boxing = False
            #    if clicked_button:
            #        self.selected_buttons = [clicked_button]
            #    return False
            if event.value == 'PRESS':
                clicked_button = op.check_button(event)
                if clicked_button:
                    print("Select button...")
                    self.moving = False
                    self.boxing = False
                    if self.shift:
                        if clicked_button in self.selected_buttons:
                            self.selected_buttons.remove(clicked_button)
                        else:
                            self.selected_buttons.append(clicked_button)
                    else:
                        self.selected_buttons = [clicked_button]
                    self.shift = False
                    return False
                self.selected_buttons.clear()
                self.box_origin = op.mousePos * 1
                # self.boxing = True
                print("Select box init...")
                #self.boxing = True
                return True
        elif event.type == 'RIGHTMOUSE':
            pass
        return False

    def modal(self, op, event) -> int:
        if self.boxing:
            print("Boxing...")
            self.box_size = op.mousePos - self.box_origin
            self.get_buttons_in_box(op)
            op.ctx_area.tag_redraw()
            #for b in self.selected_buttons:
            #    print("- %s - %i" % (b.name, b.index))
        else:
            if event.type == 'MOUSEMOVE':
                self.boxing = True
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                if self.boxing:
                    print("Select box finished...")
                    self.boxing = False
                    self.box_origin = Vector((0, 0))
                    self.box_size = [0, 0]
            return MODAL_FINISHED
        return MODAL_PASS

    def draw_callback(self, op, *args, **kwargs):
        if self.selected_buttons:
            active_view = op.picker.get_active_scene().active_view
            ox, oy = op.get_scene_position(True)
            for b in self.selected_buttons:
                b_data = b.get_data_from_view_index(active_view)
                if b.style.shape == RECTANGLE:
                    dr2drc(
                        b_data.pos[0] + ox, b_data.pos[1] + oy,
                        b_data.size, (1, 1, 0, 1)
                    )
                else:
                    dr2dcs (
                        b_data.pos[0] + ox, b_data.pos[1] + oy,
                        b_data.size[0], (1, 1, 0, 1)
                    )

        if self.boxing:
            dr2fldotmul(
                self.box_origin[0], self.box_origin[1],
                self.box_size[0], self.box_size[1],
                (.02, .02, .02, 1), (.9, .9, .9, 1),
                2, .3
            )

        if self.shift:
            drt(
                op.mousePos[0] + 4, op.mousePos[1], '+', 12, 0, 1, 1, 1, 1, True
            )
