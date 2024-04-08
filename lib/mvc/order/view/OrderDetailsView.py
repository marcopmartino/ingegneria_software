from __future__ import annotations

import traceback
from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout, QHeaderView, QGridLayout
from qfluentwidgets import PrimaryPushButton, StrongBodyLabel, BodyLabel

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.order.controller.OrderListController import OrderListController
from lib.mvc.order.model.Article import Article
from lib.mvc.order.model.Order import Order
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog
from lib.utility.ResourceManager import ResourceManager
from lib.widget.Separators import VerticalSpacer
from lib.utility.TableAdapters import SingleRowTableAdapter
from res import Colors
from res.Dimensions import FontSize, FontWeight
from res.Strings import OrderStateStrings


class OrderDetailsView(BaseWidget):

    def __init__(self, parent_widget: QWidget, order_id: str):
        super().__init__(f"order_{order_id}_view", parent_widget)
        self.controller = OrderListController()
        order = self.controller.get_order_by_id(order_id)
        article = order.article()

        # Titolo e sottotitolo
        self.setTitleText(f"Ordine {order_id}")
        self.hideSubtitle()

        # Titolo tabella dettagli ordine
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.order_details_title = QLabel(f"Dettagli ordine {order_id}")
        self.order_details_title.setFont(font)
        self.order_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli ordine
        self.order_table_adapter, self.order_table = OrderDetailsAdapter.autoSetup(self)
        headers = ["Articolo", "Data creazione", "Stato", "Quantità (paia)", "Prezzo (euro)"]
        self.order_table.setHeaders(headers)
        self.order_table_adapter.setData(order)

        # Titolo tabelle dettagli articolo
        self.article_details_title = QLabel(f"Dettagli articolo {article.article_serial}")
        self.article_details_title.setFont(font)
        self.article_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli articolo
        self.article_table_1_adapter, self.article_table_1 = ArticleMainDetailsAdapter.autoSetup(self)
        headers = ["Genere", "Taglia", "Tipo di forma", "Tipo di plastica", "Lavorazione", "Ferratura"]
        self.article_table_1.setHeaders(headers)
        self.article_table_1_adapter.setData(article)

        self.article_table_2_adapter, self.article_table_2 = ArticleAccessoriesAdapter.autoSetup(self)
        headers = ["Bussola", "Seconda bussola", "Altri accessori"]
        self.article_table_2.setHeaders(headers)
        self.article_table_2_adapter.setData(article)
        self.article_table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.article_table_2.horizontalHeader().setStretchLastSection(True)
        self.article_table_2.setColumnWidth(0, 150)
        self.article_table_2.setColumnWidth(1, 150)

        # Titolo tabelle dettagli cliente
        self.customer_details_title = QLabel(f"Dettagli cliente {order_id}")
        self.customer_details_title.setFont(font)
        self.customer_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli cliente
        ''' Aggiungere titolo e tabella dettagli cliente'''

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.order_details_title)
        self.inner_central_layout.addWidget(self.order_table)
        self.inner_central_layout.addWidget(self.article_details_title)
        self.inner_central_layout.addWidget(self.article_table_1)
        self.inner_central_layout.addWidget(self.article_table_2)
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
        state_labels_layout.setContentsMargins(0, 0, 0, 0)
        self.state_title_label = StrongBodyLabel(text="Stato attuale")
        self.state_description_label = BodyLabel()
        self.state_description_label.setWordWrap(True)
        state_labels_layout.addWidget(self.state_title_label)
        state_labels_layout.addWidget(self.state_description_label)

        self.next_state_button = PrimaryPushButton()
        self.next_state_button.clicked.connect(self.transition_to_next_state)

        self.modify_order_button = PrimaryPushButton(text="Modifica ordine")
        # self.modify_order_button.clicked.connect()

        self.delete_order_button = PrimaryPushButton(text="Annulla ordine")
        # self.delete_order_button.clicked.connect()

        self.order_completion_number_label = QLabel()
        font = QFont()
        font.setPointSize(FontSize.SUBTITLE)
        self.order_completion_number_label.setFont(font)

        self.order_completion_text_label = BodyLabel(text="paia completate")
        self.order_changes_info_label = BodyLabel()

        # Aggiungo i Widget al Layout
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.addWidget(self.order_progression_label)
        self.sidebar_layout.addLayout(self.order_states_layout)
        self.sidebar_layout.setAlignment(self.order_states_layout, Qt.AlignLeft)
        self.sidebar_layout.addLayout(state_labels_layout)

        # Stato dell'ordine
        match order.state:
            case OrderStateStrings.NOT_STARTED:
                self.state = OrderStateCreated(self)
            case OrderStateStrings.PROCESSING:
                self.state = OrderStateProcessing(self)
            case OrderStateStrings.COMPLETED:
                self.state = OrderStateCompleted(self)
            case _:
                self.state = OrderStateDelivered(self)

        # Imposta la sidebar
        self.setup_sidebar()

    # Imposta la sidebar in base allo stato
    def setup_sidebar(self):
        self.state.setup_sidebar()

    # Aggiorna la sidebar in base allo stato
    def update_sidebar(self):
        self.state.update_sidebar()

    # Esegue la transizione dell'ordine verso il nuovo stato
    def transition_to_next_state(self):
        self.state.transition_to_next_state()

    # Rimpiazza lo stato corrente con il nuovo stato "new_state"
    def change_state(self, new_state: OrderState):
        self.state = new_state

    def proceed_order_state(self):
        pass
        # self.controller.proceed() Aggiorna lo stato nel database

    def on_state_changed(self):
        self.transition_to_next_state()
        self.update_sidebar()


