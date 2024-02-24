import abc

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QVBoxLayout, QPushButton

from lib.widget.StylisableWidget import StylisableWidget
from lib.layout.FrameLayout import FrameLayout
from lib.widget.AccessBottomLabel import AccessBottomLabel
from res.Dimensions import FontSize, FormDimensions, FontWeight
from abc import abstractmethod, ABC


class AccessViewMeta(type(QWidget), type(ABC)):
    pass


class AccessView(StylisableWidget, ABC, metaclass=AccessViewMeta):

    def __init__(self, parent_widget: QWidget = None):
        super(AccessView, self).__init__(parent_widget)

        # Widget più interno
        self.setMaximumSize(QSize(500, 16777215))
        self.setObjectName("main_widget")

        # Widget più interno - Layout
        self.frameLayout = FrameLayout(self)
        self.frameLayout.setObjectName("main_layout")
        self.frameLayout.setSpacers(70, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Titolo della form
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.titleLabel = QLabel(self)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setObjectName("title_label")

        # Layout verticale con campi di input della form
        self.inputLayout = QVBoxLayout()
        self.inputLayout.setSpacing(FormDimensions.DEFAULT_INTERNAL_SPACING)  # Spazio tra gli elementi della form
        self.inputLayout.setObjectName("input_layout")

        # Pulsante di Login
        font = QFont()
        font.setWeight(FontWeight.BOLD)
        self.submitButton = QPushButton(self)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submit_button")
        self.submitButton.clicked.connect(self.on_submit)

        # Testo dopo la form
        self.bottomLabel = AccessBottomLabel(self)
        self.bottomLabel.setAlignment(Qt.AlignCenter)
        self.bottomLabel.setObjectName("bottom_label")
        self.bottomLabel.clicked.connect(self.on_bottom_label_click)

        # Layout verticale più esterno che racchiude il contenuto principale
        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(FormDimensions.DEFAULT_EXTERNAL_SPACING)
        self.contentLayout.setObjectName("content_layout")
        self.contentLayout.addWidget(self.titleLabel)  # Aggiunge il titolo
        self.contentLayout.addLayout(self.inputLayout)  # Aggiunge il layout dei campi di input
        self.contentLayout.addWidget(self.submitButton)  # Aggiunge il pulsante di Submit
        self.contentLayout.addWidget(self.bottomLabel)  # Aggiunge il testo di coda

        # Pone il layout della form al centro del frame interno
        self.frameLayout.setCentralLayout(self.contentLayout)

    # Metodo da eseguire al click sul pulsante di submit della form
    @abstractmethod
    def on_submit(self):
        pass

    # Metodo da eseguire al click sulla scritta in fondo alla vista
    @abstractmethod
    def on_bottom_label_click(self):
        pass
