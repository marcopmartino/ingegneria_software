from __future__ import annotations

from enum import Enum

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout, QMainWindow
from qfluentwidgets import IndeterminateProgressRing

from lib.controller.MainController import MainController
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.repository.Repository import Repository
from lib.repository.StorageRepository import StorageRepository
from lib.repository.UsersRepository import UsersRepository
from lib.utility.ObserverClasses import Message
from lib.utility.ResourceManager import ResourceManager
from res.Dimensions import FontSize


class LoadingWidget(QWidget):
    def __init__(self, parent: MainWindowLoadingView, text: str):
        super().__init__(parent)

        # Layout
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(16)

        # Widget
        self.__checkmark_icon = ResourceManager.icon_label("green_checkmark.png")
        self.__loading_animation = IndeterminateProgressRing(parent)
        self.__loading_animation.setFixedSize(24, 24)
        self.__loading_animation.setStrokeWidth(4)
        self.__label = QLabel(text)

        # Aggiunge i widget al layout
        self.layout.addWidget(self.__checkmark_icon)
        self.layout.addWidget(self.__loading_animation)
        self.layout.addWidget(self.__label, alignment=Qt.AlignVCenter)

    def start(self):
        self.__checkmark_icon.setHidden(True)
        self.__loading_animation.start()
        self.__loading_animation.setHidden(False)

    def stop(self):
        self.__loading_animation.setHidden(True)
        self.__loading_animation.stop()
        self.__checkmark_icon.setHidden(False)


class MainWindowLoadingView(QMainWindow):
    repository_initialized = pyqtSignal(LoadingWidget)
    initialization_completed = pyqtSignal()

    def __init__(self, controller: MainController):
        super().__init__()

        # Finestra
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(400)
        self.setContentsMargins(16, 16, 16, 16)

        # Controller
        self.controller: MainController = controller

        # Contatore dei Widget che stanno ancora caricando
        self.loading_widgets_counter: int = 0

        def on_repository_initialized(loading_widget: LoadingWidget):
            # Ferma l'animazione di caricamento
            loading_widget.stop()

            # Decrementa il contatore dei caricamenti ancora in corso
            self.loading_widgets_counter -= 1

            # Se tutti i caricamenti sono terminati, indica che l'inizializzazione è stata completata
            if self.loading_widgets_counter == 0:
                self.close()
                self.initialization_completed.emit()

        # Imposta uno slot per il segnale
        self.repository_initialized.connect(on_repository_initialized)

        # Widget centrale
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Layout
        self.layout = QVBoxLayout(widget)
        self.layout.setObjectName("layout")
        self.layout.setAlignment(Qt.AlignCenter)

        # Caricamento in corso
        self.loading_label = QLabel("Caricamento in corso, attendere...")
        font = QFont()
        font.setPointSize(FontSize.SUBTITLE)
        self.loading_label.setFont(font)
        self.layout.addWidget(self.loading_label)

        def init_loading_widget(text):
            # Crea un nuovo LoadingWidget
            loading_widget = LoadingWidget(self, text)

            # Aggiunge il layout al layout del genitore
            self.layout.addWidget(loading_widget)

            return loading_widget

        # Widget per il caricamento della finestra principale
        self.gui_widget = init_loading_widget("Interfaccia grafica")

        # Widget per il caricamento delle repository
        self.users_widget = init_loading_widget("Utenti")
        self.orders_widget = init_loading_widget("Ordini")
        self.price_catalog_widget = init_loading_widget("Listino prezzi")
        self.storage_widget = init_loading_widget("Magazzino")
        self.machines_widget = init_loading_widget("Macchinari")
        self.articles_widget = init_loading_widget("Registro articoli")
        self.cash_register_widget = init_loading_widget("Registro di cassa")
        self.transactions_widget = init_loading_widget("Transazioni")

    # Imposta la vista
    def setup(self):
        # Resetta il contatore
        self.loading_widgets_counter = 0

        # Ultima classe repository ritornata
        last_repository_class = None

        # Imposta un widget di caricamento
        def setup_loading_widget(
                loading_widget: LoadingWidget,
                repository_class: type(Repository),
                event: Enum,
                next_repository_class: Repository = None) -> bool:

            # Prende la repository
            repository = self.controller.get_repository(repository_class)

            # Se la repository è tra quelle da inizializzare, imposta il widget di caricamento
            setup: bool = repository is not None
            if setup:

                # Avvia l'animazione di caricamento
                loading_widget.start()

                # Incrementa il contatore dei widget che stanno caricando
                self.loading_widgets_counter += 1

                # Mostra il widget di caricamento
                loading_widget.setHidden(False)

                # Callback eseguita quando l'inizializzazione della repository ha termine
                def on_initialization_completed(message: Message):
                    if message.event() == event:

                        # Rimuove l'osservatore
                        repository.detach(observer)

                        # Indica alla classe che la repository è stata inizializzata
                        self.repository_initialized.emit(loading_widget)

                        # Avvia lo stream successivo
                        if next_repository_class is not None:
                            self.controller.get_repository(next_repository_class).open_stream()

                # Imposta un osservatore per la repository
                observer = repository.observe(on_initialization_completed)

                return setup

            # Altrimenti, nasconde il widget di caricamento
            else:
                loading_widget.setHidden(True)

        # Imposta i widget di caricamento
        if setup_loading_widget(
            self.cash_register_widget,
            CashRegisterRepository,
            CashRegisterRepository.Event.CASH_AVAILABILITY_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = CashRegisterRepository

        if setup_loading_widget(
            self.transactions_widget,
            CashRegisterRepository,
            CashRegisterRepository.Event.TRANSACTIONS_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = CashRegisterRepository

        if setup_loading_widget(
            self.articles_widget,
            ArticlesRepository,
            ArticlesRepository.Event.ARTICLES_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = ArticlesRepository

        if setup_loading_widget(
            self.storage_widget,
            StorageRepository,
            StorageRepository.Event.PRODUCTS_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = StorageRepository

        if setup_loading_widget(
            self.machines_widget,
            MachinesRepository,
            MachinesRepository.Event.MACHINES_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = MachinesRepository

        if setup_loading_widget(
            self.price_catalog_widget,
            PriceCatalogRepository,
            PriceCatalogRepository.Event.PRICE_CATALOG_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = PriceCatalogRepository

        if setup_loading_widget(
            self.orders_widget,
            OrdersRepository,
            OrdersRepository.Event.ORDERS_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = OrdersRepository

        if setup_loading_widget(
            self.users_widget,
            UsersRepository,
            UsersRepository.Event.USERS_INITIALIZED,
            last_repository_class
        ):
            last_repository_class = UsersRepository

        # Mostra la finestra al termine del setup
        self.show()

        # Avvio gli stream
        self.controller.get_repository(last_repository_class).open_stream()
