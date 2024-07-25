from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QInputDialog, QDialog, QLabel
from qfluentwidgets import FluentIconBase

from lib.firebaseData import Firebase
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.utility.ErrorHelpers import ConnectionErrorHelper
from lib.utility.ObserverClasses import Message
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.controller.PriceCatalogController import PriceCatalogController
from lib.utility.gui.widget.TableWidgets import PriceCatalogTable, PriceCatalogTableBuilder, TitleAndSubtitleSection, \
    SixColumnsHeaderSection, SixColumnsDataSection, HorizontalTreeSection, NamedTableItem
from res import Styles
from lib.utility.gui.widget.CustomIcon import CustomIcon


class PriceCatalogView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, svg_icon: FluentIconBase = CustomIcon.PRICE):
        super().__init__("price_list_view", parent_widget, svg_icon)

        # Controller
        self.controller = PriceCatalogController()

        # Titolo e sottotitolo
        self.setTitleText("Listino prezzi formificio")
        self.setSubtitleText("Gli importi sono espressi in euro e si riferiscono al paio di forme")

        self.sidebar_label = QLabel()
        self.sidebar_label.setWordWrap(True)
        self.sidebar_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.sidebar_label)

        # Costruisco la tabella del listino prezzi usando un PriceListTableBuilder
        table_builder = PriceCatalogTableBuilder(self.central_frame)
        table_builder.add_sections(  # Aggiungo le sezioni che compongono il listino

            # Sezione 1 - Prezzi base
            TitleAndSubtitleSection("(1) Listino prezzi standard (forma intera e liscia)", "Prezzi base"),
            SixColumnsHeaderSection("PLASTICA", ["UOMO (N.34/48)", "DONNA (N.34/44)", "BAMBINO (N.18/33)"],
                                    ["BASSA", "POLACCO"]),
            SixColumnsDataSection(["TIPO 1", "TIPO 2", "TIPO 3"],
                                  [
                                      ["standard_tipo1_uomo_bassa", "standard_tipo1_uomo_polacco",
                                       "standard_tipo1_donna_bassa", "standard_tipo1_donna_polacco",
                                       "standard_tipo1_bambino_bassa", "standard_tipo1_bambino_polacco"],
                                      ["standard_tipo2_uomo_bassa", "standard_tipo2_uomo_polacco",
                                       "standard_tipo2_donna_bassa", "standard_tipo2_donna_polacco",
                                       "standard_tipo2_bambino_bassa", "standard_tipo2_bambino_polacco"],
                                      ["standard_tipo3_uomo_bassa", "standard_tipo3_uomo_polacco",
                                       "standard_tipo3_donna_bassa", "standard_tipo3_donna_polacco",
                                       "standard_tipo3_bambino_bassa", "standard_tipo3_bambino_polacco"]
                                  ]),

            # Sezione 2 - Lavorazioni principali
            TitleAndSubtitleSection("(2) Lavorazioni principali", "Da aggiungere al prezzo base"),
            SixColumnsDataSection(["CUNEO", "SN.ALFA", "SN.TENDO"],
                                  [
                                      ["lavorazione_cuneo_uomo_bassa", "lavorazione_cuneo_uomo_polacco",
                                       "lavorazione_cuneo_donna_bassa", "lavorazione_cuneo_donna_polacco",
                                       "lavorazione_cuneo_bambino_bassa", "lavorazione_cuneo_bambino_polacco"],
                                      ["lavorazione_alfa_uomo_bassa", "lavorazione_alfa_uomo_polacco",
                                       "lavorazione_alfa_donna_bassa", "lavorazione_alfa_donna_polacco",
                                       "lavorazione_alfa_bambino_bassa", "lavorazione_alfa_bambino_polacco"],
                                      ["lavorazione_tendo_uomo_bassa", "lavorazione_tendo_uomo_polacco",
                                       "lavorazione_tendo_donna_bassa", "lavorazione_tendo_donna_polacco",
                                       "lavorazione_tendo_bambino_bassa", "lavorazione_tendo_bambino_polacco"],
                                  ]),

            # Sezione 3 - Ferratura
            TitleAndSubtitleSection("(3) Ferratura", "Da aggiungere al prezzo base"),
            SixColumnsDataSection(["TACCO", "MEZZA", "TUTTA"],
                                  [
                                      ["ferratura_tacco_uomo_bassa", "ferratura_tacco_uomo_polacco",
                                       "ferratura_tacco_donna_bassa", "ferratura_tacco_donna_polacco",
                                       "ferratura_tacco_bambino_bassa", "ferratura_tacco_bambino_polacco"],
                                      ["ferratura_mezza_uomo_bassa", "ferratura_mezza_uomo_polacco",
                                       "ferratura_mezza_donna_bassa", "ferratura_mezza_donna_polacco",
                                       "ferratura_mezza_bambino_bassa", "ferratura_mezza_bambino_polacco"],
                                      ["ferratura_tutta_uomo_bassa", "ferratura_tutta_uomo_polacco",
                                       "ferratura_tutta_donna_bassa", "ferratura_tutta_donna_polacco",
                                       "ferratura_tutta_bambino_bassa", "ferratura_tutta_bambino_polacco"],
                                  ]),

            # Sezione 4 - Lavorazioni speciali e accessori
            TitleAndSubtitleSection("(4) Lavorazioni speciali e accessori", "Da aggiungere al prezzo base"),
            HorizontalTreeSection("SEGNI E LINEE",
                                  ["NUMERAZIONE SERIALE", "TALLONE", "ANTICOLLO", "LATERALI"],
                                  ["numeratura_tallone", "numeratura_anticollo", "numeratura_laterali"],
                                  True
                                  ),
            HorizontalTreeSection("BUSSOLE",
                                  ["BUSSOLA STANDARD", "BUSSOLA RINFORZATA",
                                   "SECONDA BUSSOLA STANDARD", "SECONDA BUSSOLA RINFORZATA"],
                                  ["bussola_prima_rinforzata",
                                   "bussola_seconda_standard", "bussola_seconda_rinforzata"],
                                  True
                                  ),
            HorizontalTreeSection("ALTRI ACCESSORI",
                                  ["PERNO SOTTO TALLONE", "PUNTA FERRATA"],
                                  ["perno_sotto_tallone", "punta_ferrata"]
                                  )
        )

        # Costruisco una nuova PriceListTable "tracciando" le sezioni su di essa
        self.table: PriceCatalogTable = table_builder.build()

        # Metodo per aggiornare il listino prezzi ogni volta che ci sono cambiamenti al model
        def update_price_catalog_view(message: Message):
            data = message.data()
            match message.event():
                case PriceCatalogRepository.Event.PRICE_CATALOG_INITIALIZED:
                    # Aggiorna l'intero listino
                    self.table.updateAllNamedItems(data)

                case PriceCatalogRepository.Event.PRICE_UPDATED:
                    # Aggiorna un solo importo
                    self.table.updateNamedItem(next(iter(data.keys())), next(iter(data.values())))

        # Aggiorno i dati della tabella ogni volta che cambiano

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_price_catalog_view)
        self.controller.observe_price_catalog(self.messageReceived.emit)

        if Firebase.auth.currentUserRole() == "manager":
            # Connette il segnale "itemClicked" allo slot "on_item_clicked"
            self.table.itemClicked.connect(self.on_item_clicked)

            # Imposta il testo mostrato nella sidebar
            self.sidebar_label.setText("Clicca su un importo per modificarlo")

        else:
            # Imposta il testo mostrato nella sidebar
            self.sidebar_label.setText("Gli importi sono aggiornati in tempo reale")

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
                    ConnectionErrorHelper.handle(lambda: self.controller.update_price_list({item.itemName: new_value}),
                                                 self.window())
