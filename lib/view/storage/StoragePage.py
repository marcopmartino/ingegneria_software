from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QStackedWidget
)
from qfluentwidgets import SegmentedWidget

from lib.view.main.BaseWidget import BaseWidget
from lib.view.storage.ProductsPage import ProductsPage


class StoragePage(BaseWidget):
    def __init__(self, parent_widget: QWidget):
        super().__init__("storage_page_view", parent_widget)
        # self.central_frame.setMinimumWidth(800)
        self.hideSidebar()

        # Titolo e sottotitolo
        self.setTitleText("Magazzino")
        self.setSubtitleText("Visualizzazione magazzino formificio")

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self.central_frame)

        self.productsInterface = ProductsPage(self)
        self.materialsInterface = QLabel('Materiali', self)
        self.wasteInterface = QLabel('Scarti', self)

        # add items to pivot
        self.addSubInterface(self.productsInterface, 'productsInterface', 'Forme, Abbozzi e Semi-lavorati')
        self.addSubInterface(self.materialsInterface, 'materialsInterface', 'Materiali')
        self.addSubInterface(self.wasteInterface, 'wasteInterface', 'Scarti')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.productsInterface)
        self.pivot.setCurrentItem(self.productsInterface.objectName())

        self.central_layout.addLayout(self.vBoxLayout)
        self.central_layout.setAlignment(self.vBoxLayout, Qt.AlignCenter)

    def addSubInterface(self, widget: BaseWidget, objectName, text):
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


