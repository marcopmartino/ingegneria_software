from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle, QWidget


class StylisableWidget(QWidget):

    # Per applicare i fogli di stile alla classe
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)