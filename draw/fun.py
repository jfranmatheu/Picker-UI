from gpu_extras.batch import batch_for_shader as bat
from bgl import *
from gpu_extras.presets import draw_circle_2d
from math import radians, cos, sin
from ..functions import rotate_point_around_point
co='color';pos='pos';txco="texCoord";_pos='position';fac='factor';dep='depth'
POINTS='POINTS';LINES='LINES';LINE_STRIP='LINE_STRIP';TRIS='TRIS';TRI_FAN='TRI_FAN'
from blf import (
    enable as text_enable, disable as text_disable,
    SHADOW, shadow as text_shadow, shadow_offset as text_shadow_offset,
    color as text_color, position as text_position, size as text_size,
    dimensions as text_dim, draw as text_draw, ROTATION, rotation as text_rotation,
    clipping as text_clipping, CLIPPING, KERNING_DEFAULT, WORD_WRAP, MONOCHROME
)
from .gpu_shaders import *

# PRIMITIVE
def dr2dp(_pos, _co = (0, 0, 0, .8), s = shader_2d_color_unif):
    b = bat(s, POINTS, {pos: [_pos]})
    s.bind()
    s.uniform_float(co, _co)
    b.draw(s)

# Batching saver ♥.
def dr2dps(_co = (0, 0, 0, .8), *_puntos):
    b = bat(shader_2d_color_unif, POINTS, {pos: list(_puntos)})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float(co, _co)
    b.draw(shader_2d_color_unif)

def dr2dl(_p1, _p2, _co = (0, 0, 0, .8), s = shader_2d_color_unif):
    b = bat(s, LINES, {pos: [_p1, _p2]})
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND)
    b.draw(s)
    glDisable(GL_BLEND)

# Batching saver ♥.
def dr2dls(_co = (0, 0, 0, .8), *_puntos):
    b = bat(shader_2d_color_unif, LINES, {pos: list(_puntos)})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float(co, _co)
    glEnable(GL_BLEND)
    b.draw(shader_2d_color_unif)
    glDisable(GL_BLEND)

def dr2dl_plist(_co, _plist):
    if not _plist:
        return
    points = []
    for idx in range(0, len(_plist) - 1):
        points.append(_plist[idx])
        points.append(_plist[idx+1])
    points.append(_plist[0])
    # [_plist[idx], _plist[idx+1] for idx in range(0, len(_plist) - 1)]
    b = bat(shader_2d_color_unif, LINES, {pos: points})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float(co, _co)
    glEnable(GL_BLEND)
    b.draw(shader_2d_color_unif)
    glDisable(GL_BLEND)

def _dr2dl_plist(_co, _plist):
    b = bat(shader_2d_color_unif, LINES, {pos: _plist})
    shader_2d_color_unif.bind()
    shader_2d_color_unif.uniform_float(co, _co)
    glEnable(GL_BLEND)
    b.draw(shader_2d_color_unif)
    glDisable(GL_BLEND)

def dr2dcl(_c, _r, _segments = 32, _co = (0, 0, 0, .8)):
    draw_circle_2d(_c, _co, _r, _segments)

def dr2dcls(_c, _r, _segments = 32, _line_thickness=2, _co = (0, 0, 0, .8)):
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(_line_thickness)
    draw_circle_2d(_c, _co, _r, _segments)
    glDisable(GL_BLEND)
    glDisable(GL_LINE_SMOOTH)
    glLineWidth(_line_thickness)
# 1.3
def _dr2dldot(_p1, _p2, _co, _width=2, _factor=.3, s=gps2ldot):
    glLineWidth(_width)
    b = bat(s, LINE_STRIP, {_pos: [_p1, _p2]})
    s.bind()
    s.uniform_float(co, _co)
    s.uniform_float(fac, _factor)
    glEnable(GL_BLEND)
    b.draw(s)
    glDisable(GL_BLEND)
    glLineWidth(1.0)

def _dr2dldotmul(_p1, _p2, _color1, _color2, _width=2, _factor=.3, s=gps2ldotmul):
    glLineWidth(_width)
    b = bat(s, LINE_STRIP, {_pos: [_p1, _p2]})
    s.bind()
    s.uniform_float("color_1", _color1)
    s.uniform_float("color_2", _color2)
    s.uniform_float(fac, _factor)
    glEnable(GL_BLEND)
    b.draw(s)
    glDisable(GL_BLEND)
    glLineWidth(1.0)

def dr2dldot(_co, _width=2, _factor=.3, *_puntos):
    glLineWidth(_width)
    b = bat(gps2ldot, LINE_STRIP, {_pos: list(_puntos)})
    gps2ldot.bind()
    gps2ldot.uniform_float(co, _co)
    gps2ldot.uniform_float(fac, _factor)
    glEnable(GL_BLEND)
    b.draw(gps2ldot)
    glDisable(GL_BLEND)
    glLineWidth(1.0)

def dr2dldotmul(_color1, _color2, _width=2, _factor=.3, *_puntos):
    glLineWidth(_width)
    b = bat(gps2ldotmul, LINE_STRIP, {_pos: list(_puntos)})
    gps2ldotmul.bind()
    gps2ldotmul.uniform_float("color_1", _color1)
    gps2ldotmul.uniform_float("color_2", _color2)
    gps2ldotmul.uniform_float(fac, _factor)
    glEnable(GL_BLEND)
    b.draw(gps2ldotmul)
    glDisable(GL_BLEND)
    glLineWidth(1.0)
# PLY
triidx=((0, 1, 2),(0, 0, 0))
from mathutils import Vector
def sgeo2rpts(x, y, s):
    w, h = s
    return [
        (x, y),
        (x+w, y),
        (x, y+h),
        (x+w, y+h)
    ]
def _sgeo2rpts(x, y, w, h):
    return [
        (x, y),
        (x+w, y),
        (x, y+h),
        (x+w, y+h)
    ]
def sgeo2rcpts(x, y, s):
    w, h = s
    return [
        (x-w, y-h),
        (x+w, y-h),
        (x-w, y+h),
        (x+w, y+h)
    ]
def sgeo2rcpts_(x, y, w, h):
    return [
        (x-w, y-h),
        (x+w, y-h),
        (x-w, y+h),
        (x+w, y+h)
    ]
def EvaluateCuadraticBezierCurve(p0, p1, p2, t = .5):
    return (1-t)**2 * p0 + 2*t * (1-t) * p1 + t**2 * p2
def sgeo2rr2pts(x, y, w, h, r):
    return (
        ( x + w / 2     , y + h / 2 ),
        ( x             , y + r ),
        ( x + r         , y ),
        ( x + w - r     , y ),
        ( x + w         , y + r ),
        ( x             , y + h - r ),
        ( x + r         , y + h ),
        ( x + w - r     , y + h ),
        ( x + w         , y + h - r )
    )
def sgeo2rr2ptsbot(x, y, w, h, r):
    return (
        ( x             , y + r ),
        ( x + r         , y ),
        ( x + w - r     , y ),
        ( x + w         , y + r ),
    )
def sgeo2rr3pts(x, y, w, h, r):
    A = EvaluateCuadraticBezierCurve(Vector((x, y + r)), Vector((x, y)), Vector((x + r, y))) # 2 Bot Left mid
    B = EvaluateCuadraticBezierCurve(Vector((x + w - r, y)), Vector((x + w, y)), Vector((x + w, y + r))) # 5 Bot Right mid
    C = EvaluateCuadraticBezierCurve(Vector((x + w - r, y + h)), Vector((x + w, y + h)), Vector((x + w, y + h - r))) # 8 Top Right mid
    D = EvaluateCuadraticBezierCurve(Vector((x, y + h - r)), Vector((x, y + h)), Vector((x + r, y + h))) # 2 Top Left mid
    return (
        ( x + w / 2     , y + h / 2 ),
        ( x             , y + r ),
        ( A[0]          , A[1] ),
        ( x + r         , y ),
        ( x + w - r     , y ),
        ( B[0]          , B[1] ),
        ( x + w         , y + r ),
        ( x + w         , y + h - r ),
        ( C[0]          , C[1] ),
        ( x + w - r     , y + h ),
        ( x + r         , y + h ),
        ( D[0]          , D[1] ),
        ( x             , y + h - r )
    )
def sgeo2rr3ptsbot(x, y, w, h, r):
    A = EvaluateCuadraticBezierCurve(Vector((x, y + r)), Vector((x, y)), Vector((x + r, y))) # 2 Bot Left mid
    B = EvaluateCuadraticBezierCurve(Vector((x + w - r, y)), Vector((x + w, y)), Vector((x + w, y + r))) # 5 Bot Right mid
    return (
        ( x             , y + r ),
        ( A[0]          , A[1] ),
        ( x + r         , y ),
        ( x + w - r     , y ),
        ( B[0]          , B[1] ),
        ( x + w         , y + r ),
        (x + w          , y + h),
        (x              , y + h)
    )
def sgeo2rr3ptstop(x, y, w, h, r):
    C = EvaluateCuadraticBezierCurve(Vector((x + w - r, y + h)), Vector((x + w, y + h)), Vector((x + w, y + h - r))) # 8 Top Right mid
    D = EvaluateCuadraticBezierCurve(Vector((x, y + h - r)), Vector((x, y + h)), Vector((x + r, y + h))) # 2 Top Left mid
    return (
        ( x + w         , y + h - r ),
        ( C[0]          , C[1] ),
        ( x + w - r     , y + h ),
        ( x + r         , y + h ),
        ( D[0]          , D[1] ),
        ( x             , y + h - r ),
        (x              , y),
        (x + w          , y)
    )
sgeo2ridx = (
    ( 0, 1, 2 ),
    ( 2, 1, 3 )
)
sgeo2rr2idx = (
    ( 0,  1,  2 ),
    ( 0,  2,  3 ),
    ( 0,  3,  4 ),
    ( 0,  4,  8 ),
    ( 0,  8,  7 ),
    ( 0,  7,  6 ),
    ( 0,  6,  5 ),
    ( 0,  5,  1 )
)
sgeo2rr2idxbot = (
    ( 3,  1,  2  ),
    ( 3,  0,  1  ),
)
sgeo2rr3idx = (
    ( 0,  1,  2  ),
    ( 0,  2,  3  ),
    ( 0,  3,  4  ),
    ( 0,  4,  5  ),
    ( 0,  5,  6  ),
    ( 0,  6,  7  ),
    ( 0,  7,  8  ),
    ( 0,  8,  9  ),
    ( 0,  9, 10  ),
    ( 0, 10, 11  ),
    ( 0, 11, 12  ),
    ( 0, 12,  1  )
)
sgeo2rr3idxbot = (
    ( 3,  1,  2 ), #
    ( 1,  3,  4 ), #
    ( 1,  4,  5 ),
    ( 0,  1,  5 ),
    ( 0,  5,  6 ),
    ( 0,  6,  7 )
)
sgeo2rr3idxtop = (
    ( 6,  7,  0 ),
    ( 0,  6,  5 ),
    ( 0,  5,  1 ),
    ( 1,  5,  4 ),
    ( 4,  2,  1 ),
    ( 2,  4,  3 )
)
def dr2dt(_p1, _p2, _p3, _co = (0, 0.5, 0.5, 1.0), s = gps2gen):
    b = bat(s, TRIS, {pos: (_p1, _p2, _p3)}, indices=triidx)
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND) # transparency
    b.draw(s)
    glDisable(GL_BLEND) # transparency

def dr2ds(_c, _r, _co = [0, 0.5, 0.5, 1.0], s = gps2gen):
    _rx2 = _r * 2
    b = bat(s, TRIS,
                             {pos: _sgeo2rpts(
                                 _c[0] - _r,
                                 _c[1] - _r,
                                 _rx2,
                                 _rx2)
                              },
                             indices=sgeo2ridx)
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND) # TODO: delete
    b.draw(s)
    glDisable(GL_BLEND) # TODO: delete

def dr2dr(_posX, _posY, _width, _height, _co = [0, 0.5, 0.5, 1.0], s = gps2gen):
    b = bat(s, TRIS,
                             {pos: _sgeo2rpts(_posX, _posY, _width, _height)},
                             indices=sgeo2ridx)
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND) # TODO: delete
    b.draw(s)
    glDisable(GL_BLEND) # TODO: delete

def dr2drUniform(_posX, _posY, _width, _height, _co = [0, 0.5, 0.5, 1.0], s = shader_2d_color_unif):
    b = bat(s, TRIS,
                             {pos: _sgeo2rpts(_posX, _posY, _width, _height)},
                             indices=sgeo2ridx)
    s.bind()
    s.uniform_float(co, _co)
    b.draw(s)

def dr2drc(_posX, _posY, _sz, _co = [0, 0.5, 0.5, 1.0],
                             s = gps2gen):
    glEnable(GL_BLEND) # TODO: delete
    b = bat(s, TRIS,
                             {pos: sgeo2rcpts(_posX, _posY, _sz)},
                             indices=sgeo2ridx)
    s.bind()
    s.uniform_float(co, _co)
    b.draw(s)
    glDisable(GL_BLEND) # TODO: delete

def dr2drcdep(_posX, _posY, _sz, _co = [0, 0.5, 0.5, 1.0], _dep = 1,
                             s = gps2gendep):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glEnable(GL_BLEND) # TODO: delete

    b = bat(s, TRIS,
                             {pos: sgeo2rcpts(_posX, _posY, _sz)},
                             indices=sgeo2ridx)
    s.bind()
    s.uniform_float(dep, _dep)
    s.uniform_float(co, _co)
    b.draw(s)

    glDisable(GL_BLEND) # TODO: delete
    glDisable(GL_DEPTH_TEST) # TODO: delete

def dr2drcrotdep(_posX, _posY, _sz, _angle, _co = [0, 0.5, 0.5, 1.0], _dep = 1,
                             s = gps2gendep):
    points = sgeo2rcpts(_posX, _posY, _sz)

    if _angle != 0:
        for i, p in enumerate(points):
            points[i] = rotate_point_around_point(_posX, _posY, p, _angle)

    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glEnable(GL_BLEND) # TODO: delete

    b = bat(s, TRIS,
                             {pos: points},
                             indices=sgeo2ridx)
    s.bind()
    s.uniform_float(dep, _dep)
    s.uniform_float(co, _co)
    b.draw(s)

    glDisable(GL_BLEND) # TODO: delete
    glDisable(GL_DEPTH_TEST) # TODO: delete

def dr2drf(_x, _y, _width, _height, _co = [0, 0.5, 0.5, 1.0]):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    dr2dls(_co,
                  A, B,
                  B, D,
                  D, C,
                  C, A)

