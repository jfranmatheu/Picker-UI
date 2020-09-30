from mathutils import Vector


# 2             # 3

# 0             # 1
def sgeo2rpts(x, y, s):
    w, h = s
    return [
        (x, y),
        (x+w, y),
        (x, y+h),
        (x+w, y+h)
    ]

def _sgeo2rpts(x, y, w, h):
    return [
        (x, y),
        (x+w, y),
        (x, y+h),
        (x+w, y+h)
    ]

def sgeo2rcpts(x, y, s):
    w, h = s
    return [
        (x-w, y-h),
        (x+w, y-h),
        (x-w, y+h),
        (x+w, y+h)
    ]

def sgeo2rcpts_(x, y, w, h):
    return [
        (x-w, y-h),
        (x+w, y-h),
        (x-w, y+h),
        (x+w, y+h)
    ]

def EvaluateCuadraticBezierCurve(p0, p1, p2, t = .5):
    return (1-t)**2 * p0 + 2*t * (1-t) * p1 + t**2 * p2


    # 6     # 7
# 5             # 8

# 1             # 4
    # 2     # 3
def sgeo2rr2pts(x, y, w, h, r):
    return (
        ( x + w / 2     , y + h / 2 ), # 0 Center
        ( x             , y + r ), # 1 Bot Left up
        ( x + r         , y ), # 2 Bot Left down
        ( x + w - r     , y ), # 3 Bot Right down
        ( x + w         , y + r ), # 4 Bot Right up
        ( x             , y + h - r ), # 5 Top Left down
        ( x + r         , y + h ), # 6 Top Left up
        ( x + w - r     , y + h ), # 7 Top Right up
        ( x + w         , y + h - r ) # 8 Top Right down
    )

# 0             # 3
    # 1     # 2
def sgeo2rr2ptsbot(x, y, w, h, r):
    return (
        ( x             , y + r ), # 0 Bot Left up
        ( x + r         , y ), # 1 Bot Left down
        ( x + w - r     , y ), # 2 Bot Right down
        ( x + w         , y + r ), # 3 Bot Right up
    )


    # 10     # 9
  # 11         # 8
# 12             # 7

# 1             # 6
  # 2         # 5
    # 3     # 4
def sgeo2rr3pts(x, y, w, h, r):
    A = EvaluateCuadraticBezierCurve(Vector((x, y + r)), Vector((x, y)), Vector((x + r, y))) # 2 Bot Left mid
    B = EvaluateCuadraticBezierCurve(Vector((x + w - r, y)), Vector((x + w, y)), Vector((x + w, y + r))) # 5 Bot Right mid
    C = EvaluateCuadraticBezierCurve(Vector((x + w - r, y + h)), Vector((x + w, y + h)), Vector((x + w, y + h - r))) # 8 Top Right mid
    D = EvaluateCuadraticBezierCurve(Vector((x, y + h - r)), Vector((x, y + h)), Vector((x + r, y + h))) # 2 Top Left mid
    return (
        ( x + w / 2     , y + h / 2 ), # 0 Center

        ( x             , y + r ), # 1 Bot Left up
        ( A[0]          , A[1] ), # 2 Bot Left mid
        ( x + r         , y ), # 3 Bot Left down

        ( x + w - r     , y ), # 4 Bot Right down
        ( B[0]          , B[1] ), # 5 Bot Right mid
        ( x + w         , y + r ), # 6 Bot Right up

        ( x + w         , y + h - r ), # 7 Top Right down
        ( C[0]          , C[1] ), # 8 Top Right mid
        ( x + w - r     , y + h ), # 9 Top Right up

        ( x + r         , y + h ), # 10 Top Left up
        ( D[0]          , D[1] ), # 2 Top Left mid
        ( x             , y + h - r ) # 12 Top Left down
    )

# 7             # 6

# 0             # 5
  # 1         # 4
    # 2     # 3
