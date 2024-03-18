from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QLabel, QSizePolicy

from res import Styles
from res.Dimensions import LineEditDimensions, FontWeight


# Classe che rappresenta un layout personalizzato, costituito da un QVBoxLayout che contiene una
# QLabel e un QLineEdit. Gestisce la logica di visibilità della QLabel (mostrata solo se c'è testo nel QLineEdit).
# Il testo di QLabel e il placeholder di QLineEdit coincidono.
# noinspection PyPep8Naming
class LineEditLayout(QVBoxLayout):

    def __init__(self, field_name: str, parent_widget: QWidget = None):
        super().__init__(parent_widget)

        lowercase_field_name = field_name.lower()

        # Label del LineEdit
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.label = QLabel(parent_widget)
        self.label.setFont(font)
        self.label.setText(field_name)
        self.label.setObjectName(f"{lowercase_field_name}_label")
        self.label.setHidden(True)  # Nasconde la Label

        # LineEdit
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_TEXT_FONT_SIZE)
        self.line_edit = QLineEdit(parent_widget)
        self.line_edit.setFont(font)
        self.line_edit.setPlaceholderText(field_name)
        self.line_edit.setObjectName(f"{lowercase_field_name}_line_edit")
        self.line_edit.setMinimumSize(QSize(LineEditDimensions.DEFAULT_MINIMUM_WIDTH, 0))
        self.line_edit.setClearButtonEnabled(True)  # Abilita il pulsante per lo svuotamento del campo

        # Imposta l'oggetto Layout stesso
        self.setObjectName(f"{lowercase_field_name}_layout")
        self.setSpacing(LineEditDimensions.DEFAULT_SPACING)  # Spazio tra Label e LineEdit
        self.addWidget(self.label)  # Aggiunge la Label al layout del campo di input
        self.addWidget(self.line_edit)  # Aggiunge il LineEdit al layout del campo di input

        # Logica quando il testo cambia
        self.line_edit.textChanged.connect(self.__on_text_changed)

    # Quando è presente del testo nel LineEdit, il testo della Label viene mostrato.
    # Altrimenti il testo della Label viene nascosto.
    def __on_text_changed(self, text):
        if text:  # Una stringa è False se è vuota
            self.label.setHidden(False)
        else:
            self.label.setHidden(True)


# Estensione di LineEditLayout che oltre a una QLabel e a un QLineEdit contiene una seconda QLabel per mostrare un
# messaggio di errore; è utile nelle form per la validazione.
class LineEditCompositeLayout(LineEditLayout):
    def __init__(self, field_name: str, parent_widget: QWidget = None):

        # Imposta il layout, la Label e il LineEdit
        super().__init__(field_name, parent_widget)

        # Seconda Label per mostrare un errore di input, utile nella validazione
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        self.error_label = QLabel(parent_widget)
        self.error_label.setFont(font)
        self.error_label.setObjectName(f"{field_name.lower()}_error_label")
        self.error_label.setStyleSheet(Styles.ERROR_LABEL_INPUT)
        self.error_label.setHidden(True)  # Nasconde la Label
        self.addWidget(self.error_label)
