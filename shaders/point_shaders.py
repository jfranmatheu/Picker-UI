
circle_fill_vert_shader = """
uniform mat4 ModelViewProjectionMatrix;
uniform float size;

in vec2 pos;

void main()
{
  gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
  gl_PointSize = size;
}
"""

circle_fill_depth_vert_shader = """
uniform mat4 ModelViewProjectionMatrix;
uniform float size;
uniform float depth;

in vec2 pos;

void main()
{
  gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
  gl_Position.z = depth / 100 - .1; // Debe ser inferior a 0.92 o así por tanto hay que restarle para asegurar...
  gl_PointSize = size;
}
"""

circle_fill_frag_shader_1 = """
uniform vec4 color;

void main()
{
  float dist = length(gl_PointCoord - vec2(0.5)); // First method.

  vec4 co = vec4(1.0);
  co.rgb = color.rgb;
  co.a = mix(color.a, 0.0, smoothstep(.5, .5, dist));

  if (co.a == 1.0) {
    discard;
  }
  gl_FragColor = co;
}
"""

circle_fill_frag_shader_2 = """
uniform vec4 color;

float circleshape(vec2 _pos, float _radius){
    return step(_radius, length(_pos - vec2(0.5)));
}

void main()
{
  vec4 co = vec4(1.0);
  co.rgb = color.rgb;
  co.a = circleshape(gl_PointCoord, .5); // Second method.

  if (co.a == 1.0) {
    discard;
  }
  gl_FragColor = co;
}
"""

circle_fill_frag_shader_3 = """
uniform vec4 color;

void main()
{
  vec2 coord = gl_PointCoord - vec2(0.5);  // from [0,1] to [-0.5,0.5]
  if(length(coord) > 0.5)                  // outside of circle radius?
    discard;

  gl_FragColor = color;
}
"""

######################
#  SMOOTH
######################

circle_fill_smooth_frag_shader = """
precision mediump float;
uniform vec4 color;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  gl_FragColor = color * alpha;
}
"""

# Smoothed with hard edges.
circle_fill_smooth_2_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

uniform vec4 color;

float roundedFrame (float d, float thickness)
{
  return smoothstep(0.55, 0.45, abs(d / thickness) * 5.0);
}

void main()
{
    float r = 0.0;
    vec2 cxy = 2.0 * gl_PointCoord - 1.0;
    r = dot(cxy, cxy);

    float s = roundedFrame(r, 9.5);
    if (s < 0.05)
      discard;
    gl_FragColor = color;
    gl_FragColor.a *= s;
}
"""

# Smoothed with soft edges. really nice gradient outline BEVEL FX LIKE.
circle_fill_smooth_3_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

uniform vec4 color;

float roundedRectangle (float d, float thickness)
{
  return smoothstep(0.66, 0.33, d / thickness * 5.0);
}

void main()
{
    float r = 0.0;
    vec2 cxy = 2.0 * gl_PointCoord - 1.0;
    r = dot(cxy, cxy);

    float s = roundedRectangle(r, 8);
    gl_FragColor = color;
    gl_FragColor.a *= s;
}
"""

###################
# OUTLINE
###################

circle_fill_outline_frag_shader_3 = """
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]

void main()
{
  vec2 coord = gl_PointCoord - vec2(0.5);  // from [0,1] to [-0.5,0.5]ç
  float len = length(coord);
  if(len > 0.5)                  // outside of circle radius?
    discard;
  if (len > outline_factor)
    gl_FragColor = outline;
  else
    gl_FragColor = color;
}
"""

###################
# OUTLINE + SMOOTH
###################

circle_fill_smooth_outline_frag_shader = """
precision mediump float;
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  if (r > outline_factor)
    gl_FragColor = outline_color * alpha;
  else
    gl_FragColor = color * alpha;
}
"""


###################
# SMOOTH + OUTLINE + GRADIENT aka blur
###################

circle_fill_smooth_outline_gradient_frag_shader = """
precision mediump float;
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]
uniform float outline_blur;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  if (outline_blur == 1){
    gl_FragColor = mix(color, outline_color, r+(1-outline_factor)) * alpha;
  }
  else{
    if (r > outline_factor)
      gl_FragColor = outline_color * alpha;
    else
      gl_FragColor = color * alpha;
  }
}
"""

circle_fill_smooth_outline_gradient_frag_shader_2 = """
precision mediump float;
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]
uniform float outline_blur;

vec4 ColorLerp(vec4 a, vec4 b, float t)
{
  return vec4(
    a.r + (b.r - a.r) * t,
    a.g + (b.g - a.g) * t,
    a.b + (b.b - a.b) * t,
    a.a + (b.a - a.a) * t
  );
}

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  if (outline_blur == 1){
    gl_FragColor = ColorLerp(color, outline_color, r) * alpha;
  }
  else{
    if (r > outline_factor)
      gl_FragColor = outline_color * alpha;
    else
      gl_FragColor = color * alpha;
  }
}
"""

