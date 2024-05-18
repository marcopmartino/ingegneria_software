from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import CheckBox, PushButton

from lib.controller.WastesListController import WastesListController
from lib.model.Product import Product
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res.Dimensions import FontSize


class WastesTab(SubInterfaceChildWidget):
    def __init__(self, parent_widget: SubInterfaceWidget):
        super().__init__("wastes_list_view", parent_widget)
        self.hideHeader()

        self.controller = WastesListController()

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

        # Label per magazzino vuoto
        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_label")
        self.empty_storage.setText("Nessun prodotto presente in magazzino")
        self.empty_storage.setFont(font)

        # Layout con il checkgroup
        self.checkgroup1_layout = QVBoxLayout()
        self.checkgroup1_layout.setSpacing(8)
        self.checkgroup1_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.checkgroup1_label = QLabel(self.sidebar_frame)
        self.checkgroup1_label.setObjectName("marking_group_label")
        self.checkgroup1_label.setText("Filtra per plastica:")
        self.checkgroup1_label.setFont(font)
        self.checkgroup1_layout.addWidget(self.checkgroup1_label)

        # CheckBox "Plastica tipo 1"
        self.plastic1_checkbox = CheckBox(self.sidebar_frame)
        self.plastic1_checkbox.setObjectName("plastic1_check_box")
        self.plastic1_checkbox.setText("Tipo 1")
        self.plastic1_checkbox.setChecked(True)
        self.checkgroup1_layout.addWidget(self.plastic1_checkbox)

        # CheckBox "Plastica tipo 2"
        self.plastic2_check_box = CheckBox(self.sidebar_frame)
        self.plastic2_check_box.setObjectName("plastic2_check_box")
        self.plastic2_check_box.setText("Tipo 2")
        self.plastic2_check_box.setChecked(True)
        self.checkgroup1_layout.addWidget(self.plastic2_check_box)

        # CheckBox "Plastica tipo 2"
        self.plastic3_check_box = CheckBox(self.sidebar_frame)
        self.plastic3_check_box.setObjectName("plastic3_check_box")
        self.plastic3_check_box.setText("Tipo 3")
        self.plastic3_check_box.setChecked(True)
        self.checkgroup1_layout.addWidget(self.plastic3_check_box)

        # Layout con il checkgroup
        self.checkgroup2_layout = QVBoxLayout()
        self.checkgroup2_layout.setSpacing(8)
        self.checkgroup2_layout.setObjectName("first_checkgroup_layout")

        # self.sort_combo_box.currentIndexChanged.connect(on_sorter_combo_index_changed)
        #self.sort_combo_box.setCurrentIndex(0)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_wastes_list)

        # Button "Vendi scarti"
        self.sell_button = PushButton(self.sidebar_frame)
        self.sell_button.setText("Vendi scarti")
        self.refresh_button.clicked.connect(self.sell_wastes)

        # Spacer tra i due pulsanti
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addItem(self.storage_details_layout)
        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addItem(self.checkgroup1_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.sell_button)
        self.sidebar_layout.addWidget(self.sidebar_spacer)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Dettagli", "Quantità"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = StorageListAdapter(self.table)
        self.table_adapter.setData(self.controller.get_wastes_list())

        # self.table_adapter.onSelection(self.show_product_details)

        def update_table(message: Product | str):
            if type(message) is Product:
                self.table_adapter.addData([message])
            else:
                self.table_adapter.removeRowByKey(message)

            if self.table.isEmpty():
                self.empty_storage.setVisible(True)
                self.table.setVisible(False)
            else:
                self.empty_storage.setVisible(False)
                self.table.setVisible(True)

        self.controller.observe_wastes_list(update_table)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.empty_storage, alignment=Qt.AlignJustify)

        if self.table.isEmpty():
            self.empty_storage.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_storage.setVisible(False)
            self.table.setVisible(True)

    # Ritorna la lista degli scarti filtrata
    def get_filtered_wastes_list(self) -> list[Product]:
        return self.controller.get_filtered_wastes_list(self.form_manager.data())

    # Aggiorna la lista degli scarti in base ai filtri
    def refresh_wastes_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_wastes_list())
        if self.table.isEmpty():
            self.empty_storage.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_storage.setVisible(False)
            self.table.setVisible(True)

    # Aggiorna la lista degli scarti in base ai filtri
    def sell_wastes(self):
        pass

    # Mostra la form per l'aggiunta degli scarti
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
    def adaptData(self, waste: Product) -> list[str]:
        return [waste.get_details(),
                str(waste.get_amount())
                ]
