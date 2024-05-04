from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import SearchLineEdit, ComboBox, CheckBox, PushButton

from lib.controller.MaterialsListController import MaterialsListController
from lib.view.main.BaseWidget import BaseWidget
from lib.model.Product import Product
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res.Dimensions import FontSize


class MaterialsTab(BaseWidget):
    def __init__(self, parent_widget: QWidget):
        super().__init__("materials_list_view", parent_widget)
        self.hideHeader()

        self.controller = MaterialsListController()

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

        # Ordina ComboBox
        self.sort_combo_box = ComboBox(self.sidebar_frame)
        self.sort_combo_box.setObjectName("sort_combobox_line_edit")
        self.sort_combo_box.insertItem(0, "Quantità crescente", userData="crescente")
        self.sort_combo_box.insertItem(1, "Quantità decrescente", userData="decrescente")

        def on_sorter_combo_index_changed(index: int):
            self.search_box.setText("")
            match index:
                case 0:
                    self.controller.sort_materials(False)
                case 1:
                    self.controller.sort_materials(True)

        self.sort_combo_box.currentIndexChanged.connect(on_sorter_combo_index_changed)
        self.sort_combo_box.setCurrentIndex(0)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_materials_list)

        # Spacer tra i due pulsanti
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addItem(self.storage_details_layout)
        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.search_box)
        self.sidebar_layout.addItem(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.sort_combo_box)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.sidebar_spacer)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Seriale", "Tipo", "Dettagli", "Quantità"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = StorageListAdapter(self.table)
        self.table_adapter.setData(self.controller.get_materials_list())

        # self.table_adapter.onSelection(self.show_product_details)

        def update_table(message: Product | str):
            if type(message) is Product:
                self.table_adapter.addData([message])
            else:
                self.table_adapter.removeRowByKey(message)

        self.controller.observe_materials_list(update_table)

        self.central_layout.addWidget(self.table)

    # Ritorna la lista di ordini filtrata
    def get_filtered_materials_list(self) -> list[Product]:
        return self.controller.get_filtered_materials_list(self.form_manager.data())

    # Aggiorna la lista dei materiali in base ai filtri
    def refresh_materials_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_materials_list())

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
    def adaptData(self, product: Product) -> list[str]:
        return [product.get_serial(),
                product.get_type(),
                product.get_details(),
                str(product.get_amount())
                ]
