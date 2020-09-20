import bgl

from .polygon import Draw_2D_Rectangle_Rounded_2, Draw_2D_Rectangle, Draw_2D_Rectangle_Frame
from .primitives import Draw_2D_Line, Draw_2D_Lines


def Draw_Checkbox(_x, _y, _size, _value, _color, _hover):
    radius = max(min(_size[0], _size[1]) / 2 - 6, 1)
    if _value:
        if _hover:
            hover_color = (_color[0]+.1, _color[1]+.1, _color[2]+.1, 1)
            Draw_2D_Rectangle_Rounded_2(_x, _y, _size[0], _size[1], hover_color, 2, radius)
            Draw_2D_Rectangle_Rounded_2(_x+1, _y+1, _size[0]-2, _size[1]-2, (.44, .6, .86, 1), 2, radius)
        else:
            Draw_2D_Rectangle_Rounded_2(_x, _y, _size[0], _size[1], _color, 2, radius)
            Draw_2D_Rectangle_Rounded_2(_x+1, _y+1, _size[0]-2, _size[1]-2, (.34, .5, .76, .9), 2, radius)
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
            Draw_2D_Rectangle_Rounded_2(_x, _y, _size[0], _size[1], hover_color, 2, radius)
        else:
            Draw_2D_Rectangle_Rounded_2(_x, _y, _size[0], _size[1], _color, 2, radius)
    #blf.size(0, max(_size[1] - 4, 11), 72) #- 4
    #textsize = blf.dimensions(0, _name)
    #textY = _y + (_size[1] - textsize[1]) * .5
    #if _hover:
    #    Draw_Text(_x + _size[0] + 8, textY, _name, max(_size[1] - 4, 11), 0, 1, 1, 1, 1, True)
    #else:
    #    Draw_Text(_x + _size[0] + 8, textY, _name, max(_size[1] - 4, 11), 0, .9, .9, .9, .9, True)

def Draw_Checkbox_Simple(_x, _y, _width, _height, _value, _color, _tick_color):
    if not _value:
        Draw_2D_Rectangle_Frame(_x, _y, _width, _height, _color)
    else:
        # Calc tick points.
        firstPoint = [_x+1, _y + int(_height/2)]
        midPoint = [_x+int(_width/2), _y + int(_height/3.2)]
        lastPoint = [_x+_width-1, _y+_height-2]
        Draw_2D_Rectangle(_x, _y, _width, _height, _color)
        Draw_2D_Lines(_tick_color, firstPoint, midPoint, midPoint, lastPoint)
        firstPoint[1] -= 1
        midPoint[1] -= 1
        lastPoint[1] -= 1
        Draw_2D_Lines(_tick_color, firstPoint, midPoint, midPoint, lastPoint)
