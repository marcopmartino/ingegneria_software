from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QLabel, QSizePolicy

from res import Styles
from res.Dimensions import LineEditDimensions, FontWeight


# Classe che rappresenta un campo di input testuale personalizzato, costituito da un QVBoxLayout che contiene una
# QLabel, un qLineEdit ed eventualmente una seconda QLabel per mostrare un messaggio di errore.
# noinspection PyPep8Naming
class LineEditLayout(QVBoxLayout):

    def __init__(self, field_name: str = '', include_error_field: bool = True, parent_widget: QWidget = None):
        super().__init__(parent_widget)

        self.include_error_field = include_error_field

        # Label del LineEdit
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.label = QLabel(parent_widget)
        self.label.setFont(font)
        self.label.setHidden(True)  # Nasconde la Label

        # LineEdit
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_TEXT_FONT_SIZE)
        self.line_edit = QLineEdit(parent_widget)
        self.line_edit.setFont(font)
        self.line_edit.setMinimumSize(QSize(LineEditDimensions.DEFAULT_MINIMUM_WIDTH, 0))
        self.line_edit.setClearButtonEnabled(True)  # Abilita il pulsante per lo svuotamento del campo

        # Imposta l'oggetto Layout stesso
        self.setSpacing(LineEditDimensions.DEFAULT_SPACING)  # Spazio tra Label e LineEdit
        self.addWidget(self.label)  # Aggiunge la Label al layout del campo di input
        self.addWidget(self.line_edit)  # Aggiunge il LineEdit al layout del campo di input

        # Label per mostrare un errore di input, utile nella validazione
        if include_error_field:
            font = QFont()
            font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
            self.error_label = QLabel(parent_widget)
            self.error_label.setFont(font)
            self.error_label.setStyleSheet(Styles.ERROR_LABEL_INPUT)
            self.error_label.setHidden(True)  # Nasconde la Label
            self.addWidget(self.error_label)

        # Imposta i nomi degli oggetti, il testo di Label e il placeholder di LineEdit
        self.setFieldName(field_name)

        # Logica quando il testo cambia
        self.line_edit.textChanged.connect(self.__on_text_changed)

    # Quando è presente del testo nel LineEdit, il testo della Label viene mostrato.
    # Altrimenti il testo della Label viene nascosto.
    def __on_text_changed(self, text):
        if text:  # Una stringa è False se è vuota
            self.label.setHidden(False)
        else:
            self.label.setHidden(True)

    # Imposta i nomi degli oggetti, il testo di Label e il placeholder di LineEdit
    def setFieldName(self, field_name):
        lowercase_field_name = field_name.lower()
        self.setObjectName(f"{lowercase_field_name}_layout")
        self.label.setObjectName(f"{lowercase_field_name}_label")
        self.line_edit.setObjectName(f"{lowercase_field_name}_line_edit")
        if self.include_error_field:
            self.error_label.setObjectName(f"{lowercase_field_name}_error_label")
        self.label.setText(field_name)
        self.line_edit.setPlaceholderText(field_name)
