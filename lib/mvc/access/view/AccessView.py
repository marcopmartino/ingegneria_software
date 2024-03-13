from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QVBoxLayout, QPushButton

from lib.validation.FormManager import FormManager
from lib.widget.StylisableWidget import StylisableWidget
from lib.layout.FrameLayout import FrameLayout
from lib.widget.InteractiveLabel import InteractiveLabel
from res import Styles
from res.Dimensions import FontSize, FormDimensions, FontWeight, LineEditDimensions
from abc import abstractmethod, ABC

from res.Strings import UtilityStrings


class AccessViewMeta(type(StylisableWidget), type(ABC)):
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

        # Crea Una Label di errore
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        self.validation_error_label = QLabel(parent_widget)
        self.validation_error_label.setFont(font)
        self.validation_error_label.setObjectName("validation_error_label")
        self.validation_error_label.setAlignment(Qt.AlignCenter)
        self.validation_error_label.setStyleSheet(Styles.ERROR_LABEL_INPUT)
        self.validation_error_label.setHidden(True)  # Nasconde la Label

        # Pulsante di Login
        font = QFont()
        font.setWeight(FontWeight.BOLD)
        self.submitButton = QPushButton(self)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submit_button")

        # Testo dopo la form
        self.bottomLabel = InteractiveLabel(self)
        self.bottomLabel.setAlignment(Qt.AlignCenter)
        self.bottomLabel.setObjectName("bottom_label")
        self.bottomLabel.clicked.connect(self.on_bottom_label_click)

        # Layout verticale più esterno che racchiude il contenuto principale
        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(FormDimensions.DEFAULT_EXTERNAL_SPACING)
        self.contentLayout.setObjectName("content_layout")
        self.contentLayout.addWidget(self.titleLabel)  # Aggiunge il titolo
        self.contentLayout.addLayout(self.inputLayout)  # Aggiunge il layout dei campi di input
        self.contentLayout.addWidget(self.validation_error_label)  # Aggiunge una label di errore
        self.contentLayout.addWidget(self.submitButton)  # Aggiunge il pulsante di Submit
        self.contentLayout.addWidget(self.bottomLabel)  # Aggiunge il testo di coda

        # Pone il layout della form al centro del frame interno
        self.frameLayout.setCentralLayout(self.contentLayout)

        # Inizializza il FormManager
        self.form_manager = FormManager()

    # Metodo da eseguire al click sul pulsante di submit della form
    @abstractmethod
    def on_submit(self, form_data: dict[str, any]):
        pass

    # Metodo da eseguire al click sulla scritta in fondo alla vista
    @abstractmethod
    def on_bottom_label_click(self):
        pass

    # Da eseguire in caso di errore di connessione
    def on_connection_error(self):
        self.validation_error_label.setText(
            UtilityStrings.CONNECTION_ERROR + " -\n" + UtilityStrings.CHECK_INTERNET_CONNECTION)
        self.validation_error_label.setHidden(False)
        print("ConnectionError")

    # Da eseguire in caso di errore non previsto
    def on_unexpected_error(self):
        self.validation_error_label.setText(UtilityStrings.ERROR_SOMETHING_WENT_WRONG)
        self.validation_error_label.setHidden(False)
        print("HTTPError")

    # Ritorna il controller associato alla finestra in cui la mvc è inserita
    def controller(self):
        return self.window().controller

    # Mostra la finestra principale dell'applicazione
    def show_main_window(self):
        self.window().show_main_window()
