import gpu
import bgl
from bgl import (
    glEnable, glDisable, glScissor,
    glBindTexture, glActiveTexture, GL_TEXTURE0, GL_TEXTURE_2D,
    GL_BLEND, GL_DEPTH_TEST, GL_SCISSOR_TEST
)
from blf import (
    enable as text_enable, disable as text_disable,
    SHADOW, shadow as text_shadow, shadow_offset as text_shadow_offset,
    color as text_color, position as text_position, size as text_size,
    dimensions as text_dim, draw as text_draw,
)
from gpu_extras.batch import batch_for_shader
from .draw.gpu_shaders import (
    shader_2d_generic_basic,
    shader_image_alpha,
    shader_image_alpha_opacity
)
from .draw.rectangle_req import rectangle_points, rectangle_indices


def draw_2d_rectangle(_x, _y, _size, _color, shader=shader_2d_generic_basic):
    batch_rect = batch_for_shader(shader, 'TRIS', {"pos" : rectangle_points(_x, _y, _size)}, indices=rectangle_indices)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)

def draw_2d_rectangle_text(_x, _y, _size, _color, _text, _text_color, shader=shader_2d_generic_basic):
    ''' DRAW RECT '''
    batch_rect = batch_for_shader(shader, 'TRIS', {"pos" : rectangle_points(_x, _y, _size)}, indices=rectangle_indices)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)
    ''' DRAW TEXT '''
    if _text != '':
        dim = text_dim(0, _text)
        text_color(0, *_text_color)
        text_position(0, _x + (_size[0] - dim[0]) * .5, _y + (_size[1] - dim[1]) * .5, 0)
        text_draw(0, _text)

def draw_alpha_image(_pos, _size, _image, shader=shader_image_alpha):
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
    batch_img = batch_for_shader(shader, 'TRI_FAN', {"pos" : vertices, "texCoord" : ((0, 1), (0, 0), (1, 0), (1, 1))})
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, _image.bindcode)
    batch_img.draw(shader)

def draw_alpha_opacity_image(_pos, _size, _image, _opacity=0.6, shader=shader_image_alpha_opacity):
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
    batch_img = batch_for_shader(shader, 'TRI_FAN', { "pos" : vertices, "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) })
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, _image.bindcode)
    shader.bind()
    shader.uniform_float("opacity", _opacity)
    batch_img.draw(shader)

def mask_pk_scene(_posX, _posY, _width, _height):
    ''' PARA HACER CLAMP Y ENMASCARAR EL CONTENIDO DEL PICKER '''
    glEnable(GL_SCISSOR_TEST)
    glScissor(_posX+10, _posY+10, _width-20, _height-20)
