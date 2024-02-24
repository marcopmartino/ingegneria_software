from PyQt5.QtWidgets import QWidget, QLineEdit

from lib.layout.LineEditLayout import LineEditLayout
from lib.view.AccessView import AccessView
from res.Strings import FormStrings, AccessStrings


class SignUpView(AccessView):

    def __init__(self, parent_widget: QWidget = None):
        super(SignUpView, self).__init__(parent_widget)

        # Campo di input Nome azienda
        self.companyNameLayout = LineEditLayout(FormStrings.COMPANY_NAME, True, self)

        # Campo di input Partita IVA
        self.IVANumberLayout = LineEditLayout(FormStrings.IVA_NUMBER, True, self)

        # Campo di input Indirizzo di recapito
        self.deliveryAddressLayout = LineEditLayout(FormStrings.DELIVERY_ADDRESS, True, self)

        # Campo di input Email
        self.emailLayout = LineEditLayout(FormStrings.EMAIL, True, self)

        # Campo di input Telefono
        self.phoneLayout = LineEditLayout(FormStrings.PHONE, True, self)

        # Campo di input Password
        self.passwordLayout = LineEditLayout(FormStrings.PASSWORD, True, self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Campo di input Conferma password
        self.confirmPasswordLayout = LineEditLayout(FormStrings.PASSWORD_CONFIRM, True, self)
        self.confirmPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi

        # Aggiunge i campi di input della form al layout
        self.inputLayout.addLayout(self.companyNameLayout)  # Aggiunge il layout del campo Nome azienda
        self.inputLayout.addLayout(self.IVANumberLayout)  # Aggiunge il layout del campo Partita IVA
        self.inputLayout.addLayout(self.deliveryAddressLayout)  # Aggiunge il layout del campo Indirizzo di recapito
        self.inputLayout.addLayout(self.emailLayout)  # Aggiunge il layout del campo Email
        self.inputLayout.addLayout(self.phoneLayout)  # Aggiunge il layout del campo Telefono
        self.inputLayout.addLayout(self.passwordLayout)  # Aggiunge il layout del campo Password
        self.inputLayout.addLayout(self.confirmPasswordLayout)  # Aggiunge il layout del campo Conferma password

        # Testo
        self.titleLabel.setText(AccessStrings.TITLE_SIGN_UP)
        self.submitButton.setText(AccessStrings.SING_UP)
        self.bottomLabel.setText(AccessStrings.BOTTOM_TEXT_SIGN_UP)

    #
    def on_submit(self):
        pass

    # Mostra la form di login
    def on_bottom_label_click(self):
        self.parent().parent().show_login_form()
