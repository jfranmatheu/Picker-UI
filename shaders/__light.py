light_point_frag_shader = """
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

light_circle_frag_shader = """
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