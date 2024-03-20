# coding:utf-8
import traceback

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, qrouter)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar

from lib.mvc.order.view.CreateOrderView import CreateOrderView
from lib.mvc.pricecatalog.view.PriceCatalogView import PriceCatalogView
from res.CustomIcon import CustomIcon as CustomFIF

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.profile.view.UserProfile import UserProfilePage
from lib.mvc.profile.view.WorkerProfile import WorkerProfilePage
from lib.mvc.order.view.OrderListView import OrderListView


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

    def __init__(self, tipo: str):
        self.tipo = tipo
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # Layout orizzontale che contiene il menù (NavigationInterface) e la lista dei Widget associati (QStackedWidget)
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showReturnButton=True, collapsible=False)
        self.navigationInterface.panel.setExpandWidth(200)
        self.navigationInterface.panel.setFixedWidth(200)
        self.navigationInterface.resize(25, self.height())
        self.stackedWidget = QStackedWidget(self)

        # create sub interface
        if self.tipo == 'user':
            self.profileInterface = UserProfilePage.ProfileWidget(self)
            self.orderListInterface = OrderListView(self)
            self.priceCatalogInterface = PriceCatalogView(self)
        else:
            self.profileInterface = WorkerProfilePage.ProfileWidget(self)
            self.orderListInterface = OrderListView(self)
            self.priceCatalogInterface = PriceCatalogView(self)
            self.storageInterface = BaseWidget('Magazzino', self)
            self.machineryInterface = BaseWidget('Macchinari', self)
            if self.tipo == 'admin':
                self.workerListInterface = BaseWidget('Gestione dipendenti', self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    # Inizializza il layout che contiene il menù (NavigationInterface) e la lista dei Widget associati (QStackedWidget)
    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackedWidget)
        self.hBoxLayout.setStretchFactor(self.stackedWidget, 1)  # In questo modo sono i Widget a espandersi

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    # Inizializza la navigation aggiungendo i "pulsanti" sulla barra laterale e le relative interfacce
    def initNavigation(self):

        self.addSubInterface(self.profileInterface, FIF.PEOPLE, 'Profilo')
        if self.tipo == 'admin':
            self.addSubInterface(self.workerListInterface, CustomFIF.WORKER, 'Gestione dipendenti')
        self.addSubInterface(self.orderListInterface, FIF.DOCUMENT, 'Lista ordini')
        if self.tipo == 'user':
            pass
        else:
            self.addSubInterface(self.storageInterface, FIF.LIBRARY, 'Magazzino')
            self.addSubInterface(self.machineryInterface, CustomFIF.MACHINERY, 'Macchinari')
        self.addSubInterface(self.priceCatalogInterface, FIF.DOCUMENT, 'Listino prezzi')

        # A fini di testing
        self.addSubInterface(CreateOrderView(), FIF.SEND, "Nuovo ordine")

        # !IMPORTANT: don't forget to set the default route key
        qrouter.setDefaultRouteKey(self.stackedWidget, self.profileInterface.objectName())

        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackedWidget.setCurrentIndex(0)

    # Funzione per inizializzare la finestra (dimensione, titolo, logo e stile[dark/light])
    def initWindow(self):
        self.resize(1008, 600)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('Shoe LastFactory Manager')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    # Funzione per aggiungere le pagine ai pulsanti della sidebar
    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        """ add sub interface """
        self.stackedWidget.addWidget(interface)
        print(interface.objectName())
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    # Per la navigazione tra i Widget dello stack. Aggiorna sia l'interfaccia che la voce selezionata nel menù.
    def switchTo(self, widget):
        self.stackedWidget.setCurrentWidget(widget)

    # Eseguito dopo "switchTo", quando si naviga tra i Widget dello stack, per tenere uno storico della navigazione
    def onCurrentInterfaceChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())  # Per salvare la voce selezionata
        qrouter.push(self.stackedWidget, widget.objectName())

    # Mostra la schermata di accesso dopo aver effettuato il logout
    def show_access_window(self):
        print("About to create AccessWindow")
        self.logout.emit()
        print("AccessWindow shown")
