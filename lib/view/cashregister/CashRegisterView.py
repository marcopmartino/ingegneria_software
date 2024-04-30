from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHeaderView
from qfluentwidgets import SearchLineEdit, ComboBox, CheckBox, PushButton, PrimaryPushButton

from lib.controller.CashRegisterController import CashRegisterController
from lib.model.CashRegisterTransaction import CashRegisterTransaction
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from lib.view.main.BaseWidget import BaseWidget
from lib.widget.Separators import HorizontalLine
from lib.widget.TableWidgets import StandardTable, DateTableItem
from res.Dimensions import FontSize


class CashRegisterView(BaseWidget):
    def __init__(self, parent_widget: QWidget):
        super().__init__("cash_register_view", parent_widget)

        # Controller
        self.controller = CashRegisterController()

        # Titolo e sottotitolo
        self.setTitleText("Registro di cassa")
        self.setSubtitleText("Clicca due volte su una transazione per modificarla o eliminarla")

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

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
        self.search_combo_box.insertItem(0, "Cerca in base all'ordine", userData="ordine")
        self.search_combo_box.insertItem(1, "Cerca in base all'articolo", userData="articolo")
        self.search_combo_box.setCurrentIndex(0)

        # Layout di ricerca con SearchBox e ComboBox
        self.search_box_layout = QVBoxLayout(self.sidebar_frame)
        self.search_box_layout.setContentsMargins(0, 0, 0, 0)
        self.search_box_layout.setSpacing(12)
        self.search_box_layout.addWidget(self.search_box)
        self.search_box_layout.addWidget(self.search_combo_box)

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
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Uscite"
        self.revenue_checkbox = CheckBox(self.sidebar_frame)
        self.revenue_checkbox.setObjectName("revenue_check_box")
        self.revenue_checkbox.setText("Entrate")
        self.revenue_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.revenue_checkbox)

        # CheckBox "Entrata"
        self.spending_check_box = CheckBox(self.sidebar_frame)
        self.spending_check_box.setObjectName("spending_check_box")
        self.spending_check_box.setText("Uscite")
        self.spending_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.spending_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = PushButton(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_order_list)

        # Spacer tra i due pulsanti
        self.sidebar_spacer = HorizontalLine(self.sidebar_frame)

        # Button "Registra transazione"
        self.create_button = PrimaryPushButton(self.sidebar_frame)
        self.create_button.setText("Registra transazione")
        '''self.create_button.clicked.connect(self.show_transaction_form)'''

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)

        self.sidebar_layout.addWidget(self.sidebar_spacer)
        self.sidebar_layout.addWidget(self.create_button)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Id", "Descrizione", "Data pagamento", "Importo"]
        self.table.setHeaders(headers)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        # Table Adapter
        self.table_adapter = TransactionListAdapter(self.table)
        self.table_adapter.setColumnItemClass(2, DateTableItem)  # Per un corretto ordinamento delle date
        self.table_adapter.setData(self.get_filtered_transaction_list())
        '''self.table_adapter.onDoubleClick(self.show_order_details)'''

        def update_table(message: Message):
            match message.event():
                case CashRegisterRepository.Event.TRANSACTION_CREATED:
                    if len(self.controller.filter_transactions(self.form_manager.data(), message.data())) != 0:
                        self.table_adapter.addData(message.data())
                case CashRegisterRepository.Event.TRANSACTION_DELETED:
                    self.table_adapter.removeRowByKey(message.data())
                case CashRegisterRepository.Event.TRANSACTION_UPDATED:
                    self.table_adapter.updateDataColumns(message.data(), [1, 2, 3])

        self.controller.observe_transaction_list(update_table)

        self.central_layout.addWidget(self.table)

    # Ritorna la lista di ordini filtrata
    def get_filtered_transaction_list(self) -> list[CashRegisterTransaction]:
        return self.controller.get_transaction_list(self.form_manager.data())

    # Aggiorna la lista degli ordini mostrata in tabella
    def refresh_order_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_transaction_list())

    # Mostra la form per la creazione di ordini
    '''def show_transaction_form(self):
        CreateTransactionView(self.controller).exec()'''


class TransactionListAdapter(TableAdapter):
    def adaptData(self, transaction: CashRegisterTransaction) -> list[str]:
        return [transaction.get_transaction_id(),
                transaction.get_description(),
                transaction.get_payment_date(),
                transaction.get_amount()
                ]

    def onRowAdded(self, transaction: CashRegisterTransaction, row: int) -> None:
        self.table.setRowColor(row, QColor(114, 187, 83) if transaction.is_revenue() else QColor(255, 47, 76))

