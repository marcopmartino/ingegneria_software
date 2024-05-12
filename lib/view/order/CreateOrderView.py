from PyQt5.QtWidgets import QMessageBox

from lib.controller.OrderListController import OrderListController
from lib.utility.UtilityClasses import PriceFormatter
from lib.view.order.OrderFormView import OrderFormView


class CreateOrderView(OrderFormView):

    def __init__(self, controller: OrderListController):
        super().__init__()

        # Controller
        self.controller = controller

        # Finestra
        self.setObjectName("create_order_view")
        self.setWindowTitle("Creazione ordine")

        # Testo
        self.title.setText("Nuovo ordine")
        self.create_button.setText("Crea e invia ordine")

    # Eseguito al click sul pulsante di submit della form
    def on_submit(self, form_data: dict[str, any]):
        # Calcola il prezzo dell'ordine
        final_price: float = self.controller.calculate_order_price(form_data)

        # Crea e mostra una richiesta di conferma con indicato il prezzo
        clicked_button = QMessageBox.question(
            self,
            "Conferma creazione ordine",
            (f"Il prezzo dell'ordine è € {PriceFormatter.format(final_price)}.\n"
             f"Sei sicuro di voler creare e inviare l'ordine?"),
            QMessageBox.Yes | QMessageBox.No
        )

        # In caso di conferma, crea l'ordine e chiude la finestra
        if clicked_button == QMessageBox.Yes:
            self.controller.create_order(form_data, final_price)
            self.close()
