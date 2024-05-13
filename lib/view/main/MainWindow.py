# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QStackedWidget, QHBoxLayout, QLabel, QWidget
from qfluentwidgets import FluentIcon as FIF, InfoBar, InfoBarPosition
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, qrouter)
from qframelesswindow import FramelessWindow, TitleBar

from lib.controller.MainController import MainController
from lib.firebaseData import Firebase
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.article.ArticleListView import ArticleListView
from lib.view.cashregister.CashRegisterView import CashRegisterView
from lib.view.machine.MachineListView import MachineListView
from lib.view.main.MainWindowLoadingView import MainWindowLoadingView
from lib.view.main.NavigationWidgets import CashRegisterAvailabilityNavigationWidget, RemovableNavigationWidget
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.order.OrderListView import OrderListView
from lib.view.pricecatalog.PriceCatalogView import PriceCatalogView
from lib.view.profile.ProfileView import ProfileView
from lib.view.worker.WorkerListView import WorkerListView
# from lib.view.storage.StoragePage import StoragePage
from res.CustomIcon import CustomIcon as CustomFIF


# Widget per la Title Bar
# noinspection PyPep8Naming
class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # Stile
        self.setStyleSheet("background-color: white")

        # Inizializza e aggiunge l'icona
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # Inizializza e aggiunge il titolo
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertSpacing(2, 10)
        self.hBoxLayout.insertWidget(3, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.titleLabel.setObjectName('titleLabel')
        font = QFont()
        font.setPointSize(10)
        self.titleLabel.setFont(font)
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


# Finestra principale, che contiene sia il menù di navigazione sia i Widget associati alle singole voci
# noinspection PyPep8Naming
class MainWindow(FramelessWindow):
    logout = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Finestra
        self.setObjectName("main_window")

        # Controller
        self.controller = MainController()

        # Imposta la TitleBar
        self.setTitleBar(CustomTitleBar(self))

        # Layout orizzontale che contiene il menù (NavigationInterface) e la lista dei Widget associati (QStackedWidget)
        self.hBoxLayout = QHBoxLayout(self)

        # Pannello di navigazione
        self.navigationInterface = NavigationInterface(
            self,
            showReturnButton=True,
            showMenuButton=False,
            collapsible=True
        )

        # StackedWidget
        self.stackedWidget = QStackedWidget(self)

        # Inizializza la finestra di caricamento
        self.loading_window: MainWindowLoadingView = MainWindowLoadingView(self.controller)

        # Inizializza i segnali
        self.initSignals()

        # Inizializza il Layout principale
        self.initLayout()

        # Inizializzo la navigazione
        self.initNavigation()

        # Inizializzo la finestra
        self.initWindow()

    # Inizializza i segnali
    def initSignals(self):
        self.loading_window.initialization_completed.connect(self.show)
        self.logout.connect(Firebase.auth.sign_out)

    # Inizializza il layout che contiene il menù (NavigationInterface) e la lista dei Widget associati (QStackedWidget)
    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)  # Aggiungo il pannello di navigazione (Menù laterale)
        self.hBoxLayout.addWidget(self.stackedWidget)  # Aggiungo il Widget di visualizzazione delle varie schermate
        self.hBoxLayout.setStretchFactor(self.stackedWidget, 1)  # In questo modo sono i Widget a espandersi

        self.titleBar.raise_()

    # Inizializza la navigation aggiungendo i "pulsanti" sulla barra laterale e le relative interfacce
    def initNavigation(self):

        # Inizializza NavigationInterface
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)
        self.navigationInterface.panel.setExpandWidth(200)
        self.navigationInterface.panel.setFixedWidth(200)
        self.navigationInterface.resize(200, self.height())

        # Collega il cambiamento del widget visualizzato all'aggiornamento della voce del menù selezionata
        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)

        # Separatore tra sezioni Top e Scroll
        self.navigationInterface.addSeparator(NavigationItemPosition.TOP)

        # Separatore tra sezioni Scroll e Bottom
        self.navigationInterface.insertSeparator(0, NavigationItemPosition.BOTTOM)

        # Per mostrare correttamente i separatori
        self.navigationInterface.panel.setCollapsible(False)

    # Funzione per inizializzare la finestra (dimensione, titolo, logo e stile[dark/light])
    def initWindow(self):
        self.resize(1280, 720)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('Shoe LastFactory Manager')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    # Inserisce una voce del menù con informazioni sul ruolo dell'utente autenticato
    def insertUserInfoItem(self, text: str, index: int = 1):
        self.navigationInterface.insertItem(
            index=index,
            routeKey="user_info",
            icon=CustomFIF.USER_INFO,
            selectable=False,
            onClick=lambda: InfoBar.new(
                icon=CustomFIF.USER_INFO,
                title="Info utente",
                content=f"Stai usando l'applicazione come {text.lower()}",
                duration=3000,
                position=InfoBarPosition.BOTTOM,
                parent=self
            ),
            text=text,
            position=NavigationItemPosition.BOTTOM
        )

    # Finalizza l'impostazione del menù di navigazione
    def finalizeNavigation(self):
        # Sezione Bottom

        # Logout
        self.navigationInterface.addItem(
            routeKey="logout",
            icon=FIF.PAGE_LEFT,
            text="Logout",
            selectable=False,
            onClick=self.show_access_window,
            position=NavigationItemPosition.BOTTOM,
            tooltip="Logout"
        )

        self.navigationInterface.setCurrentItem("profile_view")

        # Imposta la route key iniziale
        qrouter.setDefaultRouteKey(self.stackedWidget, "profile_view")

    # Popola le tre sezioni del menù e finalizza la navigazione nel caso di un cliente autenticato
    def setup_customer_navigation(self):
        # Sezione Top
        self.insertSubInterface(2, ProfileView.customer(self), 'Profilo')
        self.insertSubInterface(3, OrderListView(self), 'I tuoi ordini')
        self.insertSubInterface(4, PriceCatalogView(self), 'Listino prezzi')

        # Sezione Bottom
        # Informazioni sull'utente
        self.insertUserInfoItem("Cliente")

    # Popola le tre sezioni del menù e finalizza la navigazione nel caso di un operaio autenticato
    def setup_worker_navigation(self):
        # Sezione Top
        self.insertSubInterface(2, ProfileView.worker(self), 'Profilo')
        self.insertSubInterface(3, OrderListView(self), 'Lista ordini')
        self.insertSubInterface(4, SubInterfaceWidget('Magazzino', self, FIF.LIBRARY), 'Magazzino')
        self.insertSubInterface(5, MachineListView(self), 'Macchinari')
        self.insertSubInterface(6, ArticleListView(self), 'Registro articoli')

        # Sezione Bottom
        # Informazioni sull'utente
        self.insertUserInfoItem("Dipendente")

    # Popola le tre sezioni del menù e finalizza la navigazione nel caso di un manager autenticato
    def setup_manager_navigation(self):
        # Sezione Top
        self.insertSubInterface(2, ProfileView.manager(self), 'Profilo')
        self.insertSubInterface(3, OrderListView(self), 'Lista ordini')
        self.insertSubInterface(4, PriceCatalogView(self), 'Listino prezzi')
        # self.insertSubInterface(5, StoragePage(self), 'Magazzino')
        self.insertSubInterface(6, MachineListView(self), 'Macchinari')
        self.insertSubInterface(7, ArticleListView(self), 'Registro articoli')
        self.insertSubInterface(8, CashRegisterView(self), 'Registro di cassa')
        self.insertSubInterface(9, WorkerListView(self), 'Gestione dipendenti')

        # Sezione Bottom
        # Informazioni sulla disponibilità di cassa
        cash_register_availability_item: CashRegisterAvailabilityNavigationWidget = \
            CashRegisterAvailabilityNavigationWidget(parent_widget=self, icon=CustomFIF.EURO, text="0,00")

        # Inserisce l'elemento con la disponibilità di cassa
        self.navigationInterface.insertWidget(
            index=1,  # Inserito come primo elemento in lista
            routeKey="cash_register_availability",
            widget=cash_register_availability_item,
            position=NavigationItemPosition.BOTTOM,
            onClick=lambda: InfoBar.new(
                icon=CustomFIF.EURO,
                title="Disponibilità di cassa",
                content=f"Indicatore della ricchezza di cui il formificio dispone",
                duration=3000,
                position=InfoBarPosition.BOTTOM,
                parent=self
            ),
        )

        # Callback che aggiorna il valore della disponibilità di cassa
        def update_cash_register_availability(message: Message):
            match message.event():
                case CashRegisterRepository.Event.CASH_AVAILABILITY_INITIALIZED | (
                CashRegisterRepository.Event.CASH_AVAILABILITY_UPDATED
                ):
                    data = message.data()
                    cash_register_availability_item.setText(PriceFormatter.format(data))
                    cash_register_availability_item.update()

        self.controller.observe_cash_register(update_cash_register_availability)

        # Informazioni sull'utente
        self.insertUserInfoItem("Manager", 2)

    # Funzione per aggiungere le pagine ai pulsanti della sidebar
    def addSubInterface(self,
                        interface: SubInterfaceWidget,
                        text: str = "Nuova interfaccia",
                        position: NavigationItemPosition = NavigationItemPosition.TOP):

        # Aggiunge l'interfaccia allo StackedWidget
        self.stackedWidget.addWidget(interface)

        # Aggiunge un elemento di navigazione alla NavigationInterface
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=interface.svg_icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    # Funzione per inserire le pagine ai pulsanti della sidebar
    def insertSubInterface(self,
                           index,
                           interface: SubInterfaceWidget,
                           text: str = "Nuova interfaccia",
                           position: NavigationItemPosition = NavigationItemPosition.TOP):

        # Aggiunge l'interfaccia allo StackedWidget
        self.stackedWidget.addWidget(interface)

        # Inserisce un elemento di navigazione nella NavigationInterface
        self.navigationInterface.insertItem(
            index=index,
            routeKey=interface.objectName(),
            icon=interface.svg_icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    # Aggiunge un'interfaccia rimuovibile
    def addRemovableSubInterface(self,
                                 interface: SubInterfaceWidget,
                                 text: str = "Nuova interfaccia"):

        # Aggiunge l'interfaccia allo StackedWidget
        self.stackedWidget.addWidget(interface)

        # Crea l'interfaccia rimuovibile
        removable_navigation_widget = RemovableNavigationWidget(self, interface.svg_icon, text)

        # Gestisce il click su un elemento di navigazione rimuovibile
        def onRemovableSubInterfaceClicked(event):
            # Se il click è sul corpo principale dell'elemento
            if event.pos().x() < 155:
                self.switchTo(interface)

            # Se il click è sull'icona in fondo all'elemento, chiude l'interfaccia
            else:
                self.removeSubInterface(interface)

        removable_navigation_widget.mousePressEvent = onRemovableSubInterfaceClicked  # Callback al click sull'elemento

        # Inserisce un elemento di navigazione nella NavigationInterface
        self.navigationInterface.insertWidget(
            index=0,  # Inserito come primo elemento in lista
            routeKey=interface.objectName(),
            widget=removable_navigation_widget,
            position=NavigationItemPosition.SCROLL,
            tooltip=text
        )

        self.switchTo(interface)

    # Rimuove un'interfaccia
    def removeSubInterface(self, interface: QWidget):
        print("Rimuovo widget " + interface.objectName())
        self.stackedWidget.removeWidget(interface)  # Rimuove l'interfaccia dallo StackedWidget
        print("Rimosso " + interface.objectName() + " dallo stack")
        self.navigationInterface.removeWidget(interface.objectName())  # Rimuove la voce del menù corrispondente
        print("Rimosso " + interface.objectName() + " dal menù")
        interface.close()
        interface.deleteLater()

    # Per la navigazione tra i Widget dello stack. Aggiorna sia l'interfaccia che la voce selezionata nel menù.
    def switchTo(self, widget):
        self.stackedWidget.setCurrentWidget(widget)

    # Eseguito dopo "switchTo", quando si naviga tra i Widget dello stack, per tenere uno storico della navigazione
    def onCurrentInterfaceChanged(self, index):
        # Controllo per prevenire un crash in caso in cui lo stack sia vuoto
        if index != -1:
            widget = self.stackedWidget.widget(index)  # Ottengo il widget alla posizione "index"
            self.navigationInterface.setCurrentItem(widget.objectName())  # Aggiorna la voce selezionata nel menù
            qrouter.push(self.stackedWidget, widget.objectName())  # Per salvare la voce selezionata

    # Mostra la schermata di accesso dopo aver effettuato il logout
    def show_access_window(self):
        self.logout.emit()
        print("Window changed")

    # Esegue il reset della navigazione
    def reset(self):
        # Esegue il reset delle repository
        self.controller.reset_repositories()

        # Rimuove ed elimina i widget dello StackedWidget e le corrispondenti voci del menù
        for index in reversed(range(self.stackedWidget.count())):
            print("Rimuovo widget " + str(index))
            widget = self.stackedWidget.widget(index)
            self.removeSubInterface(widget)

        # Rimuove la voce del menù con informazioni sull'account
        self.navigationInterface.removeWidget("user_info")

        # Rimuove la voce del menù con la disponibilità di cassa
        self.navigationInterface.removeWidget("cash_register_availability")

    # Reimposta la navigazione
    def setup(self):
        # Tipo di account
        user_role: str = Firebase.auth.currentUserRole()
        print("Tipo account: " + str(user_role))

        # Popolo il menù laterale, imposta le interfacce di navigazione, inizializza le repository
        match user_role:
            case "customer":
                self.controller.init_customer_repositories()
                self.setup_customer_navigation()
            case "worker":
                self.controller.init_worker_repositories()
                self.setup_worker_navigation()
            case "manager":
                self.controller.init_manager_repositories()
                self.setup_manager_navigation()
            case "unauthenticated":
                return

        # Imposta la schermata di caricamento e apre gli stream delle repository
        self.loading_window.setup()

        # Finalizza la navigazione
        self.finalizeNavigation()

        # Indica che il caricamento degli elementi grafici della MainWindow è stata completata
        self.loading_window.gui_widget.stop()




