from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem, QWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate, QFrame, QStyle, QVBoxLayout, QLabel
)
from qfluentwidgets import SearchLineEdit, CheckBox, PushButton, SpinBox, ComboBox, PrimaryPushButton

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.order.controller.OrderListController import OrderListController
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from lib.widget.TableWidgets import StandardTable
from res import Styles
from res.Dimensions import TableDimensions, ValidationDimensions, FontSize


class OrderListView(BaseWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("order_list_view", parent_widget)
        self.controller = OrderListController()
        #self.central_frame.setMinimumWidth(800)

        # Testo
        self.setTitleText("I tuoi ordini")
        self.setSubtitleText("Clicca su un ordine per visualizzare maggiori dettagli")

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)

        # ComboBox
        self.search_combo_box = ComboBox(self.sidebar_frame)
        self.search_combo_box.setObjectName("searchcombobox_line_edit")
        self.search_combo_box.insertItem(0, "Cerca su base ordine", userData="ordine")
        self.search_combo_box.insertItem(1, "Cerca su base articolo", userData="articolo")
        self.search_combo_box.insertItem(2, "Cerca su base cliente", userData="cliente")

        def on_combo_index_changed(index: int):
            self.search_box.setText("")
            match index:
                case 0 | 1:
                    self.search_box.setValidator(ValidationRule.Numbers().validator)
                    self.search_box.setMaxLength(6)
                case 2:
                    self.search_box.setValidator(None)
                    self.search_box.setMaxLength(ValidationDimensions.DEFAULT_MAX_LENGTH)

        self.search_combo_box.currentIndexChanged.connect(on_combo_index_changed)
        self.search_combo_box.setCurrentIndex(0)

        # Layout con il checkgroup
        self.checkgroup_layout = QVBoxLayout()
        self.checkgroup_layout.setSpacing(12)
        self.checkgroup_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.checkgroup_label = QLabel(self.sidebar_frame)
        self.checkgroup_label.setObjectName("marking_group_label")
        self.checkgroup_label.setText("Filtra in base allo stato:")
        self.checkgroup_label.setFont(font)
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Non iniziato"
        self.not_started_checkbox = CheckBox(self.sidebar_frame)
        self.not_started_checkbox.setObjectName("not_started_check_box")
        self.not_started_checkbox.setText("Non iniziato")
        self.checkgroup_layout.addWidget(self.not_started_checkbox)

        # CheckBox "In lavorazione"
        self.working_check_box = CheckBox(self.sidebar_frame)
        self.working_check_box.setObjectName("working_check_box")
        self.working_check_box.setText("In lavorazione")
        self.checkgroup_layout.addWidget(self.working_check_box)

        # CheckBox "Completato"
        self.completed_check_box = CheckBox(self.sidebar_frame)
        self.completed_check_box.setObjectName("completed_check_box")
        self.completed_check_box.setText("Completato")
        self.checkgroup_layout.addWidget(self.completed_check_box)

        # CheckBox "Consegnato"
        self.delivered_check_box = CheckBox(self.sidebar_frame)
        self.delivered_check_box.setObjectName("delivered_check_box")
        self.delivered_check_box.setText("Consegnato")
        self.checkgroup_layout.addWidget(self.delivered_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = PrimaryPushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")

        self.sidebar_layout.addWidget(self.search_box)
        self.sidebar_layout.addWidget(self.search_combo_box)
        self.sidebar_layout.addItem(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)

        # Tabella
        self.table = StandardTable(self.central_frame)

        headers = ["Ordine", "Articolo", "Data creazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]

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

        # Form Manager
        self.form_manager = FormManager().add_widget_fields(self.sidebar_frame)

        self.central_layout.addWidget(self.table)
