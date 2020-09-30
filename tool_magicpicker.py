from mathutils import Vector

from .draw_picker import RECTANGLE, CIRCLE, NONE, TOP, BOTTOM, LEFT, RIGHT
from .pk_ui_tool import MODAL_PASS, MODAL_RUN, MODAL_FINISHED, PK_UI_Tool
from .functions import distance_between
from .draw.fun import  (
    drt, drtcent, drtbxc, drtbxcwd, drtc, drtcs, drtcsg, drtcsout, drtcsoutg,
    dr2drf, dr2drcdep,
    dr2dcsdep, dr2dcsout,
    dr2dcl, _dr2dl_plist, dr2dps,
    dr2fldot
)
# from .draw.gpu_shaders import shader_2d_color_unif
import bgl
import time


class Tool_MagicPicker(PK_UI_Tool):
    def __init__(self, parent = None):
        super().__init__('Magic Picker', parent)
        #self.set_tooltip("Picker some color in your picker image\nand convert it to button.")
        # self.set_icon(PK_UI_Icon.TOOL_SELECTION_TWEAK)
        self.set_char_as_icon('M')

    def init(self, op):
        self.points = []
        op.override_buttons = True
        self.has_selection = True
        self.min_point = Vector((0, 0))
        self.max_point = Vector((0, 0))
        if not hasattr(self, 'buffer'):
            # 4 bytes per pixel (RGBA), 1x1 bitmap
            self.buffer = bgl.Buffer(bgl.GL_FLOAT, [4])

    def exit(self, op):
        self.points.clear()
        op.override_buttons = False
        if hasattr(self, 'buffer'):
            del self.buffer
        del self.min_point
        del self.max_point

    def invoke(self, op, event) -> bool:
        # print(self.buffer.to_list())
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.has_selection = False
                op.ctx_area.tag_redraw()
                self.points.clear()
                mx, my = op.mousePos
                mx += op.ctx_area.x
                my += op.ctx_area.y
                bgl.glReadPixels(int(mx), int(my), 1, 1, bgl.GL_RGBA, bgl.GL_FLOAT, self.buffer)
                self.get_picked_color_area(mx, my)
                off = Vector((op.ctx_area.x, op.ctx_area.y))
                for p in self.points:
                    p -= off
                self.has_selection = True
                op.ctx_area.tag_redraw()
                return True
            #if event.value == 'RELEASE':
            #    self.has_selection = False
            #    op.ctx_area.tag_redraw()
        return False

    def modal(self, op, event) -> int:
        return MODAL_FINISHED
        '''
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MODAL_FINISHED
        self.has_selection = False
        op.ctx_area.tag_redraw()
        mx, my = op.mousePos
        mx += op.ctx_area.x
        my += op.ctx_area.y
        bgl.glReadPixels(int(mx), int(my), 1, 1, bgl.GL_RGBA, bgl.GL_FLOAT, self.buffer)
        self.get_picked_color_area(mx, my)
        self.has_selection = True
        op.ctx_area.tag_redraw()
        return MODAL_PASS
        '''

    def draw_callback(self, op, *args, **kwargs):
        if self.has_selection:
            size = self.max_point - self.min_point
            #dr2fldot(
            #    self.min_point[0], self.min_point[1],
            #    size[0], size[1],
            #    (1, 1, 0, 1), 2, .3
            #)
            #off_x = op.ctx_area.x
            #off_y = op.ctx_area.y
            #dr2drf(
            #    self.min_point[0]-off_x, self.min_point[1]-off_y,
            #    size[0], size[1],
            #    (1, 1, 0, 1)
            #)
            if not self.points:
                return
            #off = Vector((off_x, off_y))
            points = []
            for idx in range(0, len(self.points) - 1):
                points.append(self.points[idx])
                points.append(self.points[idx+1])

            points.append(self.points[-1])
            points.append(self.points[0])

            _dr2dl_plist(
                (0, 1, 1, 1),
                points
            )
            #dr2dps(
            #    (0, 1, 1, 1), *self.points
            #)
        #if self.buffer:
        #    co = self.buffer.to_list()
        #    co[3] = 1.0
        #    dr2dcsout(
        #        op.mousePos[0] + 5, op.mousePos[1] + 5, 5, co, (0, 0, 0, 1), .75
        #    )

    # TODO: IMPROVE THIS MODE, COLLAPSE TO FUNCTIONS ETC... MAKE IT SIMPLE.
    def get_picked_color_area(self, ox, oy):
        start_time = time.time()
        co = self.buffer.to_list()[:3]
        co[0] = round(co[0], 2)
        co[1] = round(co[1], 2)
        co[2] = round(co[2], 2)
        #print(co)

        def equal(_next_co):
            # return co == _next_co
            return (
                abs(co[0] - _next_co[0]) < 0.1 and
                abs(co[1] - _next_co[1]) < 0.1 and
                abs(co[2] - _next_co[2]) < 0.1
            )

        def read(_x, _y):
            bgl.glReadPixels(int(_x), int(_y), 1, 1, bgl.GL_RGBA, bgl.GL_FLOAT, self.buffer)
            _co = self.buffer.to_list()[:3]
            _co[0] = round(_co[0], 2)
            _co[1] = round(_co[1], 2)
            _co[2] = round(_co[2], 2)
            #print(_co)
            return _co

        def move(_x, _y, _hor=1, _vert=1):
            return _x+_hor, _y+_vert

        for i in range(0, 10):
            min_x = ox*1
            min_y = oy*1
            max_x = ox*1
            max_y = oy*1

            next_co = co

            # Origin to Right.
            ok = True
            x = ox*1
            y = oy*1
            while ok:
                x, y = move(x, y, 2, 0)
                next_co = read(x, y)
                if equal(next_co):
                    max_x += 2
                else:
                    ok = False
                    #print("* Next *")

            # dist_o_r = distance_between((ox, oy), (x, y))

            # Origin to Left.
            ok = True
            x = ox*1
            y = oy*1
            while ok:
                x, y = move(x, y, -2, 0)
                next_co = read(x, y)
                if equal(next_co):
                    min_x -= 2
                else:
                    ok = False
                    #print("* Next *")

            # dist_o_l = distance_between((ox, oy), (x, y))

            # Origin to Top.
            ok = True
            x = ox*1
            y = oy*1
            while ok:
                x, y = move(x, y, 0, 2)
                next_co = read(x, y)
                if equal(next_co):
                    max_y += 2
                else:
                    ok = False
                    #print("* Next *")

            # dist_o_t = distance_between((ox, oy), (x, y))

            # Origin to Bottom.
            ok = True
            x = ox*1
            y = oy*1
            while ok:
                x, y = move(x, y, 0, -2)
                next_co = read(x, y)
                if equal(next_co):
                    min_y -= 2
                else:
                    ok = False
                    #print("* Next *")

            # dist_o_b = distance_between((ox, oy), (x, y))

            self.min_point = Vector((min_x, min_y))
            self.max_point = Vector((max_x, max_y))

            c = (self.min_point + self.max_point) / 2.0
            ox, oy = c

        def PerpendicularClockwise(vector2: Vector) -> Vector:
            return Vector((vector2.y, -vector2.x))

        def PerpendicularCounterClockwise(vector2: Vector) -> Vector:
            return Vector((-vector2.y, vector2.x))

        # Dimensions.
        width  = self.max_point[0] - self.min_point[0]
        height = self.max_point[1] - self.min_point[1]
        half_width  = int(width  / 2)
        half_height = int(height / 2)

        # Rectangle MidPoints.
        L = self.min_point + Vector((0, half_height))
        B = self.min_point + Vector((half_width, 0))
        R = self.max_point - Vector((0, half_height))
        T = self.max_point - Vector((half_width, 0))

        # Diagonal MidPoints. (rombo)
        MLB = (L + B) / 2.0
        MBR = (B + R) / 2.0
        MRT = (R + T) / 2.0
        MTL = (T + L) / 2.0

        # This indicate the direction.
        # positive: outside ; negative: inside.
        n_dir_MLB = 1 if equal(read(int(MLB.x), int(MLB.y))) else -1
        n_dir_MBR = 1 if equal(read(int(MBR.x), int(MBR.y))) else -1
        n_dir_MRT = 1 if equal(read(int(MRT.x), int(MRT.y))) else -1
        n_dir_MTL = 1 if equal(read(int(MTL.x), int(MTL.y))) else -1

        # Normalized normals from diagonal MidPoints.
        n_MLB = PerpendicularCounterClockwise(L - B).normalized() * n_dir_MLB
        n_MBR = PerpendicularCounterClockwise(B - R).normalized() * n_dir_MBR
        n_MRT = PerpendicularCounterClockwise(R - T).normalized() * n_dir_MRT
        n_MTL = PerpendicularCounterClockwise(T - L).normalized() * n_dir_MTL

        # Function to iter.
        def get_point(_ox, _oy, _move_x, _move_y, _move_step=2):
            if _move_x == 0 and _move_y == 0:
                return Vector((_ox, _oy))
            ok = True
            _x = _ox# + ox
            _y = _oy# + oy
            while ok:
                _x, y = move(_x, _y, _move_x*_move_step, _move_y*_move_step)
                new_co = read(int(_x), int(_y))
                #print("X:%i Y:%i" % (int(_x), int(_y)))
                #print("Color:", new_co)
                if not equal(new_co):
                    ok = False
            return Vector((_x, _y))

        # Append LEFT point.
        self.points.append(L)

        # Calc LEFT-BOTTOM corner point.
        self.points.append(get_point(MLB.x, MLB.y, n_MLB.x, n_MLB.y, 2))# + c)

        # Add BOTTOM point.
        self.points.append(B)

        # Calc BOTTOM-RIGHT corner point.
        self.points.append(get_point(MBR.x, MBR.y, n_MBR.x, n_MBR.y, 2))# + c)

        # Add RIGHT point.
        self.points.append(R)

        # Calc RIGHT-TOP point.
        self.points.append(get_point(MRT.x, MRT.y, n_MRT.x, n_MRT.y, 2))# + c)

        # Add TOP point.
        self.points.append(T)

        # Calc TOP-LEFT corner point.
        self.points.append(get_point(MTL.x, MTL.y, n_MTL.x, n_MTL.y, 2))# + c)

        # Append LEFT point to close the loop.
        #self.points.append(L)

        #for p in self.points:
        #    print(p.x, p.y)

        print("Tiempo:", time.time() - start_time)
