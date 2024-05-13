from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout
)
from qfluentwidgets import FluentIconBase, SearchLineEdit, ComboBox, PushButton, PrimaryPushButton

from lib.controller.WorkerListController import WorkerListController
from lib.model.Employee import Employee
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.worker.AddWorkerView import AddWorkerView
from lib.view.worker.EditWorkerView import EditWorkerView
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable
from res.CustomIcon import CustomIcon


class WorkerListView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.WORKER):
        super().__init__("worker_list_view", parent_widget, svg_icon)

        # Controller
        self.controller = WorkerListController()

        # Titolo e sottotitolo
        self.setTitleText("Gestione dipendenti")
        self.setSubtitleText("Clicca due volte su un dipendente per modificarlo")

        # Table
        self.table = StandardTable(self.central_frame)
        self.table.setObjectName("workers_table")
        headers = ["Id", "Nome", "E-mail", "Telefono", "Codice fiscale"]
        self.table.setHeaders(headers)
        self.central_layout.addWidget(self.table)

        # TableAdapter
        self.table_adapter = WorkerListTableAdapter(self.table)
        self.table_adapter.onDoubleClick(self.show_edit_worker_form)
        self.table_adapter.hideKeyColumn()

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # Label
        self.search_label = QLabel(self.sidebar_frame)
        self.search_label.setText("Cerca in base a:")

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)

        # Callback eseguita al cambio della selezione del ComboBox
        def on_combo_box_changed(index: int):
            self.search_box.setPlaceholderText(f"Cerca {self.search_combo_box.currentData()}")
            self.search_box.clear()
            if index == 0:
                self.search_box.setValidator(ValidationRule.Name().validator)
            elif index == 1:
                self.search_box.setValidator(ValidationRule.Email().validator)
            elif index == 2:
                self.search_box.setValidator(ValidationRule.Phone().validator)
            else:
                self.search_box.setValidator(ValidationRule.FiscalCode().validator)

        # ComboBox
        self.search_combo_box = ComboBox(self.sidebar_frame)
        self.search_combo_box.setObjectName("searchcombobox_line_edit")
        self.search_combo_box.insertItem(0, "Nome", userData="nome")
        self.search_combo_box.insertItem(1, "Email", userData="email")
        self.search_combo_box.insertItem(2, "Telefono", userData="telefono")
        self.search_combo_box.insertItem(3, "Codice fiscale", userData="codice fiscale")
        self.search_combo_box.currentIndexChanged.connect(on_combo_box_changed)
        self.search_combo_box.setCurrentIndex(0)

        # Layout di ricerca con SearchBox e ComboBox
        self.search_box_layout = QVBoxLayout(self.sidebar_frame)
        self.search_box_layout.setContentsMargins(0, 0, 0, 0)
        self.search_box_layout.setSpacing(12)
        self.search_box_layout.addWidget(self.search_label)
        self.search_box_layout.addWidget(self.search_combo_box)
        self.search_box_layout.addWidget(self.search_box)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_worker_list)

        # Spacer tra i filtri e il pulsante di registrazione di una nuova transazione
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Button "Registra transazione"
        self.create_button = PrimaryPushButton(self.sidebar_frame)
        self.create_button.setObjectName("new_worker_button")
        self.create_button.setText("Aggiungi operaio")
        self.create_button.clicked.connect(self.show_add_worker_form)

        # Aggiungo i filtri della form e altri widget al layout della sidebar
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.create_button)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Inserisce i dati in tabella e la aggiunge al central_layout
        def update_worker_list_view(message: Message):
            data = message.data()
            match message.event():
                case UsersRepository.Event.USERS_INITIALIZED:
                    self.table_adapter.setData(self.controller.filter_workers(self.form_manager.data(), *data))

                case UsersRepository.Event.USER_CREATED:
                    if len(self.controller.filter_workers(self.form_manager.data(), data)) != 0:
                        self.table_adapter.addData(data)

                case UsersRepository.Event.USER_DELETED:
                    self.table_adapter.removeRowByKey(data)

                case UsersRepository.Event.USER_UPDATED:
                    self.table_adapter.updateData(data)

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_worker_list_view)
        self.controller.observe_worker_list(self.messageReceived.emit)

        self.central_layout.addWidget(self.table)

    # Ritorna la lista di operai filtrata
    def get_filtered_worker_list(self) -> list[Employee]:
        return self.controller.get_worker_list(self.form_manager.data())

    # Aggiorna la lista degli operai mostrata in tabella
    def refresh_worker_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_worker_list())

    # Apre la finestra per aggiungere un operaio
    def show_add_worker_form(self):
        add_window = AddWorkerView(self.controller)
        add_window.exec()

    def show_edit_worker_form(self, worker_id: str):
        edit_window = EditWorkerView(self.controller, self.controller.get_worker_by_id(worker_id))
        edit_window.exec()


class WorkerListTableAdapter(TableAdapter):
    def adaptData(self, employee: Employee) -> list[str]:
        return [
            employee.get_uid(),
            employee.get_name(),
            employee.get_email(),
            employee.get_phone(),
            employee.get_CF()
        ]
