from enum import Enum


class ColorsRGBA(Enum):
    TRANSPARENT = (0, 0, 0, 0)

    # BASIC
    Black = (0, 0, 0, 1)
    White = (1, 1, 1, 1)
    Red = (1, 0, 0, 1)
    Green = (0, 1, 0, 1)
    Blue = (0, 0, 1, 1)
    # CYAN DERIVATES
    Cyan = (0, 1, 1, 1)
    Aquamarine = (.498, 1, .831, 1)
    Turquoise = (.251, .878, .816, 1)
    # ORANGE DERIVATES
    Orange = (1, .647, 0, 1)
    Orange_Dark = (1, .549, 0, 1)
    Orange_Red = (1, .27, 0, 1)
    Gold = (1, .843, 0, 1)
    Coral = (1, .498, .314, 1)
    Tomato = (1, .388, .278, 1)

    def __call__(self):
        return self.value
