from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import SearchLineEdit, CheckBox, PushButton

from lib.controller.StorageController import StorageController
from lib.firebaseData import Firebase
from lib.model.StoredItems import StoredMaterial
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.widget.CustomPushButton import CustomPushButton
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res.Dimensions import FontSize


class MaterialsTab(SubInterfaceChildWidget):
    def __init__(self, parent_widget: SubInterfaceWidget, storage_controller: StorageController):
        super().__init__("material_list_view", parent_widget)
        self.hideHeader()

        self.controller = storage_controller

        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        font.setBold(True)

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

        # Label per magazzino vuoto
        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_label")
        self.empty_storage.setText("Nessun materiale presente in magazzino, modificare i filtri")
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
        self.checkgroup_label.setText("Filtra per tipo:")
        self.checkgroup_label.setFont(font)
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Parti per ferratura"
        self.sketches_checkbox = CheckBox(self.sidebar_frame)
        self.sketches_checkbox.setObjectName("shoeing_part_check_box")
        self.sketches_checkbox.setText("Parti per ferratura")
        self.sketches_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.sketches_checkbox)

        # CheckBox "Parti per tornitura"
        self.semifinished_check_box = CheckBox(self.sidebar_frame)
        self.semifinished_check_box.setObjectName("turning_part_check_box")
        self.semifinished_check_box.setText("Parti per tornitura")
        self.semifinished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.semifinished_check_box)

        # CheckBox "Bussola"
        self.finished_check_box = CheckBox(self.sidebar_frame)
        self.finished_check_box.setObjectName("compass_check_box")
        self.finished_check_box.setText("Bussola")
        self.finished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.finished_check_box)

        # CheckBox "Altro"
        self.finished_check_box = CheckBox(self.sidebar_frame)
        self.finished_check_box.setObjectName("other_check_box")
        self.finished_check_box.setText("Altro")
        self.finished_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.finished_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = CustomPushButton.white(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_materials_list)

        # Separatore tra "Aggiorna lista" e "Acquista materiali"
        self.separator = HorizontalLine(self.sidebar_frame)

        # Button "Acquista materiali"
        self.purchase_button = CustomPushButton.cyan(self.sidebar_frame)
        self.purchase_button.setText("Acquista materiali")

        # Aggiungo i campi della form e altri widget al layout della sidebar
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.separator)
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
        headers = ["Seriale", "Dettagli", "Tipo", "Quantità"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = StorageListAdapter(self.table)
        self.table_adapter.hideKeyColumn()

        def update_table(message: Message):
            data = message.data()
            match message.event():
                case StorageRepository.Event.MATERIALS_INITIALIZED:
                    self.table_adapter.setData(
                        self.controller.filter_material_list(self.form_manager.data(), *data)
                    )
                case StorageRepository.Event.MATERIAL_UPDATED:
                    self.table_adapter.updateDataColumns(data, [3])

            self.check_empty_table()

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

    # Ritorna la lista di ordini filtrata
    def get_filtered_materials_list(self) -> list[StoredMaterial]:
        return self.controller.get_material_list(self.form_manager.data())

    # Aggiorna la lista dei materiali in base ai filtri
    def refresh_materials_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_materials_list())
        self.check_empty_table()


class StorageListAdapter(TableAdapter):
    def adaptData(self, product: StoredMaterial) -> list[str]:
        return [product.get_item_id(),
                product.get_description(),
                product.get_material_type(),
                str(product.get_quantity())
                ]
