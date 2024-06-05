from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from qfluentwidgets import SearchLineEdit, CheckBox, ComboBox, FluentIconBase, FluentIcon

from lib.controller.OrderListController import OrderListController
from lib.firebaseData import Firebase
from lib.model.Order import Order
from lib.repository.OrdersRepository import OrdersRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.utility.UtilityClasses import PriceFormatter, DatetimeUtils
from lib.utility.validation.FormManager import FormManager
from lib.utility.validation.ValidationRule import ValidationRule
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.order.CreateOrderView import CreateOrderView
from lib.view.order.OrderView import OrderView
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from lib.utility.gui.widget.Separators import HorizontalLine
from lib.utility.gui.widget.TableWidgets import StandardTable, DateTableItem, PriceTableItem, IntegerTableItem
from res.Dimensions import FontSize


class OrderListView(SubInterfaceWidget):

    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = FluentIcon.SHOPPING_CART):
        super().__init__("order_list_view", parent_widget, svg_icon)

        # Controller
        self.controller = OrderListController()

        # Titolo e sottotitolo
        self.setTitleText("I tuoi ordini" if Firebase.auth.currentUserRole() == "customer" else "Lista degli ordini")
        self.setSubtitleText("Clicca due volte su un ordine per visualizzare maggiori dettagli")

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # Label per tabella vuota
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.empty_table_label = QLabel(self.central_frame)
        self.empty_table_label.setObjectName("empty_storage_label")
        self.empty_table_label.setText("Nessun ordine trovato, modificare i filtri")
        font.setBold(True)
        self.empty_table_label.setFont(font)
        font.setBold(False)

        # Label
        self.search_label = QLabel(self.sidebar_frame)
        self.search_label.setText("Cerca in base a:")

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca")
        self.search_box.searchButton.setEnabled(False)
        self.search_box.setValidator(ValidationRule.Numbers().validator)
        self.search_box.setMaxLength(6)

        # ComboBox
        self.search_combo_box = ComboBox(self.sidebar_frame)
        self.search_combo_box.setObjectName("searchcombobox_line_edit")
        self.search_combo_box.insertItem(0, "Ordine", userData="ordine")
        self.search_combo_box.insertItem(1, "Articolo", userData="articolo")
        self.search_combo_box.currentIndexChanged.connect(
            lambda: self.search_box.setPlaceholderText(f"Cerca {self.search_combo_box.currentData()}")
        )
        self.search_combo_box.setCurrentIndex(0)

        # Layout di ricerca con SearchBox e ComboBox
        self.search_box_layout = QVBoxLayout(self.sidebar_frame)
        self.search_box_layout.setContentsMargins(0, 0, 0, 0)
        self.search_box_layout.setSpacing(12)
        self.search_box_layout.addWidget(self.search_label)
        self.search_box_layout.addWidget(self.search_combo_box)
        self.search_box_layout.addWidget(self.search_box)

        # Layout con il checkgroup
        self.checkgroup_layout = QVBoxLayout(self.sidebar_frame)
        self.checkgroup_layout.setSpacing(12)
        self.checkgroup_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Label
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
        self.refresh_button = CustomPushButton.white(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_order_list)

        # Spacer tra i due pulsanti
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Button "Crea nuovo ordine"
        self.create_button = CustomPushButton.cyan(self.sidebar_frame)
        self.create_button.setText("Crea nuovo ordine")
        self.create_button.clicked.connect(self.show_order_form)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)

        if Firebase.auth.currentUserRole() == "customer":
            self.sidebar_layout.addWidget(self.sidebar_spacer)
            self.sidebar_layout.addWidget(self.create_button)
        else:
            self.sidebar_spacer.hide()
            self.create_button.hide()

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Ordine", "Articolo", "Data creazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = OrderListAdapter(self.table)
        self.table_adapter.setColumnItemClass(0, IntegerTableItem)  # Per un corretto ordinamento degli ordini
        self.table_adapter.setColumnItemClass(1, IntegerTableItem)  # Per un corretto ordinamento degli articoli
        self.table_adapter.setColumnItemClass(2, DateTableItem)  # Per un corretto ordinamento delle date
        self.table_adapter.setColumnItemClass(4, IntegerTableItem)  # Per un corretto ordinamento delle quantità
        self.table_adapter.setColumnItemClass(5, PriceTableItem)  # Per un corretto ordinamento dei prezzi
        self.table_adapter.onDoubleClick(self.show_order_details)

        # Callback per l'observer
        def update_order_list_view(message: Message):
            data = message.data()
            match message.event():
                case OrdersRepository.Event.ORDERS_INITIALIZED:
                    self.table_adapter.setData(self.controller.filter_orders(self.form_manager.data(), *data))

                case OrdersRepository.Event.ORDER_CREATED:
                    if len(self.controller.filter_orders(self.form_manager.data(), data)) != 0:
                        self.table_adapter.addData(data)

                case OrdersRepository.Event.ORDER_DELETED:
                    self.table_adapter.removeRowByKey(data)

                case OrdersRepository.Event.ORDER_UPDATED:
                    self.table_adapter.updateDataColumns(data, [1, 4, 5])

                case OrdersRepository.Event.ORDER_STATE_UPDATED:
                    self.table_adapter.updateDataColumns(data, [3])

            self.check_empty_table()

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_order_list_view)
        self.controller.observe_order_list(self.messageReceived.emit)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.empty_table_label, alignment=Qt.AlignJustify)

    def check_empty_table(self):
        if self.table.isEmpty():
            self.empty_table_label.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_table_label.setVisible(False)
            self.table.setVisible(True)

    # Ritorna la lista di ordini filtrata
    def get_filtered_order_list(self) -> list[Order]:
        return self.controller.get_order_list(self.form_manager.data())

    # Aggiorna la lista degli ordini mostrata in tabella
    def refresh_order_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_order_list())
        self.check_empty_table()

    # Mostra la form per la creazione di ordini
    def show_order_form(self):
        CreateOrderView(self.controller).exec()

    # Mostra la schermata con i dettagli dell'ordine
    def show_order_details(self, order_serial: str):
        print(f"Ordine selezionato: {order_serial}")
        order_view = OrderView(self, self.controller.get_order_by_id(order_serial))
        self.window().addRemovableSubInterface(order_view, text=f"Ordine {order_serial}")


class OrderListAdapter(TableAdapter):
    def adaptData(self, order: Order) -> list[str]:
        return [order.get_order_serial(),
                order.get_article_serial(),
                DatetimeUtils.unformat_date(order.get_creation_date()),
                order.get_state().value,
                str(order.get_quantity()),
                PriceFormatter.format(order.get_price())
                ]
