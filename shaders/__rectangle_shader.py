rect_round_frag_shader = """
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

rect_frame_frag_shader = """
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