def dr2drfsc(_x, _y, _width, _height, _line_thickness=2, _co = [0, 0.5, 0.5, 1.0]):
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(_line_thickness)
    A = (_x-_width, _y-_height)
    B = (_x-_width, _y+_height)
    C = (_x+_width, _y-_height)
    D = (_x+_width, _y+_height)
    dr2dls(_co,
                  A, B,
                  B, D,
                  D, C,
                  C, A)
    glLineWidth(1)
    glDisable(GL_LINE_SMOOTH)

def dr2drr(_posX, _posY, _sz, _co = [0, 0.5, 0.5, 1.0], _subdivs = 2, radius = 8,
                              s = gps2gen):
    _width, _height = _sz
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius
    if _subdivs == 1:
        _vertices = sgeo2rr2pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr2idx
        #if use_shadow:
        #    p1 = [_vertices[2][0], _vertices[2][1] - 1]
        #    p2 = [_vertices[3][0], _vertices[3][1] - 1]
        #    dr2dl(p1, p2, (.22, .22, .22, .9))
    else:
        _vertices = sgeo2rr3pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr3idx
        #if use_shadow:
        #    p1 = [_vertices[3][0], _vertices[3][1] - 1]
        #    p2 = [_vertices[4][0], _vertices[4][1] - 1]
        #    dr2dl(p1, p2, (.22, .22, .22, .9))

    b = bat(s, TRIS, {pos:_vertices}, indices=_indices)
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND) # TODO: delete
    b.draw(s)
    glDisable(GL_BLEND) # TODO: delete

def dr2drr_2(_posX, _posY, _width, _height, _co = [0, 0.5, 0.5, 1.0], _subdivs = 2, radius = 8,
                                s = gps2gen):
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius
    if _subdivs == 1:
        _vertices = sgeo2rr2pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr2idx
        #if use_shadow:
        #    p1 = [_vertices[2][0], _vertices[2][1] - 1]
        #    p2 = [_vertices[3][0], _vertices[3][1] - 1]
        #    dr2dl(p1, p2, (.22, .22, .22, .9))
    else:
        _vertices = sgeo2rr3pts(_posX, _posY, _width, _height, radius)
        _indices = sgeo2rr3idx
        #if use_shadow:
        #    p1 = [_vertices[3][0], _vertices[3][1] - 1]
        #    p2 = [_vertices[4][0], _vertices[4][1] - 1]
        #    dr2dl(p1, p2, (.22, .22, .22, .9))

    b = bat(s, TRIS, {pos:_vertices}, indices=_indices)
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND) # TODO: delete
    b.draw(s)
    glDisable(GL_BLEND) # TODO: delete

def dr2drrf(_x, _y, _width, _height, _r, _co = [0, 0.5, 0.5, 1.0]):
    p = sgeo2rr3pts(_x, _y, _width, _height, _r)
    dr2dls(_co,
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

def dr2drrt(_posX, _posY, _sz, _co = [0, 0.5, 0.5, 1.0], radius = 8,
                                  s = gps2gen):
    _width, _height = _sz
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius

    _vertices = sgeo2rr3ptstop(_posX, _posY, _width, _height, radius)

    b = bat(s, TRIS, {pos:_vertices}, indices=sgeo2rr3idxtop)
    s.bind()
    s.uniform_float(co, _co)
    # glEnable(GL_BLEND) # TODO: delete
    b.draw(s)
    # glDisable(GL_BLEND) # TODO: delete

def dr2drrb(_posX, _posY, _sz, _co = [0, 0.5, 0.5, 1.0], radius = 8,
                                     s = gps2gen):
    _width, _height = _sz
    radiusx2 = radius * 2
    radius = _width/2 if radiusx2 > _width else _height/2 if radiusx2 > _height else radius

    _vertices = sgeo2rr3ptsbot(_posX, _posY, _width, _height, radius)

    b = bat(s, TRIS, {pos:_vertices}, indices=sgeo2rr3idxbot)
    s.bind()
    s.uniform_float(co, _co)
    glEnable(GL_BLEND) # TODO: delete
    b.draw(s)
    glDisable(GL_BLEND) # TODO: delete
# I
def driao(image, off_x, off_y, _width, _height, _opacity = 1, s = gps2iao):
    if image.gl_touch():
        raise Exception()
    vertices = (
            (off_x,             _height + off_y),
            (off_x,             off_y),
            (off_x + _width,    off_y),
            (off_x + _width,    _height + off_y)
    )
    batch_img = bat(s, TRI_FAN, { pos : vertices, txco: ((0, 1), (0, 0), (1, 0), (1, 1)) },)
    #glEnable(GL_DEPTH_TEST) # DETRÁS
    #glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, image.bindcode)
    s.bind()
    #s.uniform_int("image", 0)
    #opacity = s.uniform_from_name("opacity")
    #color = array([0, 0, 0, _opacity], 'f')
    s.uniform_float("opacity", _opacity)
    batch_img.draw(s)
    glDisable(GL_BLEND)

def dria(image, off_x, off_y, _width, _height, s=gps2ia):
    if image.gl_touch():
        raise Exception()
    vertices = (
            (off_x,             _height + off_y),
            (off_x,             off_y),
            (off_x + _width,    off_y),
            (off_x + _width,    _height + off_y)
    )
    batch_img = bat(s, TRI_FAN, {pos : vertices, txco: ((0, 1), (0, 0), (1, 0), (1, 1))})
    glEnable(GL_BLEND)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, image.bindcode)
    batch_img.draw(s)
    glDisable(GL_BLEND)

