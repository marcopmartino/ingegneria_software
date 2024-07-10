from __future__ import annotations

from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QMessageBox, QApplication, QSizePolicy
from qfluentwidgets import FluentIconBase

from lib.controller.ProfileController import ProfileController
from lib.model.Customer import Customer
from lib.model.Employee import Employee
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import SingleColumnTableAdapter
from lib.utility.UtilityClasses import DatetimeUtils
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.profile.EditCustomerView import EditCustomerView
from lib.view.profile.EditManagerView import EditManagerView
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from lib.utility.gui.widget.Separators import VerticalSpacer
from lib.utility.gui.widget.TableWidgets import SingleColumnStandardTable
from res import Styles
from lib.utility.gui.widget.CustomIcon import CustomIcon
from res.Strings import FormStrings, ProfileStrings


class ProfileView(SubInterfaceWidget):

    def __init__(self, parent_widget: QWidget,
                 table_adapter_class: type(ProfileTableAdapter),
                 svg_icon: FluentIconBase = CustomIcon.PROFILE):
        super().__init__("profile_view", parent_widget, svg_icon)

        # Controller
        self.controller = ProfileController()

        # Titolo e sottotitolo
        self.setTitleText("Profilo")
        self.setSubtitleText("Il tuo profilo utente")

        # Layout centrale
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        self.central_layout.setSpacing(15)
        self.central_layout.setObjectName("ProfileInfo")

        # Ruolo
        self.nameLabel = QLabel()
        self.nameLabel.adjustSize()
        self.nameLabel.setMinimumSize(450, 50)
        self.nameLabel.setStyleSheet(Styles.PROFILE_INFO_NAME)

        # Tabella con i dati dell'utente
        self.profileInfoTable = SingleColumnStandardTable(self.central_frame)
        self.profileInfoTable.setStyleSheet(Styles.PROFILE_TABLE)
        self.profileInfoTable.setObjectName("ProfileInfoTable")
        self.profileInfoTable.setFrameStyle(QFrame.Box)
        self.profileInfoTable.setShowGrid(True)
        self.profileInfoTable.verticalHeader().setFixedWidth(200)
        self.profileInfoTable.setColumnWidth(0, 400)
        self.profileInfoTable.setCellHeight(60)
        self.profileInfoTable.setFixedSize(600, 242)

        # TableAdapter
        self.tableAdapter = table_adapter_class(self.profileInfoTable, self.nameLabel)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.nameLabel, alignment=Qt.AlignLeft)
        self.inner_central_layout.addWidget(self.profileInfoTable, alignment=Qt.AlignLeft)
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addLayout(self.inner_central_layout)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))  # Costringe i widget in alto

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)

        # Label
        self.sidebarLabel = QLabel(self.sidebar_frame)
        self.sidebarLabel.setText("Operazioni profilo")

        # Layout con i pulsanti di modifica ed eliminazione
        self.buttonsLayout = QVBoxLayout()
        self.buttonsLayout.setContentsMargins(0, 4, 0, 8)
        self.buttonsLayout.setSpacing(8)
        self.buttonsLayout.setObjectName("ButtonsBox")

        # Pulsante di modifica
        self.editButton = CustomPushButton.cyan(text=ProfileStrings.EDIT_BUTTON)
        self.editButton.setObjectName("EditButton")

        # Pulsante di eliminazione
        self.deleteButton = CustomPushButton.orange(text=ProfileStrings.DELETE_BUTTON)
        self.deleteButton.clicked.connect(self.on_delete_button_clicked)
        self.deleteButton.setObjectName("DeleteButton")

        # Aggiunge i pulsanti al layout dei pulsanti
        self.buttonsLayout.addWidget(self.editButton)
        self.buttonsLayout.addWidget(self.deleteButton)

        # Aggiunge la Label e il layout del pulsanti al layout della sidebar
        self.sidebar_layout.addWidget(self.sidebarLabel)
        self.sidebar_layout.addLayout(self.buttonsLayout)

        # Callback per l'observer
        def update_profile_view(message: Message):
            match message.event():
                case UsersRepository.Event.USERS_INITIALIZED:
                    # Inizializza l'utente
                    self.controller.initialize_user()

                    # Imposta l'osservatore sul singolo utente anziché sulla repository
                    self.controller.detach_users_repository_observer(self.observer)
                    self.observer = self.controller.observe_user(self.messageReceived.emit)

                    # Inserisce i dati dell'utente nella tabella
                    self.tableAdapter.setData(self.controller.get_user())

                case UsersRepository.Event.USER_UPDATED:
                    # Aggiorna i dati nella tabella
                    self.tableAdapter.updateData(self.controller.get_user())

                case UsersRepository.Event.USER_DELETED:
                    # Informa che l'account è stato eliminato, e successivamente esegue il Logout
                    self.show_deletion_info_dialog()

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_profile_view)
        self.observer = self.controller.observe_users_repository(self.messageReceived.emit)

    # Callback eseguita al click sul pulsante di eliminazione dell'account
    def on_delete_button_clicked(self):
        self.show_confirm_deletion_dialog() if self.controller.can_delete_user() \
            else self.show_unable_to_delete_account_dialog()

    # Mostra un Dialog di conferma dell'eliminazione dell'utente
    def show_confirm_deletion_dialog(self):
        # Imposta e mostra una richiesta di conferma dell'eliminazione
        clicked_button = QMessageBox.question(
            self,
            "Conferma eliminazione account",
            (f"Sei sicuro di voler eliminare l'account?\n"
             f"L'operazione non è reversibile."),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, elimina l'utente e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.delete_user()

    # Mostra un Dialog per informare che l'account non può essere eliminato
    def show_unable_to_delete_account_dialog(self):
        # Imposta e mostra il dialog
        QMessageBox.question(
            self,
            "Impossibile eliminare account",
            (f"L'account non può essere eliminato poiché alcuni dei tuoi ordini "
             f"sono in lavorazione o in attesa di essere ritirati."),
            QMessageBox.Ok
        )

    # Mostra un Dialog che informa dell'eliminazione dell'utente
    def show_deletion_info_dialog(self):
        # Imposta e mostra il dialog
        QMessageBox.question(
            self,
            "Informazione eliminazione account",
            (f"L'account in uso è stato eliminato.\n"
             f"Verrai reindirizzato alla schermata di accesso."),
            QMessageBox.Ok
        )

        # Alla pressione del pulsante, chiude tutte le finestre di dialogo ed esegue il logout
        for window in QApplication.topLevelWidgets():
            if window.objectName() not in ("main_window", "access_window"):
                window.close()
        self.window().logout.emit()

    # Inizializza la classe con la visualizzazione del cliente
    @classmethod
    def customer(cls, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.PROFILE):
        # Inizializza la classe con un CustomerTableAdapter
        self = cls(parent_widget, CustomerProfileTableAdapter, svg_icon)

        # Imposta gli header della tabella
        self.profileInfoTable.setHeaders([
            FormStrings.EMAIL,
            FormStrings.PHONE,
            FormStrings.DELIVERY_ADDRESS,
            FormStrings.IVA_NUMBER
        ])

        # Imposta una callback per il pulsante di modifica
        self.editButton.clicked.connect(self.show_customer_edit_form)

        return self

    # Inizializza la classe con la visualizzazione da operaio
    @classmethod
    def worker(cls, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.PROFILE):
        # Inizializza la classe con un CustomerTableAdapter
        self = cls(parent_widget, EmployeeProfileTableAdapter, svg_icon)

        # Imposta gli header della tabella
        self.profileInfoTable.setHeaders([
            FormStrings.EMAIL,
            FormStrings.PHONE,
            FormStrings.BIRTH_DATE,
            FormStrings.CF
        ])

        # Nasconde la sidebar per impedire all'operaio di modificare o eliminare il proprio account
        self.hideSidebar()

        return self

    # Inizializza la classe con la visualizzazione da manager
    @classmethod
    def manager(cls, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.PROFILE):
        # Inizializza la classe con un EmployeeTableAdapter
        self = cls(parent_widget, EmployeeProfileTableAdapter, svg_icon)

        # Imposta gli header della tabella
        self.profileInfoTable.setHeaders([
            FormStrings.EMAIL,
            FormStrings.PHONE,
            FormStrings.BIRTH_DATE,
            FormStrings.CF
        ])

        # Imposta una callback per il pulsante di modifica
        self.editButton.clicked.connect(self.show_manager_edit_form)

        # Nasconde il pulsante per eliminare il proprio account
        self.deleteButton.setHidden(True)

        return self

    def show_customer_edit_form(self):
        EditCustomerView(self.controller).exec()

    def show_manager_edit_form(self):
        EditManagerView(self.controller).exec()


# Adattatore per la tabella del profilo
class ProfileTableAdapter(SingleColumnTableAdapter, ABC):

    def __init__(self, table: SingleColumnStandardTable, name_label: QLabel):
        super().__init__(table)
        self.name_label = name_label


# Adattatore per i dati di un cliente
class CustomerProfileTableAdapter(ProfileTableAdapter):

    def adaptData(self, customer: Customer) -> list[str]:
        # Imposta il testo di NameLabel
        self.name_label.setText(customer.get_company_name())

        return [
            customer.get_email(),
            customer.get_phone(),
            customer.get_delivery_address(),
            customer.get_IVA()
        ]


# Adattatore per i dati di un dipendente
class EmployeeProfileTableAdapter(ProfileTableAdapter):

    def adaptData(self, employee: Employee) -> list[str]:
        # Imposta il testo di NameLabel
        self.name_label.setText(employee.get_name())

        return [
            employee.get_email(),
            employee.get_phone(),
            DatetimeUtils.unformat_date(employee.get_birth_date()),
            employee.get_CF()
        ]
