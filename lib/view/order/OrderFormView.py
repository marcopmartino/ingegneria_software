from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLabel, QGridLayout, \
    QDialog, QMessageBox
from qfluentwidgets import ComboBox, SpinBox, CheckBox, PushButton, PrimaryPushButton

from lib.controller.OrderFormController import OrderFormController
from lib.controller.OrderListController import OrderListController
from lib.layout.FrameLayouts import HFrameLayout, VFrameLayout
from lib.controller.PriceCatalogController import PriceCatalogController
from lib.model.Order import Order
from lib.repository.PriceCatalogRepository import PriceCatalogRepository
from lib.utility.UtilityClasses import PriceFormatter
from lib.validation.FormManager import FormManager
from res.Dimensions import FontWeight, FontSize


# Metaclasse per OrderFormView
class OrderFormViewMeta(type(QDialog), type(ABC)):
    pass


# Classe astratta per la vista con la form dell'ordine (usata per inserimento e modifica ordine)
class OrderFormView(QDialog, ABC, metaclass=OrderFormViewMeta):
    def __init__(self):
        super().__init__()

        # Controller
        self.controller: OrderFormController
        self.controller = None

        # Finestra e widget
        self.resize(800, 550)

        # Layout
        self.layout = HFrameLayout(self)
        self.layout.setObjectName("layout")
        self.layout.setSpacerDimensionAndPolicy(150, QSizePolicy.Expanding)

        # Widget centrale
        self.central_widget = QWidget(self)
        self.central_widget.setMaximumHeight(800)
        self.central_widget.setObjectName("central_widget")

        # Layout centrale
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setSpacing(12)
        self.central_layout.setObjectName("central_layout")

        # Titolo della form
        self.title = QLabel(self.central_widget)
        font = QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("title")
        self.central_layout.addWidget(self.title)

        # Widget con i campi della form
        self.form_widget = QWidget(self.central_widget)
        self.form_widget.setMaximumHeight(600)
        self.form_widget.setObjectName("form_widget")

        # Layout con i campi della form
        self.form_layout = QHBoxLayout(self.form_widget)
        self.form_layout.setSpacing(16)
        self.form_layout.setObjectName("form_layout")

        # Layout sinistro della form
        self.left_form_layout = QGridLayout()
        self.left_form_layout.setSpacing(12)
        self.left_form_layout.setObjectName("gridLayout")

        # Campo Genere - Label
        self.gender_label = QLabel(self.form_widget)
        self.gender_label.setLayoutDirection(Qt.LeftToRight)
        self.gender_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gender_label.setObjectName("gender_label")
        self.left_form_layout.addWidget(self.gender_label, 0, 0, 1, 1)

        # Campo Genere - ComboBox
        self.gender_combo_box = ComboBox(self.form_widget)
        self.gender_combo_box.setObjectName("gender_combo_box")
        self.left_form_layout.addWidget(self.gender_combo_box, 0, 1, 1, 1)

        # Campo Taglia - Label
        self.size_label = QLabel(self.form_widget)
        self.size_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.size_label.setObjectName("size_label")
        self.left_form_layout.addWidget(self.size_label, 1, 0, 1, 1)

        # Campo Taglia - ComboBox
        self.size_combo_box = ComboBox(self.form_widget)
        self.size_combo_box.setObjectName("size_combo_box")
        self.left_form_layout.addWidget(self.size_combo_box, 1, 1, 1, 1)

        # Campo Tipo di forma - Label
        self.type_label = QLabel(self.form_widget)
        self.type_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.type_label.setObjectName("type_label")
        self.left_form_layout.addWidget(self.type_label, 2, 0, 1, 1)

        # Campo Tipo di forma - Combo Box
        self.type_combo_box = ComboBox(self.form_widget)
        self.type_combo_box.setObjectName("type_combo_box")
        self.left_form_layout.addWidget(self.type_combo_box, 2, 1, 1, 1)

        # Campo Tipo di plastica - Label
        self.plastic_label = QLabel(self.form_widget)
        self.plastic_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.plastic_label.setObjectName("plastic_label")
        self.left_form_layout.addWidget(self.plastic_label, 3, 0, 1, 1)

        # Campo Tipo di plastica - ComboBox
        self.plastic_combo_box = ComboBox(self.form_widget)
        self.plastic_combo_box.setObjectName("plastic_combo_box")
        self.left_form_layout.addWidget(self.plastic_combo_box, 3, 1, 1, 2)

        # Campo Prima bussola - Label
        self.first_compass_label = QLabel(self.form_widget)
        self.first_compass_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.first_compass_label.setObjectName("first_compass_label")
        self.left_form_layout.addWidget(self.first_compass_label, 4, 0, 1, 1)

        # Campo Prima bussola - ComboBox
        self.first_compass_combo_box = ComboBox(self.form_widget)
        self.first_compass_combo_box.setObjectName("first_compass_combo_box")
        self.left_form_layout.addWidget(self.first_compass_combo_box, 4, 1, 1, 2)

        # Campo Seconda bussola - Label
        self.second_compass_label = QLabel(self.form_widget)
        self.second_compass_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.second_compass_label.setObjectName("second_compass_label")
        self.left_form_layout.addWidget(self.second_compass_label, 5, 0, 1, 1)

        # Campo Seconda bussola - ComboBox
        self.second_compass_combo_box = ComboBox(self.form_widget)
        self.second_compass_combo_box.setObjectName("second_compass_combo_box")
        self.left_form_layout.addWidget(self.second_compass_combo_box, 5, 1, 1, 2)

        # Campo Lavorazione - Label
        self.processing_label = QLabel(self.form_widget)
        self.processing_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.processing_label.setObjectName("processing_label")
        self.left_form_layout.addWidget(self.processing_label, 6, 0, 1, 1)

        # Campo Lavorazione - ComboBox
        self.processing_combo_box = ComboBox(self.form_widget)
        self.processing_combo_box.setObjectName("processing_combo_box")
        self.left_form_layout.addWidget(self.processing_combo_box, 6, 1, 1, 2)

        # Campo Ferratura - Label
        self.shoeing_label = QLabel(self.form_widget)
        self.shoeing_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.shoeing_label.setObjectName("shoeing_label")
        self.left_form_layout.addWidget(self.shoeing_label, 7, 0, 1, 1)

        # Campo Ferratura - ComboBox
        self.shoeing_combo_box = ComboBox(self.form_widget)
        self.shoeing_combo_box.setObjectName("shoeing_combo_box")
        self.left_form_layout.addWidget(self.shoeing_combo_box, 7, 1, 1, 2)

        # Campo Quantità - Label
        self.quantity_label = QLabel(self.form_widget)
        self.quantity_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.quantity_label.setObjectName("quantity_label")
        self.left_form_layout.addWidget(self.quantity_label, 8, 0, 1, 1)

        # Campo Quantità - SpinBox
        self.quantity_spin_box = SpinBox(self.form_widget)
        self.quantity_spin_box.setAlignment(Qt.AlignCenter)
        self.quantity_spin_box.setSuffix("")
        self.quantity_spin_box.setMinimum(1)
        self.quantity_spin_box.setMaximum(250)
        self.quantity_spin_box.setSingleStep(5)
        self.quantity_spin_box.setProperty("value", 20)
        self.quantity_spin_box.setObjectName("quantity_spin_box")
        self.left_form_layout.addWidget(self.quantity_spin_box, 8, 1, 1, 1)

        # Campo Quantità - Seconda Label
        self.quantity_unit_label = QLabel(self.form_widget)
        self.quantity_unit_label.setObjectName("quantity_unit_label")
        self.left_form_layout.addWidget(self.quantity_unit_label, 8, 2, 1, 1)

        self.form_layout.addLayout(self.left_form_layout)

        # Spacer posto tra la parte sinistra e la parte destra della form
        inner_central_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.form_layout.addItem(inner_central_spacer)

        # Layout destro della form
        self.right_form_layout = VFrameLayout()
        self.right_form_layout.setObjectName("right_form_layout")
        self.right_form_layout.setSpacerDimensionsAndPolicy(20, 140, QSizePolicy.Expanding)

        # Layout che comprende i due gruppi di checkbox
        self.outer_checkgroup_layout = QVBoxLayout()
        self.outer_checkgroup_layout.setSpacing(24)
        self.outer_checkgroup_layout.setObjectName("outer_checkgroup_layout")

        # Layout con il primo checkgroup
        self.first_checkgroup_layout = QVBoxLayout()
        self.first_checkgroup_layout.setSpacing(12)
        self.first_checkgroup_layout.setObjectName("first_checkgroup_layout")

        # Checkgroup Numeratura - Label
        self.marking_group_label = QLabel(self.form_widget)
        self.marking_group_label.setObjectName("marking_group_label")
        self.first_checkgroup_layout.addWidget(self.marking_group_label)

        # CheckBox Numerazione
        self.numbering_check_box = CheckBox(self.form_widget)
        self.numbering_check_box.setEnabled(False)
        self.numbering_check_box.setChecked(True)
        self.numbering_check_box.setObjectName("numbering_check_box")
        self.first_checkgroup_layout.addWidget(self.numbering_check_box)

        # CheckBox Segno anticollo
        self.antineck_check_box = CheckBox(self.form_widget)
        self.antineck_check_box.setObjectName("antineck_check_box")
        self.first_checkgroup_layout.addWidget(self.antineck_check_box)

        # CheckBox Segni laterali
        self.lateral_check_box = CheckBox(self.form_widget)
        self.lateral_check_box.setObjectName("lateral_check_box")
        self.first_checkgroup_layout.addWidget(self.lateral_check_box)

        # CheckBox Segno sul tallone
        self.heel_check_box = CheckBox(self.form_widget)
        self.heel_check_box.setObjectName("heel_check_box")
        self.first_checkgroup_layout.addWidget(self.heel_check_box)
        self.outer_checkgroup_layout.addLayout(self.first_checkgroup_layout)

        # Layout con il secondo checkgroup
        self.second_checkgroup_layout = QVBoxLayout()
        self.second_checkgroup_layout.setSpacing(12)
        self.second_checkgroup_layout.setObjectName("second_checkgroup_layout")

        # Checkgroup Accessori - Label
        self.accessories_group_label = QLabel(self.form_widget)
        self.accessories_group_label.setObjectName("accessories_group_label")
        self.second_checkgroup_layout.addWidget(self.accessories_group_label)

        # CheckBox Perno sotto tallone
        self.pivot_check_box = CheckBox(self.form_widget)
        self.pivot_check_box.setObjectName("pivot_check_box")
        self.second_checkgroup_layout.addWidget(self.pivot_check_box)

        # CheckBox Punta ferrata
        self.shoetip_check_box = CheckBox(self.form_widget)
        self.shoetip_check_box.setObjectName("shoetip_check_box")
        self.second_checkgroup_layout.addWidget(self.shoetip_check_box)
        self.outer_checkgroup_layout.addLayout(self.second_checkgroup_layout)
        self.right_form_layout.setCentralLayout(self.outer_checkgroup_layout)

        # Prezzo dell'ordine - Label
        self.price_label = QLabel(self.form_widget)
        font = QFont()
        font.setBold(True)
        font.setPointSize(FontSize.TABLE_HEADER)
        font.setWeight(FontWeight.BOLD)
        self.price_label.setFont(font)
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setObjectName("price_label")
        self.right_form_layout.addWidget(self.price_label)

        self.form_layout.addLayout(self.right_form_layout)
        self.central_layout.addWidget(self.form_widget)

        # Layout con i pulsanti
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(24)
        self.button_layout.setObjectName("button_layout")

        # Spacer laterali sezione pulsanti
        bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.insertItem(0, bottom_spacer)
        self.button_layout.insertItem(3, bottom_spacer)

        # Pulsante per aggiornare il prezzo dell'ordine
        self.refresh_button = PushButton(self.central_widget)
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.setFixedSize(200, 40)
        self.button_layout.insertWidget(1, self.refresh_button)

        # Pulsante per creare e inviare l'ordine
        self.create_button = PrimaryPushButton(self.central_widget)
        self.create_button.setObjectName("create_button")
        self.create_button.setFixedSize(200, 40)
        self.button_layout.insertWidget(2, self.create_button)

        self.central_layout.addLayout(self.button_layout)
        self.layout.setCentralWidget(self.central_widget)

        # Testo
        self.title.setText("Nuovo ordine")
        self.gender_label.setText("Seleziona genere:")
        self.gender_combo_box.insertItem(0, "Uomo", userData="uomo")
        self.gender_combo_box.insertItem(1, "Donna", userData="donna")
        self.gender_combo_box.insertItem(2, "Bambino", userData="bambino")
        self.gender_combo_box.setCurrentIndex(0)
        self.size_label.setText("Seleziona taglia:")
        self.type_label.setText("Seleziona tipo forma:")
        self.type_combo_box.insertItem(0, "Bassa", userData="bassa")
        self.type_combo_box.insertItem(1, "Polacco", userData="polacco")
        self.type_combo_box.setCurrentIndex(0)
        self.plastic_label.setText("Seleziona tipo/qualità plastica:")
        self.plastic_combo_box.insertItem(0, "Tipo 1 - Discreta", userData=1)
        self.plastic_combo_box.insertItem(1, "Tipo 2 - Buona", userData=2)
        self.plastic_combo_box.insertItem(2, "Tipo 3 - Ottima", userData=3)
        self.plastic_combo_box.setCurrentIndex(0)
        self.first_compass_label.setText("Seleziona prima bussola:")
        self.first_compass_combo_box.insertItem(0, "Standard", userData=False)
        self.first_compass_combo_box.insertItem(1, "Rinforzata", userData=True)
        self.first_compass_combo_box.setCurrentIndex(0)
        self.second_compass_label.setText("Seleziona seconda bussola:")
        self.second_compass_combo_box.insertItem(0, "Nessuna", userData="nessuna")
        self.second_compass_combo_box.insertItem(1, "Standard", userData="standard")
        self.second_compass_combo_box.insertItem(2, "Rinforzata", userData="rinforzata")
        self.second_compass_combo_box.setCurrentIndex(0)
        self.processing_label.setText("Seleziona lavorazione:")
        self.processing_combo_box.insertItem(0, "Nessuna (forma intera)", userData="nessuna")
        self.processing_combo_box.insertItem(1, "Cuneo", userData="cuneo")
        self.processing_combo_box.insertItem(2, "Snodo alfa", userData="alfa")
        self.processing_combo_box.insertItem(3, "Snodo tendo", userData="tendo")
        self.processing_combo_box.setCurrentIndex(0)
        self.shoeing_label.setText("Seleziona ferratura:")
        self.shoeing_combo_box.insertItem(0, "Nessuna (forma liscia)", userData="nessuna")
        self.shoeing_combo_box.insertItem(1, "Tacco ferrato", userData="tacco")
        self.shoeing_combo_box.insertItem(2, "Mezza ferrata", userData="mezza")
        self.shoeing_combo_box.insertItem(3, "Tutta ferrata", userData="tutta")
        self.shoeing_combo_box.setCurrentIndex(0)
        self.quantity_label.setText("Inserisci quantità:")
        self.quantity_unit_label.setText("paia")
        self.marking_group_label.setText("Seleziona segni e linee:")
        self.numbering_check_box.setText("Numerazione seriale")
        self.antineck_check_box.setText("Segno anticollo")
        self.lateral_check_box.setText("Segni laterali")
        self.heel_check_box.setText("Segno sul tallone")
        self.accessories_group_label.setText("Seleziona altri accessori:")
        self.pivot_check_box.setText("Perno sotto tallone")
        self.shoetip_check_box.setText("Punta ferrata")
        self.price_label.setText("Prezzo ordine: € 0.00")
        self.refresh_button.setText("Aggiorna prezzo ordine")

        # Form
        self.form_manager: FormManager = FormManager()
        self.form_manager.add_widget_fields(self.form_widget)
        self.form_manager.add_data_button(self.create_button, self.on_submit)

        # Gestione del pulsante per aggiornare il prezzo
        self.refresh_button.clicked.connect(self.refresh_price)

        # Inizializza il ComboBox con le taglie
        self.on_gender_selected()

        # Aggiorna il ComboBox con le taglie ad ogni modifica del genere
        self.gender_combo_box.currentIndexChanged.connect(self.on_gender_selected)

    @abstractmethod
    # Eseguito al click sul pulsante di submit della form
    def on_submit(self, form_data: dict[str, any]):
        pass

    # Aggiorna il prezzo indicato
    def refresh_price(self):
        new_price: float = self.controller.calculate_order_price(self.form_manager.data())
        self.price_label.setText(f"Prezzo finale: € {PriceFormatter.format(new_price)}")

    # Aggiorna il ComboBox con le taglie in base al genere di forma selezionato
    def on_gender_selected(self):
        text: str = self.gender_combo_box.currentText()
        self.size_combo_box.clear()
        match text:
            case "Uomo":
                self.size_combo_box.addItems(
                    ["34", "34.5", "35", "35.5", "36", "36.5", "37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5",
                     "41", "41.5", "42", "42.5", "43", "43.5", "44", "44.5", "45", "45.5", "46", "46.5", "47", "47.5",
                     "48"]
                )
                self.size_combo_box.setCurrentIndex(16)
            case "Donna":
                self.size_combo_box.addItems(
                    ["34", "34.5", "35", "35.5", "36", "36.5", "37", "37.5", "38", "38.5", "39", "39.5", "40", "40.5",
                     "41", "41.5", "42", "42.5", "43", "43.5", "44"]
                )
                self.size_combo_box.setCurrentIndex(8)
            case "Bambino":
                self.size_combo_box.addItems(
                    ["18", "18.5", "19", "19.5", "20", "20.5", "21", "21.5", "22", "22.5", "23", "23.5", "24", "24.5",
                     "25", "25.5", "26", "26.5", "27", "27.5", "28", "28.5", "29", "29.5", "30", "30.5", "31", "31.5",
                     "32", "32.5", "33", "33.5"]
                )
                self.size_combo_box.setCurrentIndex(12)
