# GENERIC FLAT COLOR SHADER
generic_2d_basic_vertex_shader = '''
    uniform mat4 ModelViewProjectionMatrix;
    in vec2 pos;
    uniform vec4 color;
    out vec4 col;

    void main()
    {
        gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
        col = color;
    }
'''

generic_2d_basic_depth_vertex_shader = '''
    uniform mat4 ModelViewProjectionMatrix;
    in vec2 pos;
    uniform vec4 color;
    uniform float depth;
    out vec4 col;

    void main()
    {
        gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
        gl_Position.z = depth / 100 - .1; // Debe ser inferior a 0.92 o así por tanto hay que restarle para asegurar...
        col = color;
    }
'''

generic_2d_basic_frag_shader = '''
    // uniform vec4 color;
    in vec4 col;

    void main()
    {
        gl_FragColor = col;
    }
'''
# gl_FragDepth = -1.0;