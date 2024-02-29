from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget

from lib.widget.ClickableLabel import ClickableLabel
from res.Dimensions import FontWeight, FontSize


# ClickableLabel che appare in fondo al layout centrale nelle schermate di login e di registrazione
# noinspection PyPep8Naming
class AccessBottomLabel(ClickableLabel):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)
        self.setFont(self.__initialize_font())

    # Inizializza il font della Label
    @staticmethod
    def __initialize_font():
        font = QFont()
        font.setPointSize(FontSize.SMALL)
        font.setWeight(FontWeight.BOLD)
        return font

    # Imposta il font di default della Label
    def setDefaultFont(self):
        font = self.font()
        font.setUnderline(False)
        self.setFont(font)

    # Modifica il font aggiungendo la sottolineatura
    def setOnHoverFont(self):
        font = self.font()
        font.setUnderline(True)
        self.setFont(font)

    # Funzione eseguita quando il mouse viene spostato sopra la Label
    def enterEvent(self, event):
        super().enterEvent(event)
        self.setOnHoverFont()  # Sottolineato

    # Funzione eseguita quando il mouse viene spostato fuori dalla Label
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setDefaultFont()  # Non sottolineato
