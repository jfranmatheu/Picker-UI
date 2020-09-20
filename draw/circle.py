from gpu_extras.batch import batch_for_shader
from bgl import *
from math import radians

from .gpu_shaders import (
    shader_2d_circle,

    shader_2d_circle_smooth, shader_2d_circle_smooth_depth,
    shader_2d_circle_aa_smooth_depth,
    shader_2d_circle_smooth_gradient_radial, shader_2d_circle_smooth_gradient_radial_depth,
    shader_2d_circle_smooth_gradient_linear, shader_2d_circle_smooth_gradient_linear_depth,
    shader_2d_circle_smooth_gradient_reflect, shader_2d_circle_smooth_gradient_reflect_depth,
    shader_2d_circle_smooth_gradient_diamond, shader_2d_circle_smooth_gradient_diamond_depth,

    shader_2d_circle_smooth_outline, shader_2d_circle_smooth_outline_depth,
    shader_2d_circle_smooth_outline_gradient, shader_2d_circle_smooth_outline_gradient_depth
)

# GL_FRAMEBUFFER_SRGB
def Draw_2D_Circle(_x, _y, _radius, _color=(0, 1, 1, 1), _shader=shader_2d_circle):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def Draw_2D_Circle_Smooth(_x, _y, _radius, _color=(0, 1, 1, 1), _shader=shader_2d_circle_smooth):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
    glPointSize(_radius*2)
    glEnable(GL_BLEND) # TODO: delete
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)
    glPointSize(4)
    glDisable(GL_BLEND) # TODO: delete

def Draw_2D_Circle_Smooth_WithDepth(_x, _y, _radius, _color=(0, 1, 1, 1), _depth=1, _shader=shader_2d_circle_smooth_depth):
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

def Draw_2D_Circle_Smooth_Outline (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1,
     _shader=shader_2d_circle_smooth_outline
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

def Draw_2D_Circle_Smooth_Outline_WithDepth (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1,
     _depth=0, _shader=shader_2d_circle_smooth_outline_depth
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

def Draw_2D_Circle_Smooth_Outline_Gradient (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1, _use_outline_blur=False,
     _shader=shader_2d_circle_smooth_outline_gradient
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

def Draw_2D_Circle_Smooth_Outline_Gradient_WithDepth (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _outline_color=(0, 0, 0, 1), _outline_factor=0.1, _use_outline_blur=False,
     _depth=0, _shader=shader_2d_circle_smooth_outline_gradient_depth
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

def Draw_2D_Circle_Smooth_Gradient (
     _x, _y, _radius, _color=(0, 1, 1, 1),
     _second_color=(0, 0, 0, 1), _gradient_type='RADIAL', _gradient_factor=0.0, _gradient_rotation=0,
     _shader=shader_2d_circle_smooth_gradient_radial
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
        _shader = shader_2d_circle_smooth_gradient_linear
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('R'):
        _shader = shader_2d_circle_smooth_gradient_reflect
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('D'):
        _shader = shader_2d_circle_smooth_gradient_diamond
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


def Draw_2D_Circle_Smooth_Gradient_WithDepth (
     _x, _y, _radius, _color=(0, 1, 1, 1), _second_color=(0, 0, 0, 1),
     _gradient_type='RADIAL', _gradient_factor=0.0, _gradient_rotation=0,
     _depth=0, _shader=shader_2d_circle_smooth_gradient_radial_depth
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
        _shader = shader_2d_circle_smooth_gradient_linear_depth
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('R'):
        _shader = shader_2d_circle_smooth_gradient_reflect_depth
        batch = batch_for_shader(_shader, 'POINTS', {"pos": [(_x, _y)]})
        _shader.bind()
        _shader.uniform_float("rotation", radians(_gradient_rotation))
    elif _gradient_type.startswith('D'):
        _shader = shader_2d_circle_smooth_gradient_diamond_depth
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

def Draw_2D_Circle_AA_Smooth_WithDepth(_x, _y, _r, _rf, _f, _cf, _co, _depth=1, _shader=shader_2d_circle_aa_smooth_depth):
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
