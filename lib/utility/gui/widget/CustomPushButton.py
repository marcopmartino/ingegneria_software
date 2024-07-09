from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import PushButton

from res import Styles
from res.Dimensions import FontWeight, FontSize


# Pulsante principale usato nell'applicazione
class CustomPushButton(PushButton):
    def __init__(
            self, parent: QWidget = None,
            text: str = "",
            style_sheet: str = "",
            point_size: int = None,
            font_weight: int = None,
    ):
        super().__init__(parent)

        # Imposta il testo
        self.setText(text)

        # Imposta lo stile
        self.setStyleSheet(style_sheet)

        # Imposta il font
        font = QFont()
        if point_size is not None:
            font.setPointSize(point_size)
            self.setFont(font)
        if font_weight is not None:
            font.setWeight(font_weight)
            self.setFont(font)

    # Pulsante predefinito bianco
    @classmethod
    def white(cls, parent: QWidget = None, text: str = None, point_size: int = None, font_weight: int = None):
        return cls(parent, text, Styles.WHITE_BUTTON, point_size, font_weight)

    # Pulsante predefinito ciano
    @classmethod
    def cyan(cls, parent: QWidget = None, text: str = None, point_size: int = None, font_weight: int = None):
        return cls(parent, text, Styles.CYAN_BUTTON, point_size, font_weight)

    # Pulsante predefinito arancione
    @classmethod
    def orange(cls, parent: QWidget = None, text: str = None, point_size: int = None, font_weight: int = None):
        return cls(parent, text, Styles.ORANGE_BUTTON, point_size, font_weight)

    # Pulsante predefinito rosso
    @classmethod
    def red(cls, parent: QWidget = None, text: str = None, point_size: int = FontSize.FLUENT_DEFAULT,
            font_weight: int = FontWeight.BOLD):
        return cls(parent, text, Styles.RED_BUTTON, point_size, font_weight)
