from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import SearchLineEdit, CheckBox, PushButton

from lib.controller.ProductListController import ProductListController
from lib.model.StoredItems import StoredShoeLastVariety
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.view.storage.ProductView import ProductView
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res.Dimensions import FontSize


class ProductsTab(SubInterfaceChildWidget):

    def __init__(self, parent_widget: SubInterfaceWidget):
        super().__init__("products_list_view", parent_widget)
        self.hideHeader()

        self.controller = ProductListController()

        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(12)

        self.storage_details_layout = QVBoxLayout(self.sidebar_frame)
        self.storage_details_layout.setSpacing(8)
        self.storage_details_layout.setObjectName("storage_details_layout")

        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        font.setBold(True)

        self.details_title = QLabel(self.sidebar_frame)
        self.details_title.setObjectName("details_title_label")
        self.details_title.setText("Capienza reparto")
        self.details_title.setFont(font)

        self.max_storage = QLabel(self.sidebar_frame)
        self.max_storage.setObjectName("max_storage_label")
        self.max_storage.setText(f"Massima: {self.controller.get_max_storge()}")
        font.setBold(False)
        self.max_storage.setFont(font)
        font.setBold(True)

        self.storage_details_layout.addWidget(self.details_title)
        self.storage_details_layout.addWidget(self.max_storage, alignment=Qt.AlignLeft)

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)

        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_storage_label")
        self.empty_storage.setText("Nessun prodotto in magazzino, modificare i filtri.")
        self.empty_storage.setFont(font)

        # Layout con il checkgroup
        self.checkgroup_layout = QVBoxLayout()
        self.checkgroup_layout.setSpacing(8)
        self.checkgroup_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.checkgroup_label = QLabel(self.sidebar_frame)
        self.checkgroup_label.setObjectName("marking_group_label")
        self.checkgroup_label.setText("Filtra per tipo:")
        self.checkgroup_label.setFont(font)
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Abbozzo"
        self.sketches_checkbox = CheckBox(self.sidebar_frame)
        self.sketches_checkbox.setObjectName("sketch_check_box")
        self.sketches_checkbox.setText("Abbozzo")
        self.sketches_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.sketches_checkbox)

        # CheckBox "Abbozzo sgrossato"
        self.semifinished_check_box = CheckBox(self.sidebar_frame)
        self.semifinished_check_box.setObjectName("worked_sketch_check_box")
        self.semifinished_check_box.setText("Abbozzo sgrossato")
        self.semifinished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.semifinished_check_box)

        # CheckBox "Forme finite"
        self.finished_check_box = CheckBox(self.sidebar_frame)
        self.finished_check_box.setObjectName("finished_check_box")
        self.finished_check_box.setText("Forma finita")
        self.finished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.finished_check_box)

        # CheckBox "Forme numerata"
        self.finished_check_box = CheckBox(self.sidebar_frame)
        self.finished_check_box.setObjectName("numbered_finished_check_box")
        self.finished_check_box.setText("Forma numerata")
        self.finished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.finished_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_products_list)

        # Spacer tra i due pulsanti
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addItem(self.storage_details_layout)
        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.search_box)
        self.sidebar_layout.addItem(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.sidebar_spacer)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table_products = StandardTable(self.central_frame)
        self.products_headers = ["Seriale", "Tipo Prodotto", "Genere", "Tipo abbozzo", "Tipo plastica",
                                 "Taglia", "Lavorazione principale", "Prima bussola", "Seconda_bussola",
                                 "Perno sotto tallone", "Ferratura", "Punta ferrata", "Numeratura anticollo",
                                 "Numeratura laterale", "Numeratura tacco", "Quantità"]
        self.table_products.setHeaders(self.products_headers)

        # Table Adapter
        self.table_products_adapter = StorageListAdapter(self.table_products)
        product_list = self.controller.get_products_list()
        self.table_products_adapter.setData(product_list)
        self.table_products_adapter.onDoubleClick(self.show_product_details)

        # self.table_adapter.onSelection(self.show_product_details)

        def update_table(message: Message):
            data = message.data()
            match message.event():
                case StorageRepository.Event.PRODUCTS_INITIALIZED:
                    self.table_products_adapter.setData(
                        self.controller.filter_product_list(self.form_manager.data(), *data))

                case StorageRepository.Event.PRODUCT_CREATED:
                    if len(self.controller.filter_product_list(self.form_manager.data(), data)) != 0:
                        self.table_products_adapter.addData(data)

                case StorageRepository.Event.PRODUCT_UPDATED:
                    self.table_products_adapter.updateDataColumns(data, [15])

            self.check_empty_tables()

        self.messageReceived.connect(update_table)
        self.controller.observe_product_list(self.messageReceived.emit)

        self.central_layout.addWidget(self.table_products)
        self.central_layout.addWidget(self.empty_storage, alignment=Qt.AlignJustify)

        self.check_empty_tables()

    def check_empty_tables(self):
        if self.table_products.isEmpty():
            self.empty_storage.setVisible(True)
            self.table_products.setVisible(False)
        else:
            self.empty_storage.setVisible(False)
            self.table_products.setVisible(True)

    # Ritorna la lista di ordini filtrata
    def get_filtered_product_list(self) -> list[StoredShoeLastVariety]:
        return self.controller.get_filtered_product_list(self.form_manager.data())

    # Aggiorna la lista dei prodotti in base ai filtri
    def refresh_products_list(self):
        filtered_list = self.get_filtered_product_list()
        self.table_products_adapter.setData(filtered_list)
        self.check_empty_tables()

    # Mostra la schermata con i dettagli del prodotto
    def show_product_details(self, serial: str):
        print(f"Prodotto selezionato: {serial}")
        product_details = ProductView(self, self.controller.get_product_by_id(serial))
        self.window().addRemovableSubInterface(product_details, text=f"Prodotto {serial}")


class StorageListAdapter(TableAdapter):
    def adaptData(self, product: StoredShoeLastVariety) -> list[str]:
        return [product.get_item_id(),
                product.get_shoe_last_variety().get_product_type(),
                product.get_shoe_last_variety().get_gender(),
                product.get_shoe_last_variety().get_shoe_last_type(),
                "Tipo" + str(product.get_shoe_last_variety().get_plastic_type()),
                product.get_shoe_last_variety().get_size(),
                product.get_shoe_last_variety().get_processing(),
                product.get_shoe_last_variety().get_first_compass_type(),
                product.get_shoe_last_variety().get_second_compass_type(),
                product.get_shoe_last_variety().get_pivot_under_heel(),
                product.get_shoe_last_variety().get_shoeing(),
                product.get_shoe_last_variety().get_iron_tip(),
                product.get_shoe_last_variety().get_numbering_antineck(),
                product.get_shoe_last_variety().get_numbering_lateral(),
                product.get_shoe_last_variety().get_numbering_heel(),
                str(product.get_quantity())]
