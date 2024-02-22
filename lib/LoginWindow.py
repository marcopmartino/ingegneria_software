from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy

from res import Styles
from res.Dimensions import SpacerDimensions, LineEditDimensions, FormDimensions, FontDimensions
from res.Strings import FormStrings, AccessStrings, Config


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # Widget più esterno - Inizializzazione
        self.outerWidget = QWidget(self)
        self.outerWidget.setObjectName("outerWidget")

        # Widget più esterno - Layout
        self.outerGridLayout = QGridLayout(self.outerWidget)
        self.outerGridLayout.setObjectName("outerGridLayout")

        # Widget più esterno - Spacers
        horizontal_spacer = QSpacerItem(140, SpacerDimensions.DEFAULT, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vertical_spacer = QSpacerItem(SpacerDimensions.DEFAULT, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.outerGridLayout.addItem(horizontal_spacer, 1, 0, 1, 1)  # Spacer sinistro
        self.outerGridLayout.addItem(horizontal_spacer, 1, 2, 1, 1)  # Spacer destro
        self.outerGridLayout.addItem(vertical_spacer, 0, 1, 1, 1)  # Spacer superiore
        self.outerGridLayout.addItem(vertical_spacer, 2, 1, 1, 1)  # Spacer inferiore

        # Widget più interno - Inizializzazione
        self.widget = QWidget(self.outerWidget)
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.widget.setObjectName("widget")

        # Widget più interno - Layout
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")

        # Widget più interno - Spacers
        horizontal_spacer = QSpacerItem(70, SpacerDimensions.DEFAULT, QSizePolicy.Fixed, QSizePolicy.Minimum)
        vertical_spacer = QSpacerItem(SpacerDimensions.DEFAULT, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(horizontal_spacer, 1, 0, 1, 1)  # Spacer sinistro
        self.gridLayout.addItem(horizontal_spacer, 1, 2, 1, 1)  # Spacer destro
        self.gridLayout.addItem(vertical_spacer, 2, 1, 1, 1)  # Spacer inferiore
        self.gridLayout.addItem(vertical_spacer, 0, 1, 1, 1)  # Spacer superiore

        # Titolo della form
        font = QFont()
        font.setPointSize(FontDimensions.TITLE)
        self.titleLabel = QLabel(self.widget)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")

        # Label del campo Email
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(75)
        self.emailLabel = QLabel(self.widget)
        self.emailLabel.setFont(font)
        self.emailLabel.setObjectName("emailLabel")

        # LineEdit del campo Email
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_TEXT_FONT_SIZE)
        self.emailLineEdit = QLineEdit(self.widget)
        self.emailLineEdit.setMinimumSize(QSize(LineEditDimensions.DEFAULT_MINIMUM_WIDTH, 0))
        self.emailLineEdit.setFont(font)
        self.emailLineEdit.setObjectName("emailLineEdit")

        # Layout del campo Email
        self.emailVBoxLayout = QVBoxLayout()
        self.emailVBoxLayout.setSpacing(LineEditDimensions.DEFAULT_SPACING)  # Spazio tra Label e LineEdit
        self.emailVBoxLayout.setObjectName("emailVBoxLayout")
        self.emailVBoxLayout.addWidget(self.emailLabel)  # Aggiunge la Label al layout del campo Email
        self.emailVBoxLayout.addWidget(self.emailLineEdit)  # Aggiunge la Label al layout del campo Email

        # Label del campo Password
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel = QLabel(self.widget)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")

        # LineEdit del campo Password
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_TEXT_FONT_SIZE)
        self.passwordLineEdit = QLineEdit(self.widget)
        self.passwordLineEdit.setMinimumSize(QSize(LineEditDimensions.DEFAULT_MINIMUM_WIDTH, 0))
        self.passwordLineEdit.setFont(font)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.passwordLineEdit.setObjectName("passwordLineEdit")

        # Layout del campo Password
        self.passwordVBoxLayout = QVBoxLayout()
        self.passwordVBoxLayout.setSpacing(LineEditDimensions.DEFAULT_SPACING)  # Spazio tra Label e LineEdit
        self.passwordVBoxLayout.setObjectName("passwordVBoxLayout")
        self.passwordVBoxLayout.addWidget(self.passwordLabel)  # Aggiunge la Label al layout del campo Password
        self.passwordVBoxLayout.addWidget(self.passwordLineEdit)  # Aggiunge il LineEdit al layout del campo Password

        # Layout verticale con campi di input della form
        self.inputVBoxLayout = QVBoxLayout()
        self.inputVBoxLayout.setSpacing(FormDimensions.DEFAULT_INTERNAL_SPACING)  # Spazio tra gli elementi della form
        self.inputVBoxLayout.setObjectName("formVBoxLayout")
        self.inputVBoxLayout.addLayout(self.emailVBoxLayout)  # Aggiunge il layout del campo Email
        self.inputVBoxLayout.addLayout(self.passwordVBoxLayout)  # Aggiunge il layout del campo Password

        # Pulsante di Login
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.submitButton = QPushButton(self.widget)
        self.submitButton.setEnabled(True)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submitButton")

        # Layout verticale più esterno
        self.outerVBoxLayout = QVBoxLayout()
        self.outerVBoxLayout.setSpacing(FormDimensions.DEFAULT_EXTERNAL_SPACING)
        self.outerVBoxLayout.setObjectName("outerVBoxLayout")
        self.outerVBoxLayout.addWidget(self.titleLabel)  # Aggiunge il titolo
        self.outerVBoxLayout.addLayout(self.inputVBoxLayout)  # Aggiunge il layout dei campi di input
        self.outerVBoxLayout.addWidget(self.submitButton)  # Aggiunge il layout del pulsante di Login

        # Finestra
        self.setObjectName("MainWindow")
        self.resize(1000, 600)
        self.setStyleSheet(Styles.ACCESS)

        # Pone il layout della form al centro della griglia interna
        self.gridLayout.addLayout(self.outerVBoxLayout, 1, 1, 1, 1)

        # Pone la griglia interna al centro della griglia esterna
        self.outerGridLayout.addWidget(self.widget, 1, 1, 1, 1)
        self.setCentralWidget(self.outerWidget)

        # Testo
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.titleLabel.setText(AccessStrings.TITLE_LOGIN)
        self.submitButton.setText(AccessStrings.LOGIN)

        # Imposta i placeholder dei campi
        self.emailLineEdit.setPlaceholderText(FormStrings.EMAIL)
        self.passwordLineEdit.setPlaceholderText(FormStrings.PASSWORD)

        # Svuota i campi
        self.emailLabel.clear()
        self.passwordLabel.clear()

        # Abilita i pulsanti per lo svuota mento dei campi
        self.emailLineEdit.setClearButtonEnabled(True)
        self.passwordLineEdit.setClearButtonEnabled(True)

        # Logica quando il testo cambia
        self.emailLineEdit.textChanged.connect(self.onEmailChanged)
        self.passwordLineEdit.textChanged.connect(self.onPasswordChanged)

    def on_email_changed(self, text):
        if text:
            self.emailLabel.setText(FormStrings.EMAIL)
        else:
            self.emailLabel.clear()

    def on_password_changed(self, text):
        if text:
            self.passwordLabel.setText(FormStrings.PASSWORD)
        else:
            self.passwordLabel.clear()