# Implementazione dello State pattern
# Classe astratta OrderState
class OrderState(ABC):
    def __init__(self, view: OrderDetailsView):
        self._view: OrderDetailsView = view
        self.__state_name_font: QFont = QFont()
        self.__state_name_font.setPointSize(FontSize.DEFAULT - 1)
        self.__state_name_font.setWeight(FontWeight.BOLD)
        self._checkmark_icon: callable = lambda: ResourceManager.icon_label("green_checkmark.png")
        self._yellow_pause: callable = lambda: ResourceManager.icon_label("yellow_pause.png")
        self._black_three_dots: callable = lambda: ResourceManager.icon_label("black_three_dots.png")
        self._black_right_arrow: callable = lambda: ResourceManager.icon_label("black_right_arrow.png",
                                                                               36, 24,
                                                                               Qt.IgnoreAspectRatio)

    def __new_state_label(self, text: str) -> QLabel:
        state_label = QLabel(text)
        state_label.setFont(self.__state_name_font)
        return state_label

    def __new_disabled_state_label(self, text: str) -> QLabel:
        state_label = self.__new_state_label(text)
        state_label.setStyleSheet("color: " + Colors.DARK_GREY)
        return state_label

    def _set_state_row(self, row: int, state_icon: callable, state_name: str):
        self._view.order_states_layout.addWidget(state_icon(), row, 1)
        if state_icon == self._yellow_pause:
            self._view.order_states_layout.addWidget(
                self.__new_disabled_state_label(state_name), row, 2, 1, 3, Qt.AlignLeft
            )
        else:
            self._view.order_states_layout.addWidget(
                self.__new_state_label(state_name), row, 2, 1, 3, Qt.AlignLeft
            )
            if state_icon == self._black_three_dots:
                self._view.order_states_layout.addWidget(self._black_right_arrow(), row, 0)

    def _update_state_row(self, row: int, state_icon: callable, state_name: str):
        self._view.order_states_layout.removeItem(self._view.order_states_layout.itemAtPosition(row, 1))
        self._view.order_states_layout.removeItem(self._view.order_states_layout.itemAtPosition(row, 2))
        self._set_state_row(row, state_icon, state_name)

    def transition_to_next_state(self):
        # noinspection PyArgumentList
        self._view.change_state(self._next_state_class(self._view))

    @abstractmethod
    def setup_sidebar(self):
        pass

    @abstractmethod
    def update_sidebar(self):
        pass

    @abstractmethod
    def _next_state_class(self) -> type(OrderState):
        pass


# Classi OrderState
class OrderStateCreated(OrderState):
    def __init__(self, view):
        super().__init__(view)

    def setup_sidebar(self):
        # Imposto gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._black_three_dots, OrderStateStrings.NOT_STARTED)
        self._set_state_row(2, self._yellow_pause, OrderStateStrings.COMPLETED)
        self._set_state_row(3, self._yellow_pause, OrderStateStrings.DELIVERED)

        # Imposto la descrizione dello stato
        self._view.state_description_label.setText("In attesa che la lavorazione abbia inizio")

    def update_sidebar(self):
        pass

    def _next_state_class(self) -> type(OrderState):
        return OrderStateProcessing


