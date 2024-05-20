from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QFont
from PyQt5.QtWidgets import QLabel, QHeaderView, QVBoxLayout, QSizePolicy, QTreeWidgetItem

from lib.controller.ArticleController import ArticleController
from lib.model.Article import Article
from lib.model.Order import OrderState
from lib.model.ShoeLastVariety import ShoeLastVariety, Processing, Shoeing
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.utility.ObserverClasses import Message, Observer
from lib.utility.TableAdapters import SingleRowTableAdapter
from lib.utility.UtilityClasses import SerialNumberFormatter
from lib.view.main.SubInterfaces import SubInterfaceChildWidget, SubInterfaceWidget
from lib.widget.CustomPushButton import CustomPushButton
from lib.widget.Separators import VerticalSpacer
from lib.widget.TableWidgets import SingleRowStandardTable
from lib.widget.TreeWidgets import AutoResizableTreeWidget, DefaultFontTreeItemDelegate
from res.Dimensions import FontSize
from res.Strings import OrderStateStrings


class ArticleView(SubInterfaceChildWidget):

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.controller.detach_article_observer(self.observer)  # Rimuove l'osservatore dall'ordine

    def __init__(self, parent_widget: SubInterfaceWidget, article: Article):
        # Controller
        self.controller: ArticleController = ArticleController(article)

        # Inizializzo il widget di base
        super().__init__(f"article_{self.controller.get_article_serial()}_view", parent_widget, True)

        # Titolo e sottotitolo
        self.setTitleText(f"Articolo {self.controller.get_article_serial()}")
        self.hideSubtitle()

        # Titolo tabelle dettagli articolo
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.article_details_title = QLabel(f"Dettagli articolo {self.controller.get_article_serial()}")
        self.article_details_title.setFont(font)
        self.article_details_title.setContentsMargins(16, 16, 16, 8)

        # Prima tabella articolo
        self.article_table_main = SingleRowStandardTable(self.central_frame)
        self.article_table_adapter_main = ArticleMainDetailsAdapter(self.article_table_main)
        headers = ["Genere", "Taglia", "Tipo di forma", "Tipo di plastica", "Lavorazione", "Ferratura"]
        self.article_table_main.setHeaders(headers)
        self.article_table_adapter_main.setData(article.get_shoe_last_variety())

        # Seconda tabella articolo
        self.article_table_accessories = SingleRowStandardTable(self.central_frame)
        self.article_table_adapter_accessories = ArticleAccessoriesAdapter(self.article_table_accessories)
        headers = ["Bussola", "Seconda bussola", "Altri accessori"]
        self.article_table_accessories.setHeaders(headers)
        self.article_table_adapter_accessories.setData(article.get_shoe_last_variety())
        self.article_table_accessories.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.article_table_accessories.horizontalHeader().setStretchLastSection(True)
        self.article_table_accessories.setColumnWidth(0, 150)
        self.article_table_accessories.setColumnWidth(1, 150)

        # Titolo albero degli ordini dell'articolo
        self.tree_title_label = QLabel(f"Forme associate all'articolo {self.controller.get_article_serial()}")
        self.tree_title_label.setFont(font)
        self.tree_title_label.setContentsMargins(16, 16, 16, 8)

        # Albero delle forme dell'articolo
        self.tree_widget = AutoResizableTreeWidget(self.central_frame)
        self.tree_widget.setHeaderHidden(True)  # Nasconde gli header
        self.tree_widget.setItemDelegate(DefaultFontTreeItemDelegate(self.tree_widget))  # Personalizza gli item

        # Imposta la radice e gli elementi di secondo livello
        total_produced_shoe_lasts_item = QTreeWidgetItem(
            [],
            type=QTreeWidgetItem.DontShowIndicator)

        produced_shoe_lasts_item = QTreeWidgetItem(
            [f"Paia prodotte ({str(self.controller.get_article().get_produced_article_shoe_lasts())})"],
            type=QTreeWidgetItem.DontShowIndicatorWhenChildless)

        to_be_produced_shoe_lasts_item = QTreeWidgetItem(
            [],
            type=QTreeWidgetItem.DontShowIndicatorWhenChildless)

        # Aggiunge gli elementi di secondo livello alla radice
        total_produced_shoe_lasts_item.addChildren([produced_shoe_lasts_item, to_be_produced_shoe_lasts_item])

        # Inizializza il numero di paia di forme da produrre a zero
        to_be_produced_shoe_lasts: int = 0

        # Costruisce un ramo dell'albero per ogni ordine
        for order in self.controller.get_article_orders():
            # Base del ramo dell'ordine
            order_item = QTreeWidgetItem([""], type=QTreeWidgetItem.DontShowIndicatorWhenChildless)

            # Variabili utili
            quantity = order.get_quantity()
            first_product_serial = order.get_first_product_serial()
            last_product_serial = first_product_serial + quantity - 1

            match order.get_state():
                # Se le forme sono state già prodotte
                case OrderState.DELIVERED | OrderState.COMPLETED:
                    order_item.setText(0, f"Ordine {order.get_order_serial()} ({str(quantity)} paia - "
                                          f"da {SerialNumberFormatter.format(first_product_serial)} "
                                          f"a {SerialNumberFormatter.format(last_product_serial)})")

                    # Aggiunge una foglia per ogni paio di forme prodotte
                    for product_serial in range(first_product_serial, last_product_serial + 1):
                        order_item.addChild(
                            QTreeWidgetItem(
                                [f"Paio di forme \"{self.controller.get_article_serial()}-"
                                 f"{SerialNumberFormatter.format(product_serial)}\""],
                                type=QTreeWidgetItem.DontShowIndicator)
                        )

                    # Aggiunge il ramo dell'ordine all'albero
                    produced_shoe_lasts_item.addChild(order_item)

                # Se le forme sono da produrre o in produzione
                case OrderState.PROCESSING | OrderState.NOT_STARTED:
                    order_item.setText(0, f"Ordine {order.get_order_serial()} ({str(quantity)} paia)")

                    # Aggiorna la quantità di paia di forme da produrre
                    to_be_produced_shoe_lasts += quantity

                    # Aggiunge il ramo dell'ordine all'albero
                    to_be_produced_shoe_lasts_item.addChild(order_item)

        # Imposta il testo della radice e di un elemento di secondo livello
        total_produced_shoe_lasts_item.setText(0, f"Paia associate all'articolo ("
                                                  f"{str(to_be_produced_shoe_lasts +
                                                         + self.controller.get_produced_article_shoe_lasts())})")
        to_be_produced_shoe_lasts_item.setText(0,
                                               f"Paia da produrre ({str(to_be_produced_shoe_lasts)})")

        # Imposta la radice
        self.tree_widget.addTopLevelItem(total_produced_shoe_lasts_item)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.article_details_title)
        self.inner_central_layout.addWidget(self.article_table_main)
        self.inner_central_layout.addWidget(self.article_table_accessories)
        self.inner_central_layout.addWidget(self.tree_title_label)
        self.inner_central_layout.addWidget(self.tree_widget)
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addLayout(self.inner_central_layout)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))  # Costringe i widget in alto

        # Sidebar
        # Prima Label
        self.article_sidebar_label = QLabel("Comandi visibilità albero")

        # Primo pulsante
        self.default_visibility_button = CustomPushButton.white(text="Imposta visibilità predefinita")
        self.default_visibility_button.clicked.connect(lambda: [
            self.tree_widget.collapseAll(),
            total_produced_shoe_lasts_item.setExpanded(True)
        ])

        # Secondo pulsante
        self.expand_all_button = CustomPushButton.white(text="Espandi tutto")
        self.expand_all_button.clicked.connect(self.tree_widget.expandAll)

        # Terzo pulsante
        self.collapse_all_button = CustomPushButton.white(text="Comprimi tutto")
        self.collapse_all_button.clicked.connect(self.tree_widget.collapseAll)

        # Aggiungo i Widget al Layout
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(8)
        self.sidebar_layout.addWidget(self.article_sidebar_label, alignment=Qt.AlignHCenter)
        self.sidebar_layout.addWidget(self.default_visibility_button)
        self.sidebar_layout.addWidget(self.expand_all_button)
        self.sidebar_layout.addWidget(self.collapse_all_button)

        # Aggiorna l'altezza dell'albero
        total_produced_shoe_lasts_item.setExpanded(True)
        self.tree_widget.setMaximumHeight(99)
        self.tree_widget.setFixedWidth(400)

        # Callback per l'observer
        def update_order_view(message: Message):
            match message.event():
                case ArticlesRepository.Event.ARTICLE_PRODUCED_SHOE_LASTS_UPDATED:
                    pass

        # Imposta un observer per l'articolo
        self.observer: Observer = self.controller.observe_article(update_order_view)


class ArticleMainDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, shoe_last_variety: ShoeLastVariety) -> list[str]:
        return [
            shoe_last_variety.get_gender().value.capitalize(),
            shoe_last_variety.get_size(),
            shoe_last_variety.get_shoe_last_type().value.capitalize(),
            f"Tipo {str(shoe_last_variety.get_plastic_type().value)}",
            "Nessuna" if shoe_last_variety.get_processing() == Processing.NESSUNA
            else "Cuneo" if shoe_last_variety.get_processing() == Processing.CUNEO
            else f"Snodo {shoe_last_variety.get_processing().value}",
            "Nessuna" if shoe_last_variety.get_shoeing() == Shoeing.NESSUNA
            else "Tacco ferrato" if shoe_last_variety.get_shoeing() == Shoeing.TACCO_FERRATO
            else "Mezza ferrata" if shoe_last_variety.get_shoeing() == Shoeing.MEZZA_FERRATA
            else "Tutta ferrata"
        ]


class ArticleAccessoriesAdapter(SingleRowTableAdapter):
    def adaptData(self, shoe_last_variety: ShoeLastVariety) -> list[str]:
        accessories: str = ""

        if shoe_last_variety.get_numbering_heel():
            accessories += "Segno sul tallone, "
        if shoe_last_variety.get_numbering_lateral():
            accessories += "Segni laterali, "
        if shoe_last_variety.get_numbering_antineck():
            accessories += "Segno anticollo, "
        if shoe_last_variety.get_pivot_under_heel():
            accessories += "Perno sotto tallone, "
        if shoe_last_variety.get_iron_tip():
            accessories += "Punta ferrata, "
        if accessories:
            accessories = accessories[:-2]
        else:
            accessories = "Nessuno"

        return [
            shoe_last_variety.get_first_compass_type().value.capitalize(),
            shoe_last_variety.get_second_compass_type().value.capitalize(),
            accessories
        ]
