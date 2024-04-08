from PyQt5.QtCore import Qt, QDate

from lib.mvc.workerlist.controller.WorkerListController import WorkerListController

QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QLineEdit, QMainWindow, \
    QRadioButton

import lib.UtilityFunction as utility
from lib.layout.CustomDatePicker import CustomDatePicker
from lib.layout.LineEditLayouts import LineEditCompositeLayout
from lib.validation.FormField import LineEditCompositeFormField
from lib.validation.FormManager import FormManager
from lib.validation.ValidationRule import ValidationRule
from res import Styles, Dimensions
from res.Dimensions import LineEditDimensions, FontWeight
from res.Strings import FormStrings, Config, ValidationStrings, WorkerStrings


class EditWorkerWindow(QMainWindow):

    def __init__(self, prevWindow, uid, parent=None):
        super().__init__(parent=parent)

        self.uid = uid
        self.controller = WorkerListController()

        data = self.controller.getWorkerData(self.uid)

        self.prevWindow = prevWindow

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
        self.nameLayout = LineEditCompositeLayout(FormStrings.NAME, text=data['name'], parent_widget=self)
        self.profileForm.addLayout(self.nameLayout)
        self.profileForm.setAlignment(self.nameLayout, Qt.AlignCenter)

        # Campo input email
        self.emailLayout = LineEditCompositeLayout(FormStrings.EMAIL, text=data['mail'], parent_widget=self)
        self.emailLayout.line_edit.setEnabled(False)
        self.profileForm.addLayout(self.emailLayout)
        self.profileForm.setAlignment(self.emailLayout, Qt.AlignCenter)

        # Campo input telefono
        self.phoneLayout = LineEditCompositeLayout(FormStrings.PHONE, text=data['phone'], parent_widget=self)
        self.profileForm.addLayout(self.phoneLayout)
        self.profileForm.setAlignment(self.phoneLayout, Qt.AlignCenter)

        # Campo codice fiscale
        self.fiscalCodeLayout = LineEditCompositeLayout(FormStrings.CF, text=data['CF'], parent_widget=self)
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
        date = data['birth_date'].split('/')
        default_date = QDate()
        default_date.setDate(int(date[2]), int(date[1]), int(date[0]))
        self.birthDatePicker.setDate(default_date)

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

        self.radioBox = QHBoxLayout()
        self.radioBox.setSpacing(13)
        self.radioBox.setObjectName("ButtonsBox")

        self.workerRadio = QRadioButton(FormStrings.WORKER_TEXT, self)
        self.workerRadio.toggled.connect(lambda: self.btnState(self.workerRadio))
        self.adminRadio = QRadioButton(FormStrings.ADMIN_TEXT, self)
        self.adminRadio.toggled.connect(lambda: self.btnState(self.adminRadio))

        self.workerRadio.setChecked(True)

        self.radioBox.addWidget(self.workerRadio)
        self.radioBox.addWidget(self.adminRadio)

        self.profileForm.addLayout(self.radioBox)

        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.deleteButton = QPushButton(FormStrings.DELETE_EDIT)
        self.deleteButton.clicked.connect(self.delete_add)
        self.deleteButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.deleteButton.setObjectName("DeleteEditButton")
        self.editButton = QPushButton(FormStrings.SAVE_EDIT)
        self.editButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.editButton.setFixedWidth(Dimensions.GenericDimensions.MAX_BUTTON_WIDTH)
        self.editButton.setObjectName("SaveEditButton")

        self.buttonsBox.addWidget(self.deleteButton, alignment=Qt.AlignLeft)
        self.buttonsBox.addWidget(self.editButton, alignment=Qt.AlignLeft)

        self.profileForm.addLayout(self.buttonsBox)

        self.profileForm.setAlignment(self.buttonsBox, Qt.AlignCenter)

        self.innerLayout.addLayout(self.profileForm)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.outerWidget)

        name_field = LineEditCompositeFormField.LayoutAndRule(self.nameLayout, ValidationRule.Required())
        cf_field = LineEditCompositeFormField.LayoutAndRule(self.fiscalCodeLayout, ValidationRule.FiscalCode())
        email_field = LineEditCompositeFormField.LayoutAndRule(self.emailLayout, ValidationRule.Email())
        phone_field = LineEditCompositeFormField.LayoutAndRule(self.phoneLayout, ValidationRule.Phone())
        password_field = (LineEditCompositeFormField.Layout(self.passwordLayout))
        confirm_password_field = (LineEditCompositeFormField.Layout(self.confirmPasswordLayout))

        self.form_manager = FormManager()
        self.form_manager.add_fields(name_field, cf_field,
                                     email_field, phone_field, password_field, confirm_password_field)
        self.form_manager.add_submit_button(self.editButton, self.on_submit)

    # Funzione che gestisce l'interazione con i radio button
    def btnState(self, button):
        if button.text() == "Operario":
            if not button.isChecked():
                self.adminRadio.setChecked(False)
                self.workerRadio.setChecked(True)
        elif button.text() == "Manager":
            if not button.isChecked():
                self.workerRadio.setChecked(True)
                self.adminRadio.setChecked(False)

    # Esegue i controlli sulla password e crea un nuovo operaio
    def on_submit(self, form_data: dict[str, any]):
        print("Save_edit...")
        print(self.birthDatePicker.date)
        print(form_data)
        newPassword = ""
        print(self.passwordLayout.line_edit.text() != "")
        if self.passwordLayout.line_edit.text() != "":
            if len(self.passwordLayout.line_edit.text()) > 6:
                if self.confirmPasswordLayout.line_edit.text() != "":
                    if self.passwordLayout.line_edit.text() != self.confirmPasswordLayout.line_edit.text():
                        print("Le password non combaciano")
                        self.passwordLayout.error_label.setText(ValidationStrings.PASSWORD_CONFIRM_DIFFERENT)
                        self.passwordLayout.error_label.setHidden(False)
                        return
                    else:
                        newPassword = self.passwordLayout.line_edit.text()
                else:
                    print("Conferma nuova password richiesta")
                    self.confirmPasswordLayout.error_label.setText(ValidationStrings.FIELD_REQUIRED)
                    self.confirmPasswordLayout.error_label.setHidden(False)
                    return
            else:
                print(newPassword)
                print("Il campo nuova password deve essere lungo almeno 6 caratteri.")
                self.passwordLayout.error_label.setText(ValidationStrings.MIN_PASSWORD_ERROR)
                self.passwordLayout.error_label.setHidden(False)
                return

        try:

            data = {
                "name": self.nameLayout.line_edit.text(),
                "birth_date": self.birthDatePicker.date.toString('dd/MM/yyyy'),
                "CF": self.fiscalCodeLayout.line_edit.text(),
                "phone": utility.format_phone(self.phoneLayout.line_edit.text()),
                "mail": self.emailLayout.line_edit.text(),
                "role": "worker" if self.workerRadio.isChecked() else 'manager'
            }
            self.controller.setWorkerData(data, newPassword, uid=self.uid)
            self.close()
        except Exception as e:
            print(e)

    # Intercetta l'evento di chiusura della finestra e abilita la finestra precedente
    def closeEvent(self, event):
        self.prevWindow.setEnabled(True)

    # Chiude la finestra alla pressione di un bottone
    def delete_add(self):
        self.close()
