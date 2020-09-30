from gpu_extras.batch import batch_for_shader
from blf import (
    enable as text_enable, disable as text_disable,
    SHADOW, shadow as text_shadow, shadow_offset as text_shadow_offset,
    color as text_color, position as text_position, size as text_size,
    dimensions as text_dim, draw as text_draw, ROTATION, rotation as text_rotation,
    clipping as text_clipping, CLIPPING, KERNING_DEFAULT, WORD_WRAP, MONOCHROME
)

from .rectangle_req import sgeo2ridx, sgeo2rpts
from .gpu_shaders import gps2gen, gps2gendep
from .polygon import (
    dr2dt, dr2drr,
    dr2drc, dr2drc_WithDepth, dr2drc_Rotate_WithDepth
)
from .circle import (
    dr2dc,
    dr2dcs, dr2dcs_WithDepth,
    dr2dcs_Outline, dr2dcs_Outline_WithDepth,
    dr2dcs_Outline_Gradient, dr2dcs_Outline_Gradient_WithDepth,
    dr2dcs_Gradient, dr2dcs_Gradient_WithDepth
)
from math import radians, cos, sin
from ..functions import rotate_point_around_point


def drt(_x, _y, _text, _size, _font_id = 0, _r = 1, _g = 1, _b = 1, _a = 1, _use_shadow = False):
    if _use_shadow:
        _font_id = 1
        text_enable(_font_id, SHADOW)
        text_shadow(_font_id, 3, 0, 0, 0, .6)
        text_shadow_offset(_font_id, -1, -1)
    text_color(_font_id, _r, _g, _b, _a)
    text_position(_font_id, _x, _y, 0) # -6/-6 para "o" #
    text_size(_font_id, _size, 72)
    text_draw(_font_id, _text)
    if _use_shadow:
        text_disable(_font_id, SHADOW)

def drt_AlignCenter(_x=0, _y=0, _text='', _text_size=12, _text_color=(1, 1, 1, 1), _use_shadow=True):
    if _use_shadow:
        text_enable(0, SHADOW)
        text_shadow(0, 3, 0, 0, 0, .6)
        text_shadow_offset(0, -1, -1)
    text_size(0, _text_size, 72)
    dim = text_dim(0, _text)
    text_color(0, *_text_color)
    text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
    text_draw(0, _text)
    if _use_shadow:
        text_disable(0, SHADOW)

def drtbx(_x, _y, _size, _color, _text, _text_color, _text_size=12, _use_shadow=False, shader=gps2gen):
    ''' DRAW RECT '''
    batch_rect = batch_for_shader(shader, 'TRIS', {"pos" : sgeo2rpts(_x, _y, _size)}, indices=sgeo2ridx)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)
    ''' DRAW TEXT '''
    if _text != '':
        if _use_shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x + (_size[0] - dim[0]) * .5, _y + (_size[1] - dim[1]) * .5, 0)
        text_draw(0, _text)
        if _use_shadow:
            text_disable(0, SHADOW)


def drtbxc(_x, _y, _size, _color, _text, _text_color, _text_size=12, _use_shadow=True, shader=gps2gen):
    ''' DRAW RECT '''
    dr2drc(_x, _y, _size, _color)
    ''' DRAW TEXT '''
    if _text != '':
        if _use_shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _text)
        if _use_shadow:
            text_disable(0, SHADOW)

def drtbxcwd(_x, _y, _size, _color, _text, _text_color, _text_size=12, _use_shadow=True, _depth=1, shader=gps2gendep):
    ''' DRAW RECT '''
    dr2drc_WithDepth(_x, _y, _size, _color, _depth)
    ''' DRAW TEXT '''
    if _text != '':
        if _use_shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _text)
        if _use_shadow:
            text_disable(0, SHADOW)

def drtbxcrwd(_x, _y, _size, _angle, _color, _text, _text_color, _text_size=12, _use_shadow=True, _depth=1, shader=gps2gendep):
    angle = radians(_angle)
    ''' DRAW RECT '''
    dr2drc_Rotate_WithDepth(_x, _y, _size, angle, _color, _depth)
    ''' DRAW TEXT '''
    if _text != '':
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)

        if _use_shadow:
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
                _x-_size[0], # x_min
                _y-_size[1], # y_min
                _x+_size[0], # x_max
                _y+_size[1]  # y_max
            )

        text_draw(0, _text)

        if _use_shadow:
            text_disable(0, SHADOW)
        if _angle != 0:
            text_disable(0, ROTATION)
        else:
            text_disable(0, CLIPPING)

