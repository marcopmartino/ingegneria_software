from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QSizePolicy, QVBoxLayout
from qfluentwidgets import PrimaryPushButton

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.order.controller.OrderListController import OrderListController
from lib.mvc.order.model.Article import Article
from lib.mvc.order.model.Order import Order
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog
from lib.widget.Separators import VerticalSpacer
from lib.widget.TableWidgets import StandardTable, SingleRowTableAdapter
from res import Styles
from res.Dimensions import FontSize


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

        # Titolo tabelle dettagli cliente
        self.customer_details_title = QLabel(f"Dettagli cliente {order_id}")
        self.customer_details_title.setFont(font)
        self.customer_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli cliente
        ''' Aggiungere titolo e tabella dettagli cliente'''

        # Popola il layout centrale in modo da allineare i Widget in alto
        self.inner_central_widget = QWidget(self.central_frame)
        self.inner_central_layout = QVBoxLayout(self.inner_central_widget)
        self.inner_central_layout.addWidget(self.order_details_title)
        self.inner_central_layout.addWidget(self.order_table)
        self.inner_central_layout.addWidget(self.article_details_title)
        self.inner_central_layout.addWidget(self.article_table_1)
        self.inner_central_layout.addWidget(self.article_table_2)
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addWidget(self.inner_central_widget)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))


class OrderDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, order: Order) -> list[str]:
        return [
            order.article_serial,
            order.creation_date,
            order.state,
            str(order.quantity),
            PriceCatalog.price_format(order.price)
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
        return [
            "Rinforzata" if article.reinforced_compass else "Standard",
            article.second_compass_type.capitalize(),
            article.pivot_under_heel
        ]
