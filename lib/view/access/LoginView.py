from PyQt5.QtWidgets import QWidget, QLineEdit
from requests import ConnectionError
from requests import HTTPError

from lib.controller.AccessController import AccessController
from lib.utility.gui.layout.LineEditLayouts import LineEditLayout
from lib.utility.ErrorHelpers import InvalidEmailException, MissingPasswordException, \
    InvalidLoginCredentialsException
from lib.utility.validation.FormField import LineEditValidatableFormField
from lib.utility.validation.ValidationRule import ValidationRule
from lib.view.access.AccessView import AccessView
from res.Strings import FormStrings, AccessStrings, ValidationStrings


class LoginView(AccessView):

    def __init__(self, parent_widget: QWidget, controller: AccessController):
        super(LoginView, self).__init__(parent_widget, controller)

        # Campo di input Email
        self.emailLayout = LineEditLayout(FormStrings.EMAIL, parent_widget=self)

        # Campo di input Password
        self.passwordLayout = LineEditLayout(FormStrings.PASSWORD, parent_widget=self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Aggiunge i campi di input della form al layout
        self.inputLayout.addLayout(self.emailLayout)  # Aggiunge il layout del campo Email
        self.inputLayout.addLayout(self.passwordLayout)  # Aggiunge il layout del campo Password

        # Imposta il testo per le Label e il pulsante di submit
        self.titleLabel.setText(AccessStrings.TITLE_LOGIN)
        self.submitButton.setText(AccessStrings.LOGIN)
        self.bottomLabel.setText(AccessStrings.BOTTOM_TEXT_LOGIN)

        # Inizializzo i campi della form per la validazione
        email_field = LineEditValidatableFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        password_field = LineEditValidatableFormField.LayoutAndRule(self.passwordLayout, ValidationRule.Password())

        # Aggiungi i campi al FormManager
        self.form_manager.add_fields(email_field, password_field)
        self.form_manager.add_data_button(self.submitButton, self.on_submit)

    # Prova a effettuare il login e, in caso di successo, mostra la pagina principale
    def on_submit(self, form_data: dict[str, any]):
        print(form_data)
        print("Log in...")
        try:
            self.controller.login(form_data)

            print("Connesso!")
            self.window().show_main_window()

        except (InvalidEmailException, MissingPasswordException, InvalidLoginCredentialsException):
            self.on_invalid_credentials_error()

        except ConnectionError:
            self.on_connection_error()

        except HTTPError:
            self.on_unexpected_error()

    # Mostra la form di registrazione
    def on_bottom_label_click(self):
        self.window().show_sign_up_form()

    # Da eseguire in caso di credenziali errate
    def on_invalid_credentials_error(self):
        self.validation_error_label.setText(ValidationStrings.EMAIL_PASSWORD_WRONG)
        self.validation_error_label.setHidden(False)
        print("InvalidEmailException")
