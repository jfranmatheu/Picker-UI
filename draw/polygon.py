from gpu_extras.batch import batch_for_shader
import bgl

from .gpu_shaders import (
    shader_2d_generic_basic, shader_2d_color_unif, shader_2d_generic_basic_depth
)
from .rectangle_req import (
    rectangle_indices, rectangle_points, rectangle_points_, rectangle_center_points,
    rounded_2_rectangle_indices, rounded_2_rectangle_points,
    rounded_2_rectangle_indices_bottom, rounded_2_rectangle_points_bottom,
    rounded_3_rectangle_indices, rounded_3_rectangle_points,
    rounded_3_rectangle_indices_bottom, rounded_3_rectangle_points_bottom,
    rounded_3_rectangle_indices_top, rounded_3_rectangle_points_top
)
from .triangle_req import triangle_indices
from .primitives import Draw_2D_Lines
from ..functions import rotate_point_around_point


def Draw_2D_Triangle(_p1, _p2, _p3, _color = (0, 0.5, 0.5, 1.0), _shader = shader_2d_generic_basic):
    batch = batch_for_shader(_shader, 'TRIS', {"pos": (_p1, _p2, _p3)}, indices=triangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # transparency
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # transparency


def Draw_2D_Square(_center, _radius, _color = [0, 0.5, 0.5, 1.0], _shader = shader_2d_generic_basic):
    _radius_x2 = _radius * 2
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": rectangle_points_(
                                 _center[0] - _radius,
                                 _center[1] - _radius,
                                 _radius_x2,
                                 _radius_x2)
                              },
                             indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete


def Draw_2D_Rectangle(_posX, _posY, _width, _height, _color = [0, 0.5, 0.5, 1.0], _shader = shader_2d_generic_basic):
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": rectangle_points_(_posX, _posY, _width, _height)},
                             indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete

def Draw_2D_RectangleUniform(_posX, _posY, _width, _height, _color = [0, 0.5, 0.5, 1.0], _shader = shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": rectangle_points_(_posX, _posY, _width, _height)},
                             indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

def Draw_2D_Rectangle_Center(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0],
                             _shader = shader_2d_generic_basic):
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": rectangle_center_points(_posX, _posY, _size)},
                             indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete


def Draw_2D_Rectangle_Center_WithDepth(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], _depth = 1,
                             _shader = shader_2d_generic_basic_depth):
    bgl.glEnable(bgl.GL_DEPTH_TEST) # TODO: delete
    bgl.glDepthFunc(bgl.GL_LESS) # TODO: improve
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete

    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": rectangle_center_points(_posX, _posY, _size)},
                             indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("depth", _depth)
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

    bgl.glDisable(bgl.GL_BLEND) # TODO: delete
    bgl.glDisable(bgl.GL_DEPTH_TEST) # TODO: delete

def Draw_2D_Rectangle_Center_Rotate_WithDepth(_posX, _posY, _size, _angle, _color = [0, 0.5, 0.5, 1.0], _depth = 1,
                             _shader = shader_2d_generic_basic_depth):
    points = rectangle_center_points(_posX, _posY, _size)

    if _angle != 0:
        for i, p in enumerate(points):
            points[i] = rotate_point_around_point(_posX, _posY, p, _angle)

    bgl.glEnable(bgl.GL_DEPTH_TEST) # TODO: delete
    bgl.glDepthFunc(bgl.GL_LESS) # TODO: improve
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete

    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": points},
                             indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("depth", _depth)
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

    bgl.glDisable(bgl.GL_BLEND) # TODO: delete
    bgl.glDisable(bgl.GL_DEPTH_TEST) # TODO: delete


def Draw_2D_Rectangle_Frame(_x, _y, _width, _height, _color = [0, 0.5, 0.5, 1.0]):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    Draw_2D_Lines(_color,
                  A, B,
                  B, D,
                  D, C,
                  C, A)


def Draw_2D_Rectangle_Frame_Smooth_Center(_x, _y, _width, _height, _line_thickness=2, _color = [0, 0.5, 0.5, 1.0]):
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(_line_thickness)
    A = (_x-_width, _y-_height)
    B = (_x-_width, _y+_height)
    C = (_x+_width, _y-_height)
    D = (_x+_width, _y+_height)
    Draw_2D_Lines(_color,
                  A, B,
                  B, D,
                  D, C,
                  C, A)
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)


