from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import SearchLineEdit, ComboBox, CheckBox, PushButton

from lib.controller.ProductListController import ProductListController
from lib.model.Finished import Finished
from lib.model.Product import Product
from lib.model.SemiFinished import SemiFinished
from lib.model.Sketch import Sketch
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
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

        font.setBold(False)
        self.max_storage = QLabel(self.sidebar_frame)
        self.max_storage.setObjectName("max_storage_label")
        self.max_storage.setText(f"Massima capienza: {self.controller.get_max_storge()}")
        self.max_storage.setFont(font)

        self.used_storage = QLabel(self.sidebar_frame)
        self.used_storage.setObjectName("used_storage_label")
        self.used_storage.setText(f"Occupati: {self.controller.get_used_storage()}")
        self.used_storage.setFont(font)

        self.available_storage = QLabel(self.sidebar_frame)
        self.available_storage.setObjectName("available_storage_label")
        self.available_storage.setText(f"Disponibile: {self.controller.get_available_storage()}")
        self.available_storage.setFont(font)

        self.storage_details_layout.addWidget(self.details_title, alignment=Qt.AlignCenter)
        self.storage_details_layout.addWidget(self.max_storage, alignment=Qt.AlignLeft)
        self.storage_details_layout.addWidget(self.used_storage, alignment=Qt.AlignLeft)
        self.storage_details_layout.addWidget(self.available_storage, alignment=Qt.AlignLeft)

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)

        # Label per magazzino vuoto
        self.empty_sketches_storage = QLabel(self.central_frame)
        self.empty_sketches_storage.setObjectName("empty_sketches_label")
        self.empty_sketches_storage.setText("Nessun abbozzo presente in magazzino")
        self.empty_sketches_storage.setFont(font)
        self.empty_semifinished_storage = QLabel(self.central_frame)
        self.empty_semifinished_storage.setObjectName("empty_semifinished_label")
        self.empty_semifinished_storage.setText("Nessun semi-lavorato presente in magazzino")
        self.empty_semifinished_storage.setFont(font)
        self.empty_finished_storage = QLabel(self.central_frame)
        self.empty_finished_storage.setObjectName("empty_finished_label")
        self.empty_finished_storage.setText("Nessuna forma finita presente in magazzino")
        self.empty_finished_storage.setFont(font)

        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_storage_label")
        self.empty_storage.setText("Nessun prodotto in magazzino")
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

        # CheckBox "Abbozzi"
        self.sketches_checkbox = CheckBox(self.sidebar_frame)
        self.sketches_checkbox.setObjectName("sketches_check_box")
        self.sketches_checkbox.setText("Abbozzi")
        self.sketches_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.sketches_checkbox)

        # CheckBox "Semi-lavorati"
        self.semifinished_check_box = CheckBox(self.sidebar_frame)
        self.semifinished_check_box.setObjectName("semifinished_check_box")
        self.semifinished_check_box.setText("Semi-lavorati")
        self.semifinished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.semifinished_check_box)

        # CheckBox "Forme finite"
        self.finished_check_box = CheckBox(self.sidebar_frame)
        self.finished_check_box.setObjectName("finished_check_box")
        self.finished_check_box.setText("Forma finita")
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

        # Label sezioni
        self.sketches_section = QLabel(self.central_frame)
        self.sketches_section.setText("ABBOZZI")
        self.sketches_section.setAlignment(Qt.AlignCenter)
        self.sketches_section.setStyleSheet("background-color: lightgray")
        self.semifinished_section = QLabel(self.central_frame)
        self.semifinished_section.setText("SEMI-LAVORATI")
        self.semifinished_section.setAlignment(Qt.AlignCenter)
        self.semifinished_section.setStyleSheet("background-color: lightgray")
        self.finished_section = QLabel(self.central_frame)
        self.finished_section.setText("FORME FINITE")
        self.finished_section.setAlignment(Qt.AlignCenter)
        self.finished_section.setStyleSheet("background-color: lightgray")

        # Tabella
        self.table_sketches = StandardTable(self.central_frame)
        self.table_semifinished = StandardTable(self.central_frame)
        self.table_finished = StandardTable(self.central_frame)
        self.sketches_headers = ["Seriale", "Prodotto", "Genere", "Plastica", "Tipo", "Dettagli", "Quantità"]
        self.semifinished_headers = ["Seriale", "Prodotto", "Genere", "Plastica", "Tipo di abbozzo",
                                     "Lavorazione principale", "Ferratura", "Tipo bussola",
                                     "Dettagli", "Quantità"]
        self.finished_headers = ["Seriale", "Prodotto", "Genere", "Plastica", "Tipo di abbozzo",
                                 "Lavorazione principale", "Ferratura", "Tipo bussola", "Numeratura",
                                 "Dettagli", "Quantità"]
        self.table_sketches.setHeaders(self.sketches_headers)
        self.table_semifinished.setHeaders(self.semifinished_headers)
        self.table_finished.setHeaders(self.finished_headers)

        # Table Adapter
        self.table_sketches_adapter = StorageListAdapter(self.table_sketches)
        self.table_semifinished_adapter = StorageListAdapter(self.table_semifinished)
        self.table_finished_adapter = StorageListAdapter(self.table_finished)
        product_list = self.controller.get_products_list()
        self.table_sketches_adapter.setData(product_list)
        self.table_semifinished_adapter.setData(product_list)
        self.table_finished_adapter.setData(product_list)

        # self.table_adapter.onSelection(self.show_product_details)

        def update_table(message: Product | dict | str):
            if message['data'] is not None:
                for key, value in message['data'].items():
                    value['serial'] = key
                    match value['type']:
                        case "Abbozzo":
                            self.table_sketches_adapter.addData(value)
                        case "Semi-lavorato":
                            self.table_semifinished_adapter.addData(value)
                        case "Forma finita":
                            self.table_finished_adapter.addData(value)
            else:
                pass
                #self.table_adapter.removeRowByKey(message)

            self.check_empty_tables()

        self.controller.observe_product_list(update_table)

        self.central_layout.addWidget(self.sketches_section)
        self.central_layout.addWidget(self.table_sketches)
        self.central_layout.addWidget(self.empty_sketches_storage, alignment=Qt.AlignCenter)
        self.central_layout.addWidget(self.semifinished_section)
        self.central_layout.addWidget(self.table_semifinished)
        self.central_layout.addWidget(self.empty_semifinished_storage, alignment=Qt.AlignCenter)
        self.central_layout.addWidget(self.finished_section)
        self.central_layout.addWidget(self.table_finished)
        self.central_layout.addWidget(self.empty_finished_storage, alignment=Qt.AlignCenter)
        self.central_layout.addWidget(self.empty_storage, alignment=Qt.AlignJustify)

        self.check_empty_tables()

    def check_empty_tables(self):
        print(f"Abbozzi: {self.table_sketches.rowCount()}")
        print(f"Semi-lavorati: {self.table_semifinished.rowCount()}")
        print(f"Forme finite: {self.table_finished.rowCount()}")
        count = 0
        if self.table_sketches.isEmpty():
            self.empty_sketches_storage.setVisible(True)
            self.table_sketches.setVisible(False)
            count += 1
        else:
            self.empty_sketches_storage.setVisible(False)
            self.table_sketches.setVisible(True)

        if self.table_semifinished.isEmpty():
            self.empty_semifinished_storage.setVisible(True)
            self.table_semifinished.setVisible(False)
            count += 1
        else:
            self.empty_semifinished_storage.setVisible(False)
            self.table_semifinished.setVisible(True)

        if self.table_finished.isEmpty():
            self.empty_finished_storage.setVisible(True)
            self.table_finished.setVisible(False)
            count += 1
        else:
            self.empty_finished_storage.setVisible(False)
            self.table_finished.setVisible(True)

        if count == 3:
            self.empty_sketches_storage.setVisible(False)
            self.sketches_section.setVisible(False)
            self.empty_semifinished_storage.setVisible(False)
            self.semifinished_section.setVisible(False)
            self.empty_finished_storage.setVisible(False)
            self.finished_section.setVisible(False)
            self.empty_storage.setVisible(True)
        else:
            self.sketches_section.setVisible(True)
            self.semifinished_section.setVisible(True)
            self.finished_section.setVisible(True)
            self.empty_storage.setVisible(False)

    # Ritorna la lista di ordini filtrata
    def get_filtered_product_list(self) -> list[Product]:
        return self.controller.get_filtered_product_list(self.form_manager.data())

    # Aggiorna la lista dei prodotti in base ai filtri
    def refresh_products_list(self):
        self.table_sketches.clearSelection()
        self.table_semifinished.clearSelection()
        self.table_finished.clearSelection()
        filtered_list = self.get_filtered_product_list()
        sketches_list: list[Sketch] = []
        semifinished_list: list[SemiFinished] = []
        finished_list: list[Finished] = []
        for element in filtered_list:
            if type(element) is Sketch:
                sketches_list.append(element)
            elif type(element) is SemiFinished:
                semifinished_list.append(element)
            else:
                finished_list.append(element)
        self.table_sketches_adapter.setData(sketches_list)
        self.table_semifinished_adapter.setData(semifinished_list)
        self.table_finished_adapter.setData(finished_list)
        self.check_empty_tables()

    # Mostra la form per l'aggiunta dei prodotti
    '''def show_order_form(self):
        pass
        product_form = CreateProductView(self)
        product_form.exec()

    # Mostra la schermata con i dettagli del prodotto
    def show_product_details(self, serial: str):
        print(f"Prodotto selezionato: {serial}")
        product_details = ProductDetailsView(self, serial)
        self.window().addRemovableSubInterface(product_details, text=f"Prodotto {serial}")'''