def drtrbx(_x, _y, _size, _color, _text, _text_size, _text_color, shader=gps2gen):
    ''' DRAW RECT '''
    dr2drr(_x, _y, _size, _color, 2, 10, shader)
    ''' DRAW TEXT '''
    if _text != '':
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x + (_size[0] - dim[0]) * .5, _y + (_size[1] - dim[1]) * .5, 0)
        text_draw(0, _text)


def dr2dsbr(_tail_tip, _tail_size, _color, _text, _text_size, _text_color, _shader=gps2gen):
    margin_top_bottom = 6
    margin_left_right = 12

    _tail_tip[0] -= 2

    text_size(0, _text_size, 72)
    dim = text_dim(0, _text)

    x = _tail_tip[0] - _tail_size[0] - margin_left_right * 2 - dim[0]
    y = _tail_tip[1] - margin_top_bottom - int(dim[1] / 2.0)

    B = [_tail_tip[0] - _tail_size[0], _tail_tip[1] + _tail_size[1]]
    C = [_tail_tip[0] - _tail_size[0], _tail_tip[1] - _tail_size[1]]

    dr2dt(_tail_tip, B, C, _color)

    dr2drr(x, y, [dim[0] + margin_left_right * 2, dim[1] + margin_top_bottom * 2], _color, 2, 6)

    text_color(0, *_text_color)
    text_position(0, x + margin_left_right, y + margin_top_bottom, 0)
    text_draw(0, _text)

def drtc(_x, _y, _radius, _color, _text, _text_color, _text_size=12, _use_shadow=True):
    ''' DRAW RECT '''
    dr2dc(_x, _y, _radius, _color)
    ''' DRAW TEXT '''
    if _text != '':
        if _use_shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _text)
        if _use_shadow:
            text_disable(0, SHADOW)

def drtBoxText(_x, _y, _text, _text_color, _text_size=12, _use_shadow=True):
    ''' DRAW TEXT '''
    if _text != '':
        if _use_shadow:
            text_enable(0, SHADOW)
            text_shadow(0, 3, 0, 0, 0, .6)
            text_shadow_offset(0, -1, -1)
        text_size(0, _text_size, 72)
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x - dim[0]*.5, _y - dim[1]*.5, 0)
        text_draw(0, _text)
        if _use_shadow:
            text_disable(0, SHADOW)


def drtc_Smooth(_x, _y, _radius, _color, _text, _text_color, _text_size=12, _use_shadow=True):
    dr2dcs(_x, _y, _radius, _color)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtcswd(_x, _y, _radius, _color, _text, _text_color, _text_size=12, _use_shadow=True, _depth=1):
    dr2dcs_WithDepth(_x, _y, _radius, _color, _depth)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtc_Smooth_Outline(
     _x, _y, _radius, _color, _outline_color, _outline_factor,
     _text, _text_color, _text_size=12, _use_shadow=True
    ):
    dr2dcs_Outline(_x, _y, _radius, _color, _outline_color, _outline_factor)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtcsoutwd(
     _x, _y, _radius, _color, _outline_color, _outline_factor,
     _text, _text_color, _text_size=12, _use_shadow=True, _depth=1
    ):
    dr2dcs_Outline_WithDepth(_x, _y, _radius, _color, _outline_color, _outline_factor, _depth)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtc_Smooth_Outline_Gradient(
     _x, _y, _radius, _color, _outline_color, _outline_factor, _use_outline_blur,
     _text, _text_color, _text_size=12, _use_shadow=True
    ):
    dr2dcs_Outline_Gradient(_x, _y, _radius, _color, _outline_color, _outline_factor, _use_outline_blur)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtcsoutgwd(
     _x, _y, _radius, _color, _outline_color, _outline_factor, _use_outline_blur,
     _text, _text_color, _text_size=12, _use_shadow=True, _depth=1
    ):
    dr2dcs_Outline_Gradient_WithDepth(_x, _y, _radius, _color, _outline_color, _outline_factor, _use_outline_blur, _depth)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtc_Smooth_Gradient(
     _x, _y, _radius, _color, _second_color,
     _gradient_type, _gradient_factor, _gradient_rotation,
     _text, _text_color, _text_size=12, _use_shadow=True
    ):
    dr2dcs_Gradient(_x, _y, _radius, _color, _second_color, _gradient_type, _gradient_factor, _gradient_rotation)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)

def drtcsgwd(
     _x, _y, _radius, _color, _second_color,
     _gradient_type, _gradient_factor, _gradient_rotation,
     _text, _text_color, _text_size=12, _use_shadow=True, _depth=1
    ):
    dr2dcs_Gradient_WithDepth(_x, _y, _radius, _color, _second_color, _gradient_type, _gradient_factor, _gradient_rotation, _depth)
    drtBoxText(_x, _y, _text, _text_color, _text_size, _use_shadow)
