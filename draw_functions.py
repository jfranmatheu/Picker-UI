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
    gps2gen,
    gps2ia,
    gps2iao
)
from .draw.rectangle_req import sgeo2rpts, sgeo2ridx


def _dr2dr(_x, _y, _size, _color, shader=gps2gen):
    batch_rect = batch_for_shader(shader, 'TRIS', {"pos" : sgeo2rpts(_x, _y, _size)}, indices=sgeo2ridx)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)

def _dr2drt(_x, _y, _size, _color, _text, _text_color, shader=gps2gen):
    ''' DRAW RECT '''
    batch_rect = batch_for_shader(shader, 'TRIS', {"pos" : sgeo2rpts(_x, _y, _size)}, indices=sgeo2ridx)
    shader.bind()
    shader.uniform_float("color", _color)
    batch_rect.draw(shader)
    ''' DRAW TEXT '''
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
    batch_img = batch_for_shader(shader, 'TRI_FAN', {"pos" : vertices, "texCoord" : ((0, 1), (0, 0), (1, 0), (1, 1))})
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
