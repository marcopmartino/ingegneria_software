from PyQt5.QtWidgets import QWidget, QLineEdit

from lib.layout.LineEditLayout import LineEditLayout
from lib.view.AccessView import AccessView
from lib.view.SignUpView import SignUpView
from res.Strings import FormStrings, AccessStrings


class LoginView(AccessView):

    def __init__(self, parent_widget: QWidget = None):
        super(LoginView, self).__init__(parent_widget)

        # Campo di input Email
        self.emailLayout = LineEditLayout(FormStrings.EMAIL, False, self)

        # Campo di input Password
        self.passwordLayout = LineEditLayout(FormStrings.PASSWORD, False, self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Aggiunge i campi di input della form al layout
        self.inputLayout.addLayout(self.emailLayout)  # Aggiunge il layout del campo Email
        self.inputLayout.addLayout(self.passwordLayout)  # Aggiunge il layout del campo Password

        # Testo
        self.titleLabel.setText(AccessStrings.TITLE_LOGIN)
        self.submitButton.setText(AccessStrings.LOGIN)
        self.bottomLabel.setText(AccessStrings.BOTTOM_TEXT_LOGIN)

    #
    def on_submit(self):
        pass

    # Mostra la form di registrazione
    def on_bottom_label_click(self):
        self.parent().parent().show_sign_up_form()

