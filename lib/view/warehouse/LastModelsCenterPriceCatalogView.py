from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QInputDialog, QDialog

from lib.firebaseData import Firebase
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.widget.TableWidgets import PriceCatalogTableBuilder, SixColumnsHeaderSection, SixColumnsDataSection, \
    TitleAndSubtitleSection, HorizontalTreeSection, PriceCatalogTable, NamedTableItem
from res import Styles


class LastModelsCenterPriceCatalogView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("price_list_view", parent_widget)

        # Controller
        #self.controller = PriceCatalogController()

        # Titolo e sottotitolo
        self.setTitleText("Listino prezzi centro abbozzi")
        self.setSubtitleText("Gli importi sono espressi in euro e si riferiscono al paio di forme")

        self.sidebar_label = QLabel("Clicca su un importo per modificarlo")
        self.sidebar_label.setWordWrap(True)
        self.sidebar_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.sidebar_label)

        # Costruisco la tabella del listino prezzi usando un PriceListTableBuilder
        table_builder = PriceCatalogTableBuilder(self.central_frame)
        table_builder.add_sections(  # Aggiungo le sezioni che compongono il listino

            # Sezione 1 - Prezzi abbozzi
            TitleAndSubtitleSection("(1) Listino prezzi per gli abbozzi", "Prezzi per paio di abbozzi"),
            SixColumnsHeaderSection("PLASTICA", ["UOMO (N.34/48)", "DONNA (N.34/44)", "BAMBINO (N.18/33)"],
                                    ["BASSA", "POLACCO"]),
            SixColumnsDataSection(["TIPO 1", "TIPO 2", "TIPO 3"],
                                  [
                                      ["abbozzo_tipo1_uomo_bassa", "abbozzo_tipo1_uomo_polacco",
                                       "abbozzo_tipo1_donna_bassa", "abbozzo_tipo1_donna_polacco",
                                       "abbozzo_tipo1_bambino_bassa", "abbozzo_tipo1_bambino_polacco"],
                                      ["abbozzo_tipo2_uomo_bassa", "abbozzo_tipo2_uomo_polacco",
                                       "abbozzo_tipo2_donna_bassa", "abbozzo_tipo2_donna_polacco",
                                       "abbozzo_tipo2_bambino_bassa", "abbozzo_tipo2_bambino_polacco"],
                                      ["abbozzo_tipo3_uomo_bassa", "abbozzo_tipo3_uomo_polacco",
                                       "abbozzo_tipo3_donna_bassa", "abbozzo_tipo3_donna_polacco",
                                       "abbozzo_tipo3_bambino_bassa", "abbozzo_tipo3_bambino_polacco"]
                                  ]),

            # Sezione 2 - Prezzi vendita scarti di lavorazione
            TitleAndSubtitleSection("(2) Vendita scarti in plastica", "Valore al chilogrammo"),
            HorizontalTreeSection("PLASTICA",
                                  ["TIPO 1", "TIPO 2", "TIPO 3"],
                                  ["scarti_tipo1", "scarti_tipo2", "scarti_tipo3"]
                                  )
        )

        # Costruisco una nuova PriceListTable "tracciando" le sezioni su di essa
        self.table: PriceCatalogTable = table_builder.build()

        # Metodo per aggiornare il listino prezzi ogni volta che ci sono cambiamenti al model
        def update_prices_callback(message):
            data: dict = message["data"]
            self.table.updateNamedItem(next(iter(data.keys())), next(iter(data.values())))

        # Aggiorno i dati della tabella ogni volta che cambiano
        self.controller.observe_price_catalog(update_prices_callback)

        # Aggiorna l'intero listino
        self.table.updateAllNamedItems(self.controller.get_price_catalog())

        # Connetto il segnale "itemClicked" allo slot "on_item_clicked"
        if Firebase.auth.currentUserRole() != "customer":
            self.table.itemClicked.connect(self.on_item_clicked)

        # Imposta la tabella nel layout centrale
        self.central_layout.addWidget(self.table)

    @pyqtSlot(QTableWidgetItem)
    def on_item_clicked(self, item: QTableWidgetItem):
        if isinstance(item, NamedTableItem):

            current_value = PriceFormatter.unformat(item.text())

            # Imposto il Dialog
            dialog = QInputDialog(self)
            dialog.setStyleSheet(Styles.DIALOG)
            dialog.setWindowTitle("Modifica Prezzo")
            dialog.setLabelText("Inserisci il prezzo (euro):")
            dialog.setInputMode(QInputDialog.DoubleInput)
            dialog.setDoubleValue(current_value)
            dialog.setDoubleRange(0.00, 100.00)
            dialog.setDoubleStep(0.5)
            dialog.setOkButtonText("Salva")
            dialog.setCancelButtonText("Indietro")

            # Eseguito solo se l'utente ha scelto di salvare la modifica
            if dialog.exec_() == QDialog.Accepted:
                # Prendo il valore
                new_value = dialog.doubleValue()

                # Aggiorno il valore se è diverso
                if new_value != current_value:
                    self.controller.update_price_list({item.itemName: new_value})