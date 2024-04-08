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

        self.labelData = None

        lowercase_field_name = field_name.lower()

        self.labelText = CustomTableQLabel(f"{field_name}_text", field_name, is_header=True)
        if data is not None:
            self.labelData = CustomTableQLabel(f"{field_name}_data", str(data), position=Qt.AlignCenter)

        # Imposta l'oggetto Layout stesso
        self.setObjectName(f"{lowercase_field_name}_layout")
        self.setSpacing(0)  # Spazio tra LabelText e LabelData
        self.addWidget(self.labelText)  # Aggiunge la Label del testo
        if data is not None:
            self.addWidget(self.labelData)  # Aggiunge la Label del dato

    def edit_text(self, field_name: str, data: Any):
        if self.labelData is not None:
            self.labelData.setText(data)
        else:
            self.labelData = CustomTableQLabel(f"{field_name}_data", str(data), position=Qt.AlignCenter)
            self.addWidget(self.labelData)
