
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