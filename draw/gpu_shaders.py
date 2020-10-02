from gpu.shader import from_builtin
from gpu.types import GPUShader as S
from .glsl import *
# GPU Shaders.
shader_2d_image = from_builtin('2D_IMAGE')
shader_2d_color_unif = from_builtin('2D_UNIFORM_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_flat = from_builtin('2D_FLAT_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_smooth = from_builtin('2D_SMOOTH_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_3d_color_unif = from_builtin('3D_UNIFORM_COLOR') # 3D_FLAT_COLOR # 3D_SMOOTH_COLOR
# This is cause a Linux (and maybe MacOS too) shader issue (not in Windows! :))) ).
try:
    gps2ldot = S(*s2ldot)
    gps2ldotmul = S(*s2ldotmul)
except:
    gps2ldot = shader_2d_color_unif
    gps2ldotmul = shader_2d_color_unif
gps2gen = S(vs2gen, fs2gen)
gps2gendep = S(vs2gendep, fs2gen)
gps2rr = S(vs2gen, fs2rr)
gps2c = S(vs2c, fs2c3)
gps2cs = S(vs2c, fs2cs2)
gps2csdep = S(vs2cdep, fs2cs2)
gps2caasdep = S(vs2cdep, fs2caas)
gpgps2csgrd = S(vs2c, fs2csgrd)
gps2csgrdgam = S(vs2c, fs2csgrd2)
gps2csgrddep = S(vs2cdep, fs2csgrd)
gps2csgln = S(vs2c, fs2csgln)
gps2csglnh = S(vs2c, fs2csglnh)
gps2csglnv = S(vs2c, fs2csglnv)
gps2csglnd = S(vs2c, fs2csglnd)
gps2csglndep = S(vs2cdep, fs2csgln)
gps2csgrf = S(vs2c, fs2csgrf)
gps2csgrfh = S(vs2c, fs2csgrfh)
gps2csgrfv = S(vs2c, fs2csgrfv)
gps2csgrfdep = S(vs2cdep, fs2csgrf)
gps2csgdm = S(vs2c, fs2csgdm)
gps2csgdmdep = S(vs2cdep, fs2csgdm)
gps2csout = S(vs2c, fs2csout)
gps2csoutdep = S(vs2cdep, fs2csout)
gps2csoutg = S(vs2c, fs2csoutg)
gps2csoutgdep = S(vs2cdep, fs2csoutg)
gps2ia = S(vs2i, fs2ia)
gps2iao = S(vs2i, fs2iao)