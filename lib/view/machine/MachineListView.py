from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import CheckBox, PushButton, SearchLineEdit

from lib.controller.MachineListController import MachineListController
from lib.model.Machine import Machine
from lib.repository.MachinesRepository import MachinesRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.view.machine.MachineView import MachineView
from lib.view.main.BaseWidget import BaseWidget
from lib.widget.TableWidgets import StandardTable
from res.Dimensions import FontSize


class MachineListView(BaseWidget):
    def __init__(self, parent_widget: QWidget):
        super().__init__("machine_list_view", parent_widget)
        self.controller = MachineListController()

        # Titolo e sottotitolo
        self.setTitleText("Lista dei macchinari")
        self.setSubtitleText("Clicca due volte su un macchinario per visualizzare maggiori dettagli")

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca nome")
        self.search_box.searchButton.setEnabled(False)
        self.search_box.setMaxLength(20)

        # Layout con il checkgroup per il tipo
        self.type_checkgroup_layout = QVBoxLayout(self.sidebar_frame)
        self.type_checkgroup_layout.setSpacing(12)
        self.type_checkgroup_layout.setObjectName("type_checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.type_checkgroup_label = QLabel(self.sidebar_frame)
        self.type_checkgroup_label.setObjectName("type_checkgroup_label")
        self.type_checkgroup_label.setText("Filtra in base al tipo:")
        self.type_checkgroup_label.setFont(font)
        self.type_checkgroup_layout.addWidget(self.type_checkgroup_label)

        # CheckBox "Sgrossatore"
        self.sgrossatore_checkbox = CheckBox(self.sidebar_frame)
        self.sgrossatore_checkbox.setObjectName("sgrossatore_check_box")
        self.sgrossatore_checkbox.setText("Sgrossatore")
        self.sgrossatore_checkbox.setChecked(True)
        self.type_checkgroup_layout.addWidget(self.sgrossatore_checkbox)

        # CheckBox "Tornio"
        self.tornio_check_box = CheckBox(self.sidebar_frame)
        self.tornio_check_box.setObjectName("tornio_check_box")
        self.tornio_check_box.setText("Tornio")
        self.tornio_check_box.setChecked(True)
        self.type_checkgroup_layout.addWidget(self.tornio_check_box)

        # CheckBox "Finitore"
        self.finitore_check_box = CheckBox(self.sidebar_frame)
        self.finitore_check_box.setObjectName("finitore_check_box")
        self.finitore_check_box.setText("Finitore")
        self.finitore_check_box.setChecked(True)
        self.type_checkgroup_layout.addWidget(self.finitore_check_box)

        # CheckBox "Ferratore"
        self.ferratore_check_box = CheckBox(self.sidebar_frame)
        self.ferratore_check_box.setObjectName("ferratore_check_box")
        self.ferratore_check_box.setText("Ferratore")
        self.ferratore_check_box.setChecked(True)
        self.type_checkgroup_layout.addWidget(self.ferratore_check_box)

        # CheckBox "Numeratore"
        self.numeratore_check_box = CheckBox(self.sidebar_frame)
        self.numeratore_check_box.setObjectName("timbratrice_check_box")
        self.numeratore_check_box.setText("Timbratrice")
        self.numeratore_check_box.setChecked(True)
        self.type_checkgroup_layout.addWidget(self.numeratore_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_order_list)

        # Layout con il checkgroup per lo stato
        self.state_checkgroup_layout = QVBoxLayout(self.sidebar_frame)
        self.state_checkgroup_layout.setSpacing(12)
        self.state_checkgroup_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.state_checkgroup_label = QLabel(self.sidebar_frame)
        self.state_checkgroup_label.setObjectName("type_checkgroup_label")
        self.state_checkgroup_label.setText("Filtra in base allo stato:")
        self.state_checkgroup_label.setFont(font)
        self.state_checkgroup_layout.addWidget(self.state_checkgroup_label)

        # CheckBox "Disponiible"
        self.available_checkbox = CheckBox(self.sidebar_frame)
        self.available_checkbox.setObjectName("available_check_box")
        self.available_checkbox.setText("Disponibile")
        self.available_checkbox.setChecked(True)
        self.state_checkgroup_layout.addWidget(self.available_checkbox)

        # CheckBox "In funzione"
        self.working_checkbox = CheckBox(self.sidebar_frame)
        self.working_checkbox.setObjectName("running_check_box")
        self.working_checkbox.setText("In funzione")
        self.working_checkbox.setChecked(True)
        self.state_checkgroup_layout.addWidget(self.working_checkbox)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addWidget(self.search_box)
        self.sidebar_layout.addLayout(self.type_checkgroup_layout)
        self.sidebar_layout.addLayout(self.state_checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Nome", "Tipo", "Stato", "Progresso", "In lavorazione (paia)"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = MachineListAdapter(self.table)
        self.table_adapter.onDoubleClick(self.show_machine_details)

        def update_machine_table(message: Message):
            data = message.data()
            match message.event():
                case MachinesRepository.Event.MACHINES_INITIALIZED:
                    self.table_adapter.setData(self.controller.filter_machines(
                        self.form_manager.data(), *data))

                case MachinesRepository.Event.MACHINE_STARTED:
                    pass
                    #self.table_adapter.updateDataColumns(message.data(), [1, 4, 5])

                case MachinesRepository.Event.MACHINE_STOPPED:
                    pass
                    #self.table_adapter.updateDataColumns(message.data(), [3])

        self.controller.observe_machine_list(update_machine_table)

        self.central_layout.addWidget(self.table)

    # Ritorna la lista di ordini filtrata
    def get_filtered_machine_list(self) -> list[Machine]:
        return self.controller.get_machine_list(self.form_manager.data())

    # Aggiorna la lista degli ordini mostrata in tabella
    def refresh_order_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_machine_list())

    # Mostra la schermata con i dettagli del macchinario
    def show_machine_details(self, machine_serial: str):
        print(f"Macchinario selezionato: {machine_serial}")
        machine_view = MachineView(self, self.controller.get_machine_by_id(machine_serial))
        self.window().addRemovableSubInterface(machine_view, text=machine_serial)


class MachineListAdapter(TableAdapter):
    def adaptData(self, machine: Machine) -> list[str]:
        return [machine.get_machine_serial(),
                machine.get_machine_type(),
                "In funzione" if machine.is_running() else "Disponibile",
                "-",
                f"0/{str(machine.get_capacity())}",
                ]
