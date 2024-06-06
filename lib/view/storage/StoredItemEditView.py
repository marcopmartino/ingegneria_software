from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from qfluentwidgets import SpinBox

from lib.model.ShoeLastVariety import ProductType
from lib.model.StoredItems import MaterialDescription
from lib.utility.gui.layout.FrameLayouts import HFrameLayout
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from lib.utility.gui.widget.Separators import HorizontalLine, VerticalSpacer
from res import Styles
from res.Dimensions import GenericDimensions, FontSize, FontWeight


class StoredItemEditView(QDialog):

    @classmethod
    def shoe_last(cls, object_description: str, current_quantity: int, product_type: ProductType):
        # Inizializza il Dialog
        self = cls(object_description, current_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Modifica quantità forme")

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Quantità in magazzino (paia)")

        # Imposta il testo della Label con informazioni sull'aggiornamento automatico della quantità
        self.automatic_operation_info_label.setText(
            ("Le quantità degli abbozzi vengono modificate automaticamente tramite acquisto e utilizzo nei macchinari"
             if product_type == ProductType.ABBOZZO else
             "Le quantità degli abbozzi sgrossati vengono modificate automaticamente tramite utilizzo nei macchinari"
             if product_type == ProductType.ABBOZZO_SGROSSATO else
             "Le quantità delle forme finite vengono modificate automaticamente tramite utilizzo nei macchinari"
             if product_type == ProductType.FORMA_FINITA else
             "Le quantità delle forme numerate vengono modificate automaticamente tramite utilizzo nei macchinari e "
             "completamento degli ordini")
            + ": modificare la quantità immagazzinata solo in casi eccezionali (stop di emergenza o malfunzionamento "
              "di un macchinario, rottura accidentale di un oggetto immagazzinato, ecc.)"
        )

        # Imposta l'altezza della Label con informazioni sull'aggiornamento automatico della quantità
        self.update_automatic_operation_info_label_height()

        return self

    @classmethod
    def material(cls, object_description: str, current_quantity: int, material_description: MaterialDescription):
        # Inizializza il Dialog
        self = cls(object_description, current_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Modifica quantità materiali di lavorazione")

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Quantità in magazzino")

        # Imposta il testo della Label con informazioni sull'aggiornamento automatico della quantità
        self.automatic_operation_info_label.setText(
            "La quantità dell'inchiostro indelebile viene aumentata automaticamente tramite acquisto: modificare la "
            "quantità solo per diminuirla in accordo con l'uso che se ne fa nei macchinari, o in casi eccezionali ("
            "rottura accidentale dei contenitori di inchiostro, ecc.)"
            if material_description == MaterialDescription.INCHIOSTRO else
            "Le quantità dei materiali vengono modificate automaticamente tramite acquisto e utilizzo nei macchinari: "
            "modificare la quantità immagazzinata solo in casi eccezionali (stop di emergenza o malfunzionamento di "
            "un macchinario, rottura accidentale di un oggetto immagazzinato, ecc.)"
        )

        # Imposta l'altezza della Label con informazioni sull'aggiornamento automatico della quantità
        self.update_automatic_operation_info_label_height()

        return self

    @classmethod
    def waste(cls, object_description: str, current_quantity: int):
        # Inizializza il Dialog
        self = cls(object_description, current_quantity)

        # Imposta il titolo del Dialog
        self.setWindowTitle("Modifica quantità scarti di lavorazione")

        # Imposta il testo della Label dello SpinBox
        self.amount_label.setText("Quantità in magazzino (kg)")

        # Imposta il testo della Label con informazioni sull'aggiornamento automatico della quantità
        self.automatic_operation_info_label.setText(
            "La quantità degli scarti di lavorazione viene diminuita automaticamente tramite vendita: modificare la "
            "quantità solo per aumentarla in accordo con quella prodotta dai macchinari, o in caso di smaltimento "
            "degli scarti tramite altri metodi."
        )

        # Imposta l'altezza della Label con informazioni sull'aggiornamento automatico della quantità
        self.update_automatic_operation_info_label_height()

        return self

    def __init__(self, object_description: str, current_quantity: int):
        super().__init__()

        # Finestra
        self.setObjectName("stored_item_edit_view")

        # Finestra
        self.resize(450, 300)
        self.setMinimumWidth(350)

        # Widget
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        self.widget.setMaximumWidth(600)

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

        # Abilita il testo della Label principale ad andare a capo automaticamente
        self.title.setWordWrap(True)

        # Imposta il testo del Titolo, la label principale della finestra
        self.title.setText(f"Modifica \"{object_description}\"")

        # Imposta l'altezza della Label titolo
        self.update_title_label_height()

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
        self.amount_spin_box.setObjectName("amount_spin_box")
        self.amount_layout.addWidget(self.amount_spin_box)

        # Imposta il valore di default dello SpinBox
        self.amount_spin_box.setValue(current_quantity)

        # Info - Label
        self.info_label = QLabel(self)
        self.info_label.setFont(font)
        self.info_label.setStyleSheet(Styles.ACCESS_LABEL)
        self.info_label.setContentsMargins(0, 8, 0, 0)
        self.layout.addWidget(self.info_label)

        # Imposta il testo della Label di informazione
        self.info_label.setText("Informazioni sull'operazione")

        # Font per lo SpinBox e le Label di informazione
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)

        # Imposta il font per lo SpinBox
        self.amount_spin_box.setFont(font)

        # Quantità attuale - Label
        self.actual_quantity_label = QLabel(self)
        self.actual_quantity_label.setFont(font)
        self.actual_quantity_label.setText(f"Quantità attuale: {current_quantity}")
        self.layout.addWidget(self.actual_quantity_label)

        # Nuova quantità - Label
        self.post_edit_quantity_label = QLabel(self)
        self.post_edit_quantity_label.setFont(font)
        self.layout.addWidget(self.post_edit_quantity_label)

        # Riga orizzontale
        self.layout.addItem(VerticalSpacer(8))
        self.layout.addWidget(HorizontalLine(self))
        self.layout.addItem(VerticalSpacer(8))

        # Info - Label
        self.automatic_operation_info_label = QLabel(self)
        self.automatic_operation_info_label.setFont(font)
        self.automatic_operation_info_label.setWordWrap(True)
        self.layout.addWidget(self.automatic_operation_info_label)

        # Pulsanti di aggiornamento
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(12)
        self.buttons_layout.setContentsMargins(0, 12, 0, 8)
        self.buttons_layout.setObjectName("buttons_layout")
        self.layout.addLayout(self.buttons_layout)

        # Pulsante di conferma
        self.confirm_change_button = CustomPushButton.cyan(text="Conferma modifiche",
                                                           point_size=FontSize.FLUENT_DEFAULT)
        self.confirm_change_button.setFixedHeight(GenericDimensions.FORM_BUTTON_HEIGHT)
        self.confirm_change_button.setObjectName("confirm_change_button")
        self.buttons_layout.addWidget(self.confirm_change_button)

        # Mostra la nuova quantità in relazione con quella attuale
        def refresh_info():
            # Ottiene la nuova quantità
            new_quantity = self.amount_spin_box.value()

            # Aggiorna la nuova quantità
            self.post_edit_quantity_label.setText(f"Nuova quantità: {str(new_quantity)}")

        self.amount_spin_box.valueChanged.connect(refresh_info)

        # Aggiorna le informazioni
        refresh_info()

        # Eseguito al click sul pulsante di submit della form
        def on_confirm():
            # Ottiene la quantità modificata
            new_quantity = self.amount_spin_box.value()

            # Se la quantità non è cambiata, chiude il dialog
            if new_quantity == current_quantity:
                self.close()

            # Altrimenti chiede la conferma della modifica
            else:
                # Crea e mostra una richiesta di conferma
                clicked_button = QMessageBox.question(
                    self,
                    "Conferma modifiche",
                    f"Sei sicuro di voler modifica \"{object_description}\" da {current_quantity} a {new_quantity}?",
                    QMessageBox.Yes | QMessageBox.No
                )

                # In caso di conferma, chiude il dialog con accettazione
                if clicked_button == QMessageBox.Yes:
                    self.accept()

        # Collega i Button ai QMessageBox di conferma
        self.confirm_change_button.clicked.connect(on_confirm)

    def value(self) -> int:
        return self.amount_spin_box.value()

    # Imposta l'altezza della Label di info sulla modifica automatica della quantità
    def update_automatic_operation_info_label_height(self):
        max_extra_lines = 0

        string_length = len(self.automatic_operation_info_label.text())
        extra_lines = string_length // 40

        if extra_lines > max_extra_lines:
            max_extra_lines = extra_lines

        self.automatic_operation_info_label.setFixedHeight(20 + 20 * max_extra_lines)

    # Imposta l'altezza della Label titolo
    def update_title_label_height(self):
        max_extra_lines = 0

        string_length = len(self.title.text())
        extra_lines = string_length // 30

        if extra_lines > max_extra_lines:
            max_extra_lines = extra_lines

        self.title.setFixedHeight(30 + 30 * max_extra_lines)
