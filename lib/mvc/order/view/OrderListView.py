from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem, QWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate, QFrame, QStyle, QVBoxLayout, QLabel,
    QSpacerItem, QSizePolicy
)
from qfluentwidgets import SearchLineEdit, CheckBox, PushButton, SpinBox, ComboBox, PrimaryPushButton

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.order.controller.OrderListController import OrderListController
from lib.mvc.order.model.Order import Order
from lib.mvc.order.model.OrderList import OrderList
from lib.mvc.order.view.CreateOrderView import CreateOrderView
from lib.mvc.order.view.OrderDetailsView import OrderDetailsView
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from lib.widget.Separators import HorizontalLine, VerticalLine
from lib.widget.TableWidgets import StandardTable, AdvancedTableAdapter
from res import Styles
from res.Dimensions import TableDimensions, ValidationDimensions, FontSize, SpacerDimensions


class OrderListView(BaseWidget):
    def __init__(self, parent_widget: QWidget):
        super().__init__("order_list_view", parent_widget)
        self.controller = OrderListController()
        # self.central_frame.setMinimumWidth(800)

        # Titolo e sottotitolo
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
        self.not_started_checkbox.setObjectName("notstarted_check_box")
        self.not_started_checkbox.setText("Non iniziato")
        self.not_started_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.not_started_checkbox)

        # CheckBox "In lavorazione"
        self.working_check_box = CheckBox(self.sidebar_frame)
        self.working_check_box.setObjectName("working_check_box")
        self.working_check_box.setText("In lavorazione")
        self.working_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.working_check_box)

        # CheckBox "Completato"
        self.completed_check_box = CheckBox(self.sidebar_frame)
        self.completed_check_box.setObjectName("completed_check_box")
        self.completed_check_box.setText("Completato")
        self.completed_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.completed_check_box)

        # CheckBox "Consegnato"
        self.delivered_check_box = CheckBox(self.sidebar_frame)
        self.delivered_check_box.setObjectName("delivered_check_box")
        self.delivered_check_box.setText("Consegnato")
        self.delivered_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.delivered_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_order_list)

        # Spacer tra i due pulsanti
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Button "Crea nuovo ordine"
        self.create_button = PrimaryPushButton(self.sidebar_frame)
        self.create_button.setText("Crea nuovo ordine")
        self.create_button.clicked.connect(self.show_order_form)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addWidget(self.search_box)
        self.sidebar_layout.addWidget(self.search_combo_box)
        self.sidebar_layout.addItem(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.create_button)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Ordine", "Articolo", "Data creazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = OrderListAdapter(self.table, self.form_manager)
        self.table_adapter.setData(self.controller.get_order_list())
        self.table_adapter.onSelection(self.show_order_details)

        def update_table(message: Order | str):
            if type(message) is Order:
                self.table_adapter.addData([message])
            else:
                self.table_adapter.removeRowByKey(message)

        self.controller.order_list.observe(update_table)

        self.central_layout.addWidget(self.table)

    # Aggiorna la lista degli ordini in base al filtri
    def refresh_order_list(self):
        self.table_adapter.setData(self.controller.get_order_list())

    # Mostra la form per la creazione di ordini
    def show_order_form(self):
        order_form = CreateOrderView(self)
        order_form.exec()

    # Mostra la schermata con i dettagli dell'ordine
    def show_order_details(self, order_serial: str):
        print(f"Ordine selezionato: {order_serial}")
        order_details = OrderDetailsView(self, order_serial)
        self.window().addRemovableSubInterface(order_details, text=f"Ordine {order_serial}")


class OrderListAdapter(AdvancedTableAdapter):
    def adaptData(self, order: Order) -> list[str]:
        return [order.order_serial,
                order.article_serial,
                order.creation_date,
                order.state,
                str(order.quantity),
                PriceCatalog.price_format(order.price)
                ]

    def filterData(self, order_list: list[Order], filters: dict[str, any]) -> list[Order]:
        return OrderListController.filter_order_list(order_list, filters)
