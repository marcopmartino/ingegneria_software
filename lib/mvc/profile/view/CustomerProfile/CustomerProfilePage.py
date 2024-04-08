from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QWidget

import lib.firebaseData as firebaseConfig

from lib.layout.QLabelLayout import QLabelLayout
from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.profile.view.CustomerProfile.EditCustomerProfileWindow import EditProfileWindow
from lib.mvc.profile.controller.CustomerController import CustomerController

from res import Styles
from res.Strings import FormStrings, ProfileStrings


class ProfileWidget(BaseWidget):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__("user_profile_page", parent_widget)

        # Inizializzo una reference da una eventuale pagina di modifica, senza fare questo la pagina si chiuderebbe
        # appena aperta perché il garbage collector la eliminerebbe
        self.edit_window = None

        self.controller = CustomerController()

        self.setTitleText("Profilo")

        self.profileInfo = QVBoxLayout(self.central_frame)
        self.profileInfo.setContentsMargins(10, 10, 10, 10)
        self.profileInfo.setSpacing(15)
        self.profileInfo.setObjectName("ProfileInfo")

        self.companyNameLabel = QLabel()
        self.companyNameLabel.adjustSize()
        self.companyNameLabel.setMinimumSize(450, 50)
        self.companyNameLabel.setStyleSheet(Styles.PROFILE_INFO_NAME)

        self.profileInfo.addWidget(self.companyNameLabel)
        self.profileInfo.setAlignment(self.companyNameLabel, Qt.AlignLeft)

        self.emailLayout = QLabelLayout(FormStrings.EMAIL)
        self.phoneLayout = QLabelLayout(FormStrings.PHONE)
        self.deliveryAddressLayout = QLabelLayout(FormStrings.DELIVERY_ADDRESS)
        self.IVANumberLayout = QLabelLayout(FormStrings.IVA_NUMBER)

        self.profileInfoTable = QVBoxLayout()
        self.profileInfoTable.setContentsMargins(0, 0, 1, 1)
        self.profileInfoTable.setSpacing(0)
        self.profileInfoTable.setAlignment(Qt.AlignLeft)
        self.profileInfoTable.setObjectName("ProfileInfoTable")

        self.profileInfoTable.addLayout(self.emailLayout)
        self.profileInfoTable.addLayout(self.phoneLayout)
        self.profileInfoTable.addLayout(self.deliveryAddressLayout)
        self.profileInfoTable.addLayout(self.IVANumberLayout)

        self.profileInfoTable.setAlignment(self.emailLayout, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.phoneLayout, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.deliveryAddressLayout, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.IVANumberLayout, Qt.AlignLeft)

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
        self.deleteButton = QPushButton(ProfileStrings.DELETE_BUTTON)
        self.deleteButton.clicked.connect(self.open_delete_window)
        self.deleteButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteButton.setObjectName("DeleteButton")

        self.buttonsBox.addWidget(self.editButton, alignment=Qt.AlignCenter)
        self.buttonsBox.addWidget(self.deleteButton, alignment=Qt.AlignCenter)

        self.profileInfo.addLayout(self.buttonsBox)

        self.profileInfo.setAlignment(self.buttonsBox, Qt.AlignCenter)

        def update_data(data):
            self.companyNameLabel.setText(data.company)
            self.emailLayout.edit_text(FormStrings.EMAIL, data.email)
            self.phoneLayout.edit_text(FormStrings.PHONE, data.phone)
            self.deliveryAddressLayout.edit_text(FormStrings.DELIVERY_ADDRESS, data.delivery)
            self.IVANumberLayout.edit_text(FormStrings.IVA_NUMBER, data.IVA)

        update_data(self.controller.customer_data.get())

        self.controller.customer_data.observe(update_data)

        self.central_layout.addLayout(self.profileInfo)

    def open_edit_window(self):
        self.edit_window = EditProfileWindow(prevWindow=self)
        self.setEnabled(False)
        self.edit_window.show()

    def open_delete_window(self):
        pass

    def activateWindow(self):
        print(":)")
        self.update_data()
