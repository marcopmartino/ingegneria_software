from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QSizePolicy

from lib.layout.FrameLayout import FrameLayout
from lib.layout.LineEditLayout import LineEditLayout
from lib.widget.AccessBottomLabel import AccessBottomLabel
from res import Styles
from res.Dimensions import FormDimensions, FontSize, FontWeight
from res.Strings import FormStrings, AccessStrings, Config


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # Finestra
        self.setObjectName("main_window")
        self.resize(1000, 600)
        self.setStyleSheet(Styles.ACCESS)

        # Widget più esterno - Inizializzazione
        self.outerWidget = QWidget(self)
        self.outerWidget.setObjectName("outer_widget")

        # Widget più esterno - Layout
        self.outerFrameLayout = FrameLayout(self.outerWidget)
        self.outerFrameLayout.setObjectName("outer_layout")
        self.outerFrameLayout.setSpacers(140, 80, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Widget più interno - Inizializzazione
        self.widget = QWidget(self.outerWidget)
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.widget.setObjectName("main_widget")

        # Widget più interno - Layout
        self.frameLayout = FrameLayout(self.widget)
        self.frameLayout.setObjectName("main_layout")
        self.frameLayout.setSpacers(70, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Titolo della form
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.titleLabel = QLabel(self.widget)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setObjectName("title_label")

        # Campo di input Email
        self.emailVBoxLayout = LineEditLayout(FormStrings.EMAIL, False, self.widget)

        # Campo di input Password
        self.passwordVBoxLayout = LineEditLayout(FormStrings.PASSWORD, False, self.widget)
        self.passwordVBoxLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Layout verticale con campi di input della form
        self.inputVBoxLayout = QVBoxLayout()
        self.inputVBoxLayout.setSpacing(FormDimensions.DEFAULT_INTERNAL_SPACING)  # Spazio tra gli elementi della form
        self.inputVBoxLayout.setObjectName("input_layout")
        self.inputVBoxLayout.addLayout(self.emailVBoxLayout)  # Aggiunge il layout del campo Email
        self.inputVBoxLayout.addLayout(self.passwordVBoxLayout)  # Aggiunge il layout del campo Password

        # Pulsante di Login
        font = QFont()
        font.setBold(False)
        font.setWeight(FontWeight.BOLD)
        self.submitButton = QPushButton(self.widget)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submit_button")

        # Testo dopo la form
        self.bottomLabel = AccessBottomLabel(self.widget)
        self.bottomLabel.setAlignment(Qt.AlignCenter)
        self.bottomLabel.setObjectName("bottom_label")

        # Layout verticale più esterno
        self.outerVBoxLayout = QVBoxLayout()
        self.outerVBoxLayout.setSpacing(FormDimensions.DEFAULT_EXTERNAL_SPACING)
        self.outerVBoxLayout.setObjectName("outer_layout")
        self.outerVBoxLayout.addWidget(self.titleLabel)  # Aggiunge il titolo
        self.outerVBoxLayout.addLayout(self.inputVBoxLayout)  # Aggiunge il layout dei campi di input
        self.outerVBoxLayout.addWidget(self.submitButton)  # Aggiunge il pulsante di Login
        self.outerVBoxLayout.addWidget(self.bottomLabel)

        # Pone il layout della form al centro del frame interno
        self.frameLayout.setCentralLayout(self.outerVBoxLayout)

        # Pone il frame interno al centro del frame esterno
        self.outerFrameLayout.setCentralWidget(self.widget)

        # Pone il frame esterno come Widget di base della finestra
        self.setCentralWidget(self.outerWidget)

        # Testo
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.titleLabel.setText(AccessStrings.TITLE_LOGIN)
        self.bottomLabel.setText(AccessStrings.BOTTOM_TEXT_LOGIN)
        self.submitButton.setText(AccessStrings.LOGIN)