###################
# SMOOTH + GRADIENT
###################

# RADIAL (ORIGINAL GAMMA)
circle_fill_smooth_gradient_radial_frag_shader_2 = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  gl_FragColor = mix(color, second_color, r+factor); // * alpha

  // Gamma correct.
  // gl_FragColor.rgb = pow(gl_FragColor.rgb, vec3(.454545)); // 1.0/2.2
  gl_FragColor.a *= alpha;
}
"""

# RADIAL (CORRECTED GAMMA / TRUE LINEAR GRADIENT)
circle_fill_smooth_gradient_radial_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

float PI_4 = 0.785398;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  // Method 1:
  // gl_FragColor = mix(color, second_color, pow(r, asin(factor)));

  // Method 2:
  // gl_FragColor = mix(color, second_color, r*(1+factor));

  // Method 3:
  //if (factor > 0)
  //  gl_FragColor = mix(color, second_color, step(r, factor));
  //else
  //  gl_FragColor = mix(color, second_color, pow(r, 1+factor));

  // Method 4:
  gl_FragColor = mix(color, second_color, pow(r, tan(factor*PI_4+PI_4)));

  // Gamma correct.
  gl_FragColor.rgb = pow(gl_FragColor.rgb, vec3(0.454545)); // 1.0/2.2
  gl_FragColor.a *= alpha;
}
"""
# float k = cos(cxy.x+factor) - sin(cxy.y+factor);
# float k = cos(cxy.x+factor) - sin(cxy.y-factor); // same as before but more cool cause direction.
# float k = cos(cxy.x+factor) - cos(cxy.y+factor); // switch diagonal side.
# float k = cxy.x * cos(factor) / factor - cxy.y * sin(factor) / factor; // pivot rotation in top middle (limpia cristal coche) (sin sumas el pivote estaría abajo).
# float k = cxy.x * cos(factor) / factor - cxy.y * sin(factor) / factor + 1.0; // pivot rotation center.

# float f = clamp(abs(cxy.x)/.9, 0.0, 1.0) - clamp(abs(cxy.y)/.9, 0.0, 1.0) + factor;
##float k = f * cos(rotation) - f * sin(rotation);

# float f = clamp(abs(cxy.x)/.9, 0.0, 1.0) - clamp(abs(cxy.y)/.9, 0.0, 1.0) + factor; // Spikes/tris que se juntan/separan, hay 2 direcciones nada más.
## float k = f * cos(rotation) - f * sin(rotation) + 1.0;

# LINEAR WITH ROTATION
circle_fill_smooth_gradient_linear_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
uniform float rotation;

