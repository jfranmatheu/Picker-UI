from .primitives import dr2dl_Dotted, dr2dl_Dotted_MultiColor

def Draw_2D_Frame_Line_Dotted(_x, _y, _width, _height, _color, _line_width=2, _factor=.3):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    dr2dl_Dotted(_color, _line_width, _factor,
                  A, B,
                  B, D,
                  D, C,
                  C, A)

def Draw_2D_Frame_Line_Dotted_MultiColor(_x, _y, _width, _height, _color1, _color2, _line_width=2, _factor=.3):
    A = (_x, _y)
    B = (_x, _y + _height)
    C = (_x + _width, _y)
    D = (_x + _width, _y + _height)
    dr2dl_Dotted_MultiColor(_color1, _color2, _line_width, _factor,
                  A, B,
                  B, D,
                  D, C,
                  C, A)
