from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget
)
from qfluentwidgets import SegmentedWidget, FluentIconBase, FluentIcon

from lib.controller.StorageListController import StorageListController
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.storage.MaterialsTab import MaterialsTab
from lib.view.storage.ProductsTab import ProductsTab
from lib.view.storage.WasteTab import WasteTab


# noinspection PyPep8Naming
class StoragePage(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = FluentIcon.LIBRARY):
        super().__init__("storage_page_view", parent_widget, svg_icon)
        # self.central_frame.setMinimumWidth(800)
        self.hideSidebar()

        # Titolo e sottotitolo
        self.setTitleText("Magazzino")
        self.setSubtitleText("Visualizzazione magazzino formificio")

        self.navigation = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self.central_frame)

        self.storage_controller = StorageListController()

        self.productsInterface = ProductsTab(self, self.storage_controller)
        self.materialsInterface = MaterialsTab(self, self.storage_controller)
        self.wasteInterface = WasteTab(self, self.storage_controller)

        # add items to pivot
        self.addSubInterface(self.productsInterface, 'productsInterface', 'Forme, Abbozzi e Semi-lavorati')
        self.addSubInterface(self.materialsInterface, 'materialsInterface', 'Materiali')
        self.addSubInterface(self.wasteInterface, 'wasteInterface', 'Scarti')

        self.vBoxLayout.addWidget(self.navigation)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.productsInterface)
        self.navigation.setCurrentItem(self.productsInterface.objectName())

        self.central_layout.addLayout(self.vBoxLayout)
        self.central_layout.setAlignment(self.vBoxLayout, Qt.AlignCenter)

    def addSubInterface(self, widget: SubInterfaceWidget, objectName, text):
        self.stackedWidget.addWidget(widget)
        self.navigation.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.navigation.setCurrentItem(widget.objectName())
