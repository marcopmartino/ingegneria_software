from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHeaderView, QDialog
from qfluentwidgets import SearchLineEdit, CheckBox

from lib.controller.StorageController import StorageController
from lib.firebaseData import Firebase
from lib.model.StoredItems import StoredShoeLastVariety
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.view.storage.ManualChangeStoredItemView import ManualChangeStoredItemView
from lib.widget.CustomPushButton import CustomPushButton
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable, IntegerTableItem
from res import Styles
from res.Dimensions import FontSize


class ProductsTab(SubInterfaceChildWidget):

    def __init__(self, parent_widget: SubInterfaceWidget, storage_controller: StorageController):
        super().__init__("product_list_view", parent_widget, scrollable_sidebar=True)

        # Controller
        self.controller = storage_controller

        # Nasconde l'header
        self.hideHeader()

        # Imposta lo stile
        self.setStyleSheet(Styles.BASE_WIDGET_TAB)

        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # Informazioni sulla quantità totale immagazzinata di forme
        self.storage_details_layout = QVBoxLayout(self.sidebar_frame)
        self.storage_details_layout.setSpacing(8)
        self.storage_details_layout.setObjectName("storage_details_layout")

        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        font.setBold(True)

        self.details_title = QLabel(self.sidebar_frame)
        self.details_title.setObjectName("details_title_label")
        self.details_title.setText("Prodotti immagazzinati")
        self.details_title.setFont(font)

        self.stored_quantity_label = QLabel(self.sidebar_frame)
        self.stored_quantity_label.setObjectName("stored_products_label")

        font.setBold(False)
        self.stored_quantity_label.setFont(font)
        self.storage_details_layout.addWidget(self.details_title)
        self.storage_details_layout.addWidget(self.stored_quantity_label)

        # Search Label
        self.search_label = QLabel(self.sidebar_frame)
        self.search_label.setText("Cerca in base ai dettagli:")

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)
        self.search_box.setMaxLength(50)

        # Layout di ricerca con SearchBox e ComboBox
        self.search_box_layout = QVBoxLayout(self.sidebar_frame)
        self.search_box_layout.setContentsMargins(0, 0, 0, 0)
        self.search_box_layout.setSpacing(12)
        self.search_box_layout.addWidget(self.search_label)
        self.search_box_layout.addWidget(self.search_box)

        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_storage_label")
        self.empty_storage.setText("Nessun prodotto in magazzino, modificare i filtri.")
        font.setBold(True)
        self.empty_storage.setFont(font)

        # Layout con il checkgroup
        self.checkgroup_layout = QVBoxLayout()
        self.checkgroup_layout.setSpacing(12)
        self.checkgroup_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.checkgroup_label = QLabel(self.sidebar_frame)
        self.checkgroup_label.setObjectName("marking_group_label")
        self.checkgroup_label.setText("Filtra per tipo di prodotto:")
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

        self.checkgroup_layout.addWidget(HorizontalLine(self.sidebar_frame))  # Secondo spacer

        # CheckBox "Disponibile"
        self.available_check_box = CheckBox(self.sidebar_frame)
        self.available_check_box.setObjectName("available_check_box")
        self.available_check_box.setText("Disponibile")
        self.available_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.available_check_box)

        # CheckBox "Non disponibile"
        self.not_available_check_box = CheckBox(self.sidebar_frame)
        self.not_available_check_box.setObjectName("notavailable_check_box")
        self.not_available_check_box.setText("Non disponibile")
        self.not_available_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.not_available_check_box)

        def change_available(state: bool):
            if not state and not self.not_available_check_box.isChecked():
                self.not_available_check_box.setChecked(True)

        def change_not_available(state: bool):
            if not state and not self.available_check_box.isChecked():
                self.available_check_box.setChecked(True)

        self.available_check_box.clicked.connect(change_available)
        self.not_available_check_box.clicked.connect(change_not_available)

        # Button "Aggiorna lista"
        self.refresh_button = CustomPushButton.white(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_products_list)

        # Separatore tra "Aggiorna lista" e "Acquista abbozzi"
        self.separator = HorizontalLine(self.sidebar_frame)

        # Button "Acquista abbozzi"
        self.purchase_button = CustomPushButton.cyan(self.sidebar_frame)
        self.purchase_button.setText("Acquista abbozzi")

        # Aggiungo i campi della form e altri widget al layout della sidebar
        self.sidebar_layout.addItem(self.storage_details_layout)
        self.sidebar_layout.addWidget(HorizontalLine(self.sidebar_frame))  # Primo spacer
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.separator)  # Terzo spacer
        self.sidebar_layout.addWidget(self.purchase_button)

        # Nasconde il separatore e il pulsante di acquisto se l'utente corrente è un operaio
        if Firebase.auth.currentUserRole() == "worker":
            self.separator.hide()
            self.purchase_button.hide()

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        self.product_headers = ["Seriale", "Dettagli", "Quantità (paia)"]
        self.table.setHeaders(self.product_headers)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 200)

        # Table Adapter
        self.table_adapter = StorageListAdapter(self.table)
        self.table_adapter.setColumnItemClass(2, IntegerTableItem)
        self.table_adapter.hideKeyColumn()
        self.table_adapter.onDoubleClick(self.show_product_edit_dialog)

        def update_table(message: Message):
            data = message.data()
            match message.event():
                case StorageRepository.Event.PRODUCTS_INITIALIZED:
                    self.table_adapter.setData(
                        self.controller.filter_product_list(self.form_manager.data(), *data))

                case StorageRepository.Event.PRODUCT_CREATED:
                    if len(self.controller.filter_product_list(self.form_manager.data(), data)) != 0:
                        self.table_adapter.addData(data)

                case StorageRepository.Event.PRODUCT_UPDATED:
                    self.table_adapter.updateDataColumns(data, [2])

                case StorageRepository.Event.PRODUCT_DELETED:
                    self.table_adapter.removeRowByKey(data)

            self.check_empty_table()
            self.refresh_total_stored_products_quantity()

        self.messageReceived.connect(update_table)
        self.controller.observe_storage(self.messageReceived.emit)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.empty_storage, alignment=Qt.AlignJustify)

    def check_empty_table(self):
        if self.table.isEmpty():
            self.empty_storage.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_storage.setVisible(False)
            self.table.setVisible(True)

    # Ritorna la lista di ordini filtrata
    def get_filtered_product_list(self) -> list[StoredShoeLastVariety]:
        return self.controller.get_product_list(self.form_manager.data())

    # Aggiorna la lista dei prodotti in base ai filtri
    def refresh_products_list(self):
        filtered_list = self.get_filtered_product_list()
        self.table_adapter.setData(filtered_list)
        self.check_empty_table()

    # Aggiorna la quantità totale immagazzinata di prodotti
    def refresh_total_stored_products_quantity(self):
        self.stored_quantity_label.setText(f"{self.controller.get_total_stored_products_quantity()} paia")

    # Mostra la schermata per modificare la quantità di un prodotto
    def show_product_edit_dialog(self, serial: str):
        print(f"Prodotto selezionato: {serial}")
        selected_product = self.controller.get_product_by_id(serial)
        shoe_last_variety_description = selected_product.get_description()
        shoe_last_variety_amount = selected_product.get_quantity()
        dialog = ManualChangeStoredItemView.raw_shoe_last(
            shoe_last_variety_description,
            shoe_last_variety_amount)

        if dialog.exec() == QDialog.Accepted:
            new_quantity = dialog.value()

            # Aggiorna la quantità
            self.controller.update_product_quantity(serial, new_quantity)


class StorageListAdapter(TableAdapter):
    def adaptData(self, product: StoredShoeLastVariety) -> list[str]:
        return [product.get_item_id(),
                product.get_description(),
                str(product.get_quantity())]

    # Adatta l'altezza di cella al numero di righe del testo contenuto
    def _onRowUpdated(self, row_data: list[str], row: int) -> None:
        description_length = len(row_data[1])
        max_extra_lines = description_length // 50

        self.table.setRowHeight(row, 40 + 20 * max_extra_lines)
