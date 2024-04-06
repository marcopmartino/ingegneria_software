from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget

import lib.firebaseData as firebaseConfig

from lib.layout.QLabelLayout import QLabelLayout
from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.profile.controller.ProfileController import ProfileController
from lib.mvc.profile.view.AdminProfile.EditAdminProfileWindow import EditAdminProfileWindow
from res import Styles
from res.Strings import FormStrings, ProfileStrings


class ProfileWidget(BaseWidget):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__("admin_profile_page", parent_widget)

        # Inizializzo una reference da una eventuale pagina di modifica, senza fare questo la pagina si chiuderebbe
        # appena aperta perché il garbage collector la eliminerebbe
        self.edit_window = None

        self.controller = ProfileController()

        temp_data = self.controller.getData()

        self.setTitleText("Profilo")

        self.profileInfo = QVBoxLayout(self.central_layout)
        self.profileInfo.setContentsMargins(10, 10, 10, 10)
        self.profileInfo.setSpacing(15)
        self.profileInfo.setObjectName("ProfileInfo")

        self.nameLabel = QLabel(temp_data['name'])
        self.nameLabel.adjustSize()
        self.nameLabel.setMinimumSize(450, 50)
        self.nameLabel.setStyleSheet(Styles.PROFILE_INFO_NAME)

        self.profileInfo.addWidget(self.nameLabel)
        self.profileInfo.setAlignment(self.nameLabel, Qt.AlignLeft)

        self.profileInfoTable = QVBoxLayout()
        self.profileInfoTable.setContentsMargins(0, 0, 1, 1)
        self.profileInfoTable.setSpacing(0)
        self.profileInfoTable.setAlignment(Qt.AlignLeft)
        self.profileInfoTable.setObjectName("ProfileInfoTable")

        self.emailLabel = QLabelLayout(FormStrings.EMAIL, firebaseConfig.currentUser['email'])
        self.phoneLayout = QLabelLayout(FormStrings.PHONE, temp_data['phone'])
        self.birthDateLabel = QLabelLayout(FormStrings.BIRTH_DATE, temp_data['birth_date'])
        self.CFNumberLayout = QLabelLayout(FormStrings.CF, temp_data['CF'])

        self.profileInfoTable.addLayout(self.CFNumberLayout)
        self.profileInfoTable.addLayout(self.emailLabel)
        self.profileInfoTable.addLayout(self.phoneLayout)
        self.profileInfoTable.addLayout(self.birthDateLabel)

        self.profileInfoTable.setAlignment(self.emailLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.phoneLayout, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.birthDateLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.CFNumberLayout, Qt.AlignLeft)

        self.profileInfo.addLayout(self.profileInfoTable)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Raised)
        self.separator.setMinimumSize(self.companyNameLabel.width(), 1)

        self.profileInfo.addWidget(self.separator)
        self.profileInfo.setAlignment(self.separator, Qt.AlignLeft)

        self.buttonsBox = QVBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.editButton = QPushButton(ProfileStrings.EDIT_BUTTON)
        self.editButton.clicked.connect(self.open_edit_window)
        self.editButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.editButton.setObjectName("EditButton")

        self.buttonsBox.addWidget(self.editButton, alignment=Qt.AlignCenter)

        self.profileInfo.addLayout(self.buttonsBox)

        self.profileInfo.setAlignment(self.buttonsBox, Qt.AlignCenter)

        def update_data(message: dict[str, any]):
            data = self.controller.staff_data.get()
            self.nameLabel.setText(data.name)
            self.emailLayout.labelData.setText(data.email)
            self.phoneLayout.labelData.setText(data.phone)
            self.birthDateLabel.labelData.setText(data.birthDate)
            self.IVANumberLayout.labelData.setText(data.CF)

        self.controller.staff_data.observe(update_data)

        self.central_layout.addLayout(self.profileInfo)

    def open_edit_window(self):
        self.edit_window = EditAdminProfileWindow(prevWindow=self)
        self.setEnabled(False)
        self.edit_window.show()

    def activateWindow(self):
        print(":)")
        self.update_data()
