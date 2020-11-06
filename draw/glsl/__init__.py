vs2gen = '''
    uniform mat4 ModelViewProjectionMatrix;
    in vec2 pos;
    uniform vec4 color;
    out vec4 col;
    void main()
    {
        gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0, 1.0);
        gl_Position.z = -1.0;
        col = color;
    }
'''
vs2gendep = '''
    uniform mat4 ModelViewProjectionMatrix;
    in vec2 pos;
    uniform vec4 color;
    uniform float depth;
    out vec4 col;
    void main()
    {
        gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
        gl_Position.z = -.999999 + depth / 100; // depth / 100 - .1; // Debe ser inferior a 0.92 o así por tanto hay que restarle para asegurar...
        col = color;
    }
'''
fs2gen = '''
    // uniform vec4 color;
    in vec4 col;
    out vec4 co;
    void main()
    {
        co = col;
    }
'''
fs2rr = """
    varying vec4 v_color;
    varying vec2 v_texCoord0;
    uniform vec2 u_resolution;
    uniform vec2 u_screenOffset;
    uniform sampler2D u_sampler2D;
    const float max = pow(0.2, 4);
    out vec4 co;
    void main()
    {
        vec2 pos = (gl_FragCoord.xy - u_screenOffset) / u_resolution;
        float vignette = pos.x * pos.y * (1.-pos.x) * (1.-pos.y);
        vec4 color = texture2D(u_sampler2D, v_texCoord0) * v_color;
        color.rgb = color.rgb * smoothstep(0, max, vignette);
        co = color;
    }
"""
fs2rf = """
//---------------------------------------------------------
// draw rectangle frame with rounded edges
//---------------------------------------------------------
float roundedFrame (vec2 pos, vec2 size, float radius, float thickness)
{
  float d = length(max(abs(uv - pos),size) - size) - radius;
  return smoothstep(0.55, 0.45, abs(d / thickness) * 5.0);
}
uniform vec4 color;
in vec4 col;
out vec4 co;
void main()
{
    co = col;
}
"""
fs2plight = """
precision mediump float;
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
  color += 0.1 * 0.1 / r;
  gl_FragColor = vec4(color, 1.0); // apply alpha: (1-r) or r
}
"""
fs2plightc = """
precision mediump float;
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
  for(int i = 0; i < 40; i++){
    float radius = 0.3;
    float rad = radians(360.0 / 40.0) * float(i);
    color += 0.003 / length(cxy + vec2(radius * cos(rad), radius * sin(rad)));
  }
  gl_FragColor = vec4(color, 1.0-r); // alpha: 1.0
}
"""
vs2i = '''
    uniform mat4 ModelViewProjectionMatrix;
    /* Keep in sync with intern/opencolorio/gpu_shader_display_transform_vertex.glsl */
    in vec2 texCoord;
    in vec2 pos;
    out vec2 texCoord_interp;
    void main()
    {
        gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0f, 1.0f);
        gl_Position.z = 1.0;
        texCoord_interp = texCoord;
    }
'''
fs2ia = '''
    in vec2 texCoord_interp;
    out vec4 fragColor;
    uniform sampler2D image;
    void main()
    {
        vec4 texColor = texture(image, texCoord_interp);
        if(texColor.a < 0.05)
            discard;
        fragColor = texColor;
    }
'''
fs2iao = '''
    in vec2 texCoord_interp;
    out vec4 fragColor;
    uniform sampler2D image;
    uniform float opacity;
    void main()
    {
        vec4 texColor = texture(image, texCoord_interp);
        if(texColor.a < 0.05)
            discard;
        if(texColor.a > opacity)
            texColor.a = opacity;
        fragColor = texColor;
    }
'''
fs2iaoex = '''
    in vec2 texCoord_interp;
    out vec4 fragColor;
    uniform sampler2D image;
    uniform float opacity;
    uniform vec3 exclude_color;
    void main()
    {
        vec4 texColor = texture(image, texCoord_interp);
        if(texColor.a < 0.1)
            discard;
        if(textColor.rgb == exclude_color)
            discard;
        if(texColor.a > opacity)
            texColor.a = opacity;
        fragColor = texColor;
    }
'''

