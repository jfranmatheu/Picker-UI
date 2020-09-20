# STANDARD IMAGE VERT SHADER
image_vertex_shader = '''
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

# ALPHA IMAGE FRAG SHADER
alpha_image_frag_shader = '''
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

# ALPHA OPACITY FRAG SHADER
alpha_opacity_image_frag_shader = '''
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

# ALPHA OPACITY FRAG SHADER + EXCLUDE COLOR
alpha_opacity_exclude_image_frag_shader = '''
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
