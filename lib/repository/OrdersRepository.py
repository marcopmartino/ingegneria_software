from __future__ import annotations

from enum import Enum

from lib.firebaseData import Firebase
from lib.model.Order import Order, OrderState
from lib.network.OrdersNetwork import OrdersNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta
from lib.utility.UtilityClasses import DatetimeUtils


class OrdersRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        ORDERS_INITIALIZED = 0
        ORDER_CREATED = 1
        ORDER_DELETED = 2
        ORDER_UPDATED = 3
        ORDER_STATE_UPDATED = 4

    def __init__(self):
        self.__order_list: list[Order] = []  # Inizializza la lista degli ordini
        self.__orders_network = OrdersNetwork()
        super().__init__(self.__orders_network.stream)

    def clear(self):
        self.__order_list = []

    # Usato internamente per istanziare e aggiungere un nuovo ordine alla lista
    def __instantiate_and_append_order(self, serial: str, data: any) -> Order:
        order = Order(
            serial, data["article_serial"], OrderState(data["state"]), data["customer_id"], data["quantity"],
            data["price"], data.get("first_product_serial", -1), DatetimeUtils.format_date(data["creation_date"])
        )
        self.__order_list.append(order)
        return order

    # Stream handler che aggiorna automaticamente la lista degli ordini
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorna la lista degli ordini così che utenti diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:

            # Ottenimento\inserimento\eliminazione di ordini
            case "put":

                # All'apertura dello Stream, quando viene caricata l'intera lista di ordini
                if path == "/":
                    # Se c'è almeno un ordine nella lista
                    if data:

                        # Se l'utente è un cliente, aggiunge alla repository solo i suoi ordini
                        if Firebase.auth.currentUserRole() == "customer":
                            for key, value in data.items():
                                if Firebase.auth.currentUserId() == value["customer_id"]:
                                    # Crea e aggiunge un ordine alla lista di ordini della repository
                                    self.__instantiate_and_append_order(key, value)

                        # Altrimenti, aggiunge tutti gli ordini
                        else:
                            for key, value in data.items():
                                # Crea e aggiunge un ordine alla lista di ordini della repository
                                self.__instantiate_and_append_order(key, value)

                    # Notifico gli osservatori che la repository ha concluso l'inizializzazione
                    self.notify(Message(OrdersRepository.Event.ORDERS_INITIALIZED, self.__order_list))

                # Se il path è diverso allora siamo nell'ambito di un singolo ordine della lista
                else:
                    # Estrae il seriale dell'ordine dal path
                    order_serial = path.split("/")[1]

                    # Quando viene creato un nuovo ordine, data non è None
                    if data:

                        # Aggiunge l'ordine alla repository solo se l'utente è un dipendente o il cliente che ha
                        # creato l'ordine
                        if (Firebase.auth.currentUserRole() != "customer"
                                or Firebase.auth.currentUserId() == data["customer_id"]):
                            # Crea e aggiunge un ordine alla lista di ordini della repository
                            new_order = self.__instantiate_and_append_order(order_serial, data)

                            # Prepara il messaggio per notificare gli osservatori della lista degli ordini
                            message = Message(OrdersRepository.Event.ORDER_CREATED, new_order)

                            # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                            self.notify(message)

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

                                # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                                self.notify(message)
                                break

            # Aggiornamento di un ordine
            case "patch":
                # Estrae il seriale dell'ordine dal path
                order_serial = path.split("/")[1]

                print("Updating order " + order_serial)

                # Prende l'ordine corrispondente
                order = self.get_order_by_id(order_serial)

                # Se un ordine è stato trovato
                if order is not None:
                    print("Found order " + order.__str__())

                    # Caso di aggiornamento del numero del primo prodotto dell'ordine
                    if data.get("first_product_serial", False):
                        # Estraggo i dati
                        first_product_serial: int = data.get("first_product_serial")

                        # Aggiorna l'ordine nella lista
                        order.set_first_product_serial(first_product_serial)

                    # Caso di aggiornamento dello stato dell'ordine
                    elif data.get("state", False):
                        # Estraggo i dati
                        new_state: str = data.get("state")

                        # Aggiorna l'ordine nella lista
                        order.set_state(OrderState(new_state))

                        # Prepara il messaggio per notificare gli osservatori della lista degli ordini
                        message = Message(OrdersRepository.Event.ORDER_STATE_UPDATED)
                        order.notify(message)  # Notifica eventuali osservatori del singolo ordine
                        message.setData(order)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(message)

                    # Caso di aggiornamento dell'articolo dell'ordine
                    else:
                        # Estrae i dati (possono essere None se rimasti invariati)
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

    # Ritorna la lista degli ordini
    def get_order_list(self) -> list[Order]:
        return self.__order_list

    # Ritorna la lista degli ordini associati all'articolo di cui è passato come argomento il seriale
    def get_order_list_by_article_id(self, article_serial: str) -> list[Order]:
        filtered_order_list: list[Order] = []

        for order in self.__order_list:
            if order.get_article_serial() == article_serial:
                filtered_order_list.append(order)

        return filtered_order_list

    # Cerca un ordine in base al suo numero di serie e lo ritorna
    def get_order_by_id(self, order_serial: str) -> Order:
        for order in self.__order_list:
            if order.get_order_serial() == order_serial:
                return order

    # Salva il nuovo ordine nel database
    def create_order(self, article_serial: str, quantity: int, price: float) -> str:
        # Crea un dizionario con i dati del nuovo ordine
        order_data = dict(
            article_serial=article_serial,
            quantity=quantity,
            price=price,
            creation_date=DatetimeUtils.current_date(),
            customer_id=Firebase.auth.currentUserId(),
            state=OrderState.NOT_STARTED.value
        )
        # Salva l'ordine nel database e ne ritorna l'id
        return self.__orders_network.insert(order_data)

    # Aggiorna un ordine
    def update_order_by_id(self, order_serial: str, article_serial: str, quantity: int, price: float):
        # Crea un dizionario con i campi dell'ordine da aggiornare
        order_data = dict(
            article_serial=article_serial,
            quantity=quantity,
            price=price
        )
        # Aggiorna l'ordine nel database
        self.__orders_network.update(order_serial, order_data)

    # Aggiorna lo stato di un ordine
    def update_order_state_by_id(self, order_serial: str, state: str):
        # Crea un dizionario con i campi dell'ordine da aggiornare
        order_data = dict(
            state=state
        )
        # Aggiorna lo stato nel database
        self.__orders_network.update(order_serial, order_data)

    # Aggiorna il numero del primo paio prodotto di un ordine
    def update_order_first_product_serial_by_id(self, order_serial: str, first_product_serial: int):
        # Crea un dizionario con i campi dell'ordine da aggiornare
        order_data = dict(
            first_product_serial=first_product_serial
        )
        # Aggiorna il valore nel database
        self.__orders_network.update(order_serial, order_data)

    # Elimina un ordine
    def delete_order_by_id(self, order_serial: str):
        self.__orders_network.delete(order_serial)
