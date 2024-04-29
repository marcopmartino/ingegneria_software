from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

from lib.layout.CustomTableQLabel import CustomTableQLabel
from res import Styles
from res.Dimensions import LineEditDimensions, FontWeight


# Classe che rappresenta il nome di un campo con relativo dato in due label differenti.
# È possibile anche settare una semplice label senza bisogno del dato

class QLabelLayout(QHBoxLayout):

    def __init__(self, field_name: str, data: Any = None, parent_widget: QWidget = None):
        super().__init__(parent_widget)

        lowercase_field_name = field_name.lower()

        self.__labelText = CustomTableQLabel(f"{field_name}_text", field_name, is_header=True)
        if data is not None:
            self.__labelData = CustomTableQLabel(f"{field_name}_data", str(data), position=Qt.AlignCenter)
        else:
            self.__labelData = CustomTableQLabel(f"{field_name}_data", "", position=Qt.AlignCenter)

        # Imposta l'oggetto Layout stesso
        self.setObjectName(f"{lowercase_field_name}_layout")
        self.setSpacing(0)  # Spazio tra LabelText e LabelData
        self.addWidget(self.__labelText)  # Aggiunge la Label del testo
        self.addWidget(self.__labelData)  # Aggiunge la Label del dato

    def edit_text(self, data: Any):
        self.__labelData.setText(data)