def driac(image, off_x, off_y, _width, _height, s=gps2ia):
    if image.gl_touch():
        raise Exception()
    batch_img = bat(
        s, TRI_FAN,
        {
            pos : (
                    (off_x - _width,    off_y + _height),
                    (off_x - _width,    off_y - _height),
                    (off_x + _width,    off_y - _height),
                    (off_x + _width,    off_y + _height)
                ),
            txco: ((0, 1), (0, 0), (1, 0), (1, 1))
        }
    )
    glEnable(GL_BLEND)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, image.bindcode)
    batch_img.draw(s)
    glDisable(GL_BLEND)
# F
def dr2fldot(_x, _y, _width, _height, _co, _line_width=2, _factor=.3):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    dr2dldot(_co, _line_width, _factor,
                  A, B,
                  B, D,
                  D, C,
                  C, A)

def dr2fldotmul(_x, _y, _width, _height, _color1, _color2, _line_width=2, _factor=.3):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    dr2dldotmul(_color1, _color2, _line_width, _factor,
                  A, B,
                  B, D,
                  D, C,
                  C, A)
# C
# GL_FRAMEBUFFER_SRGB
def dr2dc(_x, _y, _r, _co=(0, 1, 1, 1), s=gps2c):
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    s.bind()
    s.uniform_float(co, _co)
    b.draw(s)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs(_x, _y, _r, _co=(0, 1, 1, 1), s=gps2cs):
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    s.bind()
    s.uniform_float(co, _co)
    b.draw(s)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcsdep(_x, _y, _r, _co=(0, 1, 1, 1), _dep=1, s=gps2csdep):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glEnable(GL_BLEND) # TODO: delete
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glPointSize(_r*2)
    s.bind()
    s.uniform_float(co, _co)
    s.uniform_float(dep, _dep)
    b.draw(s)
    # Restore.
    glDisable(GL_BLEND) # TODO: delete
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)

def dr2dcsout (
     _x, _y, _r, _co=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1,
     s=gps2csout
    ):
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    s.bind()
    s.uniform_float(co, _co)
    s.uniform_float("outline_color", _outline_color)
    s.uniform_float("outline_factor", _outline_factor)
    b.draw(s)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcsoutdep (
     _x, _y, _r, _co=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1,
     _dep=0, s=gps2csoutdep
    ):
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    s.bind()
    s.uniform_float(co, _co)
    s.uniform_float("outline_color", _outline_color)
    s.uniform_float("outline_factor", _outline_factor)
    s.uniform_float(dep, _dep)

    b.draw(s)
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcsoutg (
     _x, _y, _r, _co=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1, _use_outline_blur=False,
     s=gps2csoutg
    ):
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    s.bind()
    s.uniform_float(co, _co)
    s.uniform_float("outline_color", _outline_color)
    s.uniform_float("outline_factor", _outline_factor)
    s.uniform_float("outline_blur", float(_use_outline_blur))
    b.draw(s)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcsoutgdep (
     _x, _y, _r, _co=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1, _use_outline_blur=False,
     _dep=0, s=gps2csoutgdep
    ):
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    s.bind()
    s.uniform_float(co, _co)
    s.uniform_float("outline_color", _outline_color)
    s.uniform_float("outline_factor", _outline_factor)
    s.uniform_float("outline_blur", float(_use_outline_blur))
    s.uniform_float(dep, _dep)
    b.draw(s)
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete
rot="rotation"
def dr2dcsg (
     _x, _y, _r, _co=(0, 1, 1, 1),
     _co2=(0, 0, 0, 1), _gtype='RADIAL', _gfactor=0.0, _grot=0,
     s=gpgps2csgrd
     ):
    #glEnable(GL_SRGB8_ALPHA8)
    glPointSize(_r*2)
    # glEnable(GL_FRAMEBUFFER_SRGB)
    glEnable(GL_BLEND) # TODO: delete
    if _gtype == 'RADIAL':
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        pass
    elif _gtype.startswith('L'):
        s = gps2csgln
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        s.uniform_float(rot, radians(_grot))
    elif _gtype.startswith('R'):
        s = gps2csgrf
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        s.uniform_float(rot, radians(_grot))
    elif _gtype.startswith('D'):
        s = gps2csgdm
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        s.uniform_float(rot, radians(_grot))
    else:
        return

    s.uniform_float(co, _co)
    s.uniform_float("second_color", _co2)
    s.uniform_float(fac, _gfactor)
    b.draw(s)
    #glDisable(GL_SRGB8_ALPHA8)
    glPointSize(4)
    # glDisable(GL_FRAMEBUFFER_SRGB)
    glDisable(GL_BLEND) # TODO: delete


