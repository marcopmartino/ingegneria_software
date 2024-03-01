from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel

from lib.firebaseData import firebase
from lib.layout.LineEditLayout import LineEditLayout
from lib.validation.FormField import LineEditValidatableFormField
from lib.validation.ValidationRule import ValidationRule
from lib.view.Access.AccessView import AccessView
from res import Styles
from res.Dimensions import LineEditDimensions
from res.Strings import FormStrings, AccessStrings, ValidationStrings


class LoginView(AccessView):

    def __init__(self, parent_widget: QWidget = None):
        super(LoginView, self).__init__(parent_widget)

        # Campo di input Email
        self.emailLayout = LineEditLayout(FormStrings.EMAIL, self)

        # Campo di input Password
        self.passwordLayout = LineEditLayout(FormStrings.PASSWORD, self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Aggiunge i campi di input della form al layout
        self.inputLayout.addLayout(self.emailLayout)  # Aggiunge il layout del campo Email
        self.inputLayout.addLayout(self.passwordLayout)  # Aggiunge il layout del campo Password

        # Crea Una Label di errore
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        self.validation_error_label = QLabel(parent_widget)
        self.validation_error_label.setFont(font)
        self.validation_error_label.setObjectName("error_label")
        self.validation_error_label.setAlignment(Qt.AlignCenter)
        self.validation_error_label.setStyleSheet(Styles.ERROR_LABEL_INPUT)
        self.validation_error_label.setHidden(True)  # Nasconde la Label

        # Aggiunge la label di errore al layout che racchiude il contenuto principale
        self.contentLayout.insertWidget(2, self.validation_error_label)

        # Imposta il testo per le Label e il pulsante di submit
        self.titleLabel.setText(AccessStrings.TITLE_LOGIN)
        self.validation_error_label.setText(ValidationStrings.EMAIL_PASSWORD_WRONG)
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
        email = self.emailLayout.line_edit.text()
        password = self.passwordLayout.line_edit.text()
        try:
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            print("Connesso!")
            self.parent().parent().show_main_window()

        except:
            self.validation_error_label.setHidden(False)
            print("??")

    # Mostra la form di registrazione
    def on_bottom_label_click(self):
        self.parent().parent().show_sign_up_form()
