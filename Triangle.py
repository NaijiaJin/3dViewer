from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLineEdit, QPushButton, QRadioButton, \
    QHBoxLayout, QGroupBox, QLabel, QSizePolicy
from PySide2.QtCore import Qt
from PySide2.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo  # vertex buffer object
import numpy as np
from PySide2.QtGui import QDoubleValidator
import sys
from Material import *


class GLGeometry(QGLWidget):
    def __init__(self):
        super().__init__()
        self.vertexPosition = None
        self.VAO = None
        self.tryVBO = None
        self.colorVBO_new = None
        self.mat = None
        self.colorVBO_tri = None
        self.TriColorArray = None
        self.vertVBO_tri = None
        self.triangleVertexArray = None
        self.scaleZ = 0.0
        self.scaleY = 0.0
        self.scaleX = 0.0
        self.rotateZ = 0.0
        self.rotateY = 0.0
        self.rotateX = 0.0
        self.cubeVertexArray = None
        self.cubeColorArray = None
        self.cubeIdxArray = None
        self.colorVBO = None
        self.vertVBO = None

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

    def initTriangle(self):
        self.triangleVertexArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0]])  # cube position vertex
        self.vertVBO_tri = vbo.VBO(
            np.reshape(self.triangleVertexArray, (1, -1)).astype(
                np.float32))  # by default the target is GLBUFFER_ARRAY already
        self.vertVBO_tri.bind()  # bind it to be used as the vertex buffer

        # vertex color info
        self.TriColorArray = np.array(
            [[1.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0]])
        self.colorVBO_tri = vbo.VBO(np.reshape(self.TriColorArray,
                                               (1, -1)).astype(np.float32))
        # self.colorVBO_tri.bind()

    def initCube(self):
        """
        define the vertex position, vertex color and vertex index to render a cube.
        """
        self.cubeVertexArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        #self.vertVBO = vbo.VBO(np.reshape(self.cubeVertexArray, (1, -1)).astype(np.float32))  # by default the target is GLBUFFER_ARRAY already
        #self.vertVBO.bind()  # bind it to be used as the vertex buffer

        """
        trying VBO 
        """
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.cubeVertexArray), self.cubeVertexArray, GL_STATIC_DRAW)
        
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.cubeColorArray = np.array(
            [[1.0, 0.0, 0.0],
             [1.0, 0.5, 0.0],
             [1.0, 1.0, 0.0],
             [1.0, 1.0, 0.5],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        #self.colorVBO = vbo.VBO(np.reshape(self.cubeColorArray, (1, -1)).astype(np.float32))


        #self.colorVBO.bind()

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4])

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

        self.initCube()
        self.mat = Material("Shaders/vertbasic.glsl", "Shaders/fragbasic.glsl")

    def resizeGL(self, w: int, h: int):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / float(h), 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()  # push the current matrix to the current stack

        glTranslate(0.0, 0.0, -50.0)  # third, translate cube to specified depth
        glScale(self.scaleX, self.scaleY, self.scaleZ)  # second, scale cube
        glRotate(self.rotateX, 1, 0, 0)
        glRotate(self.rotateY, 0, 1, 0)
        glRotate(self.rotateZ, 0, 0, 1)
        glTranslate(-0.5, -0.5, -0.5)  # first, translate cube center to origin

        #glEnableClientState(GL_VERTEX_ARRAY)
        #glEnableClientState(GL_COLOR_ARRAY)  # enable the color and vertex array

        #glVertexPointer(3, GL_FLOAT, 0, self.vertVBO)
        #self.colorVBO.bind()
        #glColorPointer(3, GL_FLOAT, 0, self.colorVBO)  # set the pointer to the vbo objects

        glEnableVertexAttribArray(self.VAO)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        self.mat.use()
        glBindVertexArray(self.VAO)

        glDrawElements(GL_QUADS,
                       len(self.cubeIdxArray),
                       GL_UNSIGNED_INT,
                       self.cubeIdxArray)
        #glDisableClientState(GL_VERTEX_ARRAY)
        #glDisableClientState(GL_COLOR_ARRAY)

        glPopMatrix()  # restore the previous model view matrix
