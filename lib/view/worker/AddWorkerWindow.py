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
from res.Strings import FormStrings, Config, ValidationStrings, WorkerStrings


class AddWorkerWindow(QDialog):

    def __init__(self, controller, parent=None):
        super().__init__(parent=parent)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.controller = controller
        self.new_worker_uid = None

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
        self.titleFrame.setStyleSheet(Styles.PAGE_TITLE_FRAME)

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
        self.nameLayout = LineEditCompositeLayout(FormStrings.NAME, parent_widget=self)
        self.profileForm.addLayout(self.nameLayout)
        self.profileForm.setAlignment(self.nameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, parent_widget=self)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, parent_widget=self)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo codice fiscale
        self.fiscalCodeLayout = LineEditCompositeLayout(FormStrings.CF, parent_widget=self)
        self.profileForm.addLayout(self.fiscalCodeLayout)
        self.profileForm.setAlignment(self.fiscalCodeLayout, Qt.AlignCenter)

        # Campo data di nascità
        self.birthDateLayout = QHBoxLayout()

        self.birthDateLabel = QLabel("Data di nascita: ")
        font = QFont()
        font.setPointSize(LineEditDimensions.DEFAULT_LABEL_FONT_SIZE)
        font.setBold(True)
        font.setWeight(FontWeight.BOLD)
        self.birthDateLabel.setFont(font)

        self.birthDatePicker = CustomDatePicker()
        self.birthDatePicker.setDate(QDate.currentDate().addYears(-18))

        self.birthDateLayout.addWidget(self.birthDateLabel)
        self.birthDateLayout.addWidget(self.birthDatePicker)

        self.profileForm.addLayout(self.birthDateLayout)
        self.profileForm.setAlignment(self.birthDateLayout, Qt.AlignCenter)

        # Campo input password
        self.passwordLayout = LineEditCompositeLayout(FormStrings.PASSWORD, parent_widget=self)
        self.passwordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.passwordLayout)
        self.profileForm.setAlignment(self.passwordLayout, Qt.AlignCenter)

        # Campo input conferma password
        self.confirmPasswordLayout = LineEditCompositeLayout(FormStrings.PASSWORD_CONFIRM, parent_widget=self)
        self.confirmPasswordLayout.line_edit.setEchoMode(QLineEdit.Password)  # Nasconde il testo con asterischi
        self.profileForm.addLayout(self.confirmPasswordLayout)
        self.profileForm.setAlignment(self.confirmPasswordLayout, Qt.AlignCenter)

        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.deleteButton = QPushButton(FormStrings.DELETE_EDIT)
        self.deleteButton.clicked.connect(self.delete_add)
        self.deleteButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.deleteButton.setObjectName("DeleteEditButton")
        self.addButton = QPushButton(FormStrings.SAVE_EDIT)
        self.addButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.addButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.addButton.setObjectName("SaveEditButton")

        self.buttonsBox.addWidget(self.deleteButton, alignment=Qt.AlignLeft)
        self.buttonsBox.addWidget(self.addButton, alignment=Qt.AlignRight)

        self.profileForm.addLayout(self.buttonsBox)

        self.profileForm.setAlignment(self.buttonsBox, Qt.AlignCenter)

        self.innerLayout.addLayout(self.profileForm)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        name_field = LineEditCompositeFormField.LayoutAndRule(self.nameLayout, ValidationRule.Required())
        cf_field = LineEditCompositeFormField.LayoutAndRule(self.fiscalCodeLayout, ValidationRule.FiscalCode())
        email_field = LineEditCompositeFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        phone_field = LineEditCompositeFormField.LayoutAndRule(self.phoneLayout, ValidationRule.Phone())
        password_field = (LineEditCompositeFormField.Layout(self.passwordLayout))
        confirm_password_field = (LineEditCompositeFormField.Layout(self.confirmPasswordLayout))

        self.form_manager = FormManager()
        self.form_manager.add_fields(name_field, cf_field,
                                     email_field, phone_field, password_field, confirm_password_field)
        self.form_manager.add_submit_button(self.addButton, self.on_submit)

    # Esegue i controlli sulla password e crea un nuovo operaio
    def on_submit(self, form_data: dict[str, any]):
        print("Save_edit...")
        print(self.birthDatePicker.date)
        print(form_data)
        if self.passwordLayout.line_edit.text() is not None:
            if len(self.passwordLayout.line_edit.text()) > 6:
                if self.confirmPasswordLayout.line_edit.text() is not None:
                    if self.passwordLayout.line_edit.text() != self.confirmPasswordLayout.line_edit.text():
                        print("Le password non combaciano")
                        self.passwordLayout.error_label.setText(ValidationStrings.PASSWORD_CONFIRM_DIFFERENT)
                        self.passwordLayout.error_label.setHidden(False)
                        return
                else:
                    print("Conferma nuova password richiesta")
                    self.confirmPasswordLayout.error_label.setText(ValidationStrings.FIELD_REQUIRED)
                    self.confirmPasswordLayout.error_label.setHidden(False)
                    return
            else:
                print(self.newPassword)
                print("Il campo nuova password deve essere lungo almeno 6 caratteri.")
                self.passwordLayout.error_label.setText(ValidationStrings.MIN_PASSWORD_ERROR)
                self.passwordLayout.error_label.setHidden(False)
                return

        try:
            data = {
                "name": self.nameLayout.line_edit.text(),
                "birth_date": self.birthDatePicker.date.toString('dd/MM/yyyy'),
                "CF": self.fiscalCodeLayout.line_edit.text(),
                "phone": utility.PhoneFormatter().format(self.phoneLayout.line_edit.text()),
                "mail": self.emailLayout.line_edit.text(),
                "role": "worker"
            }
            self.new_worker_uid = self.controller.create_worker(data, self.passwordLayout.line_edit.text())
            self.close()
        except Exception as e:
            print(e)

    def closeEvent(self, a0):
        if self.new_worker_uid is not None:
            self.parent().open_edit_worker(self.new_worker_uid)

    # Chiude la finestra alla pressione di un bottone
    def delete_add(self):
        self.close()