def sgeo2rr3ptsbot(x, y, w, h, r):
    A = EvaluateCuadraticBezierCurve(Vector((x, y + r)), Vector((x, y)), Vector((x + r, y))) # 2 Bot Left mid
    B = EvaluateCuadraticBezierCurve(Vector((x + w - r, y)), Vector((x + w, y)), Vector((x + w, y + r))) # 5 Bot Right mid
    return (
        #( x + w / 2     , y + h / 2 ), # 0 Center

        ( x             , y + r ), # 0 Bot Left up
        ( A[0]          , A[1] ), # 1 Bot Left mid
        ( x + r         , y ), # 2 Bot Left down

        ( x + w - r     , y ), # 3 Bot Right down
        ( B[0]          , B[1] ), # 4 Bot Right mid
        ( x + w         , y + r ), # 5 Bot Right up

        (x + w          , y + h),
        (x              , y + h)
    )

    # 2     # 3
  # 1         # 4
# 0             # 5

# 6             # 7
def sgeo2rr3ptstop(x, y, w, h, r):
    C = EvaluateCuadraticBezierCurve(Vector((x + w - r, y + h)), Vector((x + w, y + h)), Vector((x + w, y + h - r))) # 8 Top Right mid
    D = EvaluateCuadraticBezierCurve(Vector((x, y + h - r)), Vector((x, y + h)), Vector((x + r, y + h))) # 2 Top Left mid
    return (
        #( x + w / 2     , y + h / 2 ), # 0 Center

        ( x + w         , y + h - r ), # 5 Top Right down
        ( C[0]          , C[1] ), # 4 Top Right mid
        ( x + w - r     , y + h ), # 3 Top Right up

        ( x + r         , y + h ), # 2 Top Left up
        ( D[0]          , D[1] ), # 1 Top Left mid
        ( x             , y + h - r ), # 0 Top Left down

        (x              , y),
        (x + w          , y)
    )


# 2             # 3

# 0             # 1
sgeo2ridx = (
    ( 0, 1, 2 ),
    ( 2, 1, 3 )
)
    # 6     # 7
# 5             # 8

# 1             # 4
    # 2     # 3
sgeo2rr2idx = (
    ( 0,  1,  2 ), #
    ( 0,  2,  3 ), #
    ( 0,  3,  4 ),
    ( 0,  4,  8 ),
    ( 0,  8,  7 ),
    ( 0,  7,  6 ),
    ( 0,  6,  5 ),
    ( 0,  5,  1 )
)
# 0             # 3
    # 1     # 2
sgeo2rr2idxbot = (
    ( 3,  1,  2  ), #
    ( 3,  0,  1  ), #
)
    # 10     # 9
  # 11         # 8
# 12             # 7

# 1             # 6
  # 2         # 5
    # 3     # 4
sgeo2rr3idx = (
    ( 0,  1,  2  ), #
    ( 0,  2,  3  ), #
    ( 0,  3,  4  ),
    ( 0,  4,  5  ),
    ( 0,  5,  6  ),
    ( 0,  6,  7  ),
    ( 0,  7,  8  ),
    ( 0,  8,  9  ),
    ( 0,  9, 10  ),
    ( 0, 10, 11  ),
    ( 0, 11, 12  ),
    ( 0, 12,  1  )
)
# 7             # 6

# 0             # 5
  # 1         # 4
    # 2     # 3
sgeo2rr3idxbot = (
    ( 3,  1,  2 ), #
    ( 1,  3,  4 ), #
    ( 1,  4,  5 ),
    ( 0,  1,  5 ),
    ( 0,  5,  6 ),
    ( 0,  6,  7 )
)
    # 2     # 3
  # 1         # 4
# 0             # 5

# 6             # 7
sgeo2rr3idxtop = (
    ( 6,  7,  0 ),
    ( 0,  6,  5 ),
    ( 0,  5,  1 ),
    ( 1,  5,  4 ),
    ( 4,  2,  1 ),
    ( 2,  4,  3 )
)
