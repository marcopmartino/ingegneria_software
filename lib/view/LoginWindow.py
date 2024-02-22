from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QSizePolicy

from lib.layout.FrameLayout import FrameLayout
from lib.layout.LineEditLayout import LineEditLayout
from res import Styles
from res.Dimensions import FormDimensions, FontDimensions
from res.Strings import FormStrings, AccessStrings, Config


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # Finestra
        self.setObjectName("MainWindow")
        self.resize(1000, 600)
        self.setStyleSheet(Styles.ACCESS)

        # Widget più esterno - Inizializzazione
        self.outerWidget = QWidget(self)
        self.outerWidget.setObjectName("outerWidget")

        # Widget più esterno - Layout
        self.outerFrameLayout = FrameLayout(self.outerWidget)
        self.outerFrameLayout.setObjectName("outerGridLayout")
        self.outerFrameLayout.setSpacers(140, 80, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Widget più interno - Inizializzazione
        self.widget = QWidget(self.outerWidget)
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.widget.setObjectName("layout")

        # Widget più interno - Layout
        self.frameLayout = FrameLayout(self.widget)
        self.frameLayout.setObjectName("gridLayout")
        self.frameLayout.setSpacers(70, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Titolo della form
        font = QFont()
        font.setPointSize(FontDimensions.TITLE)
        self.titleLabel = QLabel(self.widget)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")

        # Campo di input Email
        self.emailVBoxLayout = LineEditLayout(FormStrings.EMAIL, False, self.widget)

        # Campo di input Password
        self.passwordVBoxLayout = LineEditLayout(FormStrings.PASSWORD, False, self.widget)
        self.passwordVBoxLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

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
        self.outerVBoxLayout.addWidget(self.submitButton)  # Aggiunge il pulsante di Login

        # Pone il layout della form al centro del frame interno
        self.frameLayout.setCentralLayout(self.outerVBoxLayout)

        # Pone il frame interno al centro del frame esterno
        self.outerFrameLayout.setCentralWidget(self.widget)

        # Pone il frame esterno come Widget di base della finestra
        self.setCentralWidget(self.outerWidget)

        # Testo
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.titleLabel.setText(AccessStrings.TITLE_LOGIN)
        self.submitButton.setText(AccessStrings.LOGIN)
