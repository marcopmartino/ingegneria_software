from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCloseEvent
from PyQt5.QtWidgets import QLabel, QSizePolicy, QMessageBox, QVBoxLayout, QHBoxLayout
from qfluentwidgets import PrimaryPushButton

from lib.controller.ProductController import ProductController
from lib.model.StoredItems import StoredShoeLastVariety
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.widget.Separators import VerticalSpacer
from res.Dimensions import FontSize


class ProductView(SubInterfaceChildWidget):

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)

    def __init__(self, parent_widget: SubInterfaceWidget, product: StoredShoeLastVariety):
        # Controller
        self.controller: ProductController = ProductController(product)

        # Inizializzo il widget di base
        super().__init__(f"product_{self.controller.get_product_serial()}_view", parent_widget, True)

        # Titolo e sottotitolo
        self.setTitleText(f"Prodotto {self.controller.get_product_serial()}")
        self.hideSubtitle()

        title_font = QFont()
        title_font.setPointSize(FontSize.SUBTITLE)

        # Riempimento dettagli prodotto
        self.product_type_label = QLabel(f"<b>Tipo di prodotto</b>: {self.controller.get_product_type()}")
        self.product_type_label.setFont(title_font)
        self.product_type_label.setContentsMargins(16, 16, 16, 8)

        self.shoe_last_type_label = QLabel(f"<b>Tipo di abbozzo</b>: {self.controller.get_sketch_type()}")
        self.shoe_last_type_label.setFont(title_font)
        self.shoe_last_type_label.setContentsMargins(16, 16, 16, 8)

        # Primo layout orizzontale
        self.first_horizontal_layout = QHBoxLayout(self.central_frame)
        self.first_horizontal_layout.addWidget(self.product_type_label)
        self.first_horizontal_layout.addWidget(self.shoe_last_type_label)

        self.plastic_type_label = QLabel(f"<b>Tipo di plastica</b>: {self.controller.get_plastic()}")
        self.plastic_type_label.setFont(title_font)
        self.plastic_type_label.setContentsMargins(16, 16, 16, 8)

        self.gender_label = QLabel(f"<b>Genere</b>: {self.controller.get_gender()}")
        self.gender_label.setFont(title_font)
        self.gender_label.setContentsMargins(16, 16, 16, 8)

        # Secondo layout orizzontale
        self.second_horizontal_layout = QHBoxLayout(self.central_frame)
        self.second_horizontal_layout.addWidget(self.plastic_type_label)
        self.second_horizontal_layout.addWidget(self.gender_label)

        self.size_label = QLabel(f"<b>Taglia</b>: {self.controller.get_size()}")
        self.size_label.setFont(title_font)
        self.size_label.setContentsMargins(16, 16, 16, 8)

        self.processing_label = QLabel(f"<b>Tipo di lavorazione</b>: {self.controller.get_main_process()}")
        self.processing_label.setFont(title_font)
        self.processing_label.setContentsMargins(16, 16, 16, 8)

        # Terzo layout orizzontale
        self.third_horizontal_layout = QHBoxLayout(self.central_frame)
        self.third_horizontal_layout.addWidget(self.size_label)
        self.third_horizontal_layout.addWidget(self.processing_label)

        self.first_compass_label = QLabel(f"<b>Prima bussola</b>: {self.controller.get_first_compass()}")
        self.first_compass_label.setFont(title_font)
        self.first_compass_label.setContentsMargins(16, 16, 16, 8)

        self.second_compass_label = QLabel(f"<b>Seconda bussola</b>: {self.controller.get_second_compass()}")
        self.second_compass_label.setFont(title_font)
        self.second_compass_label.setContentsMargins(16, 16, 16, 8)

        # Quarto layout orizzontale
        self.fourth_horizontal_layout = QHBoxLayout(self.central_frame)
        self.fourth_horizontal_layout.addWidget(self.first_compass_label)
        self.fourth_horizontal_layout.addWidget(self.second_compass_label)

        self.pivot_under_heel_label = QLabel(f"<b>Perno sotto tacco</b>: {self.controller.get_pivot_under_heel()}")
        self.pivot_under_heel_label.setFont(title_font)
        self.pivot_under_heel_label.setContentsMargins(16, 16, 16, 8)

        self.shoeing_label = QLabel(f"<b>Ferratura</b>: {self.controller.get_shoeing()}")
        self.shoeing_label.setFont(title_font)
        self.shoeing_label.setContentsMargins(16, 16, 16, 8)

        self.iron_tip_label = QLabel(f"<b>Punta ferrata</b>: {self.controller.get_iron_tip()}")
        self.iron_tip_label.setFont(title_font)
        self.iron_tip_label.setContentsMargins(16, 16, 16, 8)

        # Quinto layout orizzontale
        self.fifth_horizontal_layout = QHBoxLayout(self.central_frame)
        self.fifth_horizontal_layout.addWidget(self.pivot_under_heel_label)
        self.fifth_horizontal_layout.addWidget(self.shoeing_label)
        self.fifth_horizontal_layout.addWidget(self.iron_tip_label)

        self.numbering_antineck_label = QLabel(f"<b>Numeratura anticollo</b>: {self.controller.get_numbering_antineck()}")
        self.numbering_antineck_label.setFont(title_font)
        self.numbering_antineck_label.setContentsMargins(16, 16, 16, 8)

        self.numbering_lateral_label = QLabel(f"<b>Numeratura laterale</b>: {self.controller.get_numbering_lateral()}")
        self.numbering_lateral_label.setFont(title_font)
        self.numbering_lateral_label.setContentsMargins(16, 16, 16, 8)

        self.numbering_heel_label = QLabel(f"<b>Numeratura tacco</b>: {self.controller.get_numbering_heel()}")
        self.numbering_heel_label.setFont(title_font)
        self.numbering_heel_label.setContentsMargins(16, 16, 16, 8)

        # Sesto layout orizzontale
        self.sixth_horizontal_layout = QHBoxLayout(self.central_frame)
        self.sixth_horizontal_layout.addWidget(self.numbering_antineck_label)
        self.sixth_horizontal_layout.addWidget(self.numbering_lateral_label)
        self.sixth_horizontal_layout.addWidget(self.numbering_heel_label)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addLayout(self.first_horizontal_layout)
        self.inner_central_layout.addLayout(self.second_horizontal_layout)
        self.inner_central_layout.addLayout(self.third_horizontal_layout)
        self.inner_central_layout.addLayout(self.fourth_horizontal_layout)
        self.inner_central_layout.addLayout(self.fifth_horizontal_layout)
        self.inner_central_layout.addLayout(self.sixth_horizontal_layout)

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
        self.sidebar_layout.setAlignment(Qt.AlignTop)

    # Mostra un Dialog di conferma dell'eliminazione del prodotto
    def show_confirm_deletion_dialog(self):
        # Imposta e mostra una richiesta di conferma dell'eliminazione
        clicked_button = QMessageBox.question(
            self,
            "Conferma eliminazione prodotto",
            (f"Il prodotto n° {self.controller.get_product().get_item_id()} verrà eliminato e spostato negli scarti.\n"
             f"Sei sicuro di voler eliminare il prodotto?"),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, elimina l'ordine e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.delete_product_by_id()
            self.window().removeSubInterface(self)


'''
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
        ]'''
