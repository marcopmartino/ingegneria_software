from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget

from lib.widget.ClickableLabel import ClickableLabel
from lib.widget.FocusableLabel import FocusableLabel
from res.Dimensions import FontWeight, FontSize


# ClickableLabel che appare in fondo al layout centrale nelle schermate di login e di registrazione
# noinspection PyPep8Naming
class InteractiveLabel(ClickableLabel, FocusableLabel):

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
