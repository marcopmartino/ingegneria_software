from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout

import lib.firebaseData as firebaseConfig

from lib.layout.QLabelLayout import QLabelLayout
from lib.mvc.profile.Controller.ProfileController import ProfileController
from res import Styles
from res.Strings import FormStrings, ProfileStrings


class ProfileWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Inizializzo una reference da una eventuale pagina di modifica, senza fare questo la pagina si chiuderebbe
        # appena aperta perché il garbage collector la eliminerebbe
        self.controller = ProfileController()

        data = self.controller.getData(firebaseConfig.currentUser['localId'])

        self.setObjectName("Profilo")
        self.setStyleSheet(Styles.PROFILE_PAGE)
        self.outerLayout = QHBoxLayout(self)
        self.innerLayout = QVBoxLayout(self)
        self.innerLayout.setSpacing(0)

        self.titleFrame = QFrame()
        self.titleFrame.setStyleSheet(Styles.PAGE_TITLE_FRAME)

        self.title = QVBoxLayout(self.titleFrame)
        self.title.setContentsMargins(10, 10, 0, 10)
        self.title.setSpacing(3)
        self.title.setObjectName("TitleVerticalBox")

        self.displayTitle = QLabel(ProfileStrings.PROFILE, self)
        self.displayTitle.setStyleSheet(Styles.LABEL_TITLE)
        self.displaySubtitle = QLabel(ProfileStrings.PROFILE_DETAILS, self)
        self.displaySubtitle.setStyleSheet(Styles.LABEL_SUBTITLE)

        self.title.addWidget(self.displayTitle)
        self.title.addWidget(self.displaySubtitle)

        self.pageSeparator = QFrame()
        self.pageSeparator.setFrameShape(QFrame.HLine)
        self.pageSeparator.setFrameShadow(QFrame.Raised)

        self.innerLayout.addWidget(self.titleFrame)
        self.innerLayout.setAlignment(self.titleFrame, Qt.AlignTop)
        self.innerLayout.addWidget(self.pageSeparator)

        self.profileInfo = QVBoxLayout()
        self.profileInfo.setContentsMargins(10, 10, 10, 10)
        self.profileInfo.setSpacing(15)
        self.profileInfo.setObjectName("ProfileInfo")

        self.nameLabel = QLabel(data['name'])
        self.nameLabel.adjustSize()
        self.nameLabel.setMinimumSize(450, 50)
        self.nameLabel.setStyleSheet(Styles.PROFILE_INFO_NAME)

        self.profileInfo.addWidget(self.nameLabel)
        self.profileInfo.setAlignment(self.nameLabel, Qt.AlignLeft)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Raised)
        self.separator.setMinimumSize(self.nameLabel.width(), 1)

        self.profileInfo.addWidget(self.separator)
        self.profileInfo.setAlignment(self.separator, Qt.AlignLeft)

        self.profileInfoTable = QVBoxLayout()
        self.profileInfoTable.setContentsMargins(0, 0, 1, 1)
        self.profileInfoTable.setSpacing(0)
        self.profileInfoTable.setAlignment(Qt.AlignLeft)
        self.profileInfoTable.setObjectName("ProfileInfoTable")

        self.emailLabel = QLabelLayout(FormStrings.EMAIL, firebaseConfig.currentUser['email'])
        self.phoneLayout = QLabelLayout(FormStrings.PHONE, data['phone'])
        self.birthDateLabel = QLabelLayout(FormStrings.BIRTH_DATE, data['birth_date'])
        self.CFNumberLayout = QLabelLayout(FormStrings.CF, data['CF'])

        self.profileInfoTable.addLayout(self.emailLabel)
        self.profileInfoTable.addLayout(self.phoneLayout)
        self.profileInfoTable.addLayout(self.CFNumberLayout)

        self.profileInfoTable.setAlignment(self.nameLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.emailLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.phoneLayout, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.birthDateLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.CFNumberLayout, Qt.AlignLeft)

        self.profileInfo.addLayout(self.profileInfoTable)
        self.profileInfo.setAlignment(self.profileInfoTable, Qt.AlignLeft)

        self.innerLayout.addLayout(self.profileInfo)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.outerLayout)
