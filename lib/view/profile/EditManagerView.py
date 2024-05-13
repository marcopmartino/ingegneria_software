from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QLineEdit, QMainWindow, \
    QDialog
from qfluentwidgets import LineEdit, PushButton

import lib.utility.UtilityClasses as utility
from lib.controller.ProfileController import ProfileController
from lib.firebaseData import Firebase
from lib.layout.CustomDatePicker import CustomDatePicker
from lib.layout.LineEditLayouts import LineEditCompositeLayout
from lib.model.Employee import Employee
from lib.utility.ErrorHelpers import InvalidLoginCredentialsException
from lib.validation.FormField import LineEditCompositeFormField, DatePickerFormField
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from res import Styles, Dimensions
from res.Dimensions import FontWeight, LineEditDimensions
from res.Strings import FormStrings, Config, ProfileStrings, ValidationStrings


class EditManagerView(QDialog):

    def __init__(self, controller: ProfileController):
        super().__init__()

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.controller = controller

        data: Employee = self.controller.get_user()

        # Finestra
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.setObjectName("edit_profile_window")
        self.resize(250, 500)
        self.setStyleSheet(Styles.EDIT_PROFILE_PAGE)

        self.outerWidget = QWidget(self)
        self.outerWidget.setMaximumHeight(200)
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

        self.displayTitle = QLabel(ProfileStrings.EDIT_BUTTON, self)
        self.displayTitle.setStyleSheet(Styles.LABEL_TITLE)

        self.title.addWidget(self.displayTitle)
        self.title.setAlignment(self.displayTitle, Qt.AlignCenter)

        self.innerLayout.addWidget(self.titleFrame)
        self.innerLayout.setAlignment(self.titleFrame, Qt.AlignTop)

        # Layout contenente i campi di input
        self.profileForm = QVBoxLayout()
        self.profileForm.setContentsMargins(10, 10, 10, 10)
        self.profileForm.setSpacing(15)
        self.profileForm.setObjectName("ProfileForm")

        # Campo input nome azienda
        self.nameLayout = LineEditCompositeLayout(FormStrings.NAME, data.get_name(), self, LineEdit)
        self.profileForm.addLayout(self.nameLayout)
        self.profileForm.setAlignment(self.nameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, Firebase.auth.currentUserEmail(), self, LineEdit)
        self.emailLayout.line_edit.setEnabled(False)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, data.get_phone(), self, LineEdit)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo input indirizzo
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
        self.birthDatePicker.setDate(utility.DatetimeUtils.format(data.get_birth_date()))

        self.birthDateLayout.addWidget(self.birthDateLabel)
        self.birthDateLayout.addWidget(self.birthDatePicker)

        self.profileForm.addLayout(self.birthDateLayout)

        # Campo input partita IVA
        self.CFNumberLayout = LineEditCompositeLayout(FormStrings.CF, data.get_CF(), self, LineEdit)
        self.profileForm.addLayout(self.CFNumberLayout)
        self.profileForm.setAlignment(self.CFNumberLayout, Qt.AlignCenter)

        # Campo input vecchia password
        self.passwordLayout = LineEditCompositeLayout(FormStrings.PASSWORD, parent_widget=self,
                                                      line_edit_class=LineEdit)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.passwordLayout)
        self.profileForm.setAlignment(self.passwordLayout, Qt.AlignCenter)

        # Campo input nuova password
        self.newPasswordWidget = QWidget(self)
        self.newPasswordLayout = LineEditCompositeLayout(FormStrings.NEW_PASSWORD, parent_widget=self.newPasswordWidget,
                                                         line_edit_class=LineEdit)
        self.newPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.newPasswordLayout.setContentsMargins(0, 0, 0, 0)
        self.profileForm.addWidget(self.newPasswordWidget)

        # Campo input conferma nuova password
        self.confirmNewPasswordWidget = QWidget(self)
        self.confirmNewPasswordLayout = LineEditCompositeLayout(FormStrings.NEW_PASSWORD_CONFIRM,
                                                                parent_widget=self.confirmNewPasswordWidget,
                                                                line_edit_class=LineEdit)
        self.confirmNewPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.confirmNewPasswordLayout.setContentsMargins(0, 0, 0, 0)
        self.profileForm.addWidget(self.confirmNewPasswordWidget)

        # Pulsante modifica password
        def show_new_password_fields():
            self.showNewPasswordFieldsButton.setHidden(True)
            self.newPasswordWidget.setHidden(False)
            self.confirmNewPasswordWidget.setHidden(False)

        self.showNewPasswordFieldsButton = PushButton(text="Imposta nuova password")
        self.showNewPasswordFieldsButton.clicked.connect(show_new_password_fields)
        self.newPasswordWidget.setHidden(True)
        self.confirmNewPasswordWidget.setHidden(True)
        self.profileForm.addWidget(self.showNewPasswordFieldsButton)

        # Sezione finale con i pulsanti
        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.deleteEditButton = QPushButton(FormStrings.DELETE_EDIT)
        self.deleteEditButton.clicked.connect(self.close)
        self.deleteEditButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteEditButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.deleteEditButton.setObjectName("DeleteEditButton")
        self.saveEditButton = QPushButton(FormStrings.SAVE_EDIT)
        self.saveEditButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.saveEditButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.saveEditButton.setObjectName("SaveEditButton")

        self.buttonsBox.addWidget(self.deleteEditButton, alignment=Qt.AlignLeft)
        self.buttonsBox.addWidget(self.saveEditButton, alignment=Qt.AlignRight)

        self.profileForm.addLayout(self.buttonsBox)

        self.profileForm.setAlignment(self.buttonsBox, Qt.AlignCenter)

        self.innerLayout.addLayout(self.profileForm)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        name_field = LineEditCompositeFormField.LayoutAndRule(self.nameLayout, ValidationRule.Required())
        fiscal_code = LineEditCompositeFormField.LayoutAndRule(self.CFNumberLayout, ValidationRule.FiscalCode())
        email_field = LineEditCompositeFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        phone_field = LineEditCompositeFormField.LayoutAndRule(self.phoneLayout, ValidationRule.Phone())
        birth_date_field = DatePickerFormField(self.birthDatePicker)
        new_password_field = (LineEditCompositeFormField.Layout(self.newPasswordLayout))
        confirm_new_password_field = (LineEditCompositeFormField.Layout(self.confirmNewPasswordLayout))
        password_field = LineEditCompositeFormField.LayoutAndRule(self.passwordLayout, ValidationRule.Password())

        self.form_manager = FormManager()
        self.form_manager.add_fields(name_field, fiscal_code, birth_date_field,
                                     email_field, phone_field, new_password_field, password_field,
                                     new_password_field, confirm_new_password_field)
        self.form_manager.add_submit_button(self.saveEditButton, self.on_submit)

    # Esegue i controlli e la modifica dei dati
    def on_submit(self, form_data: dict[str, any]):
        print(form_data)
        print("Save_edit...")

        # Estraggo i campi "Nuova password" e "Conferma nuova password"
        new_password = form_data.get("nuova password")
        confirm_new_password = form_data.pop("conferma nuova password")

        # Variabile che indica se proseguire con l'aggiornamento
        continue_submit: bool = True

        # Controlli sui campi "Nuova password" e "Conferma nuova password"
        if new_password:
            if len(new_password) >= 6:
                if confirm_new_password:
                    if new_password != confirm_new_password:
                        print("Le password non combaciano")
                        self.newPasswordLayout.error_label.setText(ValidationStrings.PASSWORD_CONFIRM_DIFFERENT)
                        self.newPasswordLayout.error_label.setHidden(False)
                        continue_submit = False
                else:
                    print("Conferma nuova password richiesta")
                    self.confirmNewPasswordLayout.error_label.setText(ValidationStrings.FIELD_REQUIRED)
                    self.confirmNewPasswordLayout.error_label.setHidden(False)
                    continue_submit = False
            else:
                print("Il campo nuova password deve essere lungo almeno 6 caratteri")
                self.newPasswordLayout.error_label.setText(ValidationStrings.MIN_PASSWORD_ERROR)
                self.newPasswordLayout.error_label.setHidden(False)
                continue_submit = False

        # Se i controlli sono passati, prosegue con l'aggiornamento
        if continue_submit:
            try:
                self.controller.update_user(form_data)
                self.close()
            except InvalidLoginCredentialsException:
                self.passwordLayout.error_label.setText("Password non corretta")
                self.passwordLayout.error_label.setHidden(False)
