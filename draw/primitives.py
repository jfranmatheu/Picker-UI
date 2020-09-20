from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_circle_2d
from bgl import glEnable, glDisable, GL_BLEND, glLineWidth, GL_LINE_SMOOTH, GL_ALIASED_LINE_WIDTH_RANGE

from .gpu_shaders import shader_2d_color_unif, shader_2d_line_dotted, shader_2d_line_dotted_multi


def Draw_2D_Point(_pos, _color = (0, 0, 0, .8), _shader = shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [_pos]})
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)


# Batching saver ♥.
def Draw_2D_Points(_color = (0, 0, 0, .8), *_points):
    batch = batch_for_shader(shader_2d_color_unif, 'POINTS', {"pos": list(_points)})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float("color", _color)
    batch.draw(shader_2d_color_unif)


def Draw_2D_Line(_p1, _p2, _color = (0, 0, 0, .8), _shader = shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'LINES', {"pos": [_p1, _p2]})
    _shader.bind()
    _shader.uniform_float("color", _color)
    glEnable(GL_BLEND)
    batch.draw(_shader)
    glDisable(GL_BLEND)


# Batching saver ♥.
def Draw_2D_Lines(_color = (0, 0, 0, .8), *_points):
    batch = batch_for_shader(shader_2d_color_unif, 'LINES', {"pos": list(_points)})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float("color", _color)
    glEnable(GL_BLEND)
    batch.draw(shader_2d_color_unif)
    glDisable(GL_BLEND)

def Draw_2D_Lines_ByPointList(_color, _point_list):
    if not _point_list:
        return
    points = []
    for idx in range(0, len(_point_list) - 1):
        points.append(_point_list[idx])
        points.append(_point_list[idx+1])
    points.append(_point_list[0])
    # [_point_list[idx], _point_list[idx+1] for idx in range(0, len(_point_list) - 1)]
    batch = batch_for_shader(shader_2d_color_unif, 'LINES', {"pos": points})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float("color", _color)
    glEnable(GL_BLEND)
    batch.draw(shader_2d_color_unif)
    glDisable(GL_BLEND)

def Draw_2D_Lines_FromPointList(_color, _point_list):
    batch = batch_for_shader(shader_2d_color_unif, 'LINES', {"pos": _point_list})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float("color", _color)
    glEnable(GL_BLEND)
    batch.draw(shader_2d_color_unif)
    glDisable(GL_BLEND)


def Draw_2D_Circle_Line(_center, _radius, _segments = 32, _color = (0, 0, 0, .8)):
    draw_circle_2d(_center, _color, _radius, _segments)


def Draw_2D_Circle_Line_Smooth(_center, _radius, _segments = 32, _line_thickness=2, _color = (0, 0, 0, .8)):
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(_line_thickness)
    draw_circle_2d(_center, _color, _radius, _segments)
    glDisable(GL_BLEND)
    glDisable(GL_LINE_SMOOTH)
    glLineWidth(_line_thickness)

# 1.3
def Draw_2D_Line_Dotted(_p1, _p2, _color, _width=2, _factor=.3, shader=shader_2d_line_dotted):
    glLineWidth(_width)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"position": [_p1, _p2]})
    shader.bind()
    shader.uniform_float("color", _color)
    shader.uniform_float("factor", _factor)
    glEnable(GL_BLEND)
    batch.draw(shader)
    glDisable(GL_BLEND)
    glLineWidth(1.0)

def Draw_2D_Line_Dotted_MultiColor(_p1, _p2, _color1, _color2, _width=2, _factor=.3, shader=shader_2d_line_dotted_multi):
    glLineWidth(_width)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"position": [_p1, _p2]})
    shader.bind()
    shader.uniform_float("color_1", _color1)
    shader.uniform_float("color_2", _color2)
    shader.uniform_float("factor", _factor)
    glEnable(GL_BLEND)
    batch.draw(shader)
    glDisable(GL_BLEND)
    glLineWidth(1.0)


def Draw_2D_Lines_Dotted(_color, _width=2, _factor=.3, *_points):
    glLineWidth(_width)
    batch = batch_for_shader(shader_2d_line_dotted, 'LINE_STRIP', {"position": list(_points)})
    shader_2d_line_dotted.bind()
    shader_2d_line_dotted.uniform_float("color", _color)
    shader_2d_line_dotted.uniform_float("factor", _factor)
    glEnable(GL_BLEND)
    batch.draw(shader_2d_line_dotted)
    glDisable(GL_BLEND)
    glLineWidth(1.0)

def Draw_2D_Lines_Dotted_MultiColor(_color1, _color2, _width=2, _factor=.3, *_points):
    glLineWidth(_width)
    batch = batch_for_shader(shader_2d_line_dotted_multi, 'LINE_STRIP', {"position": list(_points)})
    shader_2d_line_dotted_multi.bind()
    shader_2d_line_dotted_multi.uniform_float("color_1", _color1)
    shader_2d_line_dotted_multi.uniform_float("color_2", _color2)
    shader_2d_line_dotted_multi.uniform_float("factor", _factor)
    glEnable(GL_BLEND)
    batch.draw(shader_2d_line_dotted_multi)
    glDisable(GL_BLEND)
    glLineWidth(1.0)
