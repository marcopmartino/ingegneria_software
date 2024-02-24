from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VistaHome(QWidget):

    def __init__(self, parent=None):
        super(VistaHome, self).__init__(parent)

        # Layout
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Hello World'))

        # Finestra
        self.setLayout(form_layout)
        self.resize(1280, 720)
        self.setWindowTitle("ShoeLastFactoryManager - Profilo")
        self.show()
