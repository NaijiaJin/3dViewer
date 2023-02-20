import numpy
from PySide2.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo  # vertex buffer object
from Material import *
from Uniform import *
from GraphicsData import *
from Camera import *


class GLGeometry(QGLWidget):
    def __init__(self):
        super().__init__()
        self.transformation = None
        self.lookat = None
        self.projection = None
        self.tempVertices = None
        self.shader_id = None
        self.triangle = None
        self.vertexBuffer = None
        self.vertexPosition = None
        self.VAO = None
        self.mat = None
        self.triangleVertexArray = None
        self.scaleZ = 0.0
        self.scaleY = 0.0
        self.scaleX = 0.0
        self.rotateZ = 0.0
        self.rotateY = 0.0
        self.rotateX = 0.0
        self.camera = Camera(60, (1000/600),0.01,10000)


    def setRotX(self, value):
        self.rotateX = value

    def setRotY(self, value):
        self.rotateY = value

    def setRotZ(self, value):
        self.rotateZ = value

    def setScaleX(self, valueX):
        self.scaleX = valueX

    def setScaleY(self, valueY):
        self.scaleY = valueY

    def setScaleZ(self, valueZ):
        self.scaleZ = valueZ


    def initializeGL(self):
        print('gl initial')
        glClearColor(0, 0, 0, 0)
        glColor(1, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.rotateX = 0.0
        self.rotateY = 0.0
        self.rotateZ = 0.0
        self.scaleX = 20.0
        self.scaleY = 20.0
        self.scaleZ = 20.0
        self.tempVertices = np.array([0.5, 0.5, 0.0, 1.0,
                                      -1.5, 0.5, 0.0, 1.0,
                                      0.0, -1.0, 0.0, 1.0], dtype=numpy.float32)

        self.mat = Material("Shaders/vertbasic.glsl", "Shaders/fragbasic.glsl")
        self.shader_id = self.mat.program_id

    def resizeGL(self, w: int, h: int):
        glViewport(0, 0, w, h)
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        gluPerspective(45, w / float(h), 1, 100)
        #glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        self.triangle = GraphicsData("vec3", self.tempVertices)
        self.triangle.create_variable(self.shader_id,"position")

        self.mat.use()

        self.projection = Uniform("mat4", self.camera.get_PPM())
        self.projection.find_variable(self.shader_id, "projMat")
        self.projection.load()

        self.lookat = Uniform("mat4", self.camera.get_VM())
        self.lookat.find_variable(self.shader_id, "viewMat")
        self.lookat.load()

        self.transformation = Uniform("mat4",np.identity(4))
        self.transformation.find_variable(self.shader_id,"modelMat")
        self.transformation.load()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        print(glGetError())

