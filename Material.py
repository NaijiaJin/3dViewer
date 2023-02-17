from Utils import *


class Material:
    """
    Shaders are linked to models by the use of materials. A material becomes a component of a mesh, just like a transform.
    It specifies how the mesh is to be rendered. This means we can select which shader to use on a model as well as change it.
    Different models can have different shaders.
    """

    def __init__(self, vertex_shader, fragment_shader):
        """
        The material will take the vertex adn fragment code that we create, and run it through the shader creation methods we added in the Utils.py
        :param vertex_shader: vertex shader script
        :param fragment_shader: fragment shader script
        :return: create shader through Utils.py
        """
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        vertex_shader_file = open(self.vertex_shader).read()
        print("*******************************Vertex Shader*******************************************")
        print(vertex_shader_file)
        print("*******************************Fragment Shader******************************************")
        fragment_shader_file = open(self.fragment_shader).read()
        print(fragment_shader_file)
        self.program_id = create_program(vertex_shader_file, fragment_shader_file)

    def use(self):
        """
        The glUseProgram() function sets the current rendering state to sue the associated shader code to process the drawing of the model
        """
        glUseProgram(self.program_id)
