from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QInputDialog, QDialog

from lib.mvc.main.view.BaseWidget import BaseWidget
from lib.mvc.pricecatalog.controller.PriceListController import PriceListController
from lib.network.PriceCatalogNetwork import PriceCatalogNetwork
from lib.utility.ObserverClasses import Observable
from lib.widget.TableWidgets import PriceCatalogTable, NamedTableItem, PriceCatalogTableBuilder, TitleAndSubtitleSection, \
    SixColumnsHeaderSection, SixColumnsDataSection, HorizontalTreeSection
from res import Styles
from res.Dimensions import FontWeight, FontSize


class PriceListView(BaseWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__("price_list_view", parent_widget)

        # Controller
        self.controller = PriceListController()

        # Titolo e sottotitolo
        self.setTitleText("Listino prezzi formificio")
        self.setSubtitleText("Gli importi sono espressi in euro e si riferiscono al paio di forme")

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
                                  ["Gratuito", "numeratura_tallone", "numeratura_anticollo", "numeratura_laterali"],
                                  True
                                  ),
            HorizontalTreeSection("BUSSOLE",
                                  ["BUSSOLA STANDARD", "BUSSOLA RINFORZATA",
                                   "SECONDA BUSSOLA STANDARD", "SECONDA BUSSOLA RINFORZATA"],
                                  ["Gratuito", "bussola_prima_rinforzata",
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

        """
        # Listino prezzi
        self.table = PriceListTable(self.central_frame)
        self.table.setRowCount(29)

        bold_font = QFont()
        bold_font.setWeight(FontWeight.BOLD)
        bold_font.setPointSize(FontSize.DEFAULT)

        bold_header_font = QFont()
        bold_header_font.setWeight(FontWeight.BOLD)
        bold_header_font.setPointSize(FontSize.TABLE_HEADER)

        italic_font = QFont()
        italic_font.setItalic(True)
        bold_font.setPointSize(FontSize.DEFAULT)

        blue_brush = QBrush(QColor(0, 95, 184))
        red_brush = QBrush(QColor(207, 0, 0))
        green_brush = QBrush(QColor(70, 142, 35))
        brown_brush = QBrush(QColor(92, 64, 51))

        # self.table.setSection()

        # Prima sezione - Prezzi di base
        self.table.setRowAndItem(0, QTableWidgetItem("(1) Listino prezzi standard (forma intera e liscia)"))
        self.table.rowItem(0).setFont(bold_font)

        self.table.setRowAndItem(1, QTableWidgetItem("Prezzi base"))
        self.table.rowItem(1).setFont(italic_font)

        self.table.setSpan(2, 0, 2, 1)
        self.table.setItem(2, 0, QTableWidgetItem("PLASTICA"))
        self.table.item(2, 0).setFont(bold_header_font)

        self.table.setSpan(2, 1, 1, 2)
        self.table.setItem(2, 1, QTableWidgetItem("UOMO (N.34/48)"))
        self.table.item(2, 1).setFont(bold_header_font)
        self.table.item(2, 1).setForeground(blue_brush)

        self.table.setSpan(2, 3, 1, 2)
        self.table.setItem(2, 3, QTableWidgetItem("DONNA (N.34/44)"))
        self.table.item(2, 3).setFont(bold_header_font)
        self.table.item(2, 3).setForeground(red_brush)

        self.table.setSpan(2, 5, 1, 2)
        self.table.setItem(2, 5, QTableWidgetItem("BAMBINO (N.18/33)"))
        self.table.item(2, 5).setFont(bold_header_font)
        self.table.item(2, 5).setForeground(green_brush)

        self.table.setItem(3, 1, QTableWidgetItem("BASSA"))
        self.table.item(3, 1).setFont(bold_header_font)
        self.table.item(3, 1).setForeground(blue_brush)
        self.table.setItem(3, 3, QTableWidgetItem("BASSA"))
        self.table.item(3, 3).setFont(bold_header_font)
        self.table.item(3, 3).setForeground(red_brush)
        self.table.setItem(3, 5, QTableWidgetItem("BASSA"))
        self.table.item(3, 5).setFont(bold_header_font)
        self.table.item(3, 5).setForeground(green_brush)

        self.table.setItem(3, 2, QTableWidgetItem("POLACCO"))
        self.table.item(3, 2).setFont(bold_header_font)
        self.table.setItem(3, 4, QTableWidgetItem("POLACCO"))
        self.table.item(3, 4).setFont(bold_header_font)
        self.table.setItem(3, 6, QTableWidgetItem("POLACCO"))
        self.table.item(3, 6).setFont(bold_header_font)

        self.table.setItem(4, 0, QTableWidgetItem("TIPO 1"))
        self.table.item(4, 0).setFont(bold_header_font)
        self.table.setItem(5, 0, QTableWidgetItem("TIPO 2"))
        self.table.item(5, 0).setFont(bold_header_font)
        self.table.setItem(6, 0, QTableWidgetItem("TIPO 3"))
        self.table.item(6, 0).setFont(bold_header_font)

        # Seconda sezione - Lavorazioni principali
        self.table.setRowAndItem(7, QTableWidgetItem("(2) Lavorazioni principali"))
        self.table.rowItem(7).setFont(bold_font)

        self.table.setRowAndItem(8, QTableWidgetItem("Da aggiungere al prezzo base"))
        self.table.rowItem(8).setFont(italic_font)

        self.table.setItem(9, 0, QTableWidgetItem("CUNEO"))
        self.table.item(9, 0).setFont(bold_header_font)
        self.table.setItem(10, 0, QTableWidgetItem("SN.ALFA"))
        self.table.item(10, 0).setFont(bold_header_font)
        self.table.setItem(11, 0, QTableWidgetItem("SN.TENDO"))
        self.table.item(11, 0).setFont(bold_header_font)

        # Terza sezione - Ferratura
        self.table.setRowAndItem(12, QTableWidgetItem("(3) Ferratura"))
        self.table.rowItem(12).setFont(bold_font)

        self.table.setRowAndItem(13, QTableWidgetItem("Da aggiungere al prezzo base"))
        self.table.rowItem(13).setFont(italic_font)

        self.table.setItem(14, 0, QTableWidgetItem("TACCO"))
        self.table.item(14, 0).setFont(bold_header_font)
        self.table.setItem(15, 0, QTableWidgetItem("MEZZA"))
        self.table.item(15, 0).setFont(bold_header_font)
        self.table.setItem(16, 0, QTableWidgetItem("TUTTA"))
        self.table.item(16, 0).setFont(bold_header_font)

        # Quarta sezione - Accessori
        self.table.setRowAndItem(17, QTableWidgetItem("(4) Lavorazioni speciali e accessori"))
        self.table.rowItem(17).setFont(bold_font)

        self.table.setRowAndItem(18, QTableWidgetItem("Da aggiungere al prezzo base"))
        self.table.rowItem(18).setFont(italic_font)

        # Sottosezione - Segni e linee
        self.table.setSpan(19, 0, 4, 2)
        self.table.setItem(19, 0, QTableWidgetItem("SEGNI E LINEE"))

        self.table.item(19, 0).setFont(bold_header_font)
        self.table.setSpan(19, 2, 1, 3)
        self.table.setItem(19, 2, QTableWidgetItem("NUMERAZIONE SERIALE"))
        self.table.setSpan(20, 2, 1, 3)
        self.table.setItem(20, 2, QTableWidgetItem("TALLONE"))
        self.table.setSpan(21, 2, 1, 3)
        self.table.setItem(21, 2, QTableWidgetItem("ANTICOLLO"))
        self.table.setSpan(22, 2, 1, 3)
        self.table.setItem(22, 2, QTableWidgetItem("LATERALI"))

        self.table.setSpan(19, 5, 1, 2)
        self.table.setSpan(20, 5, 1, 2)
        self.table.setSpan(21, 5, 1, 2)
        self.table.setSpan(22, 5, 1, 2)

        # Sottosezione - Bussole
        self.table.setSpan(23, 0, 4, 2)
        self.table.setItem(23, 0, QTableWidgetItem("BUSSOLE"))

        self.table.item(23, 0).setFont(bold_header_font)
        self.table.setSpan(23, 2, 1, 3)
        self.table.setItem(23, 2, QTableWidgetItem("BUSSOLA STANDARD"))
        self.table.setSpan(24, 2, 1, 3)
        self.table.setItem(24, 2, QTableWidgetItem("BUSSOLA RINFORZATA"))
        self.table.setSpan(25, 2, 1, 3)
        self.table.setItem(25, 2, QTableWidgetItem("SECONDA BUSSOLA STANDARD"))
        self.table.setSpan(26, 2, 1, 3)
        self.table.setItem(26, 2, QTableWidgetItem("SECONDA BUSSOLA RINFORZATA"))

        self.table.setSpan(23, 5, 1, 2)
        self.table.setSpan(24, 5, 1, 2)
        self.table.setSpan(25, 5, 1, 2)
        self.table.setSpan(26, 5, 1, 2)

        # Sottosezione - Altri accessori
        self.table.setSpan(27, 0, 2, 2)
        self.table.setItem(27, 0, QTableWidgetItem("ALTRI ACCESSORI"))

        self.table.item(27, 0).setFont(bold_header_font)
        self.table.setSpan(27, 2, 1, 3)
        self.table.setItem(27, 2, QTableWidgetItem("PERNO SOTTO TALLONE"))
        self.table.setSpan(28, 2, 1, 3)
        self.table.setItem(28, 2, QTableWidgetItem("PUNTA FERRATA"))

        self.table.setSpan(27, 5, 1, 2)
        self.table.setSpan(28, 5, 1, 2)

        # Celle con i prezzi standard
        self.table.setNamedItem(4, 1, NamedTableItem("standard_tipo1_uomo_bassa"))
        self.table.item(4, 1).setForeground(blue_brush)
        self.table.setNamedItem(4, 2, NamedTableItem("standard_tipo1_uomo_polacco"))
        self.table.setNamedItem(4, 3, NamedTableItem("standard_tipo1_donna_bassa"))
        self.table.item(4, 3).setForeground(red_brush)
        self.table.setNamedItem(4, 4, NamedTableItem("standard_tipo1_donna_polacco"))
        self.table.setNamedItem(4, 5, NamedTableItem("standard_tipo1_bambino_bassa"))
        self.table.item(4, 5).setForeground(green_brush)
        self.table.setNamedItem(4, 6, NamedTableItem("standard_tipo1_bambino_polacco"))

        self.table.setNamedItem(5, 1, NamedTableItem("standard_tipo2_uomo_bassa"))
        self.table.item(5, 1).setForeground(blue_brush)
        self.table.setNamedItem(5, 2, NamedTableItem("standard_tipo2_uomo_polacco"))
        self.table.setNamedItem(5, 3, NamedTableItem("standard_tipo2_donna_bassa"))
        self.table.item(5, 3).setForeground(red_brush)
        self.table.setNamedItem(5, 4, NamedTableItem("standard_tipo2_donna_polacco"))
        self.table.setNamedItem(5, 5, NamedTableItem("standard_tipo2_bambino_bassa"))
        self.table.item(5, 5).setForeground(green_brush)
        self.table.setNamedItem(5, 6, NamedTableItem("standard_tipo2_bambino_polacco"))

        self.table.setNamedItem(6, 1, NamedTableItem("standard_tipo3_uomo_bassa"))
        self.table.item(6, 1).setForeground(blue_brush)
        self.table.setNamedItem(6, 2, NamedTableItem("standard_tipo3_uomo_polacco"))
        self.table.setNamedItem(6, 3, NamedTableItem("standard_tipo3_donna_bassa"))
        self.table.item(6, 3).setForeground(red_brush)
        self.table.setNamedItem(6, 4, NamedTableItem("standard_tipo3_donna_polacco"))
        self.table.setNamedItem(6, 5, NamedTableItem("standard_tipo3_bambino_bassa"))
        self.table.item(6, 5).setForeground(green_brush)
        self.table.setNamedItem(6, 6, NamedTableItem("standard_tipo3_bambino_polacco"))

        # Celle con i prezzi delle lavorazioni principali
        self.table.setNamedItem(9, 1, NamedTableItem("lavorazione_cuneo_uomo_bassa"))
        self.table.item(9, 1).setForeground(blue_brush)
        self.table.setNamedItem(9, 2, NamedTableItem("lavorazione_cuneo_uomo_polacco"))
        self.table.setNamedItem(9, 3, NamedTableItem("lavorazione_cuneo_donna_bassa"))
        self.table.item(9, 3).setForeground(red_brush)
        self.table.setNamedItem(9, 4, NamedTableItem("lavorazione_cuneo_donna_polacco"))
        self.table.setNamedItem(9, 5, NamedTableItem("lavorazione_cuneo_bambino_bassa"))
        self.table.item(9, 5).setForeground(green_brush)
        self.table.setNamedItem(9, 6, NamedTableItem("lavorazione_cuneo_bambino_polacco"))

        self.table.setNamedItem(10, 1, NamedTableItem("lavorazione_alfa_uomo_bassa"))
        self.table.item(10, 1).setForeground(blue_brush)
        self.table.setNamedItem(10, 2, NamedTableItem("lavorazione_alfa_uomo_polacco"))
        self.table.setNamedItem(10, 3, NamedTableItem("lavorazione_alfa_donna_bassa"))
        self.table.item(10, 3).setForeground(red_brush)
        self.table.setNamedItem(10, 4, NamedTableItem("lavorazione_alfa_donna_polacco"))
        self.table.setNamedItem(10, 5, NamedTableItem("lavorazione_alfa_bambino_bassa"))
        self.table.item(10, 5).setForeground(green_brush)
        self.table.setNamedItem(10, 6, NamedTableItem("lavorazione_alfa_bambino_polacco"))

        self.table.setNamedItem(11, 1, NamedTableItem("lavorazione_tendo_uomo_bassa"))
        self.table.item(11, 1).setForeground(blue_brush)
        self.table.setNamedItem(11, 2, NamedTableItem("lavorazione_tendo_uomo_polacco"))
        self.table.setNamedItem(11, 3, NamedTableItem("lavorazione_tendo_donna_bassa"))
        self.table.item(11, 3).setForeground(red_brush)
        self.table.setNamedItem(11, 4, NamedTableItem("lavorazione_tendo_donna_polacco"))
        self.table.setNamedItem(11, 5, NamedTableItem("lavorazione_tendo_bambino_bassa"))
        self.table.item(11, 5).setForeground(green_brush)
        self.table.setNamedItem(11, 6, NamedTableItem("lavorazione_tendo_bambino_polacco"))

        # Celle con i prezzi delle ferrature
        self.table.setNamedItem(14, 1, NamedTableItem("ferratura_tacco_uomo_bassa"))
        self.table.item(14, 1).setForeground(blue_brush)
        self.table.setNamedItem(14, 2, NamedTableItem("ferratura_tacco_uomo_polacco"))
        self.table.setNamedItem(14, 3, NamedTableItem("ferratura_tacco_donna_bassa"))
        self.table.item(14, 3).setForeground(red_brush)
        self.table.setNamedItem(14, 4, NamedTableItem("ferratura_tacco_donna_polacco"))
        self.table.setNamedItem(14, 5, NamedTableItem("ferratura_tacco_bambino_bassa"))
        self.table.item(14, 5).setForeground(green_brush)
        self.table.setNamedItem(14, 6, NamedTableItem("ferratura_tacco_bambino_polacco"))

        self.table.setNamedItem(15, 1, NamedTableItem("ferratura_mezza_uomo_bassa"))
        self.table.item(15, 1).setForeground(blue_brush)
        self.table.setNamedItem(15, 2, NamedTableItem("ferratura_mezza_uomo_polacco"))
        self.table.setNamedItem(15, 3, NamedTableItem("ferratura_mezza_donna_bassa"))
        self.table.item(15, 3).setForeground(red_brush)
        self.table.setNamedItem(15, 4, NamedTableItem("ferratura_mezza_donna_polacco"))
        self.table.setNamedItem(15, 5, NamedTableItem("ferratura_mezza_bambino_bassa"))
        self.table.item(15, 5).setForeground(green_brush)
        self.table.setNamedItem(15, 6, NamedTableItem("ferratura_mezza_bambino_polacco"))

        self.table.setNamedItem(16, 1, NamedTableItem("ferratura_tutta_uomo_bassa"))
        self.table.item(16, 1).setForeground(blue_brush)
        self.table.setNamedItem(16, 2, NamedTableItem("ferratura_tutta_uomo_polacco"))
        self.table.setNamedItem(16, 3, NamedTableItem("ferratura_tutta_donna_bassa"))
        self.table.item(16, 3).setForeground(red_brush)
        self.table.setNamedItem(16, 4, NamedTableItem("ferratura_tutta_donna_polacco"))
        self.table.setNamedItem(16, 5, NamedTableItem("ferratura_tutta_bambino_bassa"))
        self.table.item(16, 5).setForeground(green_brush)
        self.table.setNamedItem(16, 6, NamedTableItem("ferratura_tutta_bambino_polacco"))

        # Celle con i prezzi delle lavorazioni speciali e accessori
        self.table.setItem(19, 5, QTableWidgetItem("Gratuito"))
        self.table.item(19, 5).setForeground(brown_brush)
        self.table.setNamedItem(20, 5, NamedTableItem("numeratura_tallone"))
        self.table.item(20, 5).setForeground(brown_brush)
        self.table.setNamedItem(21, 5, NamedTableItem("numeratura_anticollo"))
        self.table.item(21, 5).setForeground(brown_brush)
        self.table.setNamedItem(22, 5, NamedTableItem("numeratura_laterali"))
        self.table.item(22, 5).setForeground(brown_brush)
        self.table.setItem(23, 5, QTableWidgetItem("Gratuito"))
        self.table.item(23, 5).setForeground(brown_brush)
        self.table.setNamedItem(24, 5, NamedTableItem("bussola_prima_rinforzata"))
        self.table.item(24, 5).setForeground(brown_brush)
        self.table.setNamedItem(25, 5, NamedTableItem("bussola_seconda_standard"))
        self.table.item(25, 5).setForeground(brown_brush)
        self.table.setNamedItem(26, 5, NamedTableItem("bussola_seconda_rinforzata"))
        self.table.item(26, 5).setForeground(brown_brush)
        self.table.setNamedItem(27, 5, NamedTableItem("perno_sotto_tallone"))
        self.table.item(27, 5).setForeground(brown_brush)
        self.table.setNamedItem(28, 5, NamedTableItem("punta_ferrata"))
        self.table.item(28, 5).setForeground(brown_brush)
        """

        # Metodo per aggiornare il listino prezzi ogni volta che ci sono cambiamenti al model
        def update_prices_callback(message):
            event: str = message["event"]
            data: dict = message["data"]
            match event:
                # Prima volta - scarica l'intero listino
                case "put":
                    self.table.updateAllNamedItems(data)
                # Ad ogni successiva modifica di un importo del listino
                case "patch":
                    self.table.updateNamedItem(next(iter(data.keys())), next(iter(data.values())))
                # Se per qualche motivo il collegamento fallisce
                case "cancel":
                    pass
                    ''' Da gestire in qualche modo '''

        # Aggiorno i dati della tabella ogni volta che cambiano
        self.controller.price_list.observe(update_prices_callback)

        # Connetto il segnale "itemClicked" allo slot "on_item_clicked"
        self.table.itemClicked.connect(self.on_item_clicked)

        # Imposta la tabella nel layout centrale
        self.central_layout.addWidget(self.table)

    @pyqtSlot(QTableWidgetItem)
    def on_item_clicked(self, item: QTableWidgetItem):
        if type(item).__name__ == "NamedTableItem":

            current_value = float(item.text())

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
                print(new_value)

                # Aggiorno il valore se è diverso
                if new_value != current_value:
                    self.controller.update_price_list({item.itemName: new_value})
