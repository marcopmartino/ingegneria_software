from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle, QWidget


# Estensione di QWidget che preserva la possibilità di applicare fogli di stile (normalmente non possono essere
# applicati alle classi che estendono QWidget)
class StylisableWidget(QWidget):

    # Per applicare i fogli di stile alla classe
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
