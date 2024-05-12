from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHeaderView
from qfluentwidgets import SearchLineEdit, ComboBox, CheckBox, PushButton, PrimaryPushButton, FluentIconBase

from lib.controller.CashRegisterController import CashRegisterController
from lib.model.CashRegisterTransaction import CashRegisterTransaction
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.utility.UtilityClasses import PriceFormatter
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from lib.view.cashregister.TransactionFormView import TransactionFormView
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable, DateTableItem, PriceTableItem, IntegerTableItem
from res import Styles
from res.CustomIcon import CustomIcon
from res.Dimensions import FontSize


class CashRegisterView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.CASH_REGISTER):
        super().__init__("cash_register_view", parent_widget, svg_icon)

        # Controller
        self.controller = CashRegisterController()

        # Titolo e sottotitolo
        self.setTitleText("Registro di cassa")
        self.setSubtitleText("Clicca due volte su una transazione per modificarla o eliminarla")

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
                self.search_box.setValidator(ValidationRule.Numbers().validator)
                self.search_box.setMaxLength(6)
            else:
                self.search_box.setValidator(None)
                self.search_box.setMaxLength(75)

        # ComboBox
        self.search_combo_box = ComboBox(self.sidebar_frame)
        self.search_combo_box.setObjectName("searchcombobox_line_edit")
        self.search_combo_box.insertItem(0, "Id", userData="id")
        self.search_combo_box.insertItem(1, "Descrizione", userData="descrizione")
        self.search_combo_box.currentIndexChanged.connect(on_combo_box_changed)
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
        self.checkgroup_layout.setObjectName("checkgroup_layout")

        # Checkgroup Label
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.checkgroup_label = QLabel(self.sidebar_frame)
        self.checkgroup_label.setObjectName("checkgroup_label")
        self.checkgroup_label.setText("Filtra in base al tipo di transazione:")
        self.checkgroup_label.setFont(font)
        self.checkgroup_label.setWordWrap(True)
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Entrate"
        self.revenue_checkbox = CheckBox(self.sidebar_frame)
        self.revenue_checkbox.setObjectName("revenue_check_box")
        self.revenue_checkbox.setText("Entrate di cassa")
        self.revenue_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.revenue_checkbox)

        # CheckBox "Uscite"
        self.spending_check_box = CheckBox(self.sidebar_frame)
        self.spending_check_box.setObjectName("spending_check_box")
        self.spending_check_box.setText("Uscite di cassa")
        self.spending_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.spending_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_transaction_list)

        # Spacer tra i filtri e il pulsante di registrazione di una nuova transazione
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Button "Registra transazione"
        self.create_button = PrimaryPushButton(self.sidebar_frame)
        self.create_button.setText("Registra transazione")
        self.create_button.clicked.connect(self.show_new_transaction_form)

        # Aggiungo i filtri della form e altri widget al layout della sidebar
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.create_button)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella transazioni
        self.table = StandardTable(self.central_frame)
        self.table.setStyleSheet(Styles.STANDARD_TABLE_NO_ITEM)
        headers = ["Id", "Descrizione", "Data pagamento", "Importo (euro)"]
        self.table.setHeaders(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        # Table Adapter
        self.table_adapter = TransactionListAdapter(self.table)
        self.table_adapter.setColumnItemClass(0, IntegerTableItem)  # Per un corretto ordinamento delle date
        self.table_adapter.setColumnItemClass(2, DateTableItem)  # Per un corretto ordinamento delle date
        self.table_adapter.setColumnItemClass(3, PriceTableItem)  # Per un corretto ordinamento delle date
        self.table_adapter.onDoubleClick(self.show_edit_transaction_form)

        def update_cash_register_view(message: Message):
            data = message.data()
            match message.event():
                case CashRegisterRepository.Event.TRANSACTIONS_INITIALIZED:
                    self.table_adapter.setData(self.controller.filter_transactions(
                        self.form_manager.data(), *data))

                case CashRegisterRepository.Event.TRANSACTION_CREATED:
                    if len(self.controller.filter_transactions(self.form_manager.data(), data)) != 0:
                        self.table_adapter.addData(data)

                case CashRegisterRepository.Event.TRANSACTION_DELETED:
                    self.table_adapter.removeRowByKey(data)

                case CashRegisterRepository.Event.TRANSACTION_UPDATED:
                    self.table_adapter.updateDataColumns(data, [1, 2, 3])

        self.controller.observe_transaction_list(update_cash_register_view)

        self.central_layout.addWidget(self.table)

    # Ritorna la lista di ordini filtrata
    def get_filtered_transaction_list(self) -> list[CashRegisterTransaction]:
        return self.controller.get_transaction_list(self.form_manager.data())

    # Aggiorna la lista degli ordini mostrata in tabella
    def refresh_transaction_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_transaction_list())

    # Mostra la form per la creazione di transazioni
    def show_new_transaction_form(self):
        TransactionFormView.new(self.controller).exec()

    # Mostra la form per la modifica di transazioni
    def show_edit_transaction_form(self, transaction_id: str):
        TransactionFormView.edit(self.controller, self.controller.get_transaction_by_id(transaction_id)).exec()


class TransactionListAdapter(TableAdapter):
    def adaptData(self, transaction: CashRegisterTransaction) -> list[str]:
        return [transaction.get_transaction_id(),
                transaction.get_description(),
                transaction.get_payment_date(),
                PriceFormatter.format(transaction.get_amount())
                ]

    def _onRowUpdated(self, row_data: list[str], row: int) -> None:
        self.table.setRowColor(row, QColor(125, 195, 95) if PriceFormatter.unformat(row_data[3]) > 0
        else QColor(255, 80, 80))
