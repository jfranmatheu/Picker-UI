from mathutils import Vector
from math import cos, sin


class Line:
    def __init__(self, x0=0, y0=0, x1=0, y1=0):
        self.A = Vector((x0, y0))
        self.B = Vector((x1, y1))


class Rect:
    def __init__(self, x0=0, y0=0, x1=0, y1=0, second_as_size=False):
        if second_as_size:
            self.width = x1
            self.height = y1
            x1 += x0
            y1 += y0
        else:
            self.width = x1 - x0
            self.height = y1 - y0
        # NOTE: binary style.
        self.A = Vector((x0, y0))
        self.B = Vector((x0, y1))
        self.C = Vector((x1, y0))
        self.D = Vector((x1, y1))

    def get_bounds(self):
        return [self.A, self.B, self.C, self.D]


class RectSimple:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.pos = Vector((x, y)) # Bottom-left corner.
        self.size = Vector((w, h))

    def set_pos(self, x, y):
        self.pos = Vector((x, y))

    def set_size(self, w, h):
        self.size = Vector((w, h))

class RectFrame:
    def __init__(self, x0=0, y0=0, x1=0, y1=0):
        self.Bottom = Line(x0, y0, x1, y0)
        self.Top = Line(x0, y1, x1, y1)
        self.Left = Line(x0, y0, x0, y1)
        self.Right = Line(x1, y0, x1, y1)


# TODO: option for unitary circle.
# TODO: option to not add center to points coords (in case circle pos change).
class Circle:
    def __init__(self, x=0, y=0, radius=0, num_segments=0):
        self.center = Vector((x, y))
        self.radius = radius
        self.num_segments = num_segments
        self.points = []
        self.calc_points()

    def calc_points(self):
        angle = 360.0 / float(self.num_segments)
        angle_inc = angle * 1
        for k in range(0, self.num_segments):
            self.points.append(
                Vector((self.center[0] + (self.radius * cos(angle)), self.center[1] + (self.radius * sin(angle))))
            )
            angle += angle_inc
