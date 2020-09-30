from gpu_extras.batch import batch_for_shader
from bgl import *
from math import radians

from .gpu_shaders import (
    gps2c,

    gps2cs, gps2csdep,
    gps2caasdep,
    gpgps2csgrd, gps2csgrddep,
    gps2csgln, gps2csglndep,
    gps2csgrf, gps2csgrfdep,
    gps2csgdm, gps2csgdmdep,

    gps2csout, gps2csoutdep,
    gps2csoutg, gps2csoutgdep
)

# GL_FRAMEBUFFER_SRGB
def dr2dc(_x, _y, _radius, _color=(0, 1, 1, 1), _shader=gps2c):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs(_x, _y, _radius, _color=(0, 1, 1, 1), _shader=gps2cs):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs_WithDepth(_x, _y, _radius, _color=(0, 1, 1, 1), _depth=1, _shader=gps2csdep):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glEnable(GL_BLEND) # TODO: delete
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    _shader.bind()
    _shader.uniform_float("color", _color)
    _shader.uniform_float("depth", _depth)
    batch.draw(_shader)
    # Restore.
    glDisable(GL_BLEND) # TODO: delete
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)

def dr2dcs_Outline (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1,
     _shader=gps2csout
    ):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    _shader.uniform_float("outline_color", _outline_color)
    _shader.uniform_float("outline_factor", _outline_factor)
    batch.draw(_shader)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs_Outline_WithDepth (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1,
     _depth=0, _shader=gps2csoutdep
    ):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    _shader.uniform_float("outline_color", _outline_color)
    _shader.uniform_float("outline_factor", _outline_factor)
    _shader.uniform_float("depth", _depth)

    batch.draw(_shader)
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs_Outline_Gradient (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1, _use_outline_blur=False,
     _shader=gps2csoutg
    ):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    _shader.uniform_float("outline_color", _outline_color)
    _shader.uniform_float("outline_factor", _outline_factor)
    _shader.uniform_float("outline_blur", float(_use_outline_blur))
    batch.draw(_shader)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs_Outline_Gradient_WithDepth (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1, _use_outline_blur=False,
     _depth=0, _shader=gps2csoutgdep
    ):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    _shader.uniform_float("outline_color", _outline_color)
    _shader.uniform_float("outline_factor", _outline_factor)
    _shader.uniform_float("outline_blur", float(_use_outline_blur))
    _shader.uniform_float("depth", _depth)
    batch.draw(_shader)
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcs_Gradient (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _second_color=(0, 0, 0, 1), _gradient_type='RADIAL', _gradient_factor=0.0, _gradient_rotation=0,
     _shader=gpgps2csgrd
     ):
    #glEnable(GL_SRGB8_ALPHA8)
    glPointSize(_radius*2)
    # glEnable(GL_FRAMEBUFFER_SRGB)
    glEnable(GL_BLEND) # TODO: delete
    if _gradient_type == 'RADIAL':
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        pass
    elif _gradient_type.startswith('L'):
        _shader = gps2csgln
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('R'):
        _shader = gps2csgrf
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('D'):
        _shader = gps2csgdm
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    else:
        return

    _shader.uniform_float("color", _color)
    _shader.uniform_float("second_color", _second_color)
    _shader.uniform_float("factor", _gradient_factor)
    batch.draw(_shader)
    #glDisable(GL_SRGB8_ALPHA8)
    glPointSize(4)
    # glDisable(GL_FRAMEBUFFER_SRGB)
    glDisable(GL_BLEND) # TODO: delete


def dr2dcs_Gradient_WithDepth (
     _x, _y, _radius, _color=(0, 1, 1, 1), _second_color=(0, 0, 0, 1),
     _gradient_type='RADIAL', _gradient_factor=0.0, _gradient_rotation=0,
     _depth=0, _shader=gps2csgrddep
     ):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    if _gradient_type == 'RADIAL':
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        pass
    elif _gradient_type.startswith('L'):
        _shader = gps2csglndep
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('R'):
        _shader = gps2csgrfdep
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('D'):
        _shader = gps2csgdmdep
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    else:
        return

    _shader.uniform_float("color", _color)
    _shader.uniform_float("second_color", _second_color)
    _shader.uniform_float("factor", _gradient_factor)
    _shader.uniform_float("depth", _depth)
    batch.draw(_shader)
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def dr2dcaaswd(_x, _y, _r, _rf, _f, _cf, _co, _depth=1, _shader=gps2caasdep):
    glEnable(GL_DEPTH_TEST) # TODO: delete
    glDepthFunc(GL_LESS) # TODO: improve
    glEnable(GL_BLEND) # TODO: delete
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_r*2)
    _shader.bind()
    _shader.uniform_float("depth", _depth)
    _shader.uniform_float("co", _co)
    _shader.uniform_float("r", _rf)
    _shader.uniform_float("f", _f)
    _shader.uniform_float("c", _cf)
    batch.draw(_shader)
    # Restore.
    glDisable(GL_BLEND) # TODO: delete
    glDisable(GL_DEPTH_TEST) # TODO: delete
    glPointSize(4)
