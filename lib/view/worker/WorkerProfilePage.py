from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

from lib.controller.ProfileController import ProfileController
from lib.layout.QLabelLayout import QLabelLayout
from res import Styles
from res.Strings import FormStrings


class ProfileWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Inizializzo una reference da una eventuale pagina di modifica, senza fare questo la pagina si chiuderebbe
        # appena aperta perché il garbage collector la eliminerebbe
        self.edit_window = None

        self.controller = ProfileController()
        self.controller.open_staff_stream()

        self.setTitleText("Profilo")

        self.profileInfo = QVBoxLayout(self.central_layout)
        self.profileInfo.setContentsMargins(10, 10, 10, 10)
        self.profileInfo.setSpacing(15)
        self.profileInfo.setObjectName("ProfileInfo")

        self.nameLabel = QLabel()
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

        self.emailLabel = QLabelLayout(FormStrings.EMAIL)
        self.phoneLayout = QLabelLayout(FormStrings.PHONE)
        self.birthDateLabel = QLabelLayout(FormStrings.BIRTH_DATE)
        self.CFNumberLayout = QLabelLayout(FormStrings.CF)

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

        def update_data(data):
            for key, value in data.items():
                match key:
                    case 'name':
                        self.nameLabel.setText(value)
                    case 'mail':
                        self.emailLayout.edit_text(value)
                    case 'phone':
                        self.phoneLayout.edit_text(value)
                    case 'birthDate':
                        self.birthDateLabel.edit_text(value)
                    case 'CF':
                        self.CFNumberLayout.edit_text(value)

        self.controller.set_staff_observer(update_data)

        self.central_layout.addLayout(self.profileInfo)
