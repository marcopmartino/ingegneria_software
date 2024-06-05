from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from qfluentwidgets import FluentIconBase, SearchLineEdit, CheckBox

from lib.controller.ArticleListController import ArticleListController
from lib.model.Article import Article
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.utility.ObserverClasses import Message
from lib.utility.TableAdapters import TableAdapter
from lib.utility.UtilityClasses import DatetimeUtils
from lib.utility.validation.FormManager import FormManager
from lib.utility.validation.ValidationRule import ValidationRule
from lib.view.article.ArticleView import ArticleView
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from lib.utility.gui.widget.TableWidgets import StandardTable, IntegerTableItem, DateTableItem
from res.CustomIcon import CustomIcon
from res.Dimensions import FontSize


class ArticleListView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.ARTICLE):
        super().__init__("article_list_view", parent_widget, svg_icon)

        # Controller
        self.controller = ArticleListController()

        # Titolo e sottotitolo
        self.setTitleText("Registro degli articoli")
        self.setSubtitleText("Clicca due volte su un articolo per visualizzare maggiori dettagli")

        # Sidebar
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(24)

        # Label per tabella vuota
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        self.empty_table_label = QLabel(self.central_frame)
        self.empty_table_label.setObjectName("empty_storage_label")
        self.empty_table_label.setText("Nessun articolo trovato, modificare i filtri")
        font.setBold(True)
        self.empty_table_label.setFont(font)

        # Label
        self.search_label = QLabel(self.sidebar_frame)
        self.search_label.setText("Cerca in base al seriale:")

        # SearchBox
        self.search_box = SearchLineEdit(self.sidebar_frame)
        self.search_box.setObjectName("searchbox_line_edit")
        self.search_box.setPlaceholderText("Cerca articolo")
        self.search_box.searchButton.setEnabled(False)
        self.search_box.setValidator(ValidationRule.Numbers().validator)
        self.search_box.setMaxLength(6)

        # Layout di ricerca con SearchBox
        self.search_box_layout = QVBoxLayout(self.sidebar_frame)
        self.search_box_layout.setContentsMargins(0, 0, 0, 0)
        self.search_box_layout.setSpacing(12)
        self.search_box_layout.addWidget(self.search_label)
        self.search_box_layout.addWidget(self.search_box)

        # Layout con il checkgroup
        self.checkgroup_layout = QVBoxLayout(self.sidebar_frame)
        self.checkgroup_layout.setSpacing(12)
        self.checkgroup_layout.setObjectName("checkgroup_layout")

        # Checkgroup Label
        font.setBold(False)
        self.checkgroup_label = QLabel(self.sidebar_frame)
        self.checkgroup_label.setObjectName("checkgroup_label")
        self.checkgroup_label.setText("Mostra solo articoli:")
        self.checkgroup_label.setFont(font)
        self.checkgroup_layout.addWidget(self.checkgroup_label)

        # CheckBox "Con paia prodotte"
        self.revenue_checkbox = CheckBox(self.sidebar_frame)
        self.revenue_checkbox.setObjectName("with_check_box")
        self.revenue_checkbox.setText("Con paia prodotte")
        self.revenue_checkbox.setChecked(True)
        self.checkgroup_layout.addWidget(self.revenue_checkbox)

        # CheckBox "Senza paia prodotte"
        self.spending_check_box = CheckBox(self.sidebar_frame)
        self.spending_check_box.setObjectName("without_check_box")
        self.spending_check_box.setText("Senza paia prodotte")
        self.spending_check_box.setChecked(True)
        self.checkgroup_layout.addWidget(self.spending_check_box)

        # Button "Aggiorna lista"
        self.refresh_button = CustomPushButton.white(self.sidebar_frame)
        self.refresh_button.setText("Aggiorna lista")
        self.refresh_button.clicked.connect(self.refresh_article_list)

        # Aggiungo i campi della form al layout della sidebar
        self.sidebar_layout.addLayout(self.search_box_layout)
        self.sidebar_layout.addLayout(self.checkgroup_layout)
        self.sidebar_layout.addWidget(self.refresh_button)

        # Form Manager
        self.form_manager = FormManager()
        self.form_manager.add_widget_fields(self.sidebar_frame)

        # Tabella
        self.table = StandardTable(self.central_frame)
        headers = ["Articolo", "Data creazione", "Paia prodotte"]
        self.table.setHeaders(headers)

        # Table Adapter
        self.table_adapter = ArticleListAdapter(self.table)
        self.table_adapter.setColumnItemClass(0, IntegerTableItem)  # Per un corretto ordinamento degli articoli
        self.table_adapter.setColumnItemClass(1, DateTableItem)  # Per un corretto ordinamento delle date
        self.table_adapter.setColumnItemClass(2, IntegerTableItem)  # Per un corretto ordinamento delle quantità
        self.table_adapter.onDoubleClick(self.show_article_details)

        def update_article_list_view(message: Message):
            data = message.data()
            match message.event():
                case ArticlesRepository.Event.ARTICLES_INITIALIZED:
                    self.table_adapter.setData(self.controller.filter_articles(self.form_manager.data(), *data))

                case ArticlesRepository.Event.ARTICLE_CREATED:
                    if len(self.controller.filter_articles(self.form_manager.data(), data)) != 0:
                        self.table_adapter.addData(data)

                case ArticlesRepository.Event.ARTICLE_PRODUCED_SHOE_LASTS_UPDATED:
                    self.table_adapter.updateDataColumns(data, [2])
            self.check_empty_table()

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_article_list_view)
        self.controller.observe_article_list(self.messageReceived.emit)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.empty_table_label, alignment=Qt.AlignJustify)

    def check_empty_table(self):
        if self.table.isEmpty():
            self.empty_table_label.setVisible(True)
            self.table.setVisible(False)
        else:
            self.empty_table_label.setVisible(False)
            self.table.setVisible(True)

    # Ritorna la lista di articoli filtrata
    def get_filtered_article_list(self) -> list[Article]:
        return self.controller.get_article_list(self.form_manager.data())

    # Aggiorna la lista degli articoli mostrata in tabella
    def refresh_article_list(self):
        self.table.clearSelection()
        self.table_adapter.setData(self.get_filtered_article_list())
        self.check_empty_table()

    # Mostra la schermata con i dettagli dell'articolo
    def show_article_details(self, article_serial: str):
        article_view = ArticleView(self, self.controller.get_article_by_id(article_serial))
        self.window().addRemovableSubInterface(article_view, text=f"Articolo {article_serial}")


class ArticleListAdapter(TableAdapter):
    def adaptData(self, article: Article) -> list[str]:
        return [article.get_article_serial(),
                DatetimeUtils.unformat_date(article.get_creation_date()),
                str(article.get_produced_article_shoe_lasts())
                ]
