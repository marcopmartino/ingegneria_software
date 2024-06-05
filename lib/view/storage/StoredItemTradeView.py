from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from qfluentwidgets import SpinBox

from lib.utility.gui.layout.FrameLayouts import HFrameLayout
from lib.utility.UtilityClasses import PriceFormatter
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from res import Styles
from res.Dimensions import GenericDimensions, FontSize, FontWeight


class StoredItemTradeView(QDialog):

    @classmethod
    def raw_shoe_last(cls, object_description: str, unit_price: float, unit_quantity: int = 1):
        # Inizializza il Dialog
        self = cls(object_description, unit_price, unit_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Acquisto abbozzi")

        # Imposta il testo della Label principale
        self.title.setText(f"Acquista \"{object_description}\"" +
                           ("" if unit_quantity == 1 else f" (x{unit_quantity})"))

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Seleziona la quantità da acquistare (paia)")

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'acquisto")

        # Nasconde il pulsante di vendita
        self.sale_button.setHidden(True)

        return self

    @classmethod
    def material(cls, object_description: str, unit_price: float, unit_quantity: int = 1):
        # Inizializza il Dialog
        self = cls(object_description, unit_price, unit_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Acquisto materiali di lavorazione")

        # Imposta il testo della Label principale
        self.title.setText(f"Acquista \"{object_description}\"" +
                           ("" if unit_quantity == 1 else f" (x{unit_quantity})"))

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Seleziona la quantità da acquistare")

        # Imposta il valore di default dello SpinBox
        self.amount_spin_box.setValue(1)

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'acquisto")

        # Nasconde il pulsante di vendita
        self.sale_button.setHidden(True)

        return self

    @classmethod
    def waste(cls, object_description: str, unit_price: float, unit_quantity: int = 1):
        # Inizializza il Dialog
        self = cls(object_description, unit_price, unit_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Vendita scarti di lavorazione")

        # Imposta il testo della Label principale
        self.title.setText(f"Vendi \"{object_description}\"" +
                           ("" if unit_quantity == 1 else f" (x{unit_quantity})"))

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Seleziona la quantità da vendere (kg)")

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sulla vendita")

        # Nasconde il pulsante di vendita
        self.purchase_button.setHidden(True)

        return self

    def __init__(self, object_description: str, unit_price: float, unit_quantity: int = 1):
        super().__init__()

        # Finestra
        self.setObjectName("stored_item_trade_view")

        # Finestra e widget
        self.resize(450, 300)

        # Widget
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")

        # Layout
        self.layout = QVBoxLayout(self.widget)
        self.layout.setObjectName("layout")
        self.layout.setAlignment(Qt.AlignCenter)

        # Frame Layout
        self.frame_layout = HFrameLayout(self)
        self.frame_layout.setSpacerDimensionAndPolicy(50, QSizePolicy.Expanding)
        self.frame_layout.setCentralWidget(self.widget)

        # Titolo
        self.title = QLabel(self)
        font = QFont()
        font.setPointSize(FontSize.SUBTITLE)
        self.title.setFont(font)
        self.title.setContentsMargins(0, 0, 0, 8)
        self.title.setObjectName("title")
        self.layout.addWidget(self.title)

        # Campo Quantità
        self.amount_layout = QVBoxLayout()
        self.layout.addLayout(self.amount_layout)

        # Campo Quantità - Label
        self.amount_label = QLabel(self)
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        font.setWeight(FontWeight.BOLD)
        self.amount_label.setFont(font)
        self.amount_label.setStyleSheet(Styles.ACCESS_LABEL)
        self.amount_label.setContentsMargins(0, 8, 0, 0)
        self.amount_label.setObjectName("amount_label")
        self.amount_layout.addWidget(self.amount_label)

        # Campo Quantità - SpinBox
        self.amount_spin_box = SpinBox(self)
        self.amount_spin_box.setRange(1, 1000)
        self.amount_spin_box.setValue(20)
        self.amount_spin_box.setObjectName("amount_spin_box")
        self.amount_layout.addWidget(self.amount_spin_box)

        # Info - Label
        self.info_label = QLabel(self)
        self.info_label.setFont(font)
        self.info_label.setStyleSheet(Styles.ACCESS_LABEL)
        self.info_label.setContentsMargins(0, 8, 0, 0)
        self.layout.addWidget(self.info_label)

        # Font per lo SpinBox e le Label di informazione
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)

        # Imposta il font per lo SpinBox
        self.amount_spin_box.setFont(font)

        # Prezzo unitario - Label
        self.unit_price_label = QLabel(self)
        self.unit_price_label.setFont(font)
        self.unit_price_label.setText(f"Prezzo unitario: € {PriceFormatter.format(unit_price)}")
        self.layout.addWidget(self.unit_price_label)

        # Quantità effettiva - Label
        self.actual_quantity_label = QLabel(self)
        self.actual_quantity_label.setFont(font)
        self.layout.addWidget(self.actual_quantity_label)

        # Nasconde la Label della quantità effettiva se la quantità per acquisto è uno
        if unit_quantity == 1:
            self.actual_quantity_label.setHidden(True)

        # Prezzo totale - Label
        self.total_price_label = QLabel(self)
        self.total_price_label.setFont(font)
        self.layout.addWidget(self.total_price_label)

        # Pulsanti di acquisto\aggiornamento
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(12)
        self.buttons_layout.setContentsMargins(0, 12, 0, 8)
        self.buttons_layout.setObjectName("buttons_layout")
        self.layout.addLayout(self.buttons_layout)

        # Pulsante di aggiornamento
        '''self.refresh_button = CustomPushButton.white(text="Aggiorna info", point_size=FontSize.FLUENT_DEFAULT)
        self.refresh_button.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.refresh_button.setObjectName("refresh_button")
        self.buttons_layout.addWidget(self.refresh_button)'''

        # Pulsante di acquisto
        self.purchase_button = CustomPushButton.cyan(text="Conferma acquisto", point_size=FontSize.FLUENT_DEFAULT)
        self.purchase_button.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.purchase_button.setObjectName("purchase_button")
        self.buttons_layout.addWidget(self.purchase_button)

        # Pulsante di vendita
        self.sale_button = CustomPushButton.cyan(text="Conferma vendita", point_size=FontSize.FLUENT_DEFAULT)
        self.sale_button.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.sale_button.setObjectName("sale_button")
        self.buttons_layout.addWidget(self.sale_button)

        # Calcola il prezzo totale
        def calculate_total_price() -> float:
            return self.amount_spin_box.value() * unit_price

        # Calcola la quantità effettiva
        def calculate_actual_quantity() -> int:
            return self.amount_spin_box.value() * unit_quantity

        # Aggiorna il prezzo totale e la quantità effettiva indicati
        def refresh_info():
            # Aggiorna il prezzo
            self.total_price_label.setText(f"Prezzo totale: € {PriceFormatter.format(calculate_total_price())}")

            # Aggiorna la quantità
            self.actual_quantity_label.setText(f"Quantità effettiva: {str(calculate_actual_quantity())}")

        self.amount_spin_box.valueChanged.connect(refresh_info)

        # Gestione del pulsante per aggiornare il prezzo totale e la quantità effettiva
        # self.refresh_button.clicked.connect(refresh_info)

        # Aggiorna il prezzo totale e la quantità effettiva
        refresh_info()

        # Eseguito al click sul pulsante di submit della form (caso acquisto)
        def on_purchase():
            # Calcola il prezzo finale di acquisto
            total_price: float = calculate_total_price()

            # Calcola la quantità effettiva (quantità inserita * quantità unitaria)
            actual_quantity: int = calculate_actual_quantity()

            # Crea e mostra una richiesta di conferma con indicato il prezzo
            clicked_button = QMessageBox.question(
                self,
                "Conferma acquisto",
                f"Sei sicuro di voler acquistare \"{object_description}\" (x{actual_quantity}) per € {total_price}?",
                QMessageBox.Yes | QMessageBox.No
            )

            # In caso di conferma, chiude il dialog con accettazione
            if clicked_button == QMessageBox.Yes:
                self.accept()

        # Eseguito al click sul pulsante di submit della form (caso vendita)
        def on_sale():
            # Calcola il prezzo finale di vendita
            total_price: float = calculate_total_price()

            # Calcola la quantità effettiva (quantità inserita * quantità unitaria)
            actual_quantity: int = calculate_actual_quantity()

            # Crea e mostra una richiesta di conferma con indicato il prezzo
            clicked_button = QMessageBox.question(
                self,
                "Conferma vendita",
                f"Sei sicuro di voler vendere \"{object_description}\" ({actual_quantity} kg) per € {total_price}?",
                QMessageBox.Yes | QMessageBox.No
            )

            # In caso di conferma, chiude il dialog con accettazione
            if clicked_button == QMessageBox.Yes:
                self.accept()

        # Collega i Button ai QMessageBox di conferma
        self.purchase_button.clicked.connect(on_purchase)
        self.sale_button.clicked.connect(on_sale)

    def value(self) -> int:
        return self.amount_spin_box.value()
