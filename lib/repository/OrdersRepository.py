from __future__ import annotations

from enum import Enum

from lib.firebaseData import currentUserId
from lib.model.Order import Order
from lib.network.OrderNetwork import OrderNetwork
from lib.utility.ObserverClasses import Observable, Message
from lib.utility.Singleton import ObservableSingleton
from lib.utility.UtilityClasses import DatetimeUtils
from res.Strings import OrderStateStrings


class OrdersRepository(Observable, metaclass=ObservableSingleton):
    class Event(Enum):
        ORDER_CREATED = 0
        ORDER_DELETED = 1
        ORDER_UPDATED = 2
        ORDER_STATE_UPDATED = 3

    def __init__(self):
        super().__init__()
        self.__order_list: list[Order] = []  # Inizializza la lista degli ordini
        self.__order_network = OrderNetwork()
        self.__order_network.stream(self.__stream_handler)

    # Usato internamente per istanziare e aggiungere un nuovo ordine alla lista
    def __instantiate_and_append_order(self, serial: str, data: any) -> Order:
        order = Order(
            serial, data["article_serial"], data["state"], data["customer_id"], data["quantity"],
            data["price"], data.get("first_product_serial", -1), data["creation_date"]
        )
        self.__order_list.append(order)
        return order

    # Stream handler che aggiorna automaticamente la lista degli ordini
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorna la lista degli ordini così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:

            # Ottenimento\inserimento\eliminazione di ordini
            case "put":

                # All'avvio del programma, quando viene caricata l'intera lista di ordini
                if path == "/":
                    # Se c'è almeno un ordine nella lista
                    if data:
                        for key, value in data.items():
                            # Crea e aggiunge un ordine alla lista di ordini della repository
                            self.__instantiate_and_append_order(key, value)

                # Se il path è diverso allora siamo nell'ambito di un singolo ordine della lista
                else:
                    # Estrae il seriale dell'ordine dal path
                    order_serial = path.split("/")[1]

                    # Quando viene creato un nuovo ordine, data non è None
                    if data:
                        # Crea e aggiunge un ordine alla lista di ordini della repository
                        order = self.__instantiate_and_append_order(order_serial, data)

                        # Prepara il messaggio per notificare gli osservatori della lista degli ordini
                        message = Message(OrdersRepository.Event.ORDER_CREATED, order)

                    # Quando viene eliminato un ordine, data è None
                    else:
                        for order in self.__order_list:
                            if order.get_order_serial() == order_serial:
                                # Rimuove l'ordine dalla lista
                                self.__order_list.remove(order)

                                # Prepara il messaggio per notificare gli osservatori della lista degli ordini
                                message = Message(OrdersRepository.Event.ORDER_DELETED)
                                order.notify(message)  # Notifica eventuali osservatori del singolo ordine
                                message.setData(order_serial)
                                break

                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                self.notify(message)

            # Aggiornamento di un ordine
            case "patch":
                # Estrae il seriale dell'ordine dal path
                order_serial = path.split("/")[1]

                print("Updating order " + order_serial)

                # Prende l'ordine corrispondente
                order = self.get_order_by_id(order_serial)

                print("Found order " + order.__str__())

                # Caso di aggiornamento dello stato dell'ordine
                if data.get("state", False):
                    # Estraggo i dati
                    new_state: str = data.get("state")

                    # Aggiorna l'ordine nella lista
                    order.set_state(new_state)

                    # Prepara il messaggio per notificare gli osservatori della lista degli ordini
                    message = Message(OrdersRepository.Event.ORDER_STATE_UPDATED)
                    order.notify(message)  # Notifica eventuali osservatori del singolo ordine
                    message.setData(order)

                # Caso di aggiornamento dell'articolo dell'ordine
                else:
                    # Estraggo i dati (possono essere None se rimasti invariati)
                    article_serial: str | None = data.get("article_serial")
                    price: float | None = data.get("price")
                    quantity: int | None = data.get("quantity")

                    # Aggiorna l'ordine nella lista
                    if article_serial is not None:
                        order.set_article_serial(article_serial)
                    if price is not None:
                        order.set_price(price)
                    if quantity is not None:
                        order.set_quantity(quantity)

                    # Prepara il messaggio per notificare gli osservatori della lista degli ordini
                    message = Message(OrdersRepository.Event.ORDER_UPDATED)
                    order.notify(message)  # Notifica eventuali osservatori del singolo ordine
                    message.setData(order)

                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                self.notify(message)

            # Terminazione imprevista dello stream
            case "cancel":
                pass

    # Ritorna una copia della lista degli ordini
    def get_order_list(self) -> list[Order]:
        return self.__order_list

    # Cerca un ordine in base al suo numero di serie e lo ritorna
    def get_order_by_id(self, order_serial: str) -> Order:
        for order in self.__order_list:
            if order.get_order_serial() == order_serial:
                return order

    # Salva il nuovo ordine nel database. Il seriale è rimosso perché viene assegnato automaticamente.
    def create_order(self, article_serial: str, quantity: int, price: float) -> str:
        # Crea un dizionario con i dati del nuovo ordine
        order_data = dict(
            article_serial=article_serial,
            quantity=quantity,
            price=price,
            creation_date=DatetimeUtils.current_date(),
            customer_id=currentUserId(),
            state=OrderStateStrings.NOT_STARTED
        )
        # Salva l'ordine nel database e ne ritorna l'id
        return self.__order_network.insert(order_data)

    # Aggiorna un ordine
    def update_order_by_id(self, order_serial: str, article_serial: str, quantity: int, price: float):
        # Crea un dizionario con i campi dell'ordine da aggiornare
        order_data = dict(
            article_serial=article_serial,
            quantity=quantity,
            price=price
        )
        # Salva l'ordine nel database e ne ritorna l'id
        return self.__order_network.update(order_serial, order_data)

    # Aggiorna lo stato di un ordine
    def update_order_state_by_id(self, order_serial: str, state: str):

        # Crea un dizionario con i campi dell'ordine da aggiornare
        order_data = dict(
            state=state
        )
        # Salva l'ordine nel database e ne ritorna l'id
        return self.__order_network.update(order_serial, order_data)

    # Elimina un ordine
    def delete_order_by_id(self, order_serial: str):
        self.__order_network.delete(order_serial)