class OrderStateProcessing(OrderState):
    def __init__(self, view: OrderDetailsView):
        super().__init__(view)

    def setup_sidebar(self):
        # Imposto gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._set_state_row(2, self._black_three_dots, OrderStateStrings.PROCESSING)
        self._set_state_row(3, self._yellow_pause, OrderStateStrings.DELIVERED)

        # Imposto la descrizione dello stato
        self._view.state_description_label.setText("In attesa che l'ordine sia completato")

    def update_sidebar(self):
        self._update_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._update_state_row(2, self._black_three_dots, OrderStateStrings.PROCESSING)

    def _next_state_class(self) -> type(OrderState):
        return OrderStateCompleted


class OrderStateCompleted(OrderState):
    def __init__(self, view: OrderDetailsView):
        super().__init__(view)

    def setup_sidebar(self):
        # Imposto gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._set_state_row(2, self._checkmark_icon, OrderStateStrings.COMPLETED)
        self._set_state_row(3, self._black_three_dots, OrderStateStrings.WAITING_COLLECTION)

        # Imposto la descrizione dello stato
        self._view.state_description_label.setText("L'ordine è pronto per essere ritirato")

    def update_sidebar(self):
        self._update_state_row(2, self._checkmark_icon, OrderStateStrings.COMPLETED)
        self._update_state_row(3, self._black_three_dots, OrderStateStrings.WAITING_COLLECTION)

    def _next_state_class(self) -> type(OrderState):
        return OrderStateDelivered


class OrderStateDelivered(OrderState):
    def __init__(self, view: OrderDetailsView):
        super().__init__(view)

    def setup_sidebar(self):
        # Imposto gli stati
        self._set_state_row(0, self._checkmark_icon, OrderStateStrings.SENT)
        self._set_state_row(1, self._checkmark_icon, OrderStateStrings.STARTED)
        self._set_state_row(2, self._checkmark_icon, OrderStateStrings.COMPLETED)
        self._set_state_row(3, self._checkmark_icon, OrderStateStrings.DELIVERED)

        # Imposto la descrizione dello stato
        self._view.state_description_label.setText("L'ordine è stato consegnato")

    def update_sidebar(self):
        self._update_state_row(3, self._checkmark_icon, OrderStateStrings.DELIVERED)

    def transition_to_next_state(self):
        pass

    def _next_state_class(self) -> type(OrderState):
        pass


# TableAdapters
class OrderDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, order: Order) -> list[str]:
        return [
            order.article_serial,
            order.creation_date,
            order.state,
            str(order.quantity),
            PriceCatalog.format(order.price)
        ]


class ArticleMainDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, article: Article) -> list[str]:
        return [
            article.article_serial,
            article.gender.capitalize(),
            article.shoe_last_type.capitalize(),
            f"Tipo {str(article.plastic_type)}",
            "Nessuna" if article.processing == "nessuna"
            else "Cuneo" if article.processing == "cuneo"
            else f"Snodo {article.processing}",
            "Nessuna" if article.shoeing == "nessuna"
            else "Tacco ferrato" if article.processing == "tacco"
            else "Mezza ferrata" if article.shoeing == "mezza"
            else "Tutta ferrata"
        ]


class ArticleAccessoriesAdapter(SingleRowTableAdapter):
    def adaptData(self, article: Article) -> list[str]:
        accessories: str = ""

        if article.numbering_heel:
            accessories += "Segno sul tallone, "
        if article.numbering_lateral:
            accessories += "Segni laterali, "
        if article.numbering_antineck:
            accessories += "Segno anticollo, "
        if article.pivot_under_heel:
            accessories += "Perno sotto tallone, "
        if article.iron_tip:
            accessories += "Punta ferrata, "
        if accessories:
            accessories = accessories[:-2]
        else:
            accessories = "Nessuno"

        return [
            "Rinforzata" if article.reinforced_compass else "Standard",
            article.second_compass_type.capitalize(),
            accessories
        ]
