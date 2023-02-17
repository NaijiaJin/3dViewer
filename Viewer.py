from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLineEdit, QPushButton, QRadioButton, \
    QHBoxLayout, QGroupBox, QLabel, QSizePolicy, QSlider, QMenu
from PySide2.QtCore import Qt
from PySide2.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide2.QtGui import QDoubleValidator
from Triangle import GLGeometry
import numpy
import sys


class mySliders(QSlider):
    def __init__(self, direction: Qt.Horizontal):
        super().__init__(direction)
        self.setMinimum(0)
        self.setMaximum(360)
        self.setSingleStep(1)
        self.setTickInterval(90)
        self.setTickPosition(QSlider.TicksLeft)


class MainWindow(QMainWindow):
    def __init__(self, glWidget: GLGeometry):
        super().__init__()
        self.windowWidth = 1000
        self.windowHeight = 600
        self.glWidget = GLGeometry()  # glWidget initialization
        self._setup_ui()
        self._connect_signals()

        timer = QtCore.QTimer(self)
        timer.setInterval(16)
        timer.timeout.connect(lambda: self.glWidget.updateGL())
        timer.start()

    def _setup_ui(self):
        """Set up the window widgets and details"""
        self.setWindowTitle("Shading Model Viewer")

        central_widget = QWidget(self)
        layout = QHBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set width and height
        self.setMinimumWidth(self.windowWidth)
        self.setMinimumHeight(self.windowHeight)

        # Radio options setup
        radio_layout = QVBoxLayout()
        options_group = QGroupBox('Mesh')
        options_group.setAlignment(Qt.AlignTop)
        options_group.setLayout(radio_layout)
        options_group.setMaximumHeight(150)
        options_group.setMaximumWidth(200)
        self.cube = QRadioButton("Cube")
        self.cube.setChecked(True)
        radio_layout.addWidget(self.cube)
        self.triangle = QRadioButton("Bunny")
        radio_layout.addWidget(self.triangle)
        # layout.addWidget(options_group)

        # transformation layout, has rotation, and scale
        transformation_layout = QVBoxLayout()
        transformation_group = QGroupBox("Transformation")
        transformation_group.setLayout(transformation_layout)
        transformation_group.setMaximumWidth(200)

        slider_layout = QVBoxLayout()
        sliders_group = QGroupBox("Rotation")
        sliders_group.setLayout(slider_layout)
        sliders_group.setMaximumWidth(200)
        slider_layout.setAlignment(Qt.AlignTop)
        self.sliderLabelX = QLabel("X Axis")
        self.sliderX = mySliders(Qt.Horizontal)
        self.sliderLabelY = QLabel("Y Axis")
        self.sliderY = mySliders(Qt.Horizontal)
        self.sliderLabelZ = QLabel("Z Axis")
        self.sliderZ = mySliders(Qt.Horizontal)

        slider_layout.addWidget(self.sliderLabelX)
        slider_layout.addWidget(self.sliderX)
        slider_layout.addWidget(self.sliderLabelY)
        slider_layout.addWidget(self.sliderY)
        slider_layout.addWidget(self.sliderLabelZ)
        slider_layout.addWidget(self.sliderZ)

        scale_layout = QHBoxLayout()
        scale_group = QGroupBox("Scale")
        scale_group.setLayout(scale_layout)
        self.scaleValidator = QDoubleValidator() # set a validator for scale input
        self.scaleX = QLabel("X")
        self.scaleXValue = QLineEdit()
        self.scaleXValue.setText("20")
        self.scaleXValue.setValidator(self.scaleValidator)
        self.scaleY = QLabel("Y")
        self.scaleYValue = QLineEdit()
        self.scaleYValue.setText("20")
        self.scaleYValue.setValidator(self.scaleValidator)
        self.scaleZ = QLabel("Z")
        self.scaleZValue = QLineEdit()
        self.scaleZValue.setText("20")
        self.scaleZValue.setValidator(self.scaleValidator)
        scale_layout.addWidget(self.scaleX)
        scale_layout.addWidget(self.scaleXValue)
        scale_layout.addWidget(self.scaleY)
        scale_layout.addWidget(self.scaleYValue)
        scale_layout.addWidget(self.scaleZ)
        scale_layout.addWidget(self.scaleZValue)

        transformation_layout.addWidget(sliders_group)
        transformation_layout.addWidget(scale_group)

        material_layout = QVBoxLayout()
        material_group = QGroupBox("Shaders")
        material_group.setLayout(material_layout)
        material_layout.setAlignment(Qt.AlignTop)
        self.lambertButton = QPushButton("Lambert")
        self.outlineButton = QPushButton("Outline")
        material_layout.addWidget(self.lambertButton)
        material_layout.addWidget(self.outlineButton)

        UI_layout = QVBoxLayout()
        UI_layout.addWidget(options_group)
        UI_layout.addWidget(transformation_group)
        UI_layout.addWidget(material_group)

        layout.addLayout(UI_layout)
        # openGL window
        GL_layout = QVBoxLayout()
        self.glWidget.setMinimumHeight(550)  # change later
        self.glWidget.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)  # resize the GL window when expanding the main window
        self.glLabel = QLabel("OpenGL Window")
        GL_layout.addWidget(self.glLabel)
        GL_layout.addWidget(self.glWidget)
        layout.addLayout(GL_layout)

    def scaleXInput(self):
        self.glWidget.scaleX = float(self.scaleXValue.text())

    def scaleYInput(self):
        self.glWidget.scaleY = float(self.scaleYValue.text())

    def scaleZInput(self):
        self.glWidget.scaleZ = float(self.scaleZValue.text())

    def _connect_signals(self):
        """Connect the widget signals so they work"""
        self.sliderX.valueChanged.connect(lambda value: self.glWidget.setRotX(value))
        self.sliderY.valueChanged.connect(lambda value: self.glWidget.setRotY(value))
        self.sliderZ.valueChanged.connect(lambda value: self.glWidget.setRotZ(value))
        try:
            self.scaleXValue.returnPressed.connect(self.scaleXInput)
            self.scaleYValue.returnPressed.connect(self.scaleYInput)
            self.scaleZValue.returnPressed.connect(self.scaleZInput)
        except:
            print("invalid value")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(GLGeometry)
    window.show()
    app.exec_()
