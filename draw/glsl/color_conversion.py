
"""
// All components are in the range [0…1], including hue.
vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}
"""
"""
// All components are in the range [0…1], including hue.
vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}
"""
"""
public static Color LerpHSV (ColorHSV a, ColorHSV b, float t)
{
 // Hue interpolation
 float h;
 float d = b.h - a.h;
 if (a.h > b.h)
 {
 // Swap (a.h, b.h)
 var h3 = b.h2;
 b.h = a.h;
 a.h = h3;

 d = -d;
 t = 1 - t;
 }

 if (d > 0.5) // 180deg
 {
 a.h = a.h + 1; // 360deg
 h = ( a.h + t * (b.h - a.h) ) % 1; // 360deg
 }
 if (d <= 0.5) // 180deg
 {
 h = a.h + t * d
 }

 // Interpolates the rest
 return new ColorHSV
 (
 h, // H
 a.s + t * (b.s-a.s), // S
 a.v + t * (b.v-a.v), // V
 a.a + t * (b.a-a.a) // A
 );
}
"""

"""
public static Color LerpHSV (ColorHSV a, ColorHSV b, float t)
{
 // Hue interpolation
 float h;
 float d = b.h - a.h;
 if (a.h > b.h)
 {
 // Swap (a.h, b.h)
 var h3 = b.h2;
 b.h = a.h;
 a.h = h3;

 d = -d;
 t = 1 - t;
 }

 if (d > 0.5) // 180deg
 {
 a.h = a.h + 1; // 360deg
 h = ( a.h + t * (b.h - a.h) ) % 1; // 360deg
 }
 if (d <= 0.5) // 180deg
 {
 h = a.h + t * d
 }

 // Interpolates the rest
 return new ColorHSV
 (
 h, // H
 a.s + t * (b.s-a.s), // S
 a.v + t * (b.v-a.v), // V
 a.a + t * (b.a-a.a) // A
 );
}
"""