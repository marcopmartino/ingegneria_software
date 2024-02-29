from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel


# Estensione di QLabel. ClickableLabel emette un segnale quando rileva un evento di click su di essa.
class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Emette il segnale "clicked" quando viene effettuato un click sulla Label con il tasto sinistro del mouse
    def mousePressEvent(self, event):
        if Qt.LeftButton == event.button():
            self.clicked.emit()
