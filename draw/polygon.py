from gpu_extras.batch import batch_for_shader
import bgl

from .gpu_shaders import (
    gps2gen, shader_2d_color_unif, gps2gendep
)
from .rectangle_req import (
    sgeo2ridx, sgeo2rpts, _sgeo2rpts, sgeo2rcpts,
    sgeo2rr2idx, sgeo2rr2pts,
    sgeo2rr2idxbot, sgeo2rr2ptsbot,
    sgeo2rr3idx, sgeo2rr3pts,
    sgeo2rr3idxbot, sgeo2rr3ptsbot,
    sgeo2rr3idxtop, sgeo2rr3ptstop
)
from .triangle_req import triangle_indices
from .primitives import dr2dl
from ..functions import rotate_point_around_point


def dr2dt(_p1, _p2, _p3, _color = (0, 0.5, 0.5, 1.0), _shader = gps2gen):
    batch = batch_for_shader(_shader, 'TRIS', {"pos": (_p1, _p2, _p3)}, indices=triangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # transparency
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # transparency

def dr2ds(_center, _radius, _color = [0, 0.5, 0.5, 1.0], _shader = gps2gen):
    _radius_x2 = _radius * 2
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": _sgeo2rpts(
                                 _center[0] - _radius,
                                 _center[1] - _radius,
                                 _radius_x2,
                                 _radius_x2)
                              },
                             indices=sgeo2ridx)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete

def dr2dr(_posX, _posY, _width, _height, _color = [0, 0.5, 0.5, 1.0], _shader = gps2gen):
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": _sgeo2rpts(_posX, _posY, _width, _height)},
                             indices=sgeo2ridx)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete

def dr2drUniform(_posX, _posY, _width, _height, _color = [0, 0.5, 0.5, 1.0], _shader = shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": _sgeo2rpts(_posX, _posY, _width, _height)},
                             indices=sgeo2ridx)
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

def dr2drc(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0],
                             _shader = gps2gen):
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": sgeo2rcpts(_posX, _posY, _size)},
                             indices=sgeo2ridx)
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete

def dr2drc_WithDepth(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], _depth = 1,
                             _shader = gps2gendep):
    bgl.glEnable(bgl.GL_DEPTH_TEST) # TODO: delete
    bgl.glDepthFunc(bgl.GL_LESS) # TODO: improve
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete

    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": sgeo2rcpts(_posX, _posY, _size)},
                             indices=sgeo2ridx)
    _shader.bind()
    _shader.uniform_float("depth", _depth)
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

    bgl.glDisable(bgl.GL_BLEND) # TODO: delete
    bgl.glDisable(bgl.GL_DEPTH_TEST) # TODO: delete

def dr2drc_Rotate_WithDepth(_posX, _posY, _size, _angle, _color = [0, 0.5, 0.5, 1.0], _depth = 1,
                             _shader = gps2gendep):
    points = sgeo2rcpts(_posX, _posY, _size)

    if _angle != 0:
        for i, p in enumerate(points):
            points[i] = rotate_point_around_point(_posX, _posY, p, _angle)

    bgl.glEnable(bgl.GL_DEPTH_TEST) # TODO: delete
    bgl.glDepthFunc(bgl.GL_LESS) # TODO: improve
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete

    batch = batch_for_shader(_shader, 'TRIS',
                             {"pos": points},
                             indices=sgeo2ridx)
    _shader.bind()
    _shader.uniform_float("depth", _depth)
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

    bgl.glDisable(bgl.GL_BLEND) # TODO: delete
    bgl.glDisable(bgl.GL_DEPTH_TEST) # TODO: delete

def dr2drf(_x, _y, _width, _height, _color = [0, 0.5, 0.5, 1.0]):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    dr2dl(_color,
                  A, B,
                  B, D,
                  D, C,
                  C, A)

def dr2drfsc(_x, _y, _width, _height, _line_thickness=2, _color = [0, 0.5, 0.5, 1.0]):
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(_line_thickness)
    A = (_x-_width, _y-_height)
    B = (_x-_width, _y+_height)
    C = (_x+_width, _y-_height)
    D = (_x+_width, _y+_height)
    dr2dl(_color,
                  A, B,
                  B, D,
                  D, C,
                  C, A)
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)

def dr2drr(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], _subdivs = 2, radius = 8,
                              shader = gps2gen):
    _width, _height = _size
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius
    if _subdivs == 1:
        _vertices = sgeo2rr2pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr2idx
        #if use_shadow:
        #    p1 = [_vertices[2][0], _vertices[2][1] - 1]
        #    p2 = [_vertices[3][0], _vertices[3][1] - 1]
        #    Draw_2D_Line(p1, p2, (.22, .22, .22, .9))
    else:
        _vertices = sgeo2rr3pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr3idx
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

def dr2drr_2(_posX, _posY, _width, _height, _color = [0, 0.5, 0.5, 1.0], _subdivs = 2, radius = 8,
                                shader = gps2gen):
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius
    if _subdivs == 1:
        _vertices = sgeo2rr2pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr2idx
        #if use_shadow:
        #    p1 = [_vertices[2][0], _vertices[2][1] - 1]
        #    p2 = [_vertices[3][0], _vertices[3][1] - 1]
        #    Draw_2D_Line(p1, p2, (.22, .22, .22, .9))
    else:
        _vertices = sgeo2rr3pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr3idx
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

def dr2drrf(_x, _y, _width, _height, _radius, _color = [0, 0.5, 0.5, 1.0]):
    p = sgeo2rr3pts(_x, _y, _width, _height, _radius)
    dr2dl(_color,
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

def dr2drrt(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], radius = 8,
                                  shader = gps2gen):
    _width, _height = _size
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius

    _vertices = sgeo2rr3ptstop(_posX, _posY, _width, _height, radius)

    batch = batch_for_shader(shader, 'TRIS', {"pos":_vertices}, indices=sgeo2rr3idxtop)
    shader.bind()
    shader.uniform_float("color", _color)
    # bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(shader)
    # bgl.glDisable(bgl.GL_BLEND) # TODO: delete

def dr2drrb(_posX, _posY, _size, _color = [0, 0.5, 0.5, 1.0], radius = 8,
                                     shader = gps2gen):
    _width, _height = _size
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius

    _vertices = sgeo2rr3ptsbot(_posX, _posY, _width, _height, radius)

    batch = batch_for_shader(shader, 'TRIS', {"pos":_vertices}, indices=sgeo2rr3idxbot)
    shader.bind()
    shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND) # TODO: delete
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND) # TODO: delete
