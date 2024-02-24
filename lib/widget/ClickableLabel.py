from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    def mousePressEvent(self, event):
        self.clicked.emit()
