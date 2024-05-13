from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QLineEdit, QMainWindow, \
    QRadioButton, QDialog
from qfluentwidgets import LineEdit

import lib.utility.UtilityClasses as utility
from lib.controller.WorkerListController import WorkerListController
from lib.layout.CustomDatePicker import CustomDatePicker
from lib.controller.ProfileController import ProfileController
from lib.layout.LineEditLayouts import LineEditCompositeLayout
from lib.utility.ErrorHelpers import InvalidLoginCredentialsException, EmailExistsException
from lib.validation.FormField import LineEditCompositeFormField, DatePickerFormField
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from res import Styles, Dimensions
from res.Dimensions import LineEditDimensions, FontWeight, FontSize
from res.Strings import FormStrings, Config, ValidationStrings, WorkerStrings


class AddWorkerView(QDialog):

    def __init__(self, controller: WorkerListController):
        super().__init__()

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.controller = controller

        # Finestra
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.setObjectName("add_worker_window")
        self.resize(250, 500)
        self.setStyleSheet(Styles.EDIT_PROFILE_PAGE)

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

        self.displayTitle = QLabel(WorkerStrings.ADD_WORKER, self)
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
        self.nameLayout = LineEditCompositeLayout(FormStrings.NAME, parent_widget=self, line_edit_class=LineEdit)
        self.profileForm.addLayout(self.nameLayout)
        self.profileForm.setAlignment(self.nameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, parent_widget=self, line_edit_class=LineEdit)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, parent_widget=self, line_edit_class=LineEdit)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo codice fiscale
        self.fiscalCodeLayout = LineEditCompositeLayout(FormStrings.CF, parent_widget=self, line_edit_class=LineEdit)
        self.profileForm.addLayout(self.fiscalCodeLayout)
        self.profileForm.setAlignment(self.fiscalCodeLayout, Qt.AlignCenter)

        # Campo data di nascità
        self.birthDateLayout = QVBoxLayout()
        self.birthDateLayout.setSpacing(0)

        self.birthDateLabel = QLabel(FormStrings.BIRTH_DATE)
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.birthDateLabel.setFont(font)

        self.birthDatePicker = CustomDatePicker()
        self.birthDatePicker.setObjectName("data di nascita_date_picker")
        self.birthDatePicker.setDate(QDate.currentDate().addYears(-18))

        self.birthDateLayout.addWidget(self.birthDateLabel)
        self.birthDateLayout.addWidget(self.birthDatePicker)

        self.profileForm.addLayout(self.birthDateLayout)

        # Campo input password
        self.passwordLayout = LineEditCompositeLayout(FormStrings.PASSWORD, parent_widget=self,
                                                      line_edit_class=LineEdit)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.passwordLayout)
        self.profileForm.setAlignment(self.passwordLayout, Qt.AlignCenter)

        # Campo input conferma password
        self.confirmPasswordLayout = LineEditCompositeLayout(FormStrings.PASSWORD_CONFIRM, parent_widget=self,
                                                             line_edit_class=LineEdit)
        self.confirmPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.confirmPasswordLayout)
        self.profileForm.setAlignment(self.confirmPasswordLayout, Qt.AlignCenter)

        # Label di errore in caso di email già in uso
        self.emailExistsLabel = QLabel(ValidationStrings.EMAIL_ALREADY_USED)
        self.emailExistsLabel.setStyleSheet(Styles.ERROR_LABEL)
        self.emailExistsLabel.setHidden(True)
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.emailExistsLabel.setFont(font)
        self.profileForm.addWidget(self.emailExistsLabel, alignment=Qt.AlignHCenter)

        # Sezione finale con i pulsanti
        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        # Pulsante per la creazione dell'account
        self.addButton = QPushButton("Crea account")
        self.addButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.addButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.addButton.setObjectName("SaveEditButton")

        self.buttonsBox.addWidget(self.addButton, alignment=Qt.AlignCenter)

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

        self.form_manager = FormManager()
        self.form_manager.add_fields(name_field, cf_field,
                                     email_field, phone_field, birth_field, password_field, confirm_password_field)
        self.form_manager.add_submit_button(self.addButton, self.on_submit)

    # Esegue i controlli sulla password e crea un nuovo operaio
    def on_submit(self, form_data: dict[str, any]):
        print("Save_edit...")
        print(form_data)

        # Nasconde la Label di errore per email già in uso
        self.emailExistsLabel.setHidden(True)

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
        else:
            print("Il campo password è richiesto")
            self.passwordLayout.error_label.setText(ValidationStrings.FIELD_REQUIRED)
            self.passwordLayout.error_label.setHidden(False)
            continue_submit = False

        # Se i controlli sono passati, prosegue con l'aggiornamento
        if continue_submit:
            try:
                self.controller.create_worker(form_data)
                self.close()
            except EmailExistsException:
                self.emailExistsLabel.setHidden(False)
