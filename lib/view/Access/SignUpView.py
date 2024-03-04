from PyQt5.QtWidgets import QWidget, QLineEdit

from requests import ConnectionError

import lib.firebaseData as firebaseConfig
from lib.firebaseData import firebase
from lib.layout.LineEditLayout import LineEditCompositeLayout
from lib.network.HTTPErrorHelper import HTTPErrorHelper, EmailExistsException
from lib.validation.FormField import LineEditCompositeFormField
from lib.validation.ValidationRule import ValidationRule
from lib.view.Access.AccessView import AccessView
from res.Strings import FormStrings, AccessStrings, ValidationStrings, UtilityStrings


class SignUpView(AccessView):

    def __init__(self, parent_widget: QWidget = None):
        super(SignUpView, self).__init__(parent_widget)

        # Campo di input Nome azienda
        self.companyNameLayout = LineEditCompositeLayout(FormStrings.COMPANY_NAME, self)

        # Campo di input Partita IVA
        self.IVANumberLayout = LineEditCompositeLayout(FormStrings.IVA_NUMBER, self)

        # Campo di input Indirizzo di recapito
        self.deliveryAddressLayout = LineEditCompositeLayout(FormStrings.DELIVERY_ADDRESS, self)

        # Campo di input Email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, self)

        # Campo di input Telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, self)

        # Campo di input Password
        self.passwordLayout = LineEditCompositeLayout(FormStrings.PASSWORD, self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Campo di input Conferma password
        self.confirmPasswordLayout = LineEditCompositeLayout(FormStrings.PASSWORD_CONFIRM, self)
        self.confirmPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Aggiunge i campi di input della form al layout
        self.inputLayout.addLayout(self.companyNameLayout)  # Aggiunge il layout del campo Nome azienda
        self.inputLayout.addLayout(self.IVANumberLayout)  # Aggiunge il layout del campo Partita IVA
        self.inputLayout.addLayout(self.deliveryAddressLayout)  # Aggiunge il layout del campo Indirizzo di recapito
        self.inputLayout.addLayout(self.emailLayout)  # Aggiunge il layout del campo Email
        self.inputLayout.addLayout(self.phoneLayout)  # Aggiunge il layout del campo Telefono
        self.inputLayout.addLayout(self.passwordLayout)  # Aggiunge il layout del campo Password
        self.inputLayout.addLayout(self.confirmPasswordLayout)  # Aggiunge il layout del campo Conferma password

        # Imposta il testo per le Label e il pulsante di submit
        self.titleLabel.setText(AccessStrings.TITLE_SIGN_UP)
        self.submitButton.setText(AccessStrings.SING_UP)
        self.bottomLabel.setText(AccessStrings.BOTTOM_TEXT_SIGN_UP)

        # Inizializzo i campi della form per la validazione
        company_field = LineEditCompositeFormField.LayoutAndRule(self.companyNameLayout, ValidationRule.Required())
        iva_field = LineEditCompositeFormField.LayoutAndRule(self.IVANumberLayout, ValidationRule.IVANumber())
        address_field = LineEditCompositeFormField.LayoutAndRule(self.deliveryAddressLayout, ValidationRule.Address())
        email_field = LineEditCompositeFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        phone_field = LineEditCompositeFormField.LayoutAndRule(self.phoneLayout, ValidationRule.Phone())
        password_field = LineEditCompositeFormField.LayoutAndRule(self.passwordLayout, ValidationRule.Password())
        confirm_password_field = LineEditCompositeFormField.Layout(self.confirmPasswordLayout)

        # Aggiungi i campi al FormManager
        self.form_manager.add_fields(
            company_field, iva_field, address_field, email_field, phone_field, password_field, confirm_password_field)
        self.form_manager.add_submit_button(self.submitButton, self.on_submit)

    # Codice eseguito se la validazione ha successo
    def on_submit(self, form_data: dict[str, any]):
        print(form_data)
        print("Sign up...")
        try:
            if form_data['password'] == form_data["conferma"]:
                self.controller().register(form_data)
                self.window().show_main_window()
            else:
                self.confirmPasswordLayout.error_label.set_error_message(ValidationStrings.PASSWORD_CONFIRM_DIFFERENT)
                self.confirmPasswordLayout.error_label.setHidden(False)

        except EmailExistsException:
            self.on_existing_email_error()

        except ConnectionError:
            self.on_connection_error()

        except HTTPErrorHelper:
            self.on_unexpected_error()

    # Mostra la form di login
    def on_bottom_label_click(self):
        self.window().show_login_form()

    # Da eseguire in caso di email già in uso
    def on_existing_email_error(self):
        self.validation_error_label.setText(ValidationStrings.EMAIL_ALREADY_USED)
        self.validation_error_label.setHidden(False)
        print("EmailExistsException")
