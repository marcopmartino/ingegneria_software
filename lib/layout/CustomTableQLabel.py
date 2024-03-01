from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QLabel, QSizePolicy

from res import Styles
from res.Dimensions import LineEditDimensions, FontWeight


class CustomTableQLabel(QLabel):
    def __init__(self, field_name: str, text: str, is_header: bool = False, position: Qt.Alignment = Qt.AlignVCenter,
                 parent: QLabel = None):
        super().__init__(parent)
        self.setText(text)
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        if is_header:
            self.setMinimumSize(150, 50)
            font.setBold(True)
            self.setStyleSheet(Styles.TABLE_HEADER)
        else:
            self.setMinimumSize(350, 50)
            self.adjustSize()
            self.setStyleSheet(Styles.LABEL_PROFILE_INFO)
        self.setFont(font)
        self.setAlignment(position)
        self.setObjectName(f"{field_name}_label")

    '''def paintEvent(self, event):
        self.paintEvent(self)
        painter = QPainter(self)
        painter.translate(0, self.height() - 1)
        painter.rotate(-90)
        self.setGeometry(self.x(), self.y(), self.height(), self.width())
        self.render(self, painter)'''

    def minimumSizeHint(self):
        size = QLabel.minimumSizeHint(self)
        return QSize(size.height(), size.width())

    def sizeHint(self):
        size = QLabel.sizeHint(self)
        return QSize(size.height(), size.width())
