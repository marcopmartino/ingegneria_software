from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem, QWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate, QFrame, QStyle
)

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.order.controller.OrderListController import OrderListController
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog
from lib.widget.TableWidgets import StandardTable
from res import Styles
from res.Dimensions import TableDimensions


class OrderListView(BaseWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("order_list_view", parent_widget)
        self.controller = OrderListController()
        #self.central_frame.setMinimumWidth(800)

        # Testo
        self.setTitleText("I tuoi ordini")
        self.setSubtitleText("Clicca su un ordine per visualizzare maggiori dettagli")

        self.table = StandardTable(self.central_frame)

        headers = ["Ordine", "Articolo", "Data di effettuazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]

        orders = [
            {'order': '1', 'article': '1480', 'date': '04/02/2024', 'status': 'Non iniziato', 'quantity': 20,
             'price': 520.00},
            {'order': '2', 'article': '1563', 'date': '10/02/2024', 'status': 'Non iniziato', 'quantity': 40,
             'price': 700.00},
            {'order': '3', 'article': '1480', 'date': '12/02/2024', 'status': 'Non iniziato', 'quantity': 75,
             'price': 980.00},
        ]

        self.table.setRowCount(len(orders))
        self.table.setHorizontalHeaders(headers)

        # self.table.setColumnWidth(0, 100)
        # self.table.setColumnWidth(1, 100)
        # self.table.setColumnWidth(2, 200)
        # self.table.setColumnWidth(3, 150)
        # self.table.setColumnWidth(4, 125)
        # self.table.setColumnWidth(5, 125)

        # self.table.horizontalHeader().setMinimumSectionSize(150)
        # font = self.table.horizontalHeader().font()
        # font.setWeight(60)
        # self.table.horizontalHeader().setFont(font)

        # self.table.resizeColumnsToContents()
        '''
        row = 0
        for order in orders:
            self.table.setItem(row, 0, QTableWidgetItem(order['order']))
            self.table.setItem(row, 1, QTableWidgetItem(order['article']))
            self.table.setItem(row, 2, QTableWidgetItem(order['date']))
            self.table.setItem(row, 3, QTableWidgetItem(order['status']))
            self.table.setItem(row, 4, QTableWidgetItem(str(order['quantity'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(order['price'])))
            row += 1
        '''

        def update_table(message: dict[str, any]):
            order_list = self.controller.order_list.get()
            self.table.setRowCount(len(order_list))

            row = 0
            for order in self.controller.order_list.get():
                self.table.setItem(row, 0, QTableWidgetItem(order.order_serial))
                self.table.setItem(row, 1, QTableWidgetItem(order.article_serial))
                self.table.setItem(row, 2, QTableWidgetItem(order.creation_date))
                self.table.setItem(row, 3, QTableWidgetItem(order.state))
                self.table.setItem(row, 4, QTableWidgetItem(str(order.quantity)))
                self.table.setItem(row, 5, QTableWidgetItem(PriceCatalog.price_format(order.price)))
                row += 1

        update_table({})
        self.controller.order_list.observe(update_table)

        self.central_layout.addWidget(self.table)
