from ..shaders.image_shaders import (
    vs2i,
    fs2ia,
    fs2iao
)
from ..shaders.generic import (
    vs2gen,
    fs2gen,
    vs2gendep
)
from ..shaders.rectangle_shader import (
    fs2rr
)
from ..shaders.point_shaders import (
    vs2c, vs2cdep,
    fs2c3,
    fs2caas,

    fs2cs,
    fs2cs2,
    fs2cs3,

    fs2csgrd, fs2csgrd2,
    fs2csgln,
    fs2csglnh,
    fs2csglnv,
    fs2csglnd,
    fs2csgrf,
    fs2csgrfh,
    fs2csgrfv,
    fs2csgdm,

    fs2csout,
    fs2csoutg
)
from ..shaders.line import (
    s2ldot, s2ldotmul
)

from gpu.shader import from_builtin
from gpu.types import GPUShader as Shader


# BUILT-IN SHADERS
shader_2d_image = from_builtin('2D_IMAGE')
shader_2d_color_unif = from_builtin('2D_UNIFORM_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_flat = from_builtin('2D_FLAT_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_smooth = from_builtin('2D_SMOOTH_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_3d_color_unif = from_builtin('3D_UNIFORM_COLOR') # 3D_FLAT_COLOR # 3D_SMOOTH_COLOR

# LINE
try:
    gps2ldot = Shader(*s2ldot)
    gps2ldotmul = Shader(*s2ldotmul)
except:
    gps2ldot = shader_2d_color_unif
    gps2ldotmul = shader_2d_color_unif

# TRIS
gps2gen = Shader(vs2gen, fs2gen)
gps2gendep = Shader(vs2gendep, fs2gen)

# POINT RECT
gps2rr = Shader(vs2gen, fs2rr)

# POINT CIRCLE
gps2c = Shader(vs2c, fs2c3)

gps2cs = Shader(vs2c, fs2cs2)
gps2csdep = Shader(vs2cdep, fs2cs2)
gps2caasdep = Shader(vs2cdep, fs2caas)

gpgps2csgrd = Shader(vs2c, fs2csgrd)
gps2csgrdgam = Shader(vs2c, fs2csgrd2)
gps2csgrddep = Shader(vs2cdep, fs2csgrd)

gps2csgln = Shader(vs2c, fs2csgln)
gps2csglnh = Shader(vs2c, fs2csglnh)
gps2csglnv = Shader(vs2c, fs2csglnv)
gps2csglnd = Shader(vs2c, fs2csglnd)
gps2csglndep = Shader(vs2cdep, fs2csgln)

gps2csgrf = Shader(vs2c, fs2csgrf)
gps2csgrfh = Shader(vs2c, fs2csgrfh)
gps2csgrfv = Shader(vs2c, fs2csgrfv)
gps2csgrfdep = Shader(vs2cdep, fs2csgrf)

gps2csgdm = Shader(vs2c, fs2csgdm)
gps2csgdmdep = Shader(vs2cdep, fs2csgdm)

gps2csout = Shader(vs2c, fs2csout)
gps2csoutdep = Shader(vs2cdep, fs2csout)

gps2csoutg = Shader(vs2c, fs2csoutg)
gps2csoutgdep = Shader(vs2cdep, fs2csoutg)

# IMAGE
gps2ia = Shader(vs2i, fs2ia)
gps2iao = Shader(vs2i, fs2iao)
