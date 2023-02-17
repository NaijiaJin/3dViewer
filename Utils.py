from OpenGL.GL import *
import numpy as np


def compile_shader(shader_type, shader_source):
    """
    The function to process and compile shader for GPU
    :param shader_type: vertex or fragment shader
    :param shader_source: shader code
    :return: shader_id
    """

    """
    glCreateShader() allocates memory to store a new shader that is referenced by shader_id 
    glShaderSource() takes the shader script and places it in the newly created shader 
    glCompileShader()  complies the shader into machine code that can be understood by the GPU
    """
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not compile_success:
        """
        checks on the status of the compiler and reports any errors might have in the shader code
        """
        error_message = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error_message = "\n" + error_message.decode("utf-8")
        raise Exception(error_message)
    return shader_id


def create_program(vertex_shader_code, fragment_shader_code):
    """
    Ture the compiled shaders into programs that we can access in code as needed.
    :param vertex_shader_code: vertex shader code
    :param fragment_shader_code: fragment shader code
    :return: program to use in python code to access shaders
    """

    """
    the text files containing our shader code are passed through to the compile_Shader function 
    """
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)

    """
    glCreateProgram creates a new program object that will link our program to the shaders. 
    Because the shaders are separatly compiled items, you must consider them programs outside of the python code. Therefore we need to link to them. 
    program_id has both the vertex shader and fragment shader attached. Then, program_id is used to point our Python program to the executable versions of the vertex and fragment shaders.   
    """
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)

    if not link_success:
        info = glGetShaderInfoLog(program_id)
        print("no link success")
        raise RuntimeError(info)
    """
    glDeletedShader() is called twice to remove the shader source from memory. Once it is contained in the GPU, there's no need to clog up memory with the shader source. 
    """
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id
