from PyQt5.QtWidgets import QWidget, QStackedWidget
from qfluentwidgets import SegmentedWidget, FluentIconBase

from lib.controller.StorageController import StorageController
from lib.utility.gui.widget.CustomIcon import CustomIcon
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.storage.HardwareStorePriceCatalogView import HardwareStorePriceCatalogView
from lib.view.storage.MaterialsTab import MaterialsTab
from lib.view.storage.ProductsTab import ProductsTab
from lib.view.storage.RawShoeLastCenterPriceCatalogView import RawShoeLastCenterPriceCatalogView
from lib.view.storage.WasteTab import WasteTab


# noinspection PyPep8Naming
class StorageView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.STORAGE):
        super().__init__("storage_page_view", parent_widget, svg_icon)

        # Titolo e sottotitolo
        self.setTitleText("Magazzino")
        self.setSubtitleText("Clicca due volte su un oggetto immagazzinato per modificarne la quantità")

        # Nasconde la sidebar
        self.hideSidebar()

        # Controller
        self.storage_controller = StorageController()

        # Inizializza la navigazione tra le tab
        self.navigation = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)

        # Inizializza le tab
        self.productsInterface = ProductsTab(self, self.storage_controller)
        self.materialsInterface = MaterialsTab(self, self.storage_controller)
        self.wasteInterface = WasteTab(self, self.storage_controller)

        # Assegna delle callback ai pulsanti per le operazioni di acquisto e vendita
        self.productsInterface.purchase_button.clicked.connect(self.show_raw_shoe_last_center_price_catalog_view)
        self.materialsInterface.purchase_button.clicked.connect(self.show_hardware_store_price_catalog_view)
        self.wasteInterface.sale_button.clicked.connect(self.show_raw_shoe_last_center_price_catalog_view)

        # Aggiunge le tab allo StackedWidget e al sistema di navigazione
        self.addSubInterface(self.productsInterface, 'productsInterface', 'Forme, Abbozzi e Semi-lavorati')
        self.addSubInterface(self.materialsInterface, 'materialsInterface', 'Materiali')
        self.addSubInterface(self.wasteInterface, 'wasteInterface', 'Scarti')

        self.central_layout.addWidget(self.navigation)
        self.central_layout.addWidget(self.stackedWidget)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(12, 12, 12, 12)

        # Assegna uno slot al signal "currentChanged" dello StackedWidget; imposta il widget e l'item corrente
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.productsInterface)
        self.navigation.setCurrentItem(self.productsInterface.objectName())

    # Aggiunge un'interfaccia di navigazione allo StackedWidget
    def addSubInterface(self, widget: SubInterfaceWidget, objectName, text):
        self.stackedWidget.addWidget(widget)
        self.navigation.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    # Aggiorna la visualizzazione delle etichette delle tab in base al widget corrente
    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.navigation.setCurrentItem(widget.objectName())

    # Mostra la schermata con il listino prezzi del centro abbozzi
    def show_raw_shoe_last_center_price_catalog_view(self):
        self.window().addRemovableSubInterface(
            RawShoeLastCenterPriceCatalogView(self, self.storage_controller), text="Centro abbozzi")

    # Mostra la schermata con il listino prezzi del centro abbozzi
    def show_hardware_store_price_catalog_view(self):
        self.window().addRemovableSubInterface(
            HardwareStorePriceCatalogView(self, self.storage_controller), text="Ferramenta")
