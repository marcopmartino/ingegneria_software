from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from qfluentwidgets import SearchLineEdit, CheckBox, PushButton

from lib.controller.MaterialsListController import MaterialsListController
from lib.model.StoredItems import StoredMaterial
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res.Dimensions import FontSize


class MaterialsTab(SubInterfaceChildWidget):
    def __init__(self, parent_widget: SubInterfaceWidget):
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
        self.max_storage.setText(f"Massima: {self.controller.get_max_storge()}")
        self.max_storage.setFont(font)

        self.storage_details_layout.addWidget(self.details_title, alignment=Qt.AlignCenter)
        self.storage_details_layout.addWidget(self.max_storage, alignment=Qt.AlignLeft)

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)

        # Label per magazzino vuoto
        self.empty_storage = QLabel(self.central_frame)
        self.empty_storage.setObjectName("empty_label")
        self.empty_storage.setText("Nessun materiale presente in magazzino, modificare i filtri")
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

        def update_table(message: Message):
            data = message.data()
            match message.event():
                case StorageRepository.Event.MATERIALS_INITIALIZED:
                    self.table_adapter.setData(
                        self.controller.filter_materials_list(self.form_manager.data(), *data)
                    )
                case StorageRepository.Event.MATERIAL_CREATED:
                    if len(self.controller.filter_materials_list(self.form_manager.data(), *data)) != 0:
                        self.table_adapter.addData(data)
                case StorageRepository.Event.MATERIAL_DELETED:
                    self.table_adapter.updateDataColumns(data, [3])

            self.check_empty_table()

        self.controller.observe_materials_list(update_table)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.empty_storage, alignment=Qt.AlignJustify)

        self.check_empty_table()

    def check_empty_table(self):
        if self.table.isEmpty():
            self.empty_storage.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_storage.setVisible(False)
            self.table.setVisible(True)

    # Ritorna la lista di ordini filtrata
    def get_filtered_materials_list(self) -> list[StoredMaterial]:
        return self.controller.get_filtered_materials_list(self.form_manager.data())

    # Aggiorna la lista dei materiali in base ai filtri
    def refresh_materials_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_materials_list())
        self.check_empty_table()


class StorageListAdapter(TableAdapter):
    def adaptData(self, product: StoredMaterial) -> list[str]:
        return [product.get_item_id(),
                product.get_material_type(),
                product.get_description,
                str(product.get_quantity())
                ]
