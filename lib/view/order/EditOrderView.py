from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox

from lib.controller import OrderController
from lib.model.Article import Article
from lib.model.ShoeLastVariety import Gender, ShoeLastType, CompassType, Processing, Shoeing
from lib.repository.OrdersRepository import OrdersRepository
from lib.utility.ObserverClasses import Message, Observer
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.order.OrderFormView import OrderFormView


class EditOrderView(OrderFormView):
    messageReceived = pyqtSignal(Message)

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.controller.detach_order_observer(self.observer)  # Rimuove l'osservatore dall'articolo

    def __init__(self, controller: OrderController):
        super().__init__()

        # Controller
        self.controller = controller

        # Finestra
        self.setObjectName(f"edit_order_{self.controller.get_order_serial()}_view")
        self.setWindowTitle("Modifica ordine")

        # Testo
        self.title.setText(f"Modifica ordine {self.controller.get_order_serial()}")
        self.create_button.setText("Salva modifiche")

        # Popola la form con i dati dell'ordine
        self.prepare_form()

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura e la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(self.on_state_changed_callback)
        self.observer: Observer = self.controller.observe_order(self.messageReceived.emit)

    # Se l'ordine viene messo in lavorazione mentre è in modifica, bisogna chiudere questa vista
    def on_state_changed_callback(self, message: Message):
        if message.event() == OrdersRepository.Event.ORDER_STATE_UPDATED:

            # Informa che l'ordine è stato messo in lavorazione
            QMessageBox.question(
                self,
                "Inizio lavorazione ordine",
                (f"L'ordine non può più essere modificato perché è stato messo in lavorazione. "
                 f"La seguente finestra sarà chiusa."),
                QMessageBox.Ok
            )

            # Se aperto, chiude il QMessageBox di conferma dell'ordine
            for widget in self.children():
                if isinstance(widget, QMessageBox):
                    widget.buttons()[1].click()
                    break

            # Chiude la form di modifica dell'ordine
            self.close()

    # Prepara la form con i dati dell'ordine
    def prepare_form(self):
        article = self.controller.get_order_article()
        shoe_last_variety = article.get_shoe_last_variety()

        # Prepara il ComboBox con il genere
        match shoe_last_variety.get_gender():
            case Gender.UOMO:
                self.gender_combo_box.setCurrentIndex(0)
            case Gender.DONNA:
                self.gender_combo_box.setCurrentIndex(1)
            case _:
                self.gender_combo_box.setCurrentIndex(2)

        # Prepara il ComboBox con la taglia
        for index in range(self.size_combo_box.count()):
            if self.size_combo_box.itemText(index) == shoe_last_variety.get_size():
                self.size_combo_box.setCurrentIndex(index)
                break

        # Prepara il ComboBox con il tipo di forma
        self.type_combo_box.setCurrentIndex(0 if shoe_last_variety.get_shoe_last_type() == ShoeLastType.BASSA else 1)

        # Prepara il ComboBox con il tipo di plastica
        self.plastic_combo_box.setCurrentIndex(shoe_last_variety.get_plastic_type().value - 1)

        # Prepara il ComboBox con il tipo di bussola
        self.first_compass_combo_box.setCurrentIndex(
            0 if shoe_last_variety.get_first_compass_type() == CompassType.STANDARD else 1)

        # Prepara il ComboBox con la seconda bussola
        match shoe_last_variety.get_second_compass_type():
            case CompassType.NESSUNA:
                self.second_compass_combo_box.setCurrentIndex(0)
            case CompassType.STANDARD:
                self.second_compass_combo_box.setCurrentIndex(1)
            case _:
                self.second_compass_combo_box.setCurrentIndex(2)

        # Prepara il ComboBox con la lavorazione principale
        match shoe_last_variety.get_processing():
            case Processing.NESSUNA:
                self.processing_combo_box.setCurrentIndex(0)
            case Processing.CUNEO:
                self.processing_combo_box.setCurrentIndex(1)
            case Processing.SNODO_ALFA:
                self.processing_combo_box.setCurrentIndex(2)
            case _:
                self.processing_combo_box.setCurrentIndex(3)

        # Prepara il ComboBox con la ferratura
        match shoe_last_variety.get_shoeing():
            case Shoeing.NESSUNA:
                self.shoeing_combo_box.setCurrentIndex(0)
            case Shoeing.TACCO_FERRATO:
                self.shoeing_combo_box.setCurrentIndex(1)
            case Shoeing.MEZZA_FERRATA:
                self.shoeing_combo_box.setCurrentIndex(2)
            case _:
                self.shoeing_combo_box.setCurrentIndex(3)

        # Prepara lo SpinBox con il numero di paia
        self.quantity_spin_box.setProperty("value", self.controller.get_order().get_quantity())

        # Prepara il Checkgroup con la numeratura
        self.antineck_check_box.setChecked(shoe_last_variety.get_numbering_antineck())
        self.heel_check_box.setChecked(shoe_last_variety.get_numbering_heel())
        self.lateral_check_box.setChecked(shoe_last_variety.get_numbering_lateral())

        # Prepara il Checkgroup con gli accessori
        self.shoetip_check_box.setChecked(shoe_last_variety.get_iron_tip())
        self.pivot_check_box.setChecked(shoe_last_variety.get_pivot_under_heel())

    # Eseguito al click sul pulsante di submit della form
    def on_submit(self, form_data: dict[str, any]):
        # Calcola il prezzo dell'ordine
        final_price: float = self.controller.calculate_order_price(form_data)

        # Crea e mostra una richiesta di conferma con indicato il prezzo
        clicked_button = QMessageBox.question(
            self,
            "Conferma modifica ordine",
            (f"Il nuovo prezzo dell'ordine è € {PriceFormatter.format(final_price)}.\n"
             f"Sei sicuro di voler modificare l'ordine?"),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, crea l'ordine e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.update_order(form_data, final_price)
            self.close()
