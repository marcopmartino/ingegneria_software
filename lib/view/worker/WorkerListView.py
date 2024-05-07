from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QTableWidgetItem, QWidget, QAbstractItemView, QPushButton
)
from qfluentwidgets import FluentIconBase

from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.controller.WorkerListController import WorkerListController
from lib.view.worker.AddWorkerWindow import AddWorkerWindow
from lib.view.worker.EditWorkerWindow import EditWorkerWindow
from lib.widget.TableWidgets import StandardTable
from res import Styles
from res.CustomIcon import CustomIcon
from res.Dimensions import FontWeight


class WorkerListView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.WORKER):
        super().__init__("worker_list_view", parent_widget, svg_icon)
        # self.central_frame.setMinimumWidth(800)

        self.setTitleText("Gestione dipendenti")
        self.setSubtitleText("Clicca due volte su un dipendente per modificarlo")

        self.workerUid = dict()
        self.isNotConnected = True

        self.headers = ["Nome", "E-mail", "Telefono", "Codice fiscale"]

        self.table = StandardTable(self.central_frame)

        self.table.setObjectName("workers_table")
        self.table.setHorizontalHeaders(self.headers)

        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.central_layout.addWidget(self.table)

        self.controller = WorkerListController()

        self.font = QFont()
        self.font.setWeight(FontWeight.BOLD)
        self.newWorkerButton = QPushButton(self)
        self.newWorkerButton.setFont(self.font)
        self.newWorkerButton.setObjectName("new_worker_button")
        self.newWorkerButton.setText("Aggiungi operaio")
        self.newWorkerButton.setStyleSheet(Styles.ACCESS_PUSH_BUTTON)

        self.newWorkerButton.clicked.connect(self.open_add_worker)

        self.sidebar_layout.addWidget(self.newWorkerButton, alignment=Qt.AlignTop)

        # Inserisce i dati in tabella e la aggiunge al central_layout
        def update_table(message: dict[str, any]):
            worker_list = self.controller.get_worker_list()
            print("Tabella")

            self.table.setRowCount(len(worker_list))
            row = 0
            for worker in worker_list:
                data = worker.get_dict()
                self.table.setItem(row, 0, QTableWidgetItem(data["name"]))
                self.table.setItem(row, 1, QTableWidgetItem(data["mail"]))
                self.table.setItem(row, 2, QTableWidgetItem(str(data["phone"])))
                self.table.setItem(row, 3, QTableWidgetItem(str(data["CF"])))
                self.workerUid[row] = data['uid']
                row += 1
            if self.isNotConnected:
                self.table.cellDoubleClicked.connect(self.open_edit_worker)
                self.isNotConnected = False

        update_table({})
        self.controller.observe_worker_list(update_table)

        self.central_layout.addWidget(self.table)

    # Apre la finestra per aggiungere un operaio
    def open_add_worker(self):
        add_window = AddWorkerWindow(self.controller)
        add_window.exec()

    def open_edit_worker(self, selected):
        edit_window = EditWorkerWindow(controller=self.controller, uid=self.workerUid[selected])
        edit_window.exec()
