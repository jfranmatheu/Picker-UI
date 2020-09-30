import bgl

from .polygon import dr2drr_2, dr2dr, dr2drf
from .primitives import Draw_2D_Line, dr2dl


def drcbx(_x, _y, _size, _value, _color, _hover):
    radius = max(min(_size[0], _size[1]) / 2 - 6, 1)
    if _value:
        if _hover:
            hover_color = (_color[0]+.1, _color[1]+.1, _color[2]+.1, 1)
            dr2drr_2(_x, _y, _size[0], _size[1], hover_color, 2, radius)
            dr2drr_2(_x+1, _y+1, _size[0]-2, _size[1]-2, (.44, .6, .86, 1), 2, radius)
        else:
            dr2drr_2(_x, _y, _size[0], _size[1], _color, 2, radius)
            dr2drr_2(_x+1, _y+1, _size[0]-2, _size[1]-2, (.34, .5, .76, .9), 2, radius)
        if _size[1] > 12:
            firstPoint = [_x+4, _y + int(_size[1]/2)]
            midPoint = [_x+int(_size[0]/2), _y + int(_size[1]/3.2)]
            lastPoint = [_x+_size[0]-4, _y+_size[1]-4]
            Draw_2D_Line(firstPoint, midPoint, (.8, .8, .8, .8))
            Draw_2D_Line(midPoint, lastPoint, (.8, .8, .8, .8))
            firstPoint[1] -= 1
            midPoint[1] -= 1
            lastPoint[1] -= 1
            Draw_2D_Line(firstPoint, midPoint, (.75, .75, .75, .75))
            Draw_2D_Line(midPoint, lastPoint, (.75, .75, .75, .75))
            firstPoint[1] -= 1
            midPoint[1] -= 1
            lastPoint[1] -= 1
            Draw_2D_Line(firstPoint, midPoint, (.7, .7, .7, .7))
            Draw_2D_Line(midPoint, lastPoint, (.7, .7, .7, .7))
    else:
        if _hover:
            hover_color = (_color[0]+.1, _color[1]+.1, _color[2]+.1, 1)
            dr2drr_2(_x, _y, _size[0], _size[1], hover_color, 2, radius)
        else:
            dr2drr_2(_x, _y, _size[0], _size[1], _color, 2, radius)
    #blf.size(0, max(_size[1] - 4, 11), 72) #- 4
    #textsize = blf.dimensions(0, _name)
    #textY = _y + (_size[1] - textsize[1]) * .5
    #if _hover:
    #    drt(_x + _size[0] + 8, textY, _name, max(_size[1] - 4, 11), 0, 1, 1, 1, 1, True)
    #else:
    #    drt(_x + _size[0] + 8, textY, _name, max(_size[1] - 4, 11), 0, .9, .9, .9, .9, True)

def drcbxsmpl(_x, _y, _width, _height, _value, _color, _tick_color):
    if not _value:
        dr2drf(_x, _y, _width, _height, _color)
    else:
        # Calc tick points.
        firstPoint = [_x+1, _y + int(_height/2)]
        midPoint = [_x+int(_width/2), _y + int(_height/3.2)]
        lastPoint = [_x+_width-1, _y+_height-2]
        dr2dr(_x, _y, _width, _height, _color)
        dr2dl(_tick_color, firstPoint, midPoint, midPoint, lastPoint)
        firstPoint[1] -= 1
        midPoint[1] -= 1
        lastPoint[1] -= 1
        dr2dl(_tick_color, firstPoint, midPoint, midPoint, lastPoint)