float PI_4 = 0.785398;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  // float k = (cxy.x + factor) * cos(rotation) - (cxy.y + factor) * sin(rotation) + 1.0;
  // gl_FragColor = mix(color, second_color, (cxy.x + factor) * cos(rotation) - (cxy.y + factor) * sin(rotation) + 1.0);  // * alpha

  float k = cxy.x * cos(rotation) - cxy.y * sin(rotation);
  gl_FragColor = mix(color, second_color, pow((k+1)/2, tan(factor*PI_4+PI_4)));

  // Gamma correct.
  gl_FragColor.rgb =  pow(gl_FragColor.rgb, vec3(0.454545)); // 1.0/2.2
  gl_FragColor.a *= alpha + (0 * rotation);
}
"""
# LINEAR HORIZONTAL
circle_fill_smooth_gradient_linear_horizontal_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  gl_FragColor = mix(color, second_color, cxy.x + factor) * alpha; // Intensity: cxy.y*1.5
}
"""
# LINEAR VERTICAL
circle_fill_smooth_gradient_linear_vertical_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  gl_FragColor = mix(color, second_color, cxy.y + factor) * alpha; // Intensity: cxy.y*1.5
}
"""
# LINEAR DIAGONAL
circle_fill_smooth_gradient_linear_diagonal_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  gl_FragColor = mix(color, second_color, cxy.y+cxy.x+factor) * alpha; // Intensity: cxy.y*1.5
}
"""
# REFLECTED WITH ROTATION
circle_fill_smooth_gradient_reflect_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
uniform float rotation;
float PI_4 = 0.785398;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  // (cxy.x + factor) * cos(rotation) - (cxy.y + factor) * sin(rotation) + 1.0

  // float k = (cxy.x + factor) * cos(rotation) - (cxy.y + factor) * sin(rotation);
  // gl_FragColor = mix(color, second_color, abs(k)); // * alpha;

  float k = cxy.x * cos(rotation) - cxy.y * sin(rotation);
  gl_FragColor = mix(color, second_color, pow(abs(k), tan(factor*PI_4+PI_4)));

  // Gamma correction.
  gl_FragColor.rgb =  pow(gl_FragColor.rgb, vec3(0.454545)); // 1.0/2.2
  gl_FragColor.a *= alpha;
}
"""
# REFLECTED HORIZONTAL
circle_fill_smooth_gradient_reflect_horizontal_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  gl_FragColor = mix(color, second_color, clamp(abs(cxy.x)/.9, 0.0, 1.0)+factor) * alpha; // Intensity: cxy.y*1.5
}
"""
# REFLECTED VERTICAL
circle_fill_smooth_gradient_reflect_vertical_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  gl_FragColor = mix(color, second_color, clamp(abs(cxy.y)/.9, 0.0, 1.0)+factor) * alpha; // Intensity: cxy.y*1.5
}
"""
# DIAMOND WITH ROTATION
circle_fill_smooth_gradient_diamond_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
uniform float rotation;
float PI_4 = 0.785398;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  // float k = abs(cxy.x + factor) * cos(rotation) - abs(cxy.y + factor) * sin(rotation)+1.0;
  // gl_FragColor = mix(color, second_color, clamp(k/.9, 0.0, 1.0)); // * alpha;

  float k = abs(cxy.x) * cos(rotation) - abs(cxy.y) * sin(rotation) + .5;
  gl_FragColor = mix(color, second_color, pow(clamp(k/.5, 0.0, 1.0), tan(factor*PI_4+PI_4)));

  // Gamma correction.
  gl_FragColor.rgb =  pow(gl_FragColor.rgb, vec3(0.454545)); // 1.0/2.2
  gl_FragColor.a *= alpha;
}
"""
# FLAT - HALF COLOR_1 HALF COLOR_2 (DIAGONAL)
circle_fill_smooth_multicolor_diagonal_frag_shader = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  gl_FragColor = mix(color, second_color, smoothstep(cxy.x-.25, cxy.x, cxy.y)) * alpha;
}
"""

# GRADIENT - DIAGONAL LINE STRIP
# LINEAR VERTICAL
circle_fill_smooth_gradient_linestrip_diagonal = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  float k = smoothstep(cxy.x-1, cxy.x, cxy.y) - smoothstep(cxy.x, cxy.x+1, cxy.y);

  gl_FragColor = mix(color, second_color, k) * alpha;
}
"""

# TEST !!! #
circle_fill_smooth_gradient_test_frag_shader = """
precision mediump float;
//uniform vec4 color;
//uniform vec4 second_color;

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.5) // threshold
    discard;

  vec3 color = vec3(1.0);
  color += 0.1 * 0.1 / r;
  gl_FragColor = vec4(color, (1-r)) * alpha;
}
"""

# TEST 2 !!! # MORE SMOOTH TO ALPHA THAN GRADIENT
circle_fill_smooth_gradient_test2_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

// unsigned round box
float udRoundBox( vec3 p, vec3 b, float r )
{
    return length(max(abs(p)-b,0.0))-r;
}

// substracts shape d1 from shape d2
float opS( float d1, float d2 )
{
    return max(-d1,d2);
}

// to get the border of a udRoundBox, simply substract a smaller udRoundBox !
float udRoundBoxBorder( vec3 p, vec3 b, float r, float borderFactor )
{
    return opS(udRoundBox(p, b*borderFactor, r), udRoundBox(p, b, r));
}

void main()
{
    float r = 0.0;
    vec2 cxy = 2.0 * gl_PointCoord - 1.0;
    r = dot(cxy, cxy);

    float s = udRoundBoxBorder(vec3(cxy, 0.0), vec3(0.0), r, 1.2);
    gl_FragColor = vec4(0., 1., 1., 1-s);
}
"""

##########################
# POLYGON POINT
##########################

polygon_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

const float PI = 3.1415926535;

float polygonshape(vec2 position, float radius, float sides){
    position = position * 2.0;
    float angle = atan(position.x, position.y);
    float slice = PI * 2.0 / sides;

    return step(radius, cos(floor(0.5 + angle / slice) * slice - angle) * length(position));
}

void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.5) // threshold
    discard;

  vec3 color = vec3(0.0);
  float polygon = polygonshape(cxy, 1.7, 5.0);
  if (polygon == 1.0)
    discard;
  color = vec3(polygon);
  gl_FragColor = vec4(color, 1.0);
}
"""

####################
# TEST !!! # RING
####################
ring_test_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

uniform vec4 color;

