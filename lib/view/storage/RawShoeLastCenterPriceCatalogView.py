from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QInputDialog, QDialog, QMessageBox
from qfluentwidgets import FluentIconBase

from lib.firebaseData import Firebase
from lib.model.ShoeLastVariety import ShoeLastVariety, ProductType, Gender, ShoeLastType, PlasticType
from lib.repository.CashRegisterRepository import CashRegisterRepository
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.storage.StoredItemTradeView import StoredItemTradeView
from lib.widget.TableWidgets import PriceCatalogTableBuilder, SixColumnsHeaderSection, SixColumnsDataSection, \
    TitleAndSubtitleSection, HorizontalTreeSection, PriceCatalogTable, NamedTableItem
from res import Styles
from res.CustomIcon import CustomIcon


class RawShoeLastCenterPriceCatalogView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.PRICE):
        super().__init__("raw_shoe_last_center_price_list_view", parent_widget, svg_icon)

        # Controller
        #self.controller = PriceCatalogController()

        # Titolo e sottotitolo
        self.setTitleText("Listino prezzi centro abbozzi")
        self.setSubtitleText("Gli importi sono espressi in euro")

        self.sidebar_label = QLabel("Clicca su un importo per modificarlo")
        self.sidebar_label.setWordWrap(True)
        self.sidebar_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.sidebar_label)

        # Costruisco la tabella del listino prezzi usando un PriceListTableBuilder
        table_builder = PriceCatalogTableBuilder(self.central_frame)
        table_builder.add_sections(  # Aggiungo le sezioni che compongono il listino

            # Sezione 1 - Prezzi abbozzi
            TitleAndSubtitleSection("(1) Listino prezzi per gli abbozzi", "Prezzi per paio di abbozzi"),
            SixColumnsHeaderSection("PLASTICA", ["UOMO", "DONNA", "BAMBINO"],
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

        def update_price_catalog_view(message: Message):
            data = message.data()
            match message.event():
                case StorageRepository.Event.PRICE_CATALOG_INITIALIZED:
                    # Aggiorna l'intero listino
                    self.table.updateAllNamedItems(data)

        # Aggiorno i dati della tabella ogni volta che cambiano

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_price_catalog_view)
        #self.controller.observe_price_catalog(self.messageReceived.emit)

        """Temporaneo"""
        self.table.updateAllNamedItems(Firebase.database.child("storage/raw_shoe_last_center_price_list").get().val())

        # Connetto il segnale "itemClicked" allo slot "on_item_clicked"
        self.table.itemClicked.connect(self.on_item_clicked)

        # Imposta il testo mostrato nella sidebar
        self.sidebar_label.setText("Clicca su un importo del listino per acquistare abbozzi o vendere scarti")

        # Imposta la tabella nel layout centrale
        self.central_layout.addWidget(self.table)

    @pyqtSlot(QTableWidgetItem)
    def on_item_clicked(self, item: QTableWidgetItem):
        if isinstance(item, NamedTableItem):

            # Estrae il prezzo per acquisto
            price_per_purchase: float = PriceFormatter.unformat(item.text())

            # Estrae le caratteristiche dell'abbozzo dal nome dell'item
            name_parts = item.itemName.split("_")

            if name_parts[0] == "abbozzo":
                # Determina la varietà di forma
                shoe_last_variety: ShoeLastVariety = ShoeLastVariety(
                    ProductType.ABBOZZO, Gender(name_parts[2]), ShoeLastType(name_parts[3]),
                    PlasticType(int(name_parts[1][-1]))
                )

                # Determina la descrizione
                shoe_last_variety_description = shoe_last_variety.get_description()

                # Crea il Dialog di acquisto
                dialog = StoredItemTradeView.raw_shoe_last(
                    shoe_last_variety_description,
                    price_per_purchase,
                )

                # Mostra Dialog acquisto abbozzi
                if dialog.exec() == QDialog.Accepted:
                    purchased_quantity = dialog.value()
                    total_price = purchased_quantity * price_per_purchase

                    """Aggiorna la quantità in deposito"""

                    """Crea transazione (da modificare)"""
                    pair_string = "paio" if purchased_quantity == 1 else "paia"

                    CashRegisterRepository().create_transaction(
                        f"Acquisto \"{shoe_last_variety_description}\" "
                        f"({str(purchased_quantity)} {pair_string})", total_price * -1
                    )

            else:
                # Determina il tipo di plastica
                plastic_type: PlasticType = PlasticType(int(name_parts[1][-1]))

                """Controllare che ci siano scarti da vendere e in che quantità"""
                stored_waste_quantity = 16  # Esempio

                # Se non ci sono scarti immagazzinati di quel tipo di plastica
                if stored_waste_quantity == 0:
                    # Informa che non è possibile effettuare la vendita
                    QMessageBox.question(
                        self,
                        "Impossibile procedere con la vendita",
                        f"In magazzino non sono presenti scarti del tipo di plastica {str(plastic_type.value)}.",
                        QMessageBox.Ok
                    )

                else:

                    # Determina la descrizione
                    waste_description = f"Scarti di lavorazione in plastica tipo {str(plastic_type.value)}"

                    # Crea il dialog di vendita
                    dialog = StoredItemTradeView.waste(
                            waste_description,
                            price_per_purchase,
                    )

                    # Imposta la quantità massima vendibile e quella di default pari alla quantità immagazzinata
                    dialog.amount_spin_box.setMaximum(stored_waste_quantity)
                    dialog.amount_spin_box.setValue(stored_waste_quantity)
                    dialog.refresh_button.click()

                    # Mostra Dialog vendita scarti
                    if dialog.exec() == QDialog.Accepted:
                        sold_quantity = dialog.value()
                        total_price = sold_quantity * price_per_purchase

                        """Aggiorna la quantità in deposito"""

                        """Crea transazione (da modificare)"""
                        CashRegisterRepository().create_transaction(
                            f"Vendita \"Scarti di lavorazione in plastica tipo {str(plastic_type.value)}\" "
                            f"({str(sold_quantity)} kg)", total_price
                        )




