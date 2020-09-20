
###############
# LINE DOTTED
###############
line_dotted_vertex_shader = '''
uniform mat4 ModelViewProjectionMatrix;

in vec2 position;

void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(position, 0.0, 1.0);
}
'''

line_dotted_fragment_shader = '''
uniform vec4 color;
uniform float factor; // 0.3

void main()
{
    if (step(sin(factor * (gl_FragCoord.x+gl_FragCoord.y)/2.0), 0.5f))
        discard;
    gl_FragColor = color;
}
'''
LINE_DOTTED_SHADER = (line_dotted_vertex_shader, line_dotted_fragment_shader)
###############
###############
# LINE DOTTED MULTI COLOR
###############
line_dotted_multi_fragment_shader = '''
uniform vec4 color_1;
uniform vec4 color_2;
uniform float factor; // 0.3

void main()
{
    if (step(sin(factor * (gl_FragCoord.x+gl_FragCoord.y)/2.0), 0.5f))
        gl_FragColor = color_1;
    else
        gl_FragColor = color_2;
}
'''
LINE_DOTTED_MULTI_SHADER = (line_dotted_vertex_shader, line_dotted_multi_fragment_shader)
###############
###############
