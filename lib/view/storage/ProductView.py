from __future__ import annotations

from PyQt5.QtGui import QFont, QCloseEvent
from PyQt5.QtWidgets import QLabel, QSizePolicy, QMessageBox, QVBoxLayout
from qfluentwidgets import PrimaryPushButton

from lib.controller.ProductController import ProductController
from lib.model.Finished import Finished
from lib.model.Product import Product
from lib.model.SemiFinished import SemiFinished
from lib.model.Sketch import Sketch
from lib.utility.TableAdapters import SingleRowTableAdapter
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.widget.Separators import VerticalSpacer
from lib.widget.TableWidgets import SingleRowStandardTable
from res.Dimensions import FontSize


class ProductView(SubInterfaceChildWidget):

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        #self.controller.detach_order_observer(self.observer)  # Rimuove l'osservatore dal prodotto

    def __init__(self, parent_widget: SubInterfaceWidget, product: Product):

        # Controller
        self.controller: ProductController = ProductController(product)

        # Inizializzo il widget di base
        super().__init__(f"product_{self.controller.get_product_serial()}_view", parent_widget, True)

        # Titolo e sottotitolo
        self.setTitleText(f"Prodotto {self.controller.get_product_serial()}")
        self.hideSubtitle()

        # Titolo tabella dettagli prodotto
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.product_details_title = QLabel(f"Dettagli prodotto {self.controller.get_product_serial()}")
        self.product_details_title.setFont(font)
        self.product_details_title.setContentsMargins(16, 16, 16, 8)

        # Dettagli prodotto
        self.product_main_table = SingleRowStandardTable(self.central_frame)
        self.product_second_table = SingleRowStandardTable(self.central_frame)
        self.product_third_table = SingleRowStandardTable(self.central_frame)

        # Riempimento tabelle dettagli
        if type(product) is Sketch:
            # Prima tabella
            self.product_main_table_adapter = SketchDetailsAdapter(self.product_main_table)
            headers = ["Tipo", "Genere", "Tipo di plastica", "Tipo di abbozzo", "Dettagli", "Quantità"]
            self.product_main_table.setHeaders(headers)
            self.product_main_table_adapter.setData(product)
            self.product_second_table.setVisible(False)
            self.product_third_table.setVisible(False)
        elif type(product) is SemiFinished:
            # Prima tabella
            self.product_main_table_adapter = SemiFinishedMainAdapter(self.product_main_table)
            headers = ["Tipo", "Genere", "Tipo di plastica", "Tipo di abbozzo", "Taglia", "Lavorazione"]
            self.product_main_table.setHeaders(headers)
            self.product_main_table_adapter.setData(product)
            # Seconda tabella
            self.product_second_table_adapter = SemiFinishedSecondAdapter(self.product_second_table)
            headers = ["Ferratura", "Prima bussola", "Seconda bussola", "Perno sotto tallone", "Punta ferrata"]
            self.product_second_table.setHeaders(headers)
            self.product_second_table_adapter.setData(product)
            # Terza tabella
            self.product_third_table_adapter = SemiFinishedThirdAdapter(self.product_third_table)
            headers = ["Dettagli", "Quantità"]
            self.product_third_table.setHeaders(headers)
            self.product_third_table_adapter.setData(product)
        elif type(product) is Finished:
            # Prima tabella
            self.product_main_table_adapter = FinishedMainAdapter(self.product_main_table)
            headers = ["Tipo", "Genere", "Tipo di plastica", "Tipo di abbozzo", "Taglia", "Numeratura"]
            self.product_main_table.setHeaders(headers)
            self.product_main_table_adapter.setData(product)
            # Seconda tabella
            self.product_second_table_adapter = FinishedSecondAdapter(self.product_second_table)
            headers = ["Lavorazione", "Ferratura", "Prima bussola", "Seconda bussola", "Perno sotto tallone"]
            self.product_second_table.setHeaders(headers)
            self.product_second_table_adapter.setData(product)
            # Terza tabella
            self.product_third_table_adapter = FinishedThirdAdapter(self.product_third_table)
            headers = ["Punta ferrata", "Dettagli", "Quantità"]
            self.product_third_table.setHeaders(headers)
            self.product_third_table_adapter.setData(product)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.product_details_title)
        self.inner_central_layout.addWidget(self.product_main_table)
        if product is SemiFinished or Finished:
            self.inner_central_layout.addWidget(self.product_second_table)
            self.inner_central_layout.addWidget(self.product_third_table)

        # Finalizza il layout centrale
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addLayout(self.inner_central_layout)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))  # Costringe i widget in alto

        # Sidebar

        # Pulsante di eliminazione del prodotto
        self.delete_product_button = PrimaryPushButton(text="Elimina prodotto")
        # self.delete_product_button.clicked.connect(self.show_confirm_deletion_dialog)

        # Imposta la sidebar
        self.sidebar_layout.addWidget(self.delete_product_button)

    # Mostra un Dialog di conferma dell'eliminazione del prodotto
    def show_confirm_deletion_dialog(self):

        # Imposta e mostra una richiesta di conferma dell'eliminazione
        clicked_button = QMessageBox.question(
            self,
            "Conferma eliminazione prodotto",
            (f"Il prodotto n° {self.controller.get_product()} verrà eliminato e spostato negli scarti.\n"
             f"Sei sicuro di voler eliminare il prodotto?"),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, elimina l'ordine e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.delete_product_by_id()
            self.window().removeSubInterface(self)


class SketchDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, sketch: Sketch) -> list[str]:
        return [
            sketch.get_product_type(),
            sketch.get_gender().capitalize(),
            sketch.get_plastic(),
            sketch.get_sketch_type(),
            sketch.get_details(),
            str(sketch.get_amount())
        ]


class SemiFinishedMainAdapter(SingleRowTableAdapter):
    def adaptData(self, semifinished: SemiFinished) -> list[str]:
        return [
            semifinished.get_product_type(),
            semifinished.get_gender().capitalize(),
            semifinished.get_plastic(),
            semifinished.get_sketch_type(),
            str(semifinished.get_size()),
            semifinished.get_main_process()
        ]


class SemiFinishedSecondAdapter(SingleRowTableAdapter):
    def adaptData(self, semifinished: SemiFinished) -> list[str]:
        return [
            semifinished.get_shoeing(),
            semifinished.get_first_compass(),
            "Nessuna " if semifinished.get_second_compass() == "" else semifinished.get_second_compass(),
            "No" if semifinished.get_pivot_under_heel() else "Si",
            "No" if semifinished.get_iron_tip() else "Si"
        ]


class SemiFinishedThirdAdapter(SingleRowTableAdapter):
    def adaptData(self, semifinished: SemiFinished) -> list[str]:
        return [
            semifinished.get_details(),
            str(semifinished.get_amount())
        ]


class FinishedMainAdapter(SingleRowTableAdapter):
    def adaptData(self, finished: Finished) -> list[str]:
        return [
            finished.get_product_type(),
            finished.get_gender().capitalize(),
            f"Tipo {str(finished.get_plastic())}",
            f"Abbozzo tipo: {str(finished.get_sketch_type())}",
            str(finished.get_size()),
            finished.get_numbering()
        ]


class FinishedSecondAdapter(SingleRowTableAdapter):
    def adaptData(self, finished: Finished) -> list[str]:
        return [
            finished.get_main_process(),
            finished.get_shoeing(),
            finished.get_first_compass(),
            finished.get_second_compass(),
            "No" if finished.get_pivot_under_heel() else "Si"
        ]


class FinishedThirdAdapter(SingleRowTableAdapter):
    def adaptData(self, finished: Finished) -> list[str]:
        return [
            "No" if finished.get_iron_tip() else "Si",
            finished.get_details(),
            str(finished.get_amount())
        ]
