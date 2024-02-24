from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from VistaRegistrazione import VistaRegistrazione


class VistaLogin(QWidget):

    def __init__(self, parent=None):
        super(VistaLogin, self).__init__(parent)

        # Titolo
        title_label = QLabel("Accedi a ShoeLastFactoryManager")
        title_label.setFont(QFont('Helvetica', 16, QFont.Medium))
        title_label.setAlignment(Qt.AlignCenter)

        # Email Input
        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setFont(QFont('Helvetica', 14))
        email_input.setFixedWidth(250)
        email_input.setFixedHeight(50)
        validator = QIntValidator(self)

        # Password Input
        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setFixedWidth(250)

        # Login Button
        def login():
            self.close()
            VistaRegistrazione()

        login_button = QPushButton("Accedi")
        login_button.clicked.connect(login)
        login_button.setFixedWidth(250)

        # Bottom Label
        bottom_label = QLabel("Non hai un account? Registrati")
        bottom_label.setStyleSheet('background-color: #CCCCCC; border-top: 1px solid')
        bottom_label.setFixedHeight(50)
        bottom_label.setAlignment(Qt.AlignCenter)

        # Layout
        form_layout = QFormLayout(self)
        form_layout.addRow(title_label)
        form_layout.addRow("Email", email_input)
        form_layout.addRow("Password", password_input)
        form_layout.addRow(login_button)
        form_layout.addRow(bottom_label)
        form_layout.setFormAlignment(Qt.AlignCenter)

        # Finestra
        self.setLayout(form_layout)
        self.setFixedSize(500, 350)
        self.setWindowTitle("ShoeLastFactoryManager - Accedi")
        self.show()