class StorageListAdapter(TableAdapter):
    def adaptData(self, product: Sketch | SemiFinished | Finished | dict) -> list[str]:
        if issubclass(type(product), Product):
            if type(product) is Sketch:
                return [product.get_serial(),
                        product.get_product_type(),
                        product.get_gender(),
                        product.get_plastic(),
                        product.get_sketch_type(),
                        product.get_details(),
                        str(product.get_amount())]
            elif type(product) is SemiFinished:
                return [product.get_serial(),
                        product.get_product_type(),
                        product.get_gender(),
                        product.get_plastic(),
                        product.get_sketch_type(),
                        product.get_main_process(),
                        product.get_shoeing(),
                        product.get_first_compass(),
                        product.get_details(),
                        str(product.get_amount())]
            else:
                return [product.get_serial(),
                        product.get_product_type(),
                        product.get_gender(),
                        product.get_plastic(),
                        product.get_sketch_type(),
                        product.get_main_process(),
                        product.get_shoeing(),
                        product.get_first_compass(),
                        product.get_numbering(),
                        product.get_details(),
                        str(product.get_amount())]
        else:
            if product['type'] == "Abbozzo":
                return [product['serial'],
                        product['type'],
                        product['gender'],
                        product['plastic'],
                        product['sketch_type'],
                        product['details'],
                        str(product['amount'])]
            elif product['type'] == "Semi-lavorato":
                return [product['serial'],
                        product['type'],
                        product['gender'],
                        product['plastic'],
                        product['sketch_type'],
                        product['main_process'],
                        product['shoeing'],
                        product['first_compass'],
                        product['details'],
                        str(product['amount'])]
            else:
                return [product['serial'],
                        product['type'],
                        product['gender'],
                        product['plastic'],
                        product['sketch_type'],
                        product['main_process'],
                        product['shoeing'],
                        product['first_compass'],
                        product['numbering'],
                        product['details'],
                        str(product['amount'])]