vs2ldot = '''
uniform mat4 ModelViewProjectionMatrix;
in vec2 position;
void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(position, 0.0, 1.0);
}
'''
fs2ldot = '''
uniform vec4 color;
uniform float factor; // 0.3
out vec4 co;
void main()
{
    if (step(sin(factor * (gl_FragCoord.x+gl_FragCoord.y)/2.0), 0.5f))
        discard;
    co = color;
}
'''
s2ldot = (vs2ldot, fs2ldot)
fs2ldotmul = '''
uniform vec4 color_1;
uniform vec4 color_2;
uniform float factor; // 0.3
out vec4 co;
void main()
{
    if (step(sin(factor * (gl_FragCoord.x+gl_FragCoord.y)/2.0), 0.5f))
        co = color_1;
    else
        co = color_2;
}
'''
s2ldotmul = (vs2ldot, fs2ldotmul)
vs2c = """
uniform mat4 ModelViewProjectionMatrix;
uniform float size;
in vec2 pos;
void main()
{
  gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
  gl_PointSize = size;
}
"""
vs2cdep = """
uniform mat4 ModelViewProjectionMatrix;
uniform float size;
uniform float depth;
in vec2 pos;
void main()
{
  gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
  gl_Position.z = -1.0 + depth / 100; // Debe ser inferior a 0.92 o así por tanto hay que restarle para asegurar...
  gl_PointSize = size;
}
"""
fs2c1 = """
uniform vec4 color;
out vec4 co;
void main()
{
  float dist = length(gl_PointCoord - vec2(0.5)); // First method.
  vec4 col = vec4(1.0);
  col.rgb = color.rgb;
  col.a = mix(color.a, 0.0, smoothstep(.5, .5, dist));
  if (col.a == 1.0) {
    discard;
  }
  co = col;
}
"""
fs2c2 = """
uniform vec4 color;
out vec4 co;
float circleshape(vec2 _pos, float _radius){
    return step(_radius, length(_pos - vec2(0.5)));
}
void main()
{
  vec4 col = vec4(1.0);
  col.rgb = color.rgb;
  col.a = circleshape(gl_PointCoord, .5); // Second method.

  if (col.a == 1.0) {
    discard;
  }
  co = col;
}
"""
fs2c3 = """
uniform vec4 color;
out vec4 co;
void main()
{
  vec2 coord = gl_PointCoord - vec2(0.5);  // from [0,1] to [-0.5,0.5]
  if(length(coord) > 0.5)                  // outside of circle radius?
    discard;

  co = color;
}
"""
fs2cs = """
precision mediump float;
uniform vec4 color;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = color * alpha;
}
"""
fs2cs2 = """
#ifdef GL_ES
precision mediump float;
#endif
uniform vec4 color;
out vec4 co;
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
    co = color;
    co.a *= s;
}
"""
fs2cs3 = """
#ifdef GL_ES
precision mediump float;
#endif
uniform vec4 color;
out vec4 co;
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
    co = color;
    co.a *= s;
}
"""
fs2cout3 = """
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]
out vec4 co;
void main()
{
  vec2 coord = gl_PointCoord - vec2(0.5);  // from [0,1] to [-0.5,0.5]ç
  float len = length(coord);
  if(len > 0.5)                  // outside of circle radius?
    discard;
  if (len > outline_factor)
    co = outline;
  else
    co = color;
}
"""
fs2csout = """
precision mediump float;
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]
out vec4 co;
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
    co = outline_color * alpha;
  else
    co = color * alpha;
}
"""
fs2csoutg = """
precision mediump float;
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]
uniform float outline_blur;
out vec4 co;
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
    co = mix(color, outline_color, r+(1-outline_factor)) * alpha;
  }
  else{
    if (r > outline_factor)
      co = outline_color * alpha;
    else
      co = color * alpha;
  }
}
"""
fs2csoutg_2 = """
precision mediump float;
uniform vec4 color;
uniform vec4 outline_color;
uniform float outline_factor; // between [-0.5, 0.5], ideal [-0.4, 0.4]
uniform float outline_blur;
out vec4 co;
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
    co = ColorLerp(color, outline_color, r) * alpha;
  }
  else{
    if (r > outline_factor)
      co = outline_color * alpha;
    else
      co = color * alpha;
  }
}
"""
fs2csgrd2 = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = mix(color, second_color, r+factor);
  co.a *= alpha;
}
"""
fs2csgrd = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
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
  // co = mix(color, second_color, pow(r, asin(factor)));
  // Method 2:
  // co = mix(color, second_color, r*(1+factor));
  // Method 3:
  //if (factor > 0)
  //  co = mix(color, second_color, step(r, factor));
  //else
  //  co = mix(color, second_color, pow(r, 1+factor));
  // Method 4:
  co = mix(color, second_color, pow(r, tan(factor*PI_4+PI_4)));
  // Gamma
  co.rgb = pow(co.rgb, vec3(0.454545)); // 1.0/2.2
  co.a *= alpha;
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
fs2csgln = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
uniform float rotation;
out vec4 co;
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
  // co = mix(color, second_color, (cxy.x + factor) * cos(rotation) - (cxy.y + factor) * sin(rotation) + 1.0);  // * alpha
  float k = cxy.x * cos(rotation) - cxy.y * sin(rotation);
  co = mix(color, second_color, pow((k+1)/2, tan(factor*PI_4+PI_4)));
  // Gamma.
  co.rgb =  pow(co.rgb, vec3(0.454545)); // 1.0/2.2
  co.a *= alpha + (0 * rotation);
}
"""
fs2csglnh = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = mix(color, second_color, cxy.x + factor) * alpha; // Intensity: cxy.y*1.5
}
"""
fs2csglnv = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = mix(color, second_color, cxy.y + factor) * alpha; // Intensity: cxy.y*1.5
}
"""
fs2csglnd = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = mix(color, second_color, cxy.y+cxy.x+factor) * alpha; // Intensity: cxy.y*1.5
}
"""
fs2csgrf = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
uniform float rotation;
float PI_4 = 0.785398;
out vec4 co;
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
  // co = mix(color, second_color, abs(k)); // * alpha;
  float k = cxy.x * cos(rotation) - cxy.y * sin(rotation);
  co = mix(color, second_color, pow(abs(k), tan(factor*PI_4+PI_4)));
  // Gamma.
  co.rgb =  pow(co.rgb, vec3(0.454545)); // 1.0/2.2
  co.a *= alpha;
}
"""
fs2csgrfh = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = mix(color, second_color, clamp(abs(cxy.x)/.9, 0.0, 1.0)+factor) * alpha; // Intensity: cxy.y*1.5
}
"""
fs2csgrfv = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
out vec4 co;
void main()
{
  float r = 0.0, delta = 0.0, alpha = 0.0;
  vec2 cxy = 2.0 * gl_PointCoord - 1.0;
  r = dot(cxy, cxy);
  delta = fwidth(r);
  alpha = 1.0 - smoothstep(1.0 - delta, 1.0 + delta, r);
  if (alpha < 0.1) // threshold
    discard;
  co = mix(color, second_color, clamp(abs(cxy.y)/.9, 0.0, 1.0)+factor) * alpha; // Intensity: cxy.y*1.5
}
"""
fs2csgdm = """
precision mediump float;
uniform vec4 color;         // vec4(1.,0.5,1.,1.)
uniform vec4 second_color;  // vec4(0.,0.,0.,1.)
uniform float factor;
uniform float rotation;
float PI_4 = 0.785398;
out vec4 co;
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
  // co = mix(color, second_color, clamp(k/.9, 0.0, 1.0)); // * alpha;
  float k = abs(cxy.x) * cos(rotation) - abs(cxy.y) * sin(rotation) + .5;
  co = mix(color, second_color, pow(clamp(k/.5, 0.0, 1.0), tan(factor*PI_4+PI_4)));
  // Gamma.
  co.rgb =  pow(co.rgb, vec3(0.454545)); // 1.0/2.2
  co.a *= alpha;
}
"""
fs2caas = """
#ifdef GL_ES
precision mediump float;
#endif

uniform float r; // Factor del radio del círculo para hacer el clamping.
uniform float f; // Factor para desenfocar el borde (0-1, siendo 0 nada).
uniform float c; // Factor de curvatura para rectangulo (siendo 0 desactivarlo y crear un círculo).
uniform vec4 co; // Color.
out vec4 coout;
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
    coout = co;
    coout.a = radius;
  }
  else if (radius > r)
    discard;
  else{
    coout = co;
    coout.a *= smoothstep(r, r-f, radius);
  }
}
"""