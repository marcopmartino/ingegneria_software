from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget

from lib.widget.ClickableLabel import ClickableLabel
from res.Dimensions import FontWeight, FontSize


# noinspection PyPep8Naming

class AccessBottomLabel(ClickableLabel):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)
        self.setDefaultFont()

    # Inizializza il font della Label
    @staticmethod
    def __initialize_font():
        font = QFont()
        font.setPointSize(FontSize.SMALL)
        font.setWeight(FontWeight.BOLD)
        return font

    # Imposta il font della Label
    def setDefaultFont(self):
        self.setFont(self.__initialize_font())

    def setOnHoverFont(self):
        font = self.__initialize_font()
        font.setUnderline(True)
        self.setFont(font)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setOnHoverFont()  # Sottolineato

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setDefaultFont()  # Non sottolineato
