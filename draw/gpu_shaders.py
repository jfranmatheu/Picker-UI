from ..shaders.image_shaders import (
    image_vertex_shader,
    alpha_image_frag_shader,
    alpha_opacity_image_frag_shader
)
from ..shaders.generic import (
    generic_2d_basic_vertex_shader,
    generic_2d_basic_frag_shader,
    generic_2d_basic_depth_vertex_shader
)
from ..shaders.rectangle_shader import (
    rect_round_frag_shader
)
from ..shaders.point_shaders import (
    circle_fill_vert_shader, circle_fill_depth_vert_shader,
    circle_fill_frag_shader_3,
    circle_fill_aa_smooth_frag_shader,

    circle_fill_smooth_frag_shader,
    circle_fill_smooth_2_frag_shader,
    circle_fill_smooth_3_frag_shader,

    circle_fill_smooth_gradient_radial_frag_shader, circle_fill_smooth_gradient_radial_frag_shader_2,
    circle_fill_smooth_gradient_linear_frag_shader,
    circle_fill_smooth_gradient_linear_horizontal_frag_shader,
    circle_fill_smooth_gradient_linear_vertical_frag_shader,
    circle_fill_smooth_gradient_linear_diagonal_frag_shader,
    circle_fill_smooth_gradient_reflect_frag_shader,
    circle_fill_smooth_gradient_reflect_horizontal_frag_shader,
    circle_fill_smooth_gradient_reflect_vertical_frag_shader,
    circle_fill_smooth_gradient_diamond_frag_shader,

    circle_fill_smooth_outline_frag_shader,
    circle_fill_smooth_outline_gradient_frag_shader
)
from ..shaders.line import (
    LINE_DOTTED_SHADER, LINE_DOTTED_MULTI_SHADER
)

from gpu.shader import from_builtin
from gpu.types import GPUShader


# BUILT-IN SHADERS
shader_2d_image = from_builtin('2D_IMAGE')
shader_2d_color_unif = from_builtin('2D_UNIFORM_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_flat = from_builtin('2D_FLAT_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_2d_color_smooth = from_builtin('2D_SMOOTH_COLOR') # 2D_FLAT_COLOR # 2D_SMOOTH_COLOR
shader_3d_color_unif = from_builtin('3D_UNIFORM_COLOR') # 3D_FLAT_COLOR # 3D_SMOOTH_COLOR

# LINE
shader_2d_line_dotted = GPUShader(*LINE_DOTTED_SHADER)
shader_2d_line_dotted_multi = GPUShader(*LINE_DOTTED_MULTI_SHADER)

# TRIS
shader_2d_generic_basic = GPUShader(generic_2d_basic_vertex_shader, generic_2d_basic_frag_shader)
shader_2d_generic_basic_depth = GPUShader(generic_2d_basic_depth_vertex_shader, generic_2d_basic_frag_shader)

# POINT RECT
shader_2d_rect_round = GPUShader(generic_2d_basic_vertex_shader, rect_round_frag_shader)

# POINT CIRCLE
shader_2d_circle = GPUShader(circle_fill_vert_shader, circle_fill_frag_shader_3)

shader_2d_circle_smooth = GPUShader(circle_fill_vert_shader, circle_fill_smooth_2_frag_shader)
shader_2d_circle_smooth_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_2_frag_shader)
shader_2d_circle_aa_smooth_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_aa_smooth_frag_shader)

shader_2d_circle_smooth_gradient_radial = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_radial_frag_shader)
shader_2d_circle_smooth_gradient_radial_gamma = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_radial_frag_shader_2)
shader_2d_circle_smooth_gradient_radial_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_gradient_radial_frag_shader)

shader_2d_circle_smooth_gradient_linear = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_linear_frag_shader)
shader_2d_circle_smooth_gradient_linear_horizontal = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_linear_horizontal_frag_shader)
shader_2d_circle_smooth_gradient_linear_vertical = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_linear_vertical_frag_shader)
shader_2d_circle_smooth_gradient_linear_diagonal = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_linear_diagonal_frag_shader)
shader_2d_circle_smooth_gradient_linear_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_gradient_linear_frag_shader)

shader_2d_circle_smooth_gradient_reflect = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_reflect_frag_shader)
shader_2d_circle_smooth_gradient_reflect_horizontal = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_reflect_horizontal_frag_shader)
shader_2d_circle_smooth_gradient_reflect_vertical = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_reflect_vertical_frag_shader)
shader_2d_circle_smooth_gradient_reflect_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_gradient_reflect_frag_shader)

shader_2d_circle_smooth_gradient_diamond = GPUShader(circle_fill_vert_shader, circle_fill_smooth_gradient_diamond_frag_shader)
shader_2d_circle_smooth_gradient_diamond_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_gradient_diamond_frag_shader)

shader_2d_circle_smooth_outline = GPUShader(circle_fill_vert_shader, circle_fill_smooth_outline_frag_shader)
shader_2d_circle_smooth_outline_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_outline_frag_shader)

shader_2d_circle_smooth_outline_gradient = GPUShader(circle_fill_vert_shader, circle_fill_smooth_outline_gradient_frag_shader)
shader_2d_circle_smooth_outline_gradient_depth = GPUShader(circle_fill_depth_vert_shader, circle_fill_smooth_outline_gradient_frag_shader)

# IMAGE
shader_image_alpha = GPUShader(image_vertex_shader, alpha_image_frag_shader)
shader_image_alpha_opacity = GPUShader(image_vertex_shader, alpha_opacity_image_frag_shader)
