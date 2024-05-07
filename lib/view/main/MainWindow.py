# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QStackedWidget, QHBoxLayout, QLabel, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, qrouter)
from qframelesswindow import FramelessWindow, TitleBar

from lib.controller.MainController import MainController
from lib.firebaseData import Firebase
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.utility.ObserverClasses import Message
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.cashregister.CashRegisterView import CashRegisterView
from lib.view.machine.MachineListView import MachineListView
from lib.view.main.NavigationWidgets import CashRegisterAvailabilityNavigationWidget, RemovableNavigationWidget
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.order.OrderListView import OrderListView
from lib.view.pricecatalog.PriceCatalogView import PriceCatalogView
from lib.view.profile import AdminProfilePage, CustomerProfilePage
from lib.view.worker import WorkerProfilePage
from lib.view.worker.WorkerListView import WorkerListView
# from lib.view.storage.StoragePage import StoragePage
from res.CustomIcon import CustomIcon as CustomFIF


# Widget per la Title Bar
# noinspection PyPep8Naming
class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

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

        # Widget
        self.stackedWidget = QStackedWidget(self)

        # Inizializza il Layout principale
        self.initLayout()

        # Inizializzo la navigazione
        self.initNavigation()

        # Inizializzo la finestra
        self.initWindow()

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

        # Carica le voci del menù in base al tipo di utente
        self.setupNavigation()

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

    # Popola le tre sezioni del menù e finalizza la navigazione
    def setupNavigation(self):

        # Tipo di account
        user_role: str = Firebase.auth.currentUserRole()
        print("Tipo account: " + str(user_role))

        # Popolo il menù laterale di navigazione
        match user_role:
            case "customer":

                # Sezione Top
                self.insertSubInterface(2, CustomerProfilePage.ProfileWidget(self), 'Profilo')
                self.insertSubInterface(3, OrderListView(self), 'I tuoi ordini')
                self.insertSubInterface(4, PriceCatalogView(self), 'Listino prezzi')

                # Sezione Bottom
                # Informazioni sull'utente
                self.navigationInterface.insertItem(
                    index=1,
                    routeKey="user_info",
                    icon=FIF.INFO,
                    selectable=False,
                    text=f"Autenticato come\ncliente",
                    position=NavigationItemPosition.BOTTOM
                )

            case "worker":

                # Sezione Top
                self.insertSubInterface(2, WorkerProfilePage.ProfileWidget(self), 'Profilo')
                self.insertSubInterface(3, OrderListView(self), 'Lista ordini')
                self.insertSubInterface(4, SubInterfaceWidget('Magazzino', self, FIF.LIBRARY), 'Magazzino')
                self.insertSubInterface(5, MachineListView(self), 'Macchinari')

                # Sezione Bottom
                # Informazioni sull'utente
                self.navigationInterface.insertItem(
                    index=1,
                    routeKey="user_info",
                    icon=FIF.INFO,
                    selectable=False,
                    text=f"Autenticato come\ndipendente",
                    position=NavigationItemPosition.BOTTOM
                )

            case "admin":

                # Sezione Top
                self.insertSubInterface(2, AdminProfilePage.ProfileWidget(self), 'Profilo')
                self.insertSubInterface(3, OrderListView(self), 'Lista ordini')
                self.insertSubInterface(4, PriceCatalogView(self), 'Listino prezzi')
                # self.insertSubInterface(5, StoragePage(self), 'Magazzino')
                self.insertSubInterface(6, MachineListView(self), 'Macchinari')
                self.insertSubInterface(7, CashRegisterView(self), 'Registro di cassa')
                self.insertSubInterface(8, WorkerListView(self), 'Gestione dipendenti')

                # Sezione Bottom
                # Informazioni sulla disponibilità di cassa
                cash_register_availability_item: CashRegisterAvailabilityNavigationWidget = \
                    CashRegisterAvailabilityNavigationWidget(parent_widget=self, icon=CustomFIF.EURO, text="0,00")

                self.navigationInterface.insertWidget(
                    index=1,  # Inserito come primo elemento in lista
                    routeKey="cash_register_availability",
                    widget=cash_register_availability_item,
                    position=NavigationItemPosition.BOTTOM,
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
                self.navigationInterface.insertItem(
                    index=2,
                    routeKey="user_info",
                    icon=FIF.INFO,
                    selectable=False,
                    text=f"Autenticato come\namministratore",
                    position=NavigationItemPosition.BOTTOM
                )

            case "unauthenticated":
                return

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

        self.navigationInterface.setCurrentItem("Profilo")

        # Imposta la route key iniziale
        qrouter.setDefaultRouteKey(self.stackedWidget, "Profilo")

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

        # Gestisce il click su un elemento di navigazione rimuovibile
        def onRemovableSubInterfaceClicked(event):
            # Se il click è sul corpo principale dell'elemento
            if event.pos().x() < 155:
                self.switchTo(interface)

            # Se il click è sull'icona in fondo all'elemento, chiude l'interfaccia
            else:
                self.removeSubInterface(interface)

        removable_navigation_widget = RemovableNavigationWidget(self, interface.svg_icon, text)
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
        # Chiude gli stream di dati
        self.controller.close_streams()

        # Rimuove ed elimina i widget dello StackedWidget e le corrispondenti voci del menù
        for index in reversed(range(self.stackedWidget.count())):
            print("Rimuovo widget " + str(index))
            widget = self.stackedWidget.widget(index)
            self.removeSubInterface(widget)

        # Rimuove la voce del menù con informazioni sull'account
        self.navigationInterface.removeWidget("user_info")

    # Reimposta la navigazione
    def setup(self):
        # Imposta nuove interfacce di navigazione
        self.setupNavigation()

        # Apre gli stream di dati
        self.controller.open_streams()
