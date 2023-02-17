from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PySide2.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the window widgets and details"""
        self.setWindowTitle("Naijia's Example - Hello")
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set width and height
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        # Add custom widgets
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        self.secondline_edit = QLineEdit()
        layout.addWidget(self.secondline_edit)
        self.secondline_edit.setFocus()
        self.button = QPushButton('Naijia Button')
        self.button.setFixedHeight(60)
        self.clear_button = QPushButton('Clear Text')
        self.clear_button.setFixedHeight(60)
        layout.addWidget(self.button)
        layout.addWidget(self.clear_button)

    def _connect_signals(self):
        """Connect the widget signals so they work"""
        self.button.clicked.connect(lambda: self.set_line_text())
        self.clear_button.clicked.connect(lambda: self.clear_text())

    def set_line_text(self):
        """Function to add text to the line edit widget"""
        self.line_edit.setText('Button was clicked, yay!')
        self.secondline_edit.setText("sssssssss")
        self.secondline_edit.setText("hahahahah")

    def clear_text(self):
        """Clear the text in the line edit widget"""
        self.line_edit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