def dr2dcsgdep (
     _x, _y, _r, _co=(0, 1, 1, 1), _co2=(0, 0, 0, 1),
     _gtype='RADIAL', _gfactor=0.0, _grot=0,
     _dep=0, s=gps2csgrddep
     ):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glPointSize(_r*2)
    glEnable(GL_BLEND) # TODO: delete
    if _gtype == 'RADIAL':
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        pass
    elif _gtype.startswith('L'):
        s = gps2csglndep
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        s.uniform_float(rot, radians(_grot))
    elif _gtype.startswith('R'):
        s = gps2csgrfdep
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        s.uniform_float(rot, radians(_grot))
    elif _gtype.startswith('D'):
        s = gps2csgdmdep
        b = bat(s, POINTS, {pos: [(_x, _y)]})
        s.bind()
        s.uniform_float(rot, radians(_grot))
    else:
        return

    s.uniform_float(co, _co)
    s.uniform_float("second_color", _co2)
    s.uniform_float(fac, _gfactor)
    s.uniform_float(dep, _dep)
    b.draw(s)
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcaaswd(_x, _y, _r, _rf, _f, _cf, _co, _dep=1, s=gps2caasdep):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glEnable(GL_BLEND) # TODO: delete
    b = bat(s, POINTS, {pos: [(_x, _y)]})
    glPointSize(_r*2)
    s.bind()
    s.uniform_float(dep, _dep)
    s.uniform_float("co", _co)
    s.uniform_float("r", _rf)
    s.uniform_float("f", _f)
    s.uniform_float("c", _cf)
    b.draw(s)
    # Restore.
    glDisable(GL_BLEND) # TODO: delete
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
# BOX
def drcbx(_x, _y, _sz, _value, _co, _hover):
    radius = max(min(_sz[0], _sz[1]) / 2 - 6, 1)
    if _value:
        if _hover:
            hover_color = (_co[0]+.1, _co[1]+.1, _co[2]+.1, 1)
            dr2drr_2(_x, _y, _sz[0], _sz[1], hover_color, 2, radius)
            dr2drr_2(_x+1, _y+1, _sz[0]-2, _sz[1]-2, (.44, .6, .86, 1), 2, radius)
        else:
            dr2drr_2(_x, _y, _sz[0], _sz[1], _co, 2, radius)
            dr2drr_2(_x+1, _y+1, _sz[0]-2, _sz[1]-2, (.34, .5, .76, .9), 2, radius)
        if _sz[1] > 12:
            firstPoint = [_x+4, _y + int(_sz[1]/2)]
            midPoint = [_x+int(_sz[0]/2), _y + int(_sz[1]/3.2)]
            lastPoint = [_x+_sz[0]-4, _y+_sz[1]-4]
            dr2dl(firstPoint, midPoint, (.8, .8, .8, .8))
            dr2dl(midPoint, lastPoint, (.8, .8, .8, .8))
            firstPoint[1] -= 1
            midPoint[1] -= 1
            lastPoint[1] -= 1
            dr2dl(firstPoint, midPoint, (.75, .75, .75, .75))
            dr2dl(midPoint, lastPoint, (.75, .75, .75, .75))
            firstPoint[1] -= 1
            midPoint[1] -= 1
            lastPoint[1] -= 1
            dr2dl(firstPoint, midPoint, (.7, .7, .7, .7))
            dr2dl(midPoint, lastPoint, (.7, .7, .7, .7))
    else:
        if _hover:
            hover_color = (_co[0]+.1, _co[1]+.1, _co[2]+.1, 1)
            dr2drr_2(_x, _y, _sz[0], _sz[1], hover_color, 2, radius)
        else:
            dr2drr_2(_x, _y, _sz[0], _sz[1], _co, 2, radius)
    #blf.size(0, max(_sz[1] - 4, 11), 72) #- 4
    #textsize = blf.dimensions(0, _name)
    #textY = _y + (_sz[1] - textsize[1]) * .5
    #if _hover:
    #    drt(_x + _sz[0] + 8, textY, _name, max(_sz[1] - 4, 11), 0, 1, 1, 1, 1, True)
    #else:
    #    drt(_x + _sz[0] + 8, textY, _name, max(_sz[1] - 4, 11), 0, .9, .9, .9, .9, True)

def drcbxsmpl(_x, _y, _width, _height, _value, _co, _tick_color):
    if not _value:
        dr2drf(_x, _y, _width, _height, _co)
    else:
        # Calc tick points.
        firstPoint = [_x+1, _y + int(_height/2)]
        midPoint = [_x+int(_width/2), _y + int(_height/3.2)]
        lastPoint = [_x+_width-1, _y+_height-2]
        dr2dr(_x, _y, _width, _height, _co)
        dr2dls(_tick_color, firstPoint, midPoint, midPoint, lastPoint)
        firstPoint[1] -= 1
        midPoint[1] -= 1
        lastPoint[1] -= 1
        dr2dls(_tick_color, firstPoint, midPoint, midPoint, lastPoint)
