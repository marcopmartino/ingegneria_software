# coding:utf-8

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QStackedWidget, QHBoxLayout, QLabel, QWidget

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, qrouter, NavigationTreeWidget, FluentIconBase)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar

from lib.firebaseData import currentUserId, getUserRole
from lib.view.machine.MachineListView import MachineListView
from lib.view.pricecatalog.PriceCatalogView import PriceCatalogView
from lib.utility.ResourceManager import ResourceManager
from res.CustomIcon import CustomIcon as CustomFIF

from lib.model.CustomerDataManager import CustomerDataManager
from lib.model.StaffDataManager import StaffDataManager

from lib.view.main.BaseWidget import BaseWidget
from lib.view.worker.WorkerListView import WorkerListView
from lib.view.worker import WorkerProfilePage
from lib.view.profile import AdminProfilePage, CustomerProfilePage
from lib.view.order.OrderListView import OrderListView


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


# NavigationWidget rimuovibile
class RemovableNavigationWidget(NavigationTreeWidget):

    def __init__(self, parent_widget: QWidget, icon: str | QIcon | FluentIconBase, text: str):
        # Inizializza il NavigationWidget
        super().__init__(icon, text, True, parent_widget)

        # Carica l'icona per chiudere l'interfaccia corrispondente
        self.close_icon = ResourceManager.icon("close_icon.png")

    # Personalizza la grafica
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)  # Imposta la penna
        painter.setBrush(QBrush(self.close_icon))  # Imposta il pennello

        # Mentre il cursore è sulla voce del menù, mostra l'icona per chiudere l'interfaccia
        if self.isEnter:
            painter.translate(160, 6)  # Sposta il cursore del QPainter
            painter.drawEllipse(0, 0, 24, 24)  # Traccia l'icona


# Finestra principale, che contiene sia il menù di navigazione sia i Widget associati alle singole voci
# noinspection PyPep8Naming
class MainWindow(FramelessWindow):
    logout = pyqtSignal()

    def __init__(self):
        super().__init__()
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
        user_role: str = getUserRole()
        print("Tipo account: " + str(user_role))

        # Sezione Top
        match user_role:
            case "customer":
                CustomerDataManager().open_stream()
                self.insertSubInterface(2, CustomerProfilePage.ProfileWidget(self), FIF.PEOPLE, 'Profilo')
                self.insertSubInterface(3, OrderListView(self), FIF.DOCUMENT, 'Lista ordini')
                self.insertSubInterface(4, PriceCatalogView(self), FIF.DOCUMENT, 'Listino prezzi')
                self.insertSubInterface(5, MachineListView(self), CustomFIF.MACHINERY, 'Macchinari')

            case "admin":
                StaffDataManager().open_stream()
                self.insertSubInterface(2, AdminProfilePage.ProfileWidget(self), FIF.PEOPLE, 'Profilo')
                self.insertSubInterface(3, OrderListView(self), FIF.DOCUMENT, 'Lista ordini')
                self.insertSubInterface(4, PriceCatalogView(self), FIF.DOCUMENT, 'Listino prezzi')
                self.insertSubInterface(5, BaseWidget('Magazzino', self), FIF.LIBRARY, 'Magazzino')
                self.insertSubInterface(6, MachineListView(self), CustomFIF.MACHINERY, 'Macchinari')
                self.insertSubInterface(7, WorkerListView(self), CustomFIF.WORKER, 'Gestione dipendenti')

            case "worker":
                StaffDataManager().open_stream()
                self.insertSubInterface(2, WorkerProfilePage.ProfileWidget(self), FIF.PEOPLE, 'Profilo')
                self.insertSubInterface(3, OrderListView(self), FIF.DOCUMENT, 'Lista ordini')
                self.insertSubInterface(4, BaseWidget('Magazzino', self), FIF.LIBRARY, 'Magazzino')
                self.insertSubInterface(5, MachineListView(self), CustomFIF.MACHINERY, 'Macchinari')

            case "unauthenticated":
                return

        # Sezione Bottom

        # Informazioni sull'utente
        self.navigationInterface.insertItem(
            index=1,
            routeKey="user_info",
            icon=FIF.INFO,
            selectable=False,
            text=f"Autenticato come\n{currentUserId()}",
            position=NavigationItemPosition.BOTTOM
        )

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

        # !IMPORTANT: don't forget to set the default route key
        qrouter.setDefaultRouteKey(self.stackedWidget, "Profilo")
        self.navigationInterface.setCurrentItem("Profilo")

    # Funzione per aggiungere le pagine ai pulsanti della sidebar
    def addSubInterface(self,
                        interface: QWidget,
                        icon: str | QIcon | FluentIconBase = FIF.INFO,
                        text: str = "Nuova interfaccia",
                        position: NavigationItemPosition = NavigationItemPosition.TOP):

        # Aggiunge l'interfaccia allo StackedWidget
        self.stackedWidget.addWidget(interface)

        # Aggiunge un elemento di navigazione alla NavigationInterface
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    # Funzione per inserire le pagine ai pulsanti della sidebar
    def insertSubInterface(self,
                           index,
                           interface: QWidget,
                           icon: str | QIcon | FluentIconBase = FIF.INFO,
                           text: str = "Nuova interfaccia",
                           position: NavigationItemPosition = NavigationItemPosition.TOP):

        # Aggiunge l'interfaccia allo StackedWidget
        self.stackedWidget.addWidget(interface)

        # Inserisce un elemento di navigazione nella NavigationInterface
        self.navigationInterface.insertItem(
            index=index,
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    # Aggiunge un'interfaccia rimuovibile
    def addRemovableSubInterface(self,
                                 interface: QWidget,
                                 icon: str | QIcon | FluentIconBase = FIF.DOCUMENT,
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

        removable_navigation_widget = RemovableNavigationWidget(self, icon, text)
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
        if getUserRole() == 'customer':
            CustomerDataManager().close_stream()
        else:
            StaffDataManager().close_stream()
        print("Window changed")

    # Esegue il reset della navigazione
    def reset(self):
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
