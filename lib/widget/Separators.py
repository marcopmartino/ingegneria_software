from PyQt5.QtWidgets import QFrame, QWidget, QSizePolicy, QSpacerItem

from res import Colors
from res.Dimensions import SpacerDimensions


# Separatore costituito da una linea orizzontale
class HorizontalLine(QFrame):

    def __init__(self, parent: QWidget = None, color: Colors = Colors.GREY):
        super().__init__(parent)

        self.setStyleSheet("color: " + color)
        self.setFrameShape(QFrame.HLine)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)


# Separatore costituito da una linea verticale
class VerticalLine(QFrame):

    def __init__(self, parent: QWidget = None, color: Colors = Colors.GREY):
        super().__init__(parent)

        self.setStyleSheet("color: " + color)
        self.setFrameShape(QFrame.VLine)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)


# Spacer orizzontale
class HorizontalSpacer(QSpacerItem):
    def __init__(self, width: int = SpacerDimensions.DEFAULT_PRIMARY, size_policy: QSizePolicy = QSizePolicy.Preferred):
        super().__init__(width, SpacerDimensions.DEFAULT_SECONDARY, size_policy, QSizePolicy.Minimum)


# Spacer verticale
class VerticalSpacer(QSpacerItem):
    def __init__(self, heigth: int = SpacerDimensions.DEFAULT_PRIMARY,
                 size_policy: QSizePolicy = QSizePolicy.Preferred):
        super().__init__(SpacerDimensions.DEFAULT_SECONDARY, heigth, QSizePolicy.Minimum, size_policy)
