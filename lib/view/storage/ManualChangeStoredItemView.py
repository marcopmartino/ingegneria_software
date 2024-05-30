from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from qfluentwidgets import SpinBox

from lib.layout.FrameLayouts import HFrameLayout
from lib.widget.CustomPushButton import CustomPushButton
from res import Styles
from res.Dimensions import GenericDimensions, FontSize, FontWeight


class ManualChangeStoredItemView(QDialog):

    @classmethod
    def raw_shoe_last(cls, object_description: str, unit_quantity: int):
        # Inizializza il Dialog
        self = cls(object_description, unit_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Modifica quantità abbozzi")

        # Imposta il testo della Label principale
        self.title.setText(f"Modifica \"{object_description}\"")
        self.title.setWordWrap(True)

        # Imposta il valore di default dello SpinBox
        self.amount_spin_box.setValue(unit_quantity)

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'acquisto")

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Quantità in magazzino (paia)")

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'operazione")

        return self

    @classmethod
    def material(cls, object_description: str, unit_quantity: int):
        # Inizializza il Dialog
        self = cls(object_description, unit_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Modifica quantità materiali di lavorazione")

        # Imposta il testo della Label principale
        self.title.setText(f"Modifica \"{object_description}\"")
        self.title.setWordWrap(True)

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Quantità in magazzino")

        # Imposta il valore di default dello SpinBox
        self.amount_spin_box.setValue(unit_quantity)

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'operazione")

        return self

    @classmethod
    def waste(cls, object_description: str, unit_quantity: int):
        # Inizializza il Dialog
        self = cls(object_description, unit_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Modifica scarti di lavorazione")

        # Imposta il testo della Label principale
        self.title.setText(f"Modifica \"{object_description}\"")
        self.title.setWordWrap(True)

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Quantità in magazzino (kg)")

        # Imposta il valore di default dello SpinBox
        self.amount_spin_box.setValue(unit_quantity)

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'operazione")

        return self

    def __init__(self, object_description: str, unit_quantity: int):
        super().__init__()

        # Finestra
        self.setObjectName("manual_change_stored_item_view")

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
        self.amount_spin_box.setRange(0, 1000)
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

        # Quantità attuale - Label
        self.actual_quantity_label = QLabel(self)
        self.actual_quantity_label.setFont(font)
        self.actual_quantity_label.setText(f"Quantità attuale:  {unit_quantity}")
        self.layout.addWidget(self.actual_quantity_label)

        # Nuova quantità - Label
        self.post_edit_quantity_label = QLabel(self)
        self.post_edit_quantity_label.setFont(font)
        self.layout.addWidget(self.post_edit_quantity_label)

        # Pulsanti di aggiornamento
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(12)
        self.buttons_layout.setContentsMargins(0, 12, 0, 8)
        self.buttons_layout.setObjectName("buttons_layout")
        self.layout.addLayout(self.buttons_layout)

        # Pulsante di conferma
        self.confirm_change_button = CustomPushButton.cyan(text="Conferma modifiche", point_size=FontSize.FLUENT_DEFAULT)
        self.confirm_change_button.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.confirm_change_button.setObjectName("confirm_change_button")
        self.buttons_layout.addWidget(self.confirm_change_button)

        # Mostra la nuova quantità in relazione con quella attuale
        def refresh_info():
            # Aggiorna il prezzo
            self.actual_quantity_label.setText(f"Quantità attuale: {unit_quantity}")

            new_quantity = self.amount_spin_box.value()
            # Aggiorna la quantità
            self.post_edit_quantity_label.setText(f"Nuova quantità: {str(new_quantity)}")

        self.amount_spin_box.valueChanged.connect(refresh_info)

        # Aggiorna le informazioni
        refresh_info()

        # Eseguito al click sul pulsante di submit della form
        def on_confirm():
            # Ottiene la quantità modificata
            new_quantity: str = str(self.amount_spin_box.value())

            # Crea e mostra una richiesta di conferma
            clicked_button = QMessageBox.question(
                self,
                "Conferma modifiche",
                f"Sei sicuro di voler modifica \"{object_description}\" da {unit_quantity} a {new_quantity}?",
                QMessageBox.Yes | QMessageBox.No
            )

            # In caso di conferma, chiude il dialog con accettazione
            if clicked_button == QMessageBox.Yes:
                self.accept()

        # Collega i Button ai QMessageBox di conferma
        self.confirm_change_button.clicked.connect(on_confirm)

    def value(self) -> int:
        return self.amount_spin_box.value()
