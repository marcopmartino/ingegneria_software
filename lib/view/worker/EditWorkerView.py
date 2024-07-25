from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QDialog, \
    QMessageBox
from qfluentwidgets import LineEdit

from lib.controller.WorkerListController import WorkerListController
from lib.utility.ErrorHelpers import ConnectionErrorHelper
from lib.utility.gui.widget.CustomDatePicker import CustomDatePicker
from lib.utility.gui.layout.LineEditLayouts import LineEditCompositeLayout
from lib.model.Employee import Employee
from lib.utility.validation.FormField import LineEditCompositeFormField, DatePickerFormField
from lib.utility.validation.FormManager import FormManager
from lib.utility.validation.ValidationRule import ValidationRule
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from res import Styles, Dimensions
from res.Dimensions import LineEditDimensions, FontWeight, FontSize, GenericDimensions
from res.Strings import FormStrings, Config, ValidationStrings, WorkerStrings


class EditWorkerView(QDialog):

    def __init__(self, controller: WorkerListController, data: Employee):
        super().__init__()

        self.controller = controller

        # Finestra
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.setObjectName("add_worker_window")
        self.resize(250, 500)
        self.setStyleSheet(Styles.EDIT_PROFILE_LINE_EDIT)

        self.outerWidget = QWidget(self)
        self.outerWidget.setObjectName("outer_widget")

        self.outerLayout = QHBoxLayout(self.outerWidget)
        self.outerLayout.setObjectName("outer_layout")
        self.innerLayout = QVBoxLayout(self)
        self.innerLayout.setObjectName("inner_layout")
        self.innerLayout.setSpacing(0)

        self.titleFrame = QFrame()
        #self.titleFrame.setStyleSheet(Styles.PAGE_TITLE_FRAME)

        self.title = QVBoxLayout(self.titleFrame)
        self.title.setContentsMargins(10, 10, 0, 10)
        self.title.setSpacing(3)
        self.title.setObjectName("TitleVerticalBox")

        self.displayTitle = QLabel(WorkerStrings.EDIT_WORKER, self)
        self.displayTitle.setStyleSheet(Styles.LABEL_TITLE)

        self.title.addWidget(self.displayTitle)
        self.title.setAlignment(self.displayTitle, Qt.AlignCenter)

        self.innerLayout.addWidget(self.titleFrame)
        self.innerLayout.setAlignment(self.titleFrame, Qt.AlignTop)

        # Layout contenente i campi di input
        self.profileForm = QVBoxLayout()
        self.profileForm.setContentsMargins(10, 10, 10, 10)
        self.profileForm.setSpacing(15)
        self.profileForm.setObjectName("AddWorkerForm")

        # Campo input nome azienda
        self.nameLayout = LineEditCompositeLayout(FormStrings.NAME, text=data.get_name(), parent_widget=self,
                                                  line_edit_class=LineEdit)
        self.nameLayout.label.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        self.profileForm.addLayout(self.nameLayout)
        self.profileForm.setAlignment(self.nameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, text=data.get_email(), parent_widget=self,
                                                   line_edit_class=LineEdit)
        self.emailLayout.line_edit.setEnabled(False)
        self.emailLayout.label.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, text=data.get_phone(), parent_widget=self,
                                                   line_edit_class=LineEdit)
        self.phoneLayout.label.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo codice fiscale
        self.fiscalCodeLayout = LineEditCompositeLayout(FormStrings.CF, text=data.get_CF(), parent_widget=self,
                                                        line_edit_class=LineEdit)
        self.fiscalCodeLayout.label.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        self.profileForm.addLayout(self.fiscalCodeLayout)
        self.profileForm.setAlignment(self.fiscalCodeLayout, Qt.AlignCenter)

        # Campo data di nascità
        self.birthDateLayout = QVBoxLayout()
        self.birthDateLayout.setSpacing(0)

        self.birthDateLabel = QLabel(FormStrings.BIRTH_DATE)
        self.birthDateLabel.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.birthDateLabel.setFont(font)

        self.birthDatePicker = CustomDatePicker()
        self.birthDatePicker.setObjectName("data di nascita_date_picker")
        self.birthDatePicker.setDate(data.get_birth_date())

        self.birthDateLayout.addWidget(self.birthDateLabel)
        self.birthDateLayout.addWidget(self.birthDatePicker)

        self.profileForm.addLayout(self.birthDateLayout)

        # Campo input password
        self.passwordWidget = QWidget(self)
        self.passwordLayout = LineEditCompositeLayout(FormStrings.PASSWORD, parent_widget=self.passwordWidget,
                                                      line_edit_class=LineEdit)
        self.passwordLayout.label.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.passwordLayout.setContentsMargins(0, 0, 0, 0)
        self.profileForm.addWidget(self.passwordWidget)

        # Campo input conferma password
        self.confirmPasswordWidget = QWidget(self)
        self.confirmPasswordLayout = LineEditCompositeLayout(FormStrings.PASSWORD_CONFIRM,
                                                             parent_widget=self.confirmPasswordWidget,
                                                             line_edit_class=LineEdit)
        self.confirmPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.confirmPasswordLayout.label.setStyleSheet(Styles.EDIT_PROFILE_LABEL)
        self.confirmPasswordLayout.setContentsMargins(0, 0, 0, 0)
        self.profileForm.addWidget(self.confirmPasswordWidget)

        # Pulsante modifica password
        def show_new_password_fields():
            self.showNewPasswordFieldsButton.setHidden(True)
            self.passwordWidget.setHidden(False)
            self.confirmPasswordWidget.setHidden(False)

        self.showNewPasswordFieldsButton = CustomPushButton.white(text="Imposta nuova password")
        self.showNewPasswordFieldsButton.clicked.connect(show_new_password_fields)
        self.passwordWidget.setHidden(True)
        self.confirmPasswordWidget.setHidden(True)
        self.profileForm.addWidget(self.showNewPasswordFieldsButton)

        # Sezione finale con i pulsanti
        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setContentsMargins(0, 0, 0, 8)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.deleteButton = CustomPushButton.orange(text="Elimina account", point_size=FontSize.DEFAULT)
        #self.deleteButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteButton.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.deleteButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.deleteButton.setObjectName("DeleteEditButton")
        self.editButton = CustomPushButton.cyan(text=FormStrings.SAVE_EDIT, point_size=FontSize.DEFAULT)
        #self.editButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.editButton.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.editButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.editButton.setObjectName("SaveEditButton")

        self.buttonsBox.addWidget(self.editButton, alignment=Qt.AlignLeft)
        self.buttonsBox.addWidget(self.deleteButton, alignment=Qt.AlignRight)

        self.profileForm.addLayout(self.buttonsBox)

        self.profileForm.setAlignment(self.buttonsBox, Qt.AlignCenter)

        self.innerLayout.addLayout(self.profileForm)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        name_field = LineEditCompositeFormField.LayoutAndRule(self.nameLayout, ValidationRule.Required())
        cf_field = LineEditCompositeFormField.LayoutAndRule(self.fiscalCodeLayout, ValidationRule.FiscalCode())
        email_field = LineEditCompositeFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        phone_field = LineEditCompositeFormField.LayoutAndRule(self.phoneLayout, ValidationRule.Phone())
        birth_field = DatePickerFormField(self.birthDatePicker)
        password_field = (LineEditCompositeFormField.Layout(self.passwordLayout))
        confirm_password_field = (LineEditCompositeFormField.Layout(self.confirmPasswordLayout))

        self.form_manager = FormManager(form_token=data.get_uid())
        self.form_manager.add_fields(name_field, cf_field,
                                     email_field, phone_field, birth_field, password_field, confirm_password_field)
        self.form_manager.add_submit_button(self.editButton, self.on_submit)
        self.form_manager.add_token_button(self.deleteButton, self.on_delete)

    # Esegue i controlli sulla password e crea un nuovo operaio
    def on_submit(self, form_data: dict[str, any]):
        print("Save_edit...")
        print(form_data)

        # Estraggo i campi "Password" e "Conferma password"
        password = form_data.get("password")
        confirm_password = form_data.pop("conferma password")

        # Variabile che indica se proseguire con l'aggiornamento
        continue_submit: bool = True

        # Controlli sui campi "Nuova password" e "Conferma nuova password"
        if password:
            if len(password) >= 6:
                if confirm_password:
                    if password != confirm_password:
                        print("Le password non combaciano")
                        self.passwordLayout.error_label.setText(ValidationStrings.PASSWORD_CONFIRM_DIFFERENT)
                        self.passwordLayout.error_label.setHidden(False)
                        continue_submit = False
                else:
                    print("Conferma password richiesta")
                    self.confirmPasswordLayout.error_label.setText(ValidationStrings.FIELD_REQUIRED)
                    self.confirmPasswordLayout.error_label.setHidden(False)
                    continue_submit = False
            else:
                print("Il campo password deve essere lungo almeno 6 caratteri")
                self.passwordLayout.error_label.setText(ValidationStrings.MIN_PASSWORD_ERROR)
                self.passwordLayout.error_label.setHidden(False)
                continue_submit = False

        # Se i controlli sono passati, prosegue con l'aggiornamento
        if continue_submit:
            ConnectionErrorHelper.handle(lambda: self.controller.update_worker(form_data), self.window())
            self.close()

    # Eseguito al click sul pulsante di eliminazione
    def on_delete(self, form_token):

        # Crea e mostra una richiesta di conferma con indicato il prezzo
        clicked_button = QMessageBox.question(
            self,
            "Conferma eliminazione dipendente",
            (f"Sei sicuro di voler eliminare il dipendente?\n"
             f"L'operazione non è reversibile."),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, elimina la transazione e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            ConnectionErrorHelper.handle(lambda: self.controller.delete_worker_by_id(form_token), self.window())
            self.close()
