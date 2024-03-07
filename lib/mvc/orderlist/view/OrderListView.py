from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem, QWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate, QFrame
)

from lib.mvc.main.view.BaseWidget import BaseWidget
from res import Styles


class OrderListView(BaseWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("order_list_view", parent_widget)
        #self.central_frame.setMinimumWidth(800)

        self.table = QTableWidget(self.central_frame)

        headers = ["Ordine", "Articolo", "Data di effettuazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]

        orders = [
            {'order': '1', 'article': '1480', 'date': '04/02/2024', 'status': 'Non iniziato', 'quantity': 20, 'price': 520.00},
            {'order': '2', 'article': '1563', 'date': '10/02/2024', 'status': 'Non iniziato', 'quantity': 40, 'price': 700.00},
            {'order': '3', 'article': '1480', 'date': '12/02/2024', 'status': 'Non iniziato', 'quantity': 75, 'price': 980.00},
        ]

        self.table.setStyleSheet(Styles.TABLE)
        self.table.setFrameStyle(QFrame.NoFrame)
        self.table.setColumnCount(len(headers))
        #self.table.setColumnWidth(0, 100)
        #self.table.setColumnWidth(1, 100)
        #self.table.setColumnWidth(2, 200)
        #self.table.setColumnWidth(3, 150)
        #self.table.setColumnWidth(4, 125)
        #self.table.setColumnWidth(5, 125)
        self.table.setRowCount(len(orders))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setFixedHeight(40)
        #self.table.horizontalHeader().setMinimumSectionSize(150)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #font = self.table.horizontalHeader().font()
        #font.setWeight(60)
        #self.table.horizontalHeader().setFont(font)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(40)
        #self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

        class AlignDelegate(QStyledItemDelegate):
            def initStyleOption(self, option, index):
                super(AlignDelegate, self).initStyleOption(option, index)
                option.displayAlignment = Qt.AlignCenter

        self.table.setItemDelegate(AlignDelegate(self.table))
        self.table.setShowGrid(False)

        row = 0
        for order in orders:
            self.table.setItem(row, 0, QTableWidgetItem(order['order']))
            self.table.setItem(row, 1, QTableWidgetItem(order['article']))
            self.table.setItem(row, 2, QTableWidgetItem(order['date']))
            self.table.setItem(row, 3, QTableWidgetItem(order['status']))
            self.table.setItem(row, 4, QTableWidgetItem(str(order['quantity'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(order['price'])))
            row += 1

        self.central_layout.addWidget(self.table)



