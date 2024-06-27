from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QDialog
from qfluentwidgets import FluentIconBase

from lib.controller.StorageController import StorageController
from lib.model.StoredItems import MaterialDescription
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.main.SubInterfaces import SubInterfaceWidget
from lib.view.storage.StoredItemTradeView import StoredItemTradeView
from lib.utility.ui.widget.TableWidgets import PriceCatalogTableBuilder, TitleAndSubtitleSection, HorizontalTreeSection, \
    PriceCatalogTable, NamedTableItem
from lib.utility.CustomIcon import CustomIcon


class HardwareStorePriceCatalogView(SubInterfaceWidget):
    def __init__(self, parent_widget: QWidget, controller: StorageController,
                 svg_icon: FluentIconBase = CustomIcon.PRICE):
        super().__init__("hardware_store_price_list_view", parent_widget, svg_icon)

        # Controller
        self.controller = controller

        # Titolo e sottotitolo
        self.setTitleText("Listino prezzi ferramenta")
        self.setSubtitleText("Gli importi sono espressi in euro")

        self.sidebar_label = QLabel()
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
                                  ["piastra_corta_10", "piastra_corta_50",
                                   "piastra_media_10", "piastra_media_50",
                                   "piastra_lunga_10", "piastra_lunga_50",
                                   "piastra_punta_20"],
                                  grey_rows={2, 3, 6}
                                  ),

            # Sezione 3 - Altro
            HorizontalTreeSection("ALTRO",
                                  ["INCHIOSTRO INDELEBILE (1L)", "INCHIOSTRO INDELEBILE (10L)",
                                   "PERNO (x20)", "PERNO (x50)",
                                   "MOLLA PER CUNEO (x20)",
                                   "GANCIO PER SNODO ALFA (x20)",
                                   "GANCIO PER SNODO TENDO (x20)"],
                                  ["inchiostro_1", "inchiostro_10",
                                   "perno_20", "perno_50",
                                   "molla_20", "gancio_alfa_20", "gancio_tendo_20"],
                                  grey_rows={2, 3, 5}
                                  )
        )

        # Costruisce una nuova PriceListTable "tracciando" le sezioni su di essa
        self.table: PriceCatalogTable = table_builder.build()

        # Popola la tabella
        self.table.updateAllNamedItems(self.controller.get_hardware_store_price_catalog())

        # Connette il segnale "itemClicked" allo slot "on_item_clicked"
        self.table.itemClicked.connect(self.on_item_clicked)

        # Imposta il testo mostrato nella sidebar
        self.sidebar_label.setText("Clicca su un importo del listino per acquistare")

        # Imposta la tabella nel layout centrale
        self.central_layout.addWidget(self.table)

    @pyqtSlot(QTableWidgetItem)
    def on_item_clicked(self, item: QTableWidgetItem):
        if isinstance(item, NamedTableItem):

            # Estrae il prezzo per acquisto
            price_per_purchase: float = PriceFormatter.unformat(item.text())

            # Estrae la descrizione del materiale e la quantità per acquisto dal nome dell'item
            name_parts = item.itemName.split("_")

            # Determina la descrizione del materiale e la quantità per acquisto
            material_description: MaterialDescription
            amount_per_purchase: int

            if len(name_parts) == 2:
                material_description = MaterialDescription[name_parts[0].upper()]
                amount_per_purchase = int(name_parts[1])

            else:
                material_description = MaterialDescription[f"{name_parts[0].upper()}_{name_parts[1].upper()}"]
                amount_per_purchase = int(name_parts[2])

            # Crea il Dialog di acquisto
            dialog = StoredItemTradeView.material(
                material_description.value,
                price_per_purchase,
                amount_per_purchase
            )

            # Mostra Dialog acquisto materiali
            if dialog.exec() == QDialog.Accepted:
                purchased_quantity = dialog.value()
                actual_purchased_quantity = purchased_quantity * amount_per_purchase
                total_price = purchased_quantity * price_per_purchase

                # Determina il nome dell'unità di misura della quantità acquistata
                liter_string = "litro" if actual_purchased_quantity == 1 else "litri"
                measurement_unit = liter_string if material_description == MaterialDescription.INCHIOSTRO else "pezzi"

                # Effettua l'acquisto dei materiali
                self.controller.purchase_material(
                    material_description=material_description,
                    purchased_quantity=actual_purchased_quantity,
                    transaction_description=f"Acquisto \"{material_description.value}\" "
                                            f"({str(actual_purchased_quantity)} {measurement_unit})",
                    transaction_amount=total_price * -1,
                )
