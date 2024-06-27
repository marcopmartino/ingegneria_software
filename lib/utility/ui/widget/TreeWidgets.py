from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTreeView, QWidget
from qfluentwidgets import TreeItemDelegate, TreeWidget

from res.Dimensions import FontSize


class DefaultFontTreeItemDelegate(TreeItemDelegate):

    def __init__(self, parent: QTreeView):
        super().__init__(parent)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # Modifica la dimensione del font
        font = QFont()
        font.setPointSize(FontSize.DEFAULT)
        option.font = font


# noinspection PyPep8Naming
class AutoResizableTreeWidget(TreeWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Disabilita lo scrolling
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Calcola la nuova altezza a ogni espansione o compressione
        self.expanded.connect(self.updateHeight)
        self.collapsed.connect(self.updateHeight)

    def updateHeight(self):
        self.setMaximumHeight(self.sizeHint().height())

    def getHeight(self, parent=None):
        height = 0
        if not parent:
            parent = self.rootIndex()
        for row in range(self.model().rowCount(parent)):
            child = self.model().index(row, 0, parent)
            height += self.rowHeight(child)
            if self.isExpanded(child) and self.model().hasChildren(child):
                height += self.getHeight(child)
        return height

    def sizeHint(self):
        hint = super().sizeHint()
        hint.setHeight(self.getHeight() + self.frameWidth() * 2)
        return hint

    def minimumSizeHint(self):
        return self.sizeHint()