# T
def drt(_x, _y, _t, _sz, _font_id = 0, _r = 1, _g = 1, _b = 1, _a = 1, _shadow = False):
    if _shadow:
        _font_id = 1
        text_enable(_font_id, SHADOW)
        text_shadow(_font_id, 3, 0, 0, 0, .6)
        text_shadow_offset(_font_id, -1, -1)
    text_color(_font_id, _r, _g, _b, _a)
    text_position(_font_id, _x, _y, 0) # -6/-6 para "o" #
    text_size(_font_id, _sz, 72)
    text_draw(_font_id, _t)
    if _shadow:
        text_disable(_font_id, SHADOW)

def drtcent(_x=0, _y=0, _t='', _ts=12, _tco=(1, 1, 1, 1), _shadow=True):
    if _shadow:
        text_enable(0, SHADOW)
        text_shadow(0, 3, 0, 0, 0, .6)
        text_shadow_offset(0, -1, -1)
    text_size(0, _ts, 72)
    dim = text_dim(0, _t)
    text_color(0, *_tco)
    text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
    text_draw(0, _t)
    if _shadow:
        text_disable(0, SHADOW)

def drtbx(_x, _y, _sz, _co, _t, _tco, _ts=12, _shadow=False, s=gps2gen):
    batch_rect = bat(s, TRIS, {pos : sgeo2rpts(_x, _y, _sz)}, indices=sgeo2ridx)
    s.bind()
    s.uniform_float(co, _co)
    batch_rect.draw(s)
    if _t != '':
        if _shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)
        text_position(0, _x + (_sz[0] - dim[0]) * .5, _y + (_sz[1] - dim[1]) * .5, 0)
        text_draw(0, _t)
        if _shadow:
            text_disable(0, SHADOW)

def drtbxc(_x, _y, _sz, _co, _t, _tco, _ts=12, _shadow=True, s=gps2gen):
    dr2drc(_x, _y, _sz, _co)
    if _t != '':
        if _shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _t)
        if _shadow:
            text_disable(0, SHADOW)

def drtbxcwd(_x, _y, _sz, _co, _t, _tco, _ts=12, _shadow=True, _dep=1, s=gps2gendep):
    dr2drcdep(_x, _y, _sz, _co, _dep)
    if _t != '':
        if _shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _t)
        if _shadow:
            text_disable(0, SHADOW)

def drtbxcrwd(_x, _y, _sz, _angle, _co, _t, _tco, _ts=12, _shadow=True, _dep=1, s=gps2gendep):
    angle = radians(_angle)
    dr2drcrotdep(_x, _y, _sz, angle, _co, _dep)
    if _t != '':
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)

        if _shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        if _angle != 0:
            text_enable(0, ROTATION)
            text_rotation(0, angle)

            #p = (_x - dim[0]*.5, _y - dim[1]*.5)
            x, y = rotate_point_around_point(_x, _y, (_x - dim[0]*.5, _y - dim[1]*.5), angle)
            text_position(0, x, y, 0)

            #ver = sin(angle) # how vertical it is? 1 == vertical ; 0 = horizontal (no verticality)
            #hor = cos(angle) # how horizontal it is? 1 == horizontal ; 0 = vertical (no horizontality)
            #dim_x = dim[0] * hor + dim[1] * (1 - ver)
            #dim_y = dim[1] * ver + dim[0] * (1 - hor)
            #print("x:", dim_x)
            #print("y:", dim_y)
            #text_enable(0, CLIPPING)
            #text_clipping(
            #    0,
            #    x, # x_min
            #    y, # y_min
            #    x+dim_x, # x_max
            #    y+dim_y  # y_max
            #)
        else:
            text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
            text_enable(0, CLIPPING)
            text_clipping(
                0,
                _x-_sz[0], # x_min
                _y-_sz[1], # y_min
                _x+_sz[0], # x_max
                _y+_sz[1]  # y_max
            )

        text_draw(0, _t)

        if _shadow:
            text_disable(0, SHADOW)
        if _angle != 0:
            text_disable(0, ROTATION)
        else:
            text_disable(0, CLIPPING)

def drtrbx(_x, _y, _sz, _co, _t, _ts, _tco, s=gps2gen):
    dr2drr(_x, _y, _sz, _co, 2, 10, s)
    if _t != '':
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)
        text_position(0, _x + (_sz[0] - dim[0]) * .5, _y + (_sz[1] - dim[1]) * .5, 0)
        text_draw(0, _t)


