from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from VistaHome import VistaHome


class VistaRegistrazione(QWidget):

    def __init__(self, parent=None):
        super(VistaRegistrazione, self).__init__(parent)

        # Titolo
        title_label = QLabel("Registrati su ShoeLastFactoryManager")
        title_label.setFont(QFont('Roboto', 16, QFont.Medium))
        title_label.setAlignment(Qt.AlignCenter)

        # Nome azienda Input
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nome azienda")

        # Partita IVA Input
        partita_IVA_input = QLineEdit()
        partita_IVA_input.setPlaceholderText("Partita IVA")

        # Indirizzo di recapito Input
        address_input = QLineEdit()
        address_input.setPlaceholderText("Indirizzo di recapito")

        # Email Input
        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")

        # Telefono Input
        phone_input = QLineEdit()
        phone_input.setPlaceholderText("Telefono")

        # Password Input
        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")

        # Conferma password Input
        confirm_password_input = QLineEdit()
        confirm_password_input.setPlaceholderText("Conferma password")

        # Sign up Button
        def register_account():
            self.close()
            VistaHome()

        login_button = QPushButton("Registrati")
        login_button.clicked.connect(register_account)

        # Layout
        column_layout = QFormLayout(self)
        column_layout.addRow(title_label)
        column_layout.addRow("Nome azienda", name_input)
        column_layout.addRow("Partita IVA", partita_IVA_input)
        column_layout.addRow("Indirizzo di recapito", address_input)
        column_layout.addRow("Email", email_input)
        column_layout.addRow("Telefono", phone_input)
        column_layout.addRow("Password", password_input)
        column_layout.addRow("Conferma password", confirm_password_input)
        column_layout.addRow(login_button)

        # Finestra
        self.setLayout(column_layout)
        self.setFixedSize(500, 750)
        self.setWindowTitle("ShoeLastFactoryManager - Registrati")
        self.show()
