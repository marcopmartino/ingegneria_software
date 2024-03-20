from lib.mvc.order.model.Order import Order
from lib.network.OrderNetwork import OrderNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import singleton, ObservableSingleton


class OrderList(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__order_list: list[Order] = []
        OrderNetwork.stream(self.__stream_handler)

    # Usato internamente per aggiungere un ordine alla lista
    def __append_order(self, serial: str, data: any):
        self.__order_list.append(Order(
            serial, data["article_serial"], data["state"], data["customer_id"], data["quantity"],
            data["price"], data["first_product_serial"], data["creation_date"]
        ))

    # Stream handler che aggiorna automaticamente la lista degli ordini
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista degli ordini così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        if data is not None:
            path = message["path"]
            match message["event"]:
                case "put":

                    # All'avvio del programma, quando viene caricata l'intera lista di ordini
                    if path == "/":
                        for key, value in data.items():
                            self.__append_order(key, value)

                    # Quando viene creato un nuovo ordine
                    else:
                        self.__append_order(path.split("/")[1], data)
                case "patch":
                    pass
                case "cancel":
                    pass

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        message["notifier"] = "OrderList"
        self.notify(message)

    # Ritorna la lista di ordini
    def get(self) -> list[Order]:
        return self.__order_list

    # Cerca un ordine in base al suo numero e lo ritorna
    def get_by_id(self, order_serial: str) -> Order:
        for order in self.__order_list:
            if order.order_serial == order_serial:
                return order

    # Salva il nuovo ordine nel database. Il seriale è rimosso perché viene assegnato automaticamente.
    @staticmethod
    def add(order: Order) -> str:
        # Converte l'ordine in dizionario
        order_dict = vars(order)
        # Rimuove il numero dell'ordine
        order_dict.pop("order_serial")
        # Salva l'ordine nel database e ne ritorna l'id
        return OrderNetwork.create(order_dict)

    @staticmethod
    def delete(order_number: int):
        OrderNetwork.delete_by_id(order_number)
