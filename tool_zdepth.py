from mathutils import Vector

from .draw_picker import RECTANGLE, CIRCLE, NONE, TOP, BOTTOM, LEFT, RIGHT
from .pk_ui_tool import MODAL_PASS, MODAL_RUN, MODAL_FINISHED, PK_UI_Tool
from .functions import distance_between
from .draw.fun import  (
    drt, drtcent,
    drtbxc, drtbxcwd,
    drtc, drtcs, drtcsg,
    drtcsout, drtcsoutg,
    dr2drf, dr2drcdep,
    dr2dcsdep,
    dr2dcls
)
# from .draw.gpu_shaders import shader_2d_color_unif


class Tool_ZDepth(PK_UI_Tool):
    def __init__(self, parent = None):
        super().__init__('Z Depth', parent)
        #self.set_tooltip("Change active button's Z depth")
        # self.set_icon(PK_UI_Icon.TOOL_SELECTION_TWEAK)
        self.set_char_as_icon('Z')

    def init(self, op):
        self.z_value = 0.0
        self.prev_mousePos = Vector((0, 0))
        self.b_data = None
        op.override_buttons = True

    def exit(self, op):
        op.override_buttons = False

    def invoke(self, op, event) -> bool:
        # CHECK IF WE CLICKED ACTUAL HOVERED BUTTON.
        b_data = op.on_click_hovered_button(event)
        if b_data:
            self.z_value = b_data.depth
            self.prev_mousePos = op.mousePos
            self.b_data = b_data
            return True
        return False

    def modal(self, op, event) -> int:
        # We are using out tool.
        if op.active_button and self.b_data: # self.hover_type == HoverType.BUTTON
            op.ctx_area.tag_redraw()

            # Change z depth value based on distance.
            dist = distance_between(self.prev_mousePos, op.mousePos)
            if dist > 2:
                dir = 1.0 if op.mousePos[0] - self.prev_mousePos[0] > 0 else -1.0
                self.prev_mousePos = op.mousePos
                if event.shift:
                    dir *= .5
                elif event.ctrl:
                    dir *= 5
                # new_value = (dist * dir) / 10.0
                self.b_data.depth += dir #max(100.0, min(0.0, dist / 10))

            if event.type == 'LEFTMOUSE':
                if event.value == 'RELEASE':
                    self.b_data = None
                    return MODAL_FINISHED
                return MODAL_RUN
            elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
                self.b_data.depth = self.z_value
                self.b_data = None
                return MODAL_FINISHED
        return MODAL_PASS

    def draw_callback(self, op, *args, **kwargs):
        active_scene = op.picker.get_active_scene()
        _args = args[0]
        text_size = op.picker.theme.button_text_size
        ox = _args[0]
        oy = _args[1]

        self.draw_buttons(active_scene.active_view, active_scene.get_active_view().layers, active_scene.buttons, ox, oy, text_size)

        if self.b_data:
            depth = round(self.b_data.depth, 2)
            x, y = self.b_data.pos
            drtbxc(
                ox+x, oy+y, self.b_data.size, (1, 1, 1, 0), str(depth), (0, 0, 0, 1), text_size
            )
        if op.on_hover_button:
            b = op.on_hover_button
            data = b.get_data_from_view_index(active_scene.active_view)
            x, y, w, h = data.get_real_pos_size()
            if b.style.shape == RECTANGLE:
                dr2drf(
                    x+ox, y+oy, w, h, (0, 1, 1, 1)
                )
            else:
                dr2dcls(
                    (data.pos[0]+ox, data.pos[1]+oy), data.size[0], 32, 2.0, (0, 1, 1, 1)
                )
            depth = round(data.depth, 2)
            drtcent(
                data.pos[0]+ox, data.pos[1]+oy, str(depth), text_size, (0, 1, 1, 1), True
            )

    def draw_buttons(self, active_view, layers, buttons, ox, oy, text_size):
        # for b in buttons:
        # data = b.get_data_from_view_index(active_view)
        for layer in layers:
            if layer.is_active:
                for indice in layer.button_indices:
                    if indice == -1:
                        break
                    b = buttons[indice]
                    data = b.get_data_from_view_index(active_view)
                    style = b.style

                    c = 1.0 - (data.depth / 100.0)
                    color = (c, c, c, 1.0)
                    # t = 1.0 if c < 0.5 else 0.0
                    # t_color = (t, t, t, 1.0)
                    # Draw button.
                    # drtbx(data.pos[0] + ox, data.pos[1] + oy, data.size, b.style.color, b.text, b.style.text_color, text_size, True)
                    if style.shape == RECTANGLE:
                        dr2drcdep(
                            data.pos[0] + ox, data.pos[1] + oy,
                            data.size, color, data.depth
                        )
                    else: # CIRCLE
                        dr2dcsdep (
                                data.pos[0] + ox, data.pos[1] + oy,
                                data.size[0], color, data.depth
                            )
