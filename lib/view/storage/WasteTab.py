from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QInputDialog, QDialog
from qfluentwidgets import CheckBox, PushButton

from lib.controller.StorageController import StorageController
from lib.firebaseData import Firebase
from lib.model.StoredItems import StoredWaste
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.widget.CustomPushButton import CustomPushButton
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res import Styles
from res.Dimensions import FontSize


class WasteTab(SubInterfaceChildWidget):
    def __init__(self, parent_widget: SubInterfaceWidget, storage_controller: StorageController):
        super().__init__("waste_list_view", parent_widget)
        self.hideHeader()

        self.controller = storage_controller

        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # Informazioni sulla quantità totale immagazzinata di scarti
        self.storage_details_layout = QVBoxLayout(self.sidebar_frame)
        self.storage_details_layout.setSpacing(8)
        self.storage_details_layout.setObjectName("storage_details_layout")

        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        font.setBold(True)

        self.details_title = QLabel(self.sidebar_frame)
        self.details_title.setObjectName("details_title_label")
        self.details_title.setText("Scarti immagazzinati")
        self.details_title.setFont(font)

        font.setBold(False)
        self.stored_quantity_label = QLabel(self.sidebar_frame)
        self.stored_quantity_label.setObjectName("stored_waste_label")
        self.stored_quantity_label.setFont(font)

        self.storage_details_layout.addWidget(self.details_title)
        self.storage_details_layout.addWidget(self.stored_quantity_label)

        # Label per magazzino vuoto
        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_label")
        self.empty_storage.setText("Nessuno scarto presente in magazzino, modificare i filtri.")
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
        self.checkgroup_label.setText("Filtra per tipo di plastica:")
        self.checkgroup_label.setFont(font)
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Plastica tipo 1"
        self.plastic1_checkbox = CheckBox(self.sidebar_frame)
        self.plastic1_checkbox.setObjectName("plastic1_check_box")
        self.plastic1_checkbox.setText("Tipo 1")
        self.plastic1_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.plastic1_checkbox)

        # CheckBox "Plastica tipo 2"
        self.plastic2_check_box = CheckBox(self.sidebar_frame)
        self.plastic2_check_box.setObjectName("plastic2_check_box")
        self.plastic2_check_box.setText("Tipo 2")
        self.plastic2_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.plastic2_check_box)

        # CheckBox "Plastica tipo 2"
        self.plastic3_check_box = CheckBox(self.sidebar_frame)
        self.plastic3_check_box.setObjectName("plastic3_check_box")
        self.plastic3_check_box.setText("Tipo 3")
        self.plastic3_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.plastic3_check_box)

        # Button "Aggiorna lista"
        self.refresh_waste_button = PushButton(self.sidebar_frame)
        self.refresh_waste_button.setText("Aggiorna lista")
        self.refresh_waste_button.clicked.connect(self.refresh_waste_list)

        # Separatore tra "Aggiorna lista" e "Vendi scarti"
        self.separator = HorizontalLine(self.sidebar_frame)

        # Button "Acquista materiali"
        self.sale_button = CustomPushButton.cyan(self.sidebar_frame)
        self.sale_button.setText("Vendi scarti")

        # Aggiungo i campi della form e altri widget al layout della sidebar
        self.sidebar_layout.addItem(self.storage_details_layout)
        self.sidebar_layout.addWidget(HorizontalLine(self.sidebar_frame))
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_waste_button)
        self.sidebar_layout.addWidget(self.separator)
        self.sidebar_layout.addWidget(self.sale_button)

        # Nasconde il separatore e il pulsante di acquisto se l'utente corrente è un operaio
        if Firebase.auth.currentUserRole() == "worker":
            self.separator.hide()
            self.sale_button.hide()

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Serial", "Dettagli", "Quantità (kg)"]
        self.table.setHeaders(headers)
        self.table.hideColumn(0)

        # Table Adapter
        self.table_adapter = StorageListAdapter(self.table)
        self.table_adapter.hideKeyColumn()
        self.table_adapter.onDoubleClick(self.show_sell_dialog)

        def update_table(message: Message):
            data = message.data()
            match message.event():
                case StorageRepository.Event.WASTE_INITIALIZED:
                    self.table_adapter.setData(
                        self.controller.filter_waste_list(self.form_manager.data(), *data)
                    )
                case StorageRepository.Event.WASTE_UPDATED:
                    self.table_adapter.updateDataColumns(data, [2])

            self.check_empty_table()
            self.refresh_total_stored_waste_quantity()

        self.controller.observe_storage(update_table)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.empty_storage, alignment=Qt.AlignJustify)

    def check_empty_table(self):
        if self.table.isEmpty():
            self.empty_storage.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_storage.setVisible(False)
            self.table.setVisible(True)

    # Ritorna la lista degli scarti filtrata
    def get_filtered_waste_list(self) -> list[StoredWaste]:
        return self.controller.get_waste_list(self.form_manager.data())

    # Aggiorna la lista degli scarti in base ai filtri
    def refresh_waste_list(self):
        self.table_adapter.setData(self.get_filtered_waste_list())
        self.check_empty_table()

    # Aggiorna la quantità totale immagazzinata di scarti
    def refresh_total_stored_waste_quantity(self):
        self.stored_quantity_label.setText(f"{self.controller.get_total_stored_waste_quantity()} kg")

    # Aggiorna la lista degli scarti in base ai filtri
    def show_sell_dialog(self, waste_id: str):

        data = self.controller.get_waste_by_id(waste_id)

        sell_dialog = QInputDialog(self)
        sell_dialog.setStyleSheet(Styles.DIALOG)
        sell_dialog.setWindowTitle(f"Vendita scarti plastica tipo {data.get_plastic_type().value}")
        sell_dialog.setLabelText("Quantità da vendere: ")
        sell_dialog.setInputMode(QInputDialog.IntInput)
        sell_dialog.setIntValue(0)
        sell_dialog.setIntMaximum(data.get_quantity())
        sell_dialog.setIntMinimum(0)
        sell_dialog.setIntStep(1)
        sell_dialog.setOkButtonText("Vendi")
        sell_dialog.setCancelButtonText("Annulla")

        # Eseguito solo se l'utente ha scelto di salvare la modifica
        if sell_dialog.exec_() == QDialog.Accepted:
            # Prendo il valore
            new_value = sell_dialog.intValue()

            # Aggiorno il valore se è diverso
            if new_value != data.get_quantity():
                self.controller.update_waste_quantity(waste_id, new_value)
        # SellWasteDialog(waste_id, self.controller).exec()


class StorageListAdapter(TableAdapter):
    def adaptData(self, waste: StoredWaste) -> list[str]:
        return [waste.get_item_id(),
                waste.get_description(),
                str(waste.get_quantity())]
