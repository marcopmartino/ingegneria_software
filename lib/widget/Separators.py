from PyQt5.QtWidgets import QFrame, QWidget, QSizePolicy

from res import Colors


# Separatore costituito da una linea orizzontale
class HorizontalLine(QFrame):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setStyleSheet("color: " + Colors.GREY)
        self.setFrameShape(QFrame.HLine)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)


# Separatore costituito da una linea verticale
class VerticalLine(QFrame):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setStyleSheet("color: " + Colors.GREY)
        self.setFrameShape(QFrame.VLine)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
