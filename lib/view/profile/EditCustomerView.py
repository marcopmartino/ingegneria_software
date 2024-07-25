from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QDialog
from qfluentwidgets import LineEdit

from lib.controller.ProfileController import ProfileController
from lib.utility.gui.layout.LineEditLayouts import LineEditCompositeLayout
from lib.model.Customer import Customer
from lib.utility.ErrorHelpers import InvalidLoginCredentialsException, ConnectionErrorHelper
from lib.utility.validation.FormField import LineEditCompositeFormField
from lib.utility.validation.FormManager import FormManager
from lib.utility.validation.ValidationRule import ValidationRule
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from res import Styles, Dimensions
from res.Dimensions import FontSize, GenericDimensions
from res.Strings import FormStrings, Config, ProfileStrings, ValidationStrings


class EditCustomerView(QDialog):

    def __init__(self, controller: ProfileController):
        super().__init__()

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.controller = controller

        data: Customer = self.controller.get_user()

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
        self.companyNameLayout = LineEditCompositeLayout(FormStrings.COMPANY_NAME, data.get_company_name(), self,
                                                         line_edit_class=LineEdit)
        self.profileForm.addLayout(self.companyNameLayout)
        self.profileForm.setAlignment(self.companyNameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, data.get_email(), self, line_edit_class=LineEdit)
        self.emailLayout.line_edit.setEnabled(False)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, data.get_phone(), self, line_edit_class=LineEdit)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo input indirizzo
        self.deliveryAddressLayout = LineEditCompositeLayout(FormStrings.DELIVERY_ADDRESS, data.get_delivery_address(),
                                                             self, line_edit_class=LineEdit)
        self.profileForm.addLayout(self.deliveryAddressLayout)
        self.profileForm.setAlignment(self.deliveryAddressLayout, Qt.AlignCenter)

        # Campo input partita IVA
        self.IVANumberLayout = LineEditCompositeLayout(FormStrings.IVA_NUMBER, data.get_IVA(), self,
                                                       line_edit_class=LineEdit)
        self.profileForm.addLayout(self.IVANumberLayout)
        self.profileForm.setAlignment(self.IVANumberLayout, Qt.AlignCenter)

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
        self.profileForm.setAlignment(self.newPasswordLayout, Qt.AlignCenter)

        # Campo input conferma nuova password
        self.confirmNewPasswordWidget = QWidget(self)
        self.confirmNewPasswordLayout = LineEditCompositeLayout(FormStrings.NEW_PASSWORD_CONFIRM,
                                                                parent_widget=self.confirmNewPasswordWidget,
                                                                line_edit_class=LineEdit)
        self.confirmNewPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.confirmNewPasswordLayout.setContentsMargins(0, 0, 0, 0)
        self.profileForm.addWidget(self.confirmNewPasswordWidget)
        self.profileForm.setAlignment(self.confirmNewPasswordLayout, Qt.AlignCenter)

        # Pulsante modifica password
        def show_new_password_fields():
            self.showNewPasswordFieldsButton.setHidden(True)
            self.newPasswordWidget.setHidden(False)
            self.confirmNewPasswordWidget.setHidden(False)

        self.showNewPasswordFieldsButton = CustomPushButton.white(text="Imposta nuova password")
        self.showNewPasswordFieldsButton.clicked.connect(show_new_password_fields)
        self.newPasswordWidget.setHidden(True)
        self.confirmNewPasswordWidget.setHidden(True)
        self.profileForm.addWidget(self.showNewPasswordFieldsButton)

        # Sezione finale con i pulsanti
        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setContentsMargins(0, 8, 0, 0)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.deleteEditButton = CustomPushButton.white(text=FormStrings.DELETE_EDIT, point_size=FontSize.FLUENT_DEFAULT)
        self.deleteEditButton.clicked.connect(self.close)
        #self.deleteEditButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteEditButton.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.deleteEditButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.deleteEditButton.setObjectName("DeleteEditButton")
        self.saveEditButton = CustomPushButton.cyan(text=FormStrings.SAVE_EDIT, point_size=FontSize.FLUENT_DEFAULT)
        # self.saveEditButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.saveEditButton.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.saveEditButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.saveEditButton.setObjectName("SaveEditButton")

        self.buttonsBox.addWidget(self.saveEditButton, alignment=Qt.AlignLeft)
        self.buttonsBox.addWidget(self.deleteEditButton, alignment=Qt.AlignRight)

        self.profileForm.addLayout(self.buttonsBox)

        self.profileForm.setAlignment(self.buttonsBox, Qt.AlignCenter)

        self.innerLayout.addLayout(self.profileForm)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        company_field = LineEditCompositeFormField.LayoutAndRule(self.companyNameLayout, ValidationRule.Required())
        iva_field = LineEditCompositeFormField.LayoutAndRule(self.IVANumberLayout, ValidationRule.IVANumber())
        address_field = LineEditCompositeFormField.LayoutAndRule(self.deliveryAddressLayout, ValidationRule.Address())
        email_field = LineEditCompositeFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        phone_field = LineEditCompositeFormField.LayoutAndRule(self.phoneLayout, ValidationRule.Phone())
        new_password_field = (LineEditCompositeFormField.Layout(self.newPasswordLayout))
        confirm_new_password_field = (LineEditCompositeFormField.Layout(self.confirmNewPasswordLayout))
        password_field = LineEditCompositeFormField.LayoutAndRule(self.passwordLayout, ValidationRule.Password())

        self.form_manager = FormManager()
        self.form_manager.add_fields(company_field, iva_field, address_field,
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
                ConnectionErrorHelper.handle(lambda: self.controller.update_user(form_data), self.window())
                self.close()
            except InvalidLoginCredentialsException:
                self.passwordLayout.error_label.setText("Password non corretta")
                self.passwordLayout.error_label.setHidden(False)