def dr2dsbr(_tail_tip, _tail_size, _co, _t, _ts, _tco, s=gps2gen):
    margin_top_bottom = 6
    margin_left_right = 12

    _tail_tip[0] -= 2

    text_size(0, _ts, 72)
    dim = text_dim(0, _t)

    x = _tail_tip[0] - _tail_size[0] - margin_left_right * 2 - dim[0]
    y = _tail_tip[1] - margin_top_bottom - int(dim[1] / 2.0)

    B = [_tail_tip[0] - _tail_size[0], _tail_tip[1] + _tail_size[1]]
    C = [_tail_tip[0] - _tail_size[0], _tail_tip[1] - _tail_size[1]]

    dr2dt(_tail_tip, B, C, _co)

    dr2drr(x, y, [dim[0] + margin_left_right * 2, dim[1] + margin_top_bottom * 2], _co, 2, 6)

    text_color(0, *_tco)
    text_position(0, x + margin_left_right, y + margin_top_bottom, 0)
    text_draw(0, _t)

def drtc(_x, _y, _r, _co, _t, _tco, _ts=12, _shadow=True):
    dr2dc(_x, _y, _r, _co)
    if _t != '':
        if _shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _t)
        if _shadow:
            text_disable(0, SHADOW)

def _drtbx(_x, _y, _t, _tco, _ts=12, _shadow=True):
    if _t != '':
        if _shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _ts, 72)
        dim = text_dim(0, _t)
        text_color(0, *_tco)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _t)
        if _shadow:
            text_disable(0, SHADOW)

def drtcs(_x, _y, _r, _co, _t, _tco, _ts=12, _shadow=True):
    dr2dcs(_x, _y, _r, _co)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcswd(_x, _y, _r, _co, _t, _tco, _ts=12, _shadow=True, _dep=1):
    dr2dcsdep(_x, _y, _r, _co, _dep)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcsout(
     _x, _y, _r, _co, _outline_color, _outline_factor,
     _t, _tco, _ts=12, _shadow=True
    ):
    dr2dcsout(_x, _y, _r, _co, _outline_color, _outline_factor)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcsoutwd(
     _x, _y, _r, _co, _outline_color, _outline_factor,
     _t, _tco, _ts=12, _shadow=True, _dep=1
    ):
    dr2dcsoutdep(_x, _y, _r, _co, _outline_color, _outline_factor, _dep)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcsoutg(
     _x, _y, _r, _co, _outline_color, _outline_factor, _use_outline_blur,
     _t, _tco, _ts=12, _shadow=True
    ):
    dr2dcsoutg(_x, _y, _r, _co, _outline_color, _outline_factor, _use_outline_blur)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcsoutgwd(
     _x, _y, _r, _co, _outline_color, _outline_factor, _use_outline_blur,
     _t, _tco, _ts=12, _shadow=True, _dep=1
    ):
    dr2dcsoutgdep(_x, _y, _r, _co, _outline_color, _outline_factor, _use_outline_blur, _dep)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcsg(
     _x, _y, _r, _co, _co2,
     _gtype, _gfactor, _grot,
     _t, _tco, _ts=12, _shadow=True
    ):
    dr2dcsg(_x, _y, _r, _co, _co2, _gtype, _gfactor, _grot)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

def drtcsgwd(
     _x, _y, _r, _co, _co2,
     _gtype, _gfactor, _grot,
     _t, _tco, _ts=12, _shadow=True, _dep=1
    ):
    dr2dcsgdep(_x, _y, _r, _co, _co2, _gtype, _gfactor, _grot, _dep)
    _drtbx(_x, _y, _t, _tco, _ts, _shadow)

# Draw func.
def _dr2dr(_x, _y, _size, _color, shader=gps2gen):
    batch_rect = bat(shader, 'TRIS', {"pos" : sgeo2rpts(_x, _y, _size)}, indices=sgeo2ridx)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)

def _dr2drt(_x, _y, _size, _color, _text, _text_color, shader=gps2gen):
    batch_rect = bat(shader, 'TRIS', {"pos" : sgeo2rpts(_x, _y, _size)}, indices=sgeo2ridx)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)
    if _text != '':
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x + (_size[0] - dim[0]) * .5, _y + (_size[1] - dim[1]) * .5, 0)
        text_draw(0, _text)

def _drai(_pos, _size, _image, shader=gps2ia):
    x, y = _pos
    w, h = _size
    if _image.gl_touch():
        raise Exception()
    vertices = [
        [x,     y + h],
        [x,     y],
        [x + w, y],
        [x + w, y + h]
    ]
    batch_img = bat(shader, 'TRI_FAN', {"pos" : vertices, "texCoord" : ((0, 1), (0, 0), (1, 0), (1, 1))})
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, _image.bindcode)
    batch_img.draw(shader)

def _draoi(_pos, _size, _image, _opacity=0.6, shader=gps2iao):
    x, y = _pos
    w, h = _size
    if _image.gl_touch():
        raise Exception()
    vertices = [
        [x,     y + h],
        [x,     y],
        [x + w, y],
        [x + w, y + h]
    ]
    batch_img = bat(shader, 'TRI_FAN', { "pos" : vertices, "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) })
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, _image.bindcode)
    shader.bind()
    shader.uniform_float("opacity", _opacity)
    batch_img.draw(shader)
'''
def mask_pk_scene(_posX, _posY, _width, _height):
    glEnable(GL_SCISSOR_TEST)
    glScissor(_posX+10, _posY+10, _width-20, _height-20)
'''