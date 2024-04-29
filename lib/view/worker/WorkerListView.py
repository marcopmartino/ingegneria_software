from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QTableWidgetItem, QWidget, QAbstractItemView, QPushButton
)

from lib.view.main.BaseWidget import BaseWidget
from lib.controller.WorkerListController import WorkerListController
from lib.view.worker.AddWorkerWindow import AddWorkerWindow
from lib.view.worker.EditWorkerWindow import EditWorkerWindow
from lib.widget.TableWidgets import StandardTable
from res import Styles
from res.Dimensions import FontWeight


class WorkerListView(BaseWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("worker_list_view", parent_widget)
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
            worker_list = self.controller.worker_list.get()
            print("Tabella")

            self.table.setRowCount(len(worker_list))
            row = 0
            for worker in worker_list:
                self.table.setItem(row, 0, QTableWidgetItem(worker.name))
                self.table.setItem(row, 1, QTableWidgetItem(worker.mail))
                self.table.setItem(row, 2, QTableWidgetItem(str(worker.phone)))
                self.table.setItem(row, 3, QTableWidgetItem(str(worker.CF)))
                self.workerUid[row] = worker.uid
                row += 1
            if self.isNotConnected:
                self.table.cellDoubleClicked.connect(self.open_edit_worker)
                self.isNotConnected = False

        update_table({})
        self.controller.worker_list.observe(update_table)

        self.central_layout.addWidget(self.table)

    # Apre la finestra per aggiungere un operaio
    def open_add_worker(self):
        add_window = AddWorkerWindow(prevWindow=self)
        self.setEnabled(False)
        add_window.show()

    def open_edit_worker(self, selected):
        edit_window = EditWorkerWindow(prevWindow=self, uid=self.workerUid[selected])
        self.setEnabled(False)
        edit_window.show()