def Draw_2D_Rectangle_Rounded(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], _subdivs = 2, radius = 8,
                              shader = shader_2d_generic_basic):
    _width, _height = _size
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius
    if _subdivs == 1:
        _vertices = rounded_2_rectangle_points(_posX, _posY, _width, _height, radius)
        _indices = rounded_2_rectangle_indices
        #if use_shadow:
        #    p1 = [_vertices[2][0], _vertices[2][1] - 1]
        #    p2 = [_vertices[3][0], _vertices[3][1] - 1]
        #    Draw_2D_Line(p1, p2, (.22, .22, .22, .9))
    else:
        _vertices = rounded_3_rectangle_points(_posX, _posY, _width, _height, radius)
        _indices = rounded_3_rectangle_indices
        #if use_shadow:
        #    p1 = [_vertices[3][0], _vertices[3][1] - 1]
        #    p2 = [_vertices[4][0], _vertices[4][1] - 1]
        #    Draw_2D_Line(p1, p2, (.22, .22, .22, .9))

    batch = batch_for_shader(shader, 'TRIS', {"pos":_vertices}, indices=_indices)
    shader.bind()
    shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete


def Draw_2D_Rectangle_Rounded_2(_posX, _posY, _width, _height, _color = [0, 0.5, 0.5, 1.0], _subdivs = 2, radius = 8,
                                shader = shader_2d_generic_basic):
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius
    if _subdivs == 1:
        _vertices = rounded_2_rectangle_points(_posX, _posY, _width, _height, radius)
        _indices = rounded_2_rectangle_indices
        #if use_shadow:
        #    p1 = [_vertices[2][0], _vertices[2][1] - 1]
        #    p2 = [_vertices[3][0], _vertices[3][1] - 1]
        #    Draw_2D_Line(p1, p2, (.22, .22, .22, .9))
    else:
        _vertices = rounded_3_rectangle_points(_posX, _posY, _width, _height, radius)
        _indices = rounded_3_rectangle_indices
        #if use_shadow:
        #    p1 = [_vertices[3][0], _vertices[3][1] - 1]
        #    p2 = [_vertices[4][0], _vertices[4][1] - 1]
        #    Draw_2D_Line(p1, p2, (.22, .22, .22, .9))

    batch = batch_for_shader(shader, 'TRIS', {"pos":_vertices}, indices=_indices)
    shader.bind()
    shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete


    # 10     # 9
  # 11         # 8
# 12             # 7
        # 0
# 1             # 6
  # 2         # 5
    # 3     # 4
def Draw_2D_Rectangle_Rounded_Frame(_x, _y, _width, _height, _radius, _color = [0, 0.5, 0.5, 1.0]):
    p = rounded_3_rectangle_points(_x, _y, _width, _height, _radius)
    Draw_2D_Lines(_color,
                  p[1], p[2],
                  p[2], p[3],
                  p[3], p[4],
                  p[4], p[5],
                  p[5], p[6],
                  p[6], p[7],
                  p[7], p[8],
                  p[8], p[9],
                  p[9], p[10],
                  p[10], p[11],
                  p[11], p[12],
                  p[12], p[1]
                  )


def Draw_2D_Rectangle_Rounded_Top(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], radius = 8,
                                  shader = shader_2d_generic_basic):
    _width, _height = _size
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius

    _vertices = rounded_3_rectangle_points_top(_posX, _posY, _width, _height, radius)

    batch = batch_for_shader(shader, 'TRIS', {"pos":_vertices}, indices=rounded_3_rectangle_indices_top)
    shader.bind()
    shader.uniform_float("color", _color)
    # bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(shader)
    # bgl.glDisable(bgl.GL_BLEND) # TODO: delete


def Draw_2D_Rectangle_Rounded_Bottom(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], radius = 8,
                                     shader = shader_2d_generic_basic):
    _width, _height = _size
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius

    _vertices = rounded_3_rectangle_points_bottom(_posX, _posY, _width, _height, radius)

    batch = batch_for_shader(shader, 'TRIS', {"pos":_vertices}, indices=rounded_3_rectangle_indices_bottom)
    shader.bind()
    shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete
