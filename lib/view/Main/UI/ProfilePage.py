from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QFrame, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QTableWidget, \
    QGridLayout, QSpacerItem, QSizePolicy, QPushButton, QTableView
from firebase_admin import firestore

from lib.layout.QLabelLayout import QLabelLayout
from res import Styles
from lib.firebaseData import firebase


class ProfileWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        #db = firestore.database().child('users').child(firebase.auth.uid)
        #data = db.get()
        #print(data)

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

        self.displayTitle = QLabel("PROFILO", self)
        self.displayTitle.setStyleSheet(Styles.LABEL_TITLE)
        self.displaySubtitle = QLabel("Dettagli profilo", self)
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

        self.nomeLabel = QLabel("Nome azienda")
        self.nomeLabel.adjustSize()
        self.nomeLabel.setMinimumSize(450, 50)
        self.nomeLabel.setStyleSheet(Styles.PROFILE_INFO_NAME)

        self.profileInfo.addWidget(self.nomeLabel)
        self.profileInfo.setAlignment(self.nomeLabel, Qt.AlignLeft)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Raised)
        self.separator.setMinimumSize(self.nomeLabel.width(), 1)

        self.profileInfo.addWidget(self.separator)
        self.profileInfo.setAlignment(self.separator, Qt.AlignLeft)

        self.profileInfoTable = QVBoxLayout()
        self.profileInfoTable.setContentsMargins(0, 0, 1, 1)
        self.profileInfoTable.setSpacing(0)
        self.profileInfoTable.setAlignment(Qt.AlignLeft)
        self.profileInfoTable.setObjectName("ProfileInfoTable")

        self.emailLabel = QLabelLayout("Email", "azienda@mail.com")
        self.telefonoLabel = QLabelLayout("Telefono", "1234567890")
        self.indirizzoLabel = QLabelLayout("Indirizzo", "Via delle aziende 1")
        self.ivaLabel = QLabelLayout("Partita Iva", "86334519757")

        self.profileInfoTable.addLayout(self.emailLabel)
        self.profileInfoTable.addLayout(self.telefonoLabel)
        self.profileInfoTable.addLayout(self.indirizzoLabel)
        self.profileInfoTable.addLayout(self.ivaLabel)

        self.profileInfoTable.setAlignment(self.nomeLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.emailLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.telefonoLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.indirizzoLabel, Qt.AlignLeft)
        self.profileInfoTable.setAlignment(self.ivaLabel, Qt.AlignLeft)

        self.profileInfo.addLayout(self.profileInfoTable)
        self.profileInfo.setAlignment(self.profileInfoTable, Qt.AlignLeft)

        self.buttonsBox = QVBoxLayout()
        self.buttonsBox.setSpacing(13)
        self.buttonsBox.setObjectName("ButtonsBox")

        self.editButton = QPushButton("Modifica profilo")
        self.editButton.setStyleSheet(Styles.EDIT_BUTTON)
        self.editButton.setObjectName("EditButton")
        self.deleteButton = QPushButton("Elimina profilo")
        self.deleteButton.setStyleSheet(Styles.DELETE_BUTTON)
        self.deleteButton.setObjectName("DeleteButton")

        self.buttonsBox.addWidget(self.editButton, alignment=Qt.AlignCenter)
        self.buttonsBox.addWidget(self.deleteButton, alignment=Qt.AlignCenter)

        self.profileInfo.addLayout(self.buttonsBox)

        self.profileInfo.setAlignment(self.buttonsBox, Qt.AlignCenter)

        self.innerLayout.addLayout(self.profileInfo)
        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.outerLayout)
