from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QSizePolicy, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QWidget
from qfluentwidgets import DoubleSpinBox, PushButton, LineEdit

from lib.controller.CashRegisterController import CashRegisterController
from lib.layout.CustomDatePicker import CustomDatePicker
from lib.layout.FrameLayouts import HFrameLayout
from lib.layout.LineEditLayouts import LineEditCompositeLayout
from lib.model.CashRegisterTransaction import CashRegisterTransaction
from lib.utility.UtilityClasses import DatetimeUtils
from lib.validation.FormField import LineEditCompositeFormField, SpinBoxFormField, DatePickerFormField
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from res import Styles
from res.Dimensions import FontWeight, LineEditDimensions, FontSize
from res.Strings import FormStrings


class TransactionFormView(QDialog):

    @classmethod
    def new(cls, controller: CashRegisterController):

        # Inizializza la vista
        self = cls(controller)

        # Imposta nome e titolo della vista
        self.setObjectName("create_transaction_view")
        self.setWindowTitle("Registrazione transazione")
        self.title.setText("Nuova transazione")

        # Mostra il pulsante di creazione
        self.create_button.setHidden(False)

        return self

    @classmethod
    def edit(cls, controller: CashRegisterController, transaction: CashRegisterTransaction):

        # Inizializza la vista
        self = cls(controller)

        # Imposta nome e titolo della vista
        self.setObjectName(f"edit_transaction_{transaction.get_transaction_id()}_view")
        self.setWindowTitle("Modifica transazione")
        self.title.setText(f"Modifica transazione {transaction.get_transaction_id()}")

        # Popola la form con i dati della transazione
        self.form_manager.set_token(transaction.get_transaction_id())
        self.description_line_edit_layout.line_edit.setText(transaction.get_description())
        self.amount_spin_box.setValue(transaction.get_amount())
        self.date_picker.setDate(DatetimeUtils.format(transaction.get_payment_date()))

        # Mostra i pulsanti di modifica ed eliminazione
        self.edit_button.setHidden(False)
        self.delete_button.setHidden(False)

        return self

    def __init__(self, controller: CashRegisterController):
        super().__init__()

        # Controller
        self.controller: CashRegisterController = controller

        # Finestra
        self.resize(320, 180)

        # Widget
        self.widget = QWidget(self)
        self.widget.setMaximumHeight(400)
        self.widget.setObjectName("widget")

        # Layout
        self.layout = QVBoxLayout(self.widget)
        self.layout.setObjectName("layout")

        # Frame Layout
        self.frame_layout = HFrameLayout(self)
        self.frame_layout.setSpacerDimensionAndPolicy(50, QSizePolicy.Expanding)
        self.frame_layout.setCentralWidget(self.widget)

        # Titolo
        self.title = QLabel(self)
        font = QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setContentsMargins(0, 0, 0, 8)
        self.title.setObjectName("title")
        self.layout.addWidget(self.title)

        # Campo Descrizione
        self.description_line_edit_layout = LineEditCompositeLayout(
            field_name=FormStrings.DESCRIPTION, parent_widget=self, line_edit_class=LineEdit)
        self.description_line_edit_layout.label.setStyleSheet(Styles.ACCESS_LABEL)
        self.description_line_edit_layout.setSpacing(4)
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.description_line_edit_layout.line_edit.setFont(font)
        self.description_line_edit_layout.setObjectName("description_line_edit_layout")
        self.layout.addLayout(self.description_line_edit_layout)

        # Campo Importo
        self.amount_layout = QVBoxLayout()
        self.layout.addLayout(self.amount_layout)

        # Campo Importo - Label
        self.amount_label = QLabel(FormStrings.AMOUNT)
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.amount_label.setFont(font)
        self.amount_label.setStyleSheet(Styles.ACCESS_LABEL)
        self.amount_label.setContentsMargins(0, 8, 0, 0)
        self.amount_label.setObjectName("amount_label")
        self.amount_layout.addWidget(self.amount_label)

        # Campo Importo - SpinBox
        self.amount_spin_box = DoubleSpinBox(self)
        self.amount_spin_box.setRange(-9999999.99, 9999999.99)
        self.amount_spin_box.setDecimals(2)  # Due cifre dopo la virgola
        self.amount_spin_box.setObjectName("importo_spin_box")
        self.amount_layout.addWidget(self.amount_spin_box)

        # Seconda Label per mostrare un errore di input, utile nella validazione
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        self.amount_error_label = QLabel(self)
        self.amount_error_label.setFont(font)
        self.amount_error_label.setText("L'importo non può essere nullo")
        self.amount_error_label.setObjectName(f"amount_error_label")
        self.amount_error_label.setStyleSheet(Styles.ERROR_LABEL_INPUT)
        self.amount_error_label.setHidden(True)  # Nasconde la Label
        self.amount_layout.addWidget(self.amount_error_label)

        # Campo Data di pagamento
        self.date_picker_layout = QVBoxLayout()
        self.layout.addLayout(self.date_picker_layout)

        # Campo Data di pagamento - Label
        self.date_picker_label = QLabel("Data pagamento")
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.date_picker_label.setFont(font)
        self.date_picker_label.setStyleSheet(Styles.ACCESS_LABEL)
        self.date_picker_label.setContentsMargins(0, 8, 0, 0)
        self.date_picker_label.setObjectName("date_picker_label")
        self.date_picker_layout.addWidget(self.date_picker_label)

        # Campo Data di pagamento - DatePicker
        self.date_picker = CustomDatePicker()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setObjectName("data_picker")
        self.date_picker_layout.addWidget(self.date_picker)

        # Pulsanti di creazione\eliminazione\modifica
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(12)
        self.buttons_layout.setContentsMargins(0, 8, 0, 8)
        self.buttons_layout.setObjectName("buttons_layout")
        self.layout.addLayout(self.buttons_layout)

        # Pulsante di creazione
        self.create_button = PushButton(text="Crea transazione")
        self.create_button.setStyleSheet(Styles.EDIT_BUTTON)
        self.create_button.setObjectName("create_button")
        self.create_button.setHidden(True)
        self.buttons_layout.addWidget(self.create_button)

        # Pulsante di modifica
        self.edit_button = PushButton(text="Salva modifiche")
        self.edit_button.setStyleSheet(Styles.EDIT_BUTTON)
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setHidden(True)
        self.edit_button.setFixedWidth(150)
        self.buttons_layout.addWidget(self.edit_button)

        # Pulsante di eliminazione
        self.delete_button = PushButton(text="Elimina transazione")
        self.delete_button.setStyleSheet(Styles.DELETE_BUTTON)
        self.delete_button.setObjectName("back_button")
        self.delete_button.setHidden(True)
        self.delete_button.setFixedWidth(150)
        self.buttons_layout.addWidget(self.delete_button)

        # FormManager
        self.form_manager = FormManager()
        self.form_manager.add_fields(
            LineEditCompositeFormField.LayoutAndRule(self.description_line_edit_layout,
                                                     ValidationRule.Required("La descrizione è richiesta")),
            SpinBoxFormField(self.amount_spin_box),
            DatePickerFormField(self.date_picker)
        )
        self.description_line_edit_layout.line_edit.setMaxLength(75)
        self.form_manager.add_submit_button(self.create_button, self.on_create)
        self.form_manager.add_submit_button(self.edit_button, self.on_edit)
        self.form_manager.add_token_button(self.delete_button, self.on_delete)

    # Funzione che esegue la validazione per lo SpinBox
    def validate_amount(self) -> bool:
        if self.amount_spin_box.value() == 0:
            self.amount_error_label.setHidden(False)
            return False
        self.amount_error_label.setHidden(True)
        return True

    # Eseguito al click sul pulsante di creazione
    def on_create(self, form_data: dict[str, any]):

        # True solo se l'importo è non nullo
        if self.validate_amount():

            # Crea e mostra una richiesta di conferma con indicato il prezzo
            clicked_button = QMessageBox.question(
                self,
                "Conferma registrazione transazione",
                (f"La disponibilità di cassa sarà aggiornata automaticamente.\n"
                 f"Sei sicuro di voler registrare la transazione?"),
                QMessageBox.Yes | QMessageBox.No
            )

            # In caso di conferma, crea la transazione e chiude la finestra
            if clicked_button == QMessageBox.Yes:
                self.controller.create_transaction(form_data)
                self.close()

    # Eseguito al click sul pulsante di modifica
    def on_edit(self, form_data: dict[str, any]):

        # True solo se l'importo è non nullo
        if self.validate_amount():

            # Crea e mostra una richiesta di conferma con indicato il prezzo
            clicked_button = QMessageBox.question(
                self,
                "Conferma modifica transazione",
                (f"La disponibilità di cassa sarà aggiornata automaticamente.\n"
                 f"Sei sicuro di voler modificare la transazione?"),
                QMessageBox.Yes | QMessageBox.No
            )

            # In caso di conferma, aggiorna la transazione e chiude la finestra
            if clicked_button == QMessageBox.Yes:
                self.controller.update_transaction_by_id(form_data.pop("form_token"), form_data)
                self.close()

    # Eseguito al click sul pulsante di eliminazione
    def on_delete(self, form_token):

        # Crea e mostra una richiesta di conferma con indicato il prezzo
        clicked_button = QMessageBox.question(
            self,
            "Conferma eliminazione transazione",
            (f"La transazione {form_token} sarà eliminata.\n"
             f"Sei sicuro di voler eliminare la transazione?"),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, elimina la transazione e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.delete_transaction_by_id(form_token)
            self.close()
