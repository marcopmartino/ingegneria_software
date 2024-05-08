from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QLineEdit, QDialog

import lib.utility.UtilityClasses as utility
from lib.layout.CustomDatePicker import CustomDatePicker
from lib.layout.LineEditLayouts import LineEditCompositeLayout
from lib.validation.FormField import LineEditCompositeFormField
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from res import Styles, Dimensions
from res.Dimensions import LineEditDimensions, FontWeight
from res.Strings import FormStrings, Config, ProfileStrings, ValidationStrings


class EditAdminProfileWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.controller = self.parent().controller

        data = self.controller.get_user_data()

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
        self.titleFrame.setStyleSheet(Styles.PAGE_TITLE_FRAME)

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
        self.nameLayout = LineEditCompositeLayout(FormStrings.NAME, data['name'], self)
        self.profileForm.addLayout(self.nameLayout)
        self.profileForm.setAlignment(self.nameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, data['mail'], self)
        self.emailLayout.line_edit.setEnabled(False)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, data['phone'], self)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo data di nascità
        self.birthDateLayout = QHBoxLayout()

        self.birthDateLabel = QLabel("Data di nascita: ")
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.birthDateLabel.setFont(font)

        self.birthDatePicker = CustomDatePicker()
        date = data['birth_date'].split('/')
        default_date = QDate()
        default_date.setDate(int(date[2]), int(date[1]), int(date[0]))
        self.birthDatePicker.setDate(default_date)

        self.birthDateLayout.addWidget(self.birthDateLabel)
        self.birthDateLayout.addWidget(self.birthDatePicker)

        self.profileForm.addLayout(self.birthDateLayout)
        self.profileForm.setAlignment(self.birthDateLayout, Qt.AlignCenter)

        # Campo input partita IVA
        self.CFNumberLayout = LineEditCompositeLayout(FormStrings.CF, data['CF'], self)
        self.profileForm.addLayout(self.CFNumberLayout)
        self.profileForm.setAlignment(self.CFNumberLayout, Qt.AlignCenter)

        # Campo input nuova password
        self.newPasswordLayout = LineEditCompositeLayout(FormStrings.NEW_PASSWORD, parent_widget=self)
        self.newPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.newPasswordLayout)
        self.profileForm.setAlignment(self.newPasswordLayout, Qt.AlignCenter)

        # Campo input conferma nuova password
        self.confirmNewPasswordLayout = LineEditCompositeLayout(FormStrings.NEW_PASSWORD_CONFIRM, parent_widget=self)
        self.confirmNewPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.confirmNewPasswordLayout)
        self.profileForm.setAlignment(self.confirmNewPasswordLayout, Qt.AlignCenter)

        # Campo input vecchia password
        self.passwordLayout = LineEditCompositeLayout(FormStrings.PASSWORD, parent_widget=self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.passwordLayout)
        self.profileForm.setAlignment(self.passwordLayout, Qt.AlignCenter)

        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.deleteEditButton = QPushButton(FormStrings.DELETE_EDIT)
        self.deleteEditButton.clicked.connect(self.delete_edit)
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
        new_password_field = (LineEditCompositeFormField.Layout(self.newPasswordLayout))
        confirm_new_password_field = (LineEditCompositeFormField.Layout(self.confirmNewPasswordLayout))
        password_field = LineEditCompositeFormField.LayoutAndRule(self.passwordLayout, ValidationRule.Password())

        self.form_manager = FormManager()
        self.form_manager.add_fields(name_field, fiscal_code,
                                     email_field, phone_field, new_password_field, password_field,
                                     new_password_field, confirm_new_password_field)
        self.form_manager.add_submit_button(self.saveEditButton, self.on_submit)

    # Esegue i controlli e la modifica dei dati
    def on_submit(self, form_data: dict[str, any]):
        newPassword = None
        print("Save_edit...")
        currentData = self.controller.get_user_data()
        password = self.passwordLayout.line_edit.text()
        if self.newPasswordLayout.line_edit.text() != "":
            if len(self.newPasswordLayout.line_edit.text()) > 6:
                if self.confirmNewPasswordLayout.line_edit.text() != "":
                    if self.newPasswordLayout.line_edit.text() != self.confirmNewPasswordLayout.line_edit.text():
                        print("Le password non combaciano")
                        self.newPasswordLayout.error_label.setText(ValidationStrings.PASSWORD_CONFIRM_DIFFERENT)
                        self.newPasswordLayout.error_label.setHidden(False)
                    else:
                        newPassword = self.newPasswordLayout.line_edit.text()
                else:
                    print("Conferma nuova password richiesta")
                    self.confirmNewPasswordLayout.error_label.setText(ValidationStrings.FIELD_REQUIRED)
            else:
                print("Il campo nuova password deve essere lungo almeno 6 caratteri.")
                self.newPasswordLayout.error_label.setText(ValidationStrings.MIN_PASSWORD_ERROR)

        try:
            self.controller.check_login(currentData['mail'], password)
            data = {
                "name": self.nameLayout.line_edit.text(),
                "CF": self.CFNumberLayout.line_edit.text(),
                "birth": self.birthDatePicker.date.toString('dd/MM/yyyy'),
                "phone": utility.PhoneFormatter().format(self.phoneLayout.line_edit.text()),
                "role": "manager"
            }
            self.controller.set_user_data(data, newPassword, currentData['uid'])
            self.close()
        except Exception as e:
            print(e)

    # Chiude la finestra alla pressione di un bottone
    def delete_edit(self):
        self.close()