void main()
{
  // Ring outer.
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;

  // Ring inner.
  r = r * 0.9;
  delta = fwidth(r);
  alpha = 1 - smoothstep(.9 - delta, .9 + delta, r);
  if (alpha > 0.9999) // threshold
    discard;

  gl_FragColor = color * alpha;
}
"""

####################
# SQUARE PERFECT + OUTLINE
####################
square_outline_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor;

void main()
{
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;

  // float aspect = 1; // For not perfect squares aka rectangles...
  float maxX = 1.0 - outline_factor;
  float minX = outline_factor - 1.0;
  float maxY = maxX; // / aspect;
  float minY = minX; // / aspect;

  if (cxy.x < maxX && cxy.x > minX &&
      cxy.y < maxY && cxy.y > minY)
  {
    gl_FragColor = color;
  }
  else
  {
    gl_FragColor = outline_color;
  }
}
"""

###################
# CIRCLE AA SMOOTH
###################
# Try_DrwRR_AA(o, 64, .008, .8, 1, (0, 1, 1, 1), (.5, .5, .5, 1))
circle_fill_aa_smooth_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

uniform float r; // Factor del radio del círculo para hacer el clamping.
uniform float f; // Factor para desenfocar el borde (0-1, siendo 0 nada).
uniform float c; // Factor de curvatura para rectangulo (siendo 0 desactivarlo y crear un círculo).
uniform vec4 co; // Color.

void main()
{
  if (co.a == 0)
    discard;
  // Use polar coordinates instead of cartesian
  vec2 toCenter = vec2(0.5)-gl_PointCoord.xy;
  float radius = length(toCenter)*2.0;

  if (c != 0){
    vec2 cxy = gl_PointCoord; //2.0 * gl_PointCoord - .5;

    float corner = cxy.x * cxy.y * (1.-cxy.x) * (1.-cxy.y);
    if (corner < r) // pow(.2, 3) 0.008
      discard;
    radius = smoothstep(f, 1, clamp(corner*100*f, 0., 1.));
    gl_FragColor = co;
    gl_FragColor.a = radius;
  }
  else if (radius > r)
    discard;
  else{
    gl_FragColor = co;
    gl_FragColor.a *= smoothstep(r, r-f, radius);
  }
}
"""

#######################
# TEST !!! # Square Smooth Rounded Top Left Corner
#######################
square_smooth_top_left_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

// This approximates the error function, needed for the gaussian integral
vec4 erf(vec4 x) {
  vec4 s = sign(x), a = abs(x);
  x = 1.0 + (0.278393 + (0.230389 + 0.078108 * (a * a)) * a) * a;
  x *= x;
  return s - s / (x * x);
}

// Return the mask for the shadow of a box from lower to upper
float boxShadow(vec2 lower, vec2 upper, vec2 point, float sigma) {
  vec4 query = vec4(point - lower, upper - point);
  vec4 integral = 0.5 + 0.5 * erf(query * (sqrt(0.5) / sigma));
  return (integral.z - integral.x) * (integral.w - integral.y);
}

void main()
{
  // float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  // r = dot(cxy, cxy);

  // 1st try.
  // vec2 lower = vec2(-0.5);
  // vec2 upper = vec2(0.5);

  // 2nd try.
  cxy += 1.8;
  vec2 lower = vec2(-1.);
  vec2 upper = vec2(1.);

  float s = boxShadow(lower, upper, cxy, .08);
  //gl_FragColor = vec4(0.0, 1.0, 1.0, 0.0);
  //gl_FragColor.a = s*10;
  gl_FragColor = vec4(vec3(s*10), 1.0)
}
"""

###########################
# TEST !!! Mira de apuntar, ring + dot.
###########################
ringdot_aim_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

float roundedFrame (vec2 pos, float radius, float thickness)
{
  float d = length(pos) - radius;
  return smoothstep(0.55, 0.45, abs(d / thickness) * 5.0);
}

void main()
{
    float r = 0.0;
    vec2 cxy = 2.0 * gl_PointCoord - 1.0;
    r = dot(cxy, cxy);

    float s = roundedFrame(cxy, r+.1, 1.);
    gl_FragColor = vec4(0., 1., 1., s);
}
"""

###########################
# TEST !!! Mira de apuntar, ring + dot.
###########################
circle_dot_frag_shader = """
#ifdef GL_ES
precision mediump float;
#endif

float roundedFrame (float d, float thickness)
{
  return smoothstep(0.55, 0.45, abs(d / thickness) * 5.0);
}

void main()
{
    float r = 0.0;
    vec2 cxy = 2.0 * gl_PointCoord - 1.0;
    r = dot(cxy, cxy);

    float s = roundedFrame(r, .1);
    gl_FragColor = vec4(0., 1., 1., s);
}
"""

