from __future__ import annotations

from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCloseEvent
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout, QHeaderView, QGridLayout, QMessageBox
from qfluentwidgets import PrimaryPushButton, StrongBodyLabel, BodyLabel

from lib.controller.OrderController import OrderController
from lib.firebaseData import Firebase
from lib.model.Customer import Customer
from lib.model.Order import Order
from lib.repository.OrdersRepository import OrdersRepository
from lib.utility.ObserverClasses import Observer, Message
from lib.utility.ResourceManager import ResourceManager
from lib.utility.TableAdapters import SingleRowTableAdapter
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.article.ArticleView import ArticleMainDetailsAdapter, ArticleAccessoriesAdapter
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.view.order.EditOrderView import EditOrderView
from lib.widget.Separators import VerticalSpacer
from lib.widget.TableWidgets import SingleRowStandardTable
from res import Colors
from res.Dimensions import FontSize, FontWeight
from res.Strings import OrderStateStrings


class OrderView(SubInterfaceChildWidget):

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.controller.detach_order_observer(self.observer)  # Rimuove l'osservatore dall'ordine

    def __init__(self, parent_widget: SubInterfaceWidget, order: Order):

        # Controller
        self.controller: OrderController = OrderController(order)

        # Inizializzo il widget di base
        super().__init__(f"order_{self.controller.get_order_serial()}_view", parent_widget, True)

        # Titolo e sottotitolo
        self.setTitleText(f"Ordine {self.controller.get_order_serial()}")
        self.hideSubtitle()

        # Titolo tabella dettagli ordine
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.order_details_title = QLabel(f"Dettagli ordine {self.controller.get_order_serial()}")
        self.order_details_title.setFont(font)
        self.order_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli ordine
        self.order_table = SingleRowStandardTable(self.central_frame)
        self.order_table_adapter = OrderDetailsAdapter(self.order_table)
        headers = ["Articolo", "Data creazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]
        self.order_table.setHeaders(headers)
        self.order_table_adapter.setData(self.controller.get_order())

        # Titolo tabelle dettagli articolo
        self.article_details_title = QLabel(f"Dettagli articolo {self.controller.get_order_article_serial()}")
        self.article_details_title.setFont(font)
        self.article_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli articolo
        article = self.controller.get_order_article()

        # Prima tabella articolo
        self.article_table_main = SingleRowStandardTable(self.central_frame)
        self.article_table_adapter_main = ArticleMainDetailsAdapter(self.article_table_main)
        headers = ["Genere", "Taglia", "Tipo di forma", "Tipo di plastica", "Lavorazione", "Ferratura"]
        self.article_table_main.setHeaders(headers)
        self.article_table_adapter_main.setData(article)

        # Seconda tabella articolo
        self.article_table_accessories = SingleRowStandardTable(self.central_frame)
        self.article_table_adapter_accessories = ArticleAccessoriesAdapter(self.article_table_accessories)
        headers = ["Bussola", "Seconda bussola", "Altri accessori"]
        self.article_table_accessories.setHeaders(headers)
        self.article_table_adapter_accessories.setData(article)
        self.article_table_accessories.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.article_table_accessories.horizontalHeader().setStretchLastSection(True)
        self.article_table_accessories.setColumnWidth(0, 150)
        self.article_table_accessories.setColumnWidth(1, 150)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"

        # Aggiunge i widget comuni a tutti gli utenti
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.order_details_title)
        self.inner_central_layout.addWidget(self.order_table)
        self.inner_central_layout.addWidget(self.article_details_title)
        self.inner_central_layout.addWidget(self.article_table_main)
        self.inner_central_layout.addWidget(self.article_table_accessories)

        # I dettagli del cliente sono visibili ai soli dipendenti
        if Firebase.auth.currentUserRole() != "customer":

            # Dettagli cliente
            customer = self.controller.get_order_creator()

            # Se il cliente non ha cancellato il proprio account
            if customer is not None:
                # Titolo tabella dettagli cliente
                self.customer_details_title = QLabel(f"Dettagli cliente {customer.get_company_name()}")
                self.customer_details_title.setFont(font)
                self.customer_details_title.setContentsMargins(16, 16, 16, 8)

                # Prima tabella creatore ordine
                self.customer_details_table = SingleRowStandardTable(self.central_frame)
                self.customer_details_adapter = CustomerDetailsAdapter(self.customer_details_table)
                headers = ["Email", "Telefono"]
                self.customer_details_table.setHeaders(headers)
                self.customer_details_adapter.setData(customer)

                # Seconda tabella creatore ordine
                self.second_customer_details_table = SingleRowStandardTable(self.central_frame)
                self.second_customer_details_adapter = SecondCustomerDetailsAdapter(self.second_customer_details_table)
                headers = ["Indirizzo di recapito", "Partita IVA"]
                self.second_customer_details_table.setHeaders(headers)
                self.second_customer_details_adapter.setData(customer)

                # Aggiunge i widget al layout centrale
                self.inner_central_layout.addWidget(self.customer_details_title)
                self.inner_central_layout.addWidget(self.customer_details_table)
                self.inner_central_layout.addWidget(self.second_customer_details_table)

            # Altrimenti, se l'utente ha eliminato il proprio account
            else:
                # Titolo dettabli cliente
                self.customer_details_title = QLabel("Dettagli cliente")
                self.customer_details_title.setFont(font)
                self.customer_details_title.setContentsMargins(16, 16, 16, 8)

                # Label per informare che l'account cercato non esiste più
                self.deleted_account_info_label = QLabel(
                    "Il cliente che ha creato quest'ordine ha eliminato il proprio account")
                self.deleted_account_info_label.setContentsMargins(16, 0, 16, 8)

                # Aggiunge le Label al layout centrale
                self.inner_central_layout.addWidget(self.customer_details_title)
                self.inner_central_layout.addWidget(self.deleted_account_info_label)

        # Finalizza il layout centrale
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addLayout(self.inner_central_layout)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))  # Costringe i widget in alto

        # Sidebar
        # Progressione dell'ordine - Titolo della sidebar
        self.order_progression_label = QLabel("Progressione dell'ordine")

        # GridLayout che mostra la progressione dell'ordine
        self.order_states_layout = QGridLayout(self.sidebar_frame)
        self.order_states_layout.setVerticalSpacing(12)
        self.order_states_layout.setHorizontalSpacing(8)
        self.order_states_layout.setContentsMargins(0, 12, 0, 12)
        self.order_states_layout.setAlignment(Qt.AlignHCenter)

        # Informazioni sullo stato - Labels
        state_labels_layout = QVBoxLayout(self.sidebar_frame)
        state_labels_layout.setSpacing(0)
        state_labels_layout.setContentsMargins(0, 0, 0, 8)
        self.state_title_label = StrongBodyLabel(text="Stato attuale")
        self.state_description_label = BodyLabel()
        self.state_description_label.setWordWrap(True)
        state_labels_layout.addWidget(self.state_title_label)
        state_labels_layout.addWidget(self.state_description_label)

        # Pulsante per il passaggio di stato
        self.state_transition_button = PrimaryPushButton()
        self.state_transition_button.clicked.connect(self.transition_to_next_state)

        # Pulsante di modifica dell'ordine
        self.modify_order_button = PrimaryPushButton(text="Modifica ordine")
        self.modify_order_button.clicked.connect(self.show_order_form)

        # Pulsante di eliminazione dell'ordine
        self.delete_order_button = PrimaryPushButton(text="Annulla ordine")
        self.delete_order_button.clicked.connect(self.show_confirm_deletion_dialog)

        # Label sul completamento dell'ordine
        self.order_completion_number_label = QLabel(f"0/{str(self.controller.get_order().get_quantity())}")
        font = QFont()
        font.setPointSize(FontSize.SUBTITLE)
        self.order_completion_number_label.setFont(font)
        self.order_completion_text_label = BodyLabel(text="paia completate")
        self.order_completion_text_label.setContentsMargins(0, 0, 0, 8)

        # Widget e layout con le Label sul completamento dell'ordine
        self.order_completion_labels_widget = QWidget()
        order_completion_labels_layout = QVBoxLayout(self.order_completion_labels_widget)
        order_completion_labels_layout.setSpacing(0)
        order_completion_labels_layout.setContentsMargins(0, 0, 0, 0)
        order_completion_labels_layout.addWidget(self.order_completion_number_label, alignment=Qt.AlignHCenter)
        order_completion_labels_layout.addWidget(self.order_completion_text_label, alignment=Qt.AlignHCenter)
        self.order_completion_labels_widget.setLayout(order_completion_labels_layout)
        self.order_completion_labels_widget.setHidden(True)

        # Label di informazione sulla possibilità di modifica ed eliminazione dell'ordine
        self.order_changes_info_label = BodyLabel()
        self.order_changes_info_label.setWordWrap(True)
        self.order_changes_info_label.setContentsMargins(0, 8, 0, 16)

        # Aggiungo i Widget al Layout
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.addWidget(self.order_progression_label)
        self.sidebar_layout.addLayout(self.order_states_layout)
        self.sidebar_layout.setAlignment(self.order_states_layout, Qt.AlignLeft)
        self.sidebar_layout.addLayout(state_labels_layout)

        # Stato dell'ordine
        match self.controller.get_order_state():
            case OrderStateStrings.NOT_STARTED:
                self.state = OrderStateCreated(self)
            case OrderStateStrings.PROCESSING:
                self.state = OrderStateProcessing(self)
            case OrderStateStrings.COMPLETED:
                self.state = OrderStateCompleted(self)
            case OrderStateStrings.DELIVERED:
                self.state = OrderStateDelivered(self)

        # Imposta la sidebar
        self.setup_sidebar()

        # Callback per l'observer
        def update_order_view(message: Message):
            print(message.event())
            match message.event():
                case OrdersRepository.Event.ORDER_UPDATED:
                    # Aggiorna la tabella dell'ordine
                    self.order_table_adapter.updateDataColumns(self.controller.get_order(), [0, 3, 4])
                    # Aggiorna le tabelle dell'articolo
                    new_article = self.controller.get_order_article()
                    self.article_table_adapter_main.updateData(new_article)
                    self.article_table_adapter_accessories.updateData(new_article)

                case OrdersRepository.Event.ORDER_STATE_UPDATED:
                    # Aggiorna la tabella dell'ordine
                    self.order_table.columnItem(2).setText(self.controller.get_order_state())
                    # Aggiorna la sidebar
                    self.on_transition_to_next_state()
                    print("Stato aggiornato")

                case OrdersRepository.Event.ORDER_DELETED:
                    if order.get_customer_id() != Firebase.auth.currentUserId():
                        # Informa che il cliente ha eliminato l'ordine
                        self.show_deletion_info_dialog()

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_order_view)
        self.observer: Observer = self.controller.observe_order(self.messageReceived.emit)

    # Mostra un Dialog di conferma dell'eliminazione dell'ordine
    def show_confirm_deletion_dialog(self):

        # Imposta e mostra una richiesta di conferma dell'eliminazione
        clicked_button = QMessageBox.question(
            self,
            "Conferma eliminazione ordine",
            (f"L'ordine n° {self.controller.get_order_serial()} verrà annullato.\n"
             f"Sei sicuro di voler annullare l'ordine?"),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, elimina l'ordine e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.delete_order()
            self.window().removeSubInterface(self)

    # Mostra un Dialog che informa dell'eliminazione dell'ordine
    def show_deletion_info_dialog(self):
        # Imposta e mostra una richiesta di conferma dell'eliminazione
        QMessageBox.question(
            self,
            "Informazione eliminazione ordine",
            (f"L'ordine n° {self.controller.get_order_serial()} è stato annullato.\n"
             f"La finestra con i dettagli dell'ordine sarà chiusa."),
            QMessageBox.Ok
        )

        # Alla pressione del pulsante, chiude la finestra
        self.window().removeSubInterface(self)

    # Imposta la sidebar in base allo stato
    def setup_sidebar(self):
        self.state.setup_sidebar()

    # Aggiorna la sidebar in base allo stato
    def update_sidebar(self):
        self.state.update_sidebar()

    # Esegue la transizione dell'ordine verso il nuovo stato
    def transition_to_next_state(self):
        self.state.transition_to_next_state()

    # Eseguito dopo che l'ordine ha subito una transizione di stato (callback)
    def on_transition_to_next_state(self):
        self.state.on_transition_to_next_state()

    # Rimpiazza lo stato corrente con il nuovo stato "new_state"
    def change_state(self, new_state: OrderState):
        self.state = new_state

    # Mostra la form per la modifica dell'ordine
    def show_order_form(self):
        EditOrderView(self.controller).exec()


# Implementazione dello State pattern
# Classe astratta OrderState
class OrderState(ABC):
    STATE_NAME: str

    def __init__(self, view: OrderView):
        self._view: OrderView = view
        self.__state_name_font: QFont = QFont()
        self.__state_name_font.setPointSize(FontSize.DEFAULT - 1)
        self.__state_name_font.setWeight(FontWeight.BOLD)
        # Bisogna generare ogni volta una nuova icona per poterla mostrare più volte
        self._checkmark_icon: callable = lambda: ResourceManager.icon_label("green_checkmark.png")
        self._yellow_pause: callable = lambda: ResourceManager.icon_label("yellow_pause.png")
        self._black_three_dots: callable = lambda: ResourceManager.icon_label("black_three_dots.png")
        self._black_right_arrow: callable = lambda: ResourceManager.icon_label("black_right_arrow.png",
                                                                               36, 24,
                                                                               Qt.IgnoreAspectRatio)

    # Metodo privato per la creazione di una Label con il nome di uno stato
    def __new_state_label(self, text: str) -> QLabel:
        state_label = QLabel(text)
        state_label.setFont(self.__state_name_font)
        return state_label

    # Metodo privato per la creazione di una Label disabilitata (testo più chiaro) con il nome di uno stato
    def __new_disabled_state_label(self, text: str) -> QLabel:
        state_label = self.__new_state_label(text)
        state_label.setStyleSheet("color: " + Colors.DARK_GREY)
        return state_label

    # Imposta un riga del layout dello stato dell'ordine con icone e testo
    def _set_state_row(self, row: int, state_icon: callable, state_name: str):
        # Aggiunge l'icona alla riga "row" del layout, seconda colonna
        self._view.order_states_layout.addWidget(state_icon(), row, 1)

        # Se si tratta dell'icona di pausa (stato futuro), il testo viene aggiunto in una Label disabilitata
        if state_icon == self._yellow_pause:
            # Aggiunge il testo (nome dello stato) alla riga "row" del layout, terza colonna
            self._view.order_states_layout.addWidget(
                self.__new_disabled_state_label(state_name), row, 2, 1, 3, Qt.AlignLeft
            )
        # Altrimenti (stato attuale o passato), il testo viene aggiunto in una Label normale
        else:
            # Aggiunge il testo (nome dello stato) alla riga "row" del layout, terza colonna
            self._view.order_states_layout.addWidget(
                self.__new_state_label(state_name), row, 2, 1, 3, Qt.AlignLeft
            )
            # Se si tratta dell'icona con una freccia (stato attuale)...
            if state_icon == self._black_three_dots:
                # ...aggiunge suddetta icona alla riga "row" del layout, prima colonna
                self._view.order_states_layout.addWidget(self._black_right_arrow(), row, 0)

    # Aggiorna un riga del layout dello stato dell'ordine
    def _update_state_row(self, row: int, state_icon: callable, state_name: str):
        # Rimuove e nasconde gli item della riga "row"
        arrow_item = self._view.order_states_layout.itemAtPosition(row, 0)
        icon_item = self._view.order_states_layout.itemAtPosition(row, 1)
        text_item = self._view.order_states_layout.itemAtPosition(row, 2)

        if arrow_item is not None:
            self._view.order_states_layout.removeItem(arrow_item)
            arrow_item.widget().setHidden(True)

        self._view.order_states_layout.removeItem(icon_item)
        self._view.order_states_layout.removeItem(text_item)

        icon_item.widget().setHidden(True)
        text_item.widget().setHidden(True)

        # Imposta nuovamente la riga
        self._set_state_row(row, state_icon, state_name)

    @abstractmethod
    # Passa al prossimo stato dell'ordine
    def transition_to_next_state(self):
        self._view.state_transition_button.setEnabled(False)

    # Eseguito dopo che l'ordine è passato allo stato successivo
    def on_transition_to_next_state(self):
        self._view.state_transition_button.setEnabled(True)
        self._view.change_state(self._next_state_class()(self._view))
        self._view.update_sidebar()

    # Metodo per impostare la sidebar di una vista OrderView
    @abstractmethod
    def setup_sidebar(self):
        pass

    # Metodo per aggiornare la sidebar di una vista OrderView dopo un passaggio di stato
    @abstractmethod
    def update_sidebar(self):
        pass

    # Ritorna la classe del prossimo stato
    @abstractmethod
    def _next_state_class(self) -> type(OrderState):
        pass


# Classi OrderState
class OrderStateCreated(OrderState):
    STATE_NAME: str = OrderStateStrings.NOT_STARTED

    def __init__(self, view):
        super().__init__(view)

    # Passa al prossimo stato dell'ordine
    def transition_to_next_state(self):
        super().transition_to_next_state()
        self._view.controller.start_order()

    def setup_sidebar(self):
        # Imposta gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._black_three_dots, OrderStateStrings.NOT_STARTED)
        self._set_state_row(2, self._yellow_pause, OrderStateStrings.COMPLETED)
        self._set_state_row(3, self._yellow_pause, OrderStateStrings.DELIVERED)

        # Imposto la descrizione dello stato
        self._view.state_description_label.setText("In attesa che la lavorazione abbia inizio")

        match Firebase.auth.currentUserRole():
            case "customer":
                # Aggiunge i pulsanti di modifica e annullamento dell'ordine al layout
                self._view.sidebar_layout.addWidget(self._view.modify_order_button)
                self._view.sidebar_layout.addWidget(self._view.delete_order_button)

                # Aggiunge la Label di info sulla modifica e sull'annullamento dell'ordine al layout
                self._view.sidebar_layout.addWidget(self._view.order_changes_info_label)
                self._view.order_changes_info_label.setText(
                    "Sarà possibile modificare o annullare l'ordine solo finché la lavorazione non avrà inizio."
                )
            case "manager":
                # Aggiunge il pulsante per mettere l'ordine in lavorazione
                self._view.sidebar_layout.addWidget(self._view.state_transition_button)
                self._view.state_transition_button.setText("Metti in lavorazione")

    # Non esegue nessuna operazione perché non vi è uno stato precedente
    def update_sidebar(self):
        pass

    def _next_state_class(self) -> type(OrderState):
        return OrderStateProcessing


class OrderStateProcessing(OrderState):
    STATE_NAME: str = OrderStateStrings.PROCESSING

    def __init__(self, view: OrderView):
        super().__init__(view)

    # Passa al prossimo stato dell'ordine
    def transition_to_next_state(self):
        super().transition_to_next_state()
        self._view.controller.complete_order()

    def setup_sidebar(self):
        # Imposta gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._set_state_row(2, self._black_three_dots, OrderStateStrings.PROCESSING)
        self._set_state_row(3, self._yellow_pause, OrderStateStrings.DELIVERED)

        # Imposta la descrizione dello stato
        self._view.state_description_label.setText("In attesa che l'ordine sia completato")

        match Firebase.auth.currentUserRole():
            case "customer":
                # Aggiunge i pulsanti (disabilitati) di modifica e annullamento dell'ordine al layout
                self._view.sidebar_layout.addWidget(self._view.modify_order_button)
                self._view.sidebar_layout.addWidget(self._view.delete_order_button)
                self._view.modify_order_button.setEnabled(False)
                self._view.delete_order_button.setEnabled(False)

                # Aggiunge la Label di info sulla modifica e sull'annullamento dell'ordine al layout
                self._view.sidebar_layout.addWidget(self._view.order_changes_info_label)
                self._view.order_changes_info_label.setText(
                    "Non è più possibile modificare o annullare l'ordine poiché la lavorazione è iniziata"
                )
            case "worker" | "manager":
                # Aggiunge le Label con le informazioni sul completamento dell'ordne
                self._view.sidebar_layout.addWidget(self._view.order_completion_labels_widget)

                # Aggiunge il pulsante per il passaggio al prossimo stato
                self._view.sidebar_layout.addWidget(self._view.state_transition_button)
                self._view.state_transition_button.setText("Completa ordine")

                # Mostra le Label di completamento dell'ordine
                self._view.order_completion_labels_widget.setHidden(False)

    def update_sidebar(self):
        # Aggiorna gli stati
        self._update_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._update_state_row(2, self._black_three_dots, OrderStateStrings.PROCESSING)

        # Aggiorna la descrizione dello stato
        self._view.state_description_label.setText("In attesa che l'ordine sia completato")

        match Firebase.auth.currentUserRole():
            case "customer":
                # Disabilita i pulsanti di modifica e di eliminazione dell'ordine
                self._view.modify_order_button.setEnabled(False)
                self._view.delete_order_button.setEnabled(False)

                # Aggiorna la Label di info sulla modifica e sull'annullamento dell'ordine al layout
                self._view.order_changes_info_label.setText(
                    "Non è più possibile modificare o annullare l'ordine poiché la lavorazione è iniziata"
                )
            case "worker":
                # Aggiunge le Label con le informazioni sul completamento dell'ordne
                self._view.sidebar_layout.addWidget(self._view.order_completion_labels_widget)

                # Aggiorna il testo del pulsante per il passaggio al prossimo stato
                self._view.state_transition_button.setText("Completa ordine")

                # Aggiunge il pulsante per il passaggio al prossimo stato
                self._view.sidebar_layout.addWidget(self._view.state_transition_button)

                # Mostra le Label di completamento dell'ordine
                self._view.order_completion_labels_widget.setHidden(False)
            case "manager":
                # Aggiunge le Label con le informazioni sul completamento dell'ordine
                self._view.sidebar_layout.insertWidget(
                    self._view.sidebar_layout.count() - 1,  # Viene aggiunta prima del pulsante (penultima posizione)
                    self._view.order_completion_labels_widget
                )

                # Aggiorna il testo del pulsante per il passaggio al prossimo stato
                self._view.state_transition_button.setText("Completa ordine")

                # Mostra le Label di completamento dell'ordine
                self._view.order_completion_labels_widget.setHidden(False)

    def _next_state_class(self) -> type(OrderState):
        return OrderStateCompleted


class OrderStateCompleted(OrderState):
    STATE_NAME: str = OrderStateStrings.COMPLETED

    # Passa al prossimo stato dell'ordine
    def transition_to_next_state(self):
        super().transition_to_next_state()
        self._view.controller.deliver_order()

    def __init__(self, view: OrderView):
        super().__init__(view)

    def setup_sidebar(self):
        # Imposta gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._set_state_row(2, self._checkmark_icon, OrderStateStrings.COMPLETED)
        self._set_state_row(3, self._black_three_dots, OrderStateStrings.WAITING_COLLECTION)

        # Imposta la descrizione dello stato
        self._view.state_description_label.setText("L'ordine è pronto per essere ritirato")

        match Firebase.auth.currentUserRole():
            case "manager":
                # Aggiunge il pulsante per il passaggio al prossimo stato
                self._view.sidebar_layout.addWidget(self._view.state_transition_button)

                # Aggiorna il testo del pulsante per il passaggio al prossimo stato
                self._view.state_transition_button.setText("Conferma consegna ordine")

    def update_sidebar(self):

        # Aggiorna gli stati
        self._update_state_row(2, self._checkmark_icon, OrderStateStrings.COMPLETED)
        self._update_state_row(3, self._black_three_dots, OrderStateStrings.WAITING_COLLECTION)

        # Aggiorna la descrizione dello stato
        self._view.state_description_label.setText("L'ordine è pronto per essere ritirato")

        match Firebase.auth.currentUserRole():
            case "customer":
                # Nasconde i pulsanti di modifica e di eliminazione dell'ordine
                self._view.modify_order_button.setHidden(True)
                self._view.delete_order_button.setEnabled(True)

                # Nasconde la Label di info sulla modifica e sull'annullamento dell'ordine al layout
                self._view.order_changes_info_label.setHidden(True)
            case "worker":
                # Nasconde il widget con le Label di info sul completamento dell'ordine
                self._view.order_completion_labels_widget.setHidden(True)

                # Nasconde il pulsante per il passaggio al prossimo stato
                self._view.state_transition_button.setHidden(True)

            case "manager":
                # Nasconde il widget con le Label di info sul completamento dell'ordine
                self._view.order_completion_labels_widget.setHidden(True)

                # Aggiorna il testo del pulsante per il passaggio al prossimo stato
                self._view.state_transition_button.setText("Conferma consegna ordine")

    def _next_state_class(self) -> type(OrderState):
        return OrderStateDelivered


class OrderStateDelivered(OrderState):
    STATE_NAME: str = OrderStateStrings.DELIVERED

    def __init__(self, view: OrderView):
        super().__init__(view)

    def setup_sidebar(self):
        # Imposta gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._set_state_row(2, self._checkmark_icon, OrderStateStrings.COMPLETED)
        self._set_state_row(3, self._checkmark_icon, OrderStateStrings.DELIVERED)

        # Imposta la descrizione dello stato
        self._view.state_description_label.setText("L'ordine è stato consegnato")

    def update_sidebar(self):
        # Aggiorna gli stati
        self._update_state_row(3, self._checkmark_icon, OrderStateStrings.DELIVERED)

        # Aggiorna la descrizione dello stato
        self._view.state_description_label.setText("L'ordine è stato consegnato")

        match Firebase.auth.currentUserRole():
            case "manager":
                self._view.state_transition_button.setHidden(True)

    def transition_to_next_state(self):
        pass

    def _next_state_class(self) -> type(OrderState):
        pass


# TableAdapters
class OrderDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, order: Order) -> list[str]:
        return [
            order.get_article_serial(),
            order.get_creation_date(),
            order.get_state(),
            str(order.get_quantity()),
            PriceFormatter.format(order.get_price())
        ]


class CustomerDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, customer: Customer) -> list[str]:
        return [
            customer.get_email(),
            customer.get_phone(),
        ]


class SecondCustomerDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, customer: Customer) -> list[str]:
        return [
            customer.get_delivery_address(),
            customer.get_IVA(),
        ]
