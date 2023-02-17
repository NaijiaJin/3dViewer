from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLineEdit, QPushButton, QRadioButton, \
    QHBoxLayout, QGroupBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QDoubleValidator
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the window widgets and details"""
        self.setWindowTitle("Naijia's Temperature Homework!")
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set width and height
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)

        # Horizontal setup
        hor_layout = QHBoxLayout()

        # Add custom widgets
        self.input_temperature = QLineEdit()
        self.input_temperature.setPlaceholderText("enter the value to convert")  # set placeholder text
        self.input_temperature.setValidator(QDoubleValidator(-999, 999, 8))  # only allows numbers input
        hor_layout.addWidget(self.input_temperature)
        self.convert_button = QPushButton('Convert')
        self.convert_button.setFixedHeight(60)
        self.output_temperature = QLineEdit()
        self.output_temperature.setPlaceholderText("result value shows up here")
        self.output_temperature.setReadOnly(True)
        hor_layout.addWidget(self.convert_button)
        hor_layout.addWidget(self.output_temperature)

        # Add to central widget
        layout.addLayout(hor_layout)

        # Radio options setup
        radio_layout = QVBoxLayout()
        options_group = QGroupBox('Converting Options')
        options_group.setLayout(radio_layout)
        self.fahrenheit = QRadioButton("Convert to Fahrenheit")
        self.fahrenheit.setChecked(True)
        radio_layout.addWidget(self.fahrenheit)
        self.celsius = QRadioButton("Convert to Celsius")
        radio_layout.addWidget(self.celsius)
        layout.addWidget(options_group)

        # pig selection section
        pig_layout = QVBoxLayout()
        self.pig_name = QLineEdit()
        pig_layout.addWidget(self.pig_name)
        layout.addLayout(pig_layout)

    def fahrenheit_to_celsius(self, input_value):
        output_value = (float(input_value) - 32) * 5 / 9
        return output_value

    def celsius_to_fahrenheit(self, input_value):
        output_value = (float(input_value) * 1.8 + 32)
        return output_value

    def _connect_signals(self):
        """Connect the widget signals so they work"""
        self.convert_button.clicked.connect(lambda: self.convert_temperature("result"))

    def convert_temperature(self, text):
        """Convert the input temperature to the desired output"""
        self.output_temperature.clear()
        if self.fahrenheit.isChecked():
            f_value = round(self.fahrenheit_to_celsius(self.input_temperature.text()), 2)
            self.output_temperature.setText(str(f_value))
        elif self.celsius.isChecked():
            c_value = round(self.celsius_to_fahrenheit(self.input_temperature.text()), 2)
            self.output_temperature.setText(str(c_value))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
