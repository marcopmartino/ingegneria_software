from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QInputDialog, QDialog

from lib.utility.UtilityClasses import PriceFormatter
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.widget.TableWidgets import PriceCatalogTableBuilder, SixColumnsHeaderSection, SixColumnsDataSection, \
    TitleAndSubtitleSection, HorizontalTreeSection, PriceCatalogTable, NamedTableItem
from res import Styles


class BlockCenterPriceCatalogView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("price_list_view", parent_widget)

        # Controller
        # self.controller = WarehouseController()

        # Titolo e sottotitolo
        self.setTitleText("Listino prezzi ferramenta")
        self.setSubtitleText("Gli importi sono espressi in euro")

        self.sidebar_label = QLabel("Clicca su un importo per modificarlo")
        self.sidebar_label.setWordWrap(True)
        self.sidebar_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.sidebar_label)

        # Costruisco la tabella del listino prezzi usando un PriceListTableBuilder
        table_builder = PriceCatalogTableBuilder(self.central_frame)
        table_builder.add_sections(  # Aggiungo le sezioni che compongono il listino

            # Sezione 0 - Header e Sotto-header della tabella
            TitleAndSubtitleSection("Materiale per settore calzaturiero",
                                    "Valore per le quantità indicate tra parentesi"),

            # Sezione 1 - Bussole
            HorizontalTreeSection("BUSSOLE",
                                  ["BUSSOLA STANDARD (x20)", "BUSSOLA STANDARD (x50)", "BUSSOLA STANDARD (x100)",
                                   "BUSSOLA RINFORZATA (x20)", "BUSSOLA RINFORZATA (x50)", "BUSSOLA RINFORZATA (x100)"],
                                  ["bussola_standard_20", "bussola_standard_50", "bussola_standard_100",
                                   "bussola_rinforzata_20", "bussola_rinforzata_50", "bussola_rinforzata_100"],
                                  grey_rows={3, 4, 5}
                                  ),

            # Sezione 2 - Prezzi per ferratura
            HorizontalTreeSection("PARTI PER FERRATURA",
                                  ["PIASTRA SOTTILE CORTA (x10)", "PIASTRA SOTTILE CORTA (x50)",
                                   "PIASTRA SOTTILE MEDIA (x10)", "PIASTRA SOTTILE MEDIA (x50)",
                                   "PIASTRA SOTTILE LUNGA (x10)", "PIASTRA SOTTILE LUNGA (x50)",
                                   "PIASTRA PER PUNTA FERRATA (x20)"],
                                  ["piastra_corta_10", "piastra_corta_50"
                                   "piastra_media_10", "piastra_media_50"
                                   "piastra_lunga_10", "piastra_lunga_50"
                                   "piastra_punta_20"],
                                  grey_rows={2, 3, 6}
                                  ),

            # Sezione 3 - Altro
            HorizontalTreeSection("ALTRO",
                                  ["INCHIOSTRO INDELEBILE (1L)", "INCHIOSTRO INDELEBILE (10L)",
                                   "PERNO (x20)", "PERNO (x50)",
                                   "MOLLA PER CUNEO (x20)",
                                   "GUSCIO PER SNODO ALFA (x20)",
                                   "GUSCIO PER SNODO TENDO (x20)"],
                                  ["inchiostro_1", "inchiostro_10",
                                   "perno_20", "perno_50",
                                   "molla_cuneo", "guscio_alfa", "guscio_tendo"],
                                  grey_rows={2, 3, 5}
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
