from gpu_extras.batch import batch_for_shader
import bgl

from .gpu_shaders import gps2iao, gps2ia


def driao(image, off_x, off_y, _width, _height, _opacity = 1, shader = gps2iao):
    if image.gl_touch():
        raise Exception()
    vertices = (
            (off_x,             _height + off_y),
            (off_x,             off_y),
            (off_x + _width,    off_y),
            (off_x + _width,    _height + off_y)
    )
    batch_img = batch_for_shader(shader, 'TRI_FAN', { "pos" : vertices, "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)
    #bgl.glEnable(bgl.GL_DEPTH_TEST) # DETRÁS
    #bgl.glDisable(bgl.GL_DEPTH_TEST)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)
    shader.bind()
    #shader.uniform_int("image", 0)
    #opacity = shader.uniform_from_name("opacity")
    #color = array([0, 0, 0, _opacity], 'f')
    shader.uniform_float("opacity", _opacity)
    batch_img.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

def dria(image, off_x, off_y, _width, _height, shader=gps2ia):
    if image.gl_touch():
        raise Exception()
    vertices = (
            (off_x,             _height + off_y),
            (off_x,             off_y),
            (off_x + _width,    off_y),
            (off_x + _width,    _height + off_y)
    )
    batch_img = batch_for_shader(shader, 'TRI_FAN', {"pos" : vertices, "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1))})
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)
    batch_img.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)


def driac(image, off_x, off_y, _width, _height, shader=gps2ia):
    if image.gl_touch():
        raise Exception()
    batch_img = batch_for_shader(
        shader, 'TRI_FAN',
        {
            "pos" : (
                    (off_x - _width,    off_y + _height),
                    (off_x - _width,    off_y - _height),
                    (off_x + _width,    off_y - _height),
                    (off_x + _width,    off_y + _height)
                ),
            "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1))
        }
    )
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)
    batch_img.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)
