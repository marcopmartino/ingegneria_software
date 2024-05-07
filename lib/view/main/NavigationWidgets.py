from PyQt5.QtCore import Qt, QRect, QPoint, QRectF
from PyQt5.QtGui import QIcon, QPainter, QBrush, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import NavigationTreeWidget, FluentIconBase, NavigationPushButton, themeColor, drawIcon

from lib.utility.ResourceManager import ResourceManager
from lib.utility.UtilityClasses import PriceFormatter


# NavigationWidget rimuovibile
class RemovableNavigationWidget(NavigationTreeWidget):

    def __init__(self, parent_widget: QWidget, icon: str | QIcon | FluentIconBase, text: str):
        # Inizializza il NavigationWidget
        super().__init__(icon, text, True, parent_widget)

        # Carica l'icona per chiudere l'interfaccia corrispondente
        self.close_icon = ResourceManager.icon("close_icon.png")

    # Personalizza la grafica
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)  # Imposta la penna
        painter.setBrush(QBrush(self.close_icon))  # Imposta il pennello

        # Mentre il cursore è sulla voce del menù, mostra l'icona per chiudere l'interfaccia
        if self.isEnter:
            painter.translate(160, 6)  # Sposta il cursore del QPainter
            painter.drawEllipse(0, 0, 24, 24)  # Traccia l'icona


# NavigationWidget per mostrare la disponibilità di cassa
class CashRegisterAvailabilityNavigationWidget(NavigationPushButton):

    def __init__(self, parent_widget: QWidget, icon: str | QIcon | FluentIconBase, text: str):
        # Inizializza il NavigationWidget
        super().__init__(icon, text, False, parent_widget)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        # draw background
        c = 0
        m = self._margins()
        pl, pr = m.left(), m.right()
        global_rect = QRect(self.mapToGlobal(QPoint()), self.size())

        if self._canDrawIndicator():
            painter.setBrush(QColor(c, c, c, 6 if self.isEnter else 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

            # draw indicator
            painter.setBrush(themeColor())
            painter.drawRoundedRect(pl, 10, 3, 16, 1.5, 1.5)
        elif self.isEnter and self.isEnabled() and global_rect.contains(QCursor.pos()):
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)  # Disegna il rettangolo

        # Disegna l'icona
        drawIcon(self._icon, painter, QRectF(11.5 + pl, 10, 16, 16))

        if self.isCompacted:
            return

        # Imposta il font
        painter.setFont(self.font())

        # Estrae il valore dal testo
        value = PriceFormatter.unformat(self.text())

        # Imposta il colore
        color = QColor(0, 0, 0)
        if value > 0:
            color = QColor(0, 100, 0)
        elif value < 0:
            color = QColor(139, 0, 0)

        # Imposta la penna
        painter.setPen(color)

        # Disegna il testo
        left = 44
        painter.drawText(QRectF(left, 0, self.width() - 13 - left, self.height()), Qt.AlignVCenter, self.text())