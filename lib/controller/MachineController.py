from lib.model.Machine import Machine, MachineOperation
from lib.model.Order import OrderState, Order
from lib.model.ShoeLastVariety import ShoeLastVariety
from lib.repository.ArticlesRepository import ArticlesRepository
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Observer, AnonymousObserver


class MachineController:
    def __init__(self, machine: Machine):
        super().__init__()

        # Repositories
        self.__machines_repository: MachinesRepository = MachinesRepository()
        self.__orders_repository: OrdersRepository = OrdersRepository()
        self.__articles_repository: ArticlesRepository = ArticlesRepository()
        self.__storage_repository: StorageRepository = StorageRepository()

        # Models
        self.__machine: Machine = machine

    def get_machine(self):
        return self.__machine

    def get_machine_serial(self):
        return self.__machine.get_machine_serial()

    def is_machine_running(self):
        return self.__machine.is_running()

    def get_machine_type(self):
        return self.__machine.__class__.__name__

    # Ottiene informazioni su tutte le operazioni possibili eseguibili dal macchinario
    def get_operation_list(self) -> list[MachineOperation]:

        # Inizializza una lista vuota.
        # L'idea è di raggruppare gli ordini sulla base dell'operazione di cui necessitano (stesso ShoeLastVariety in
        # output); gli ordini relativi allo stesso articolo appariranno insieme, ma anche ordini di articoli diversi se
        # hanno in comune una parte (iniziale) del processo produttivo.
        operation_list: list[MachineOperation] = []

        # Itera sugli ordini che sono in lavorazione (stato "PROCESSING")
        for order in self.__orders_repository.get_order_list():
            if order.get_state() == OrderState.PROCESSING:
                # Estrae l'articolo dell'ordine
                article = self.__articles_repository.get_article_by_id(order.get_article_serial())

                # Calcola la varietà di forma data in output dal macchinario come parte del processo per giungere alla
                # varietà desiderata (quella dell'articolo)
                output_shoe_last_variety = self.__machine.calculate_output_shoe_last_variety(
                    article.get_shoe_last_variety())

                # Imposta a False una variabile che indica se l'ordine è stato aggiunto al dizionario
                order_added = False

                # Itera sugli elementi già presenti nella lista
                for operation in operation_list:
                    # Aggiunge l'ordine alla lista se l'output dell'operazione coincide con l'output calcolato
                    if operation.get_output_shoe_last_variety().equals(output_shoe_last_variety):
                        operation.append_order(order)
                        order_added = True
                        break

                # Se l'ordine non è stato aggiunto, crea una nuova OperationData con l'ordine in questione
                if not order_added:
                    # Calcola la varietà di forma data in input al macchinario come parte del processo per giungere alla
                    # varietà desiderata (quella dell'articolo)
                    input_shoe_last_variety = self.__machine.calculate_input_shoe_last_variety(
                        article.get_shoe_last_variety())

                    # Calcola i materiali in input necessari all'operazione
                    input_materials = self.__machine.calculate_input_materials(article.get_shoe_last_variety())

                    # Calcola le forme in produzione in macchinari dello stesso tipo
                    in_production_shoe_lasts = 0
                    for machine in self.__machines_repository.get_machine_list():
                        if isinstance(machine, type(self.__machine)) and machine.is_running():
                            in_production_shoe_lasts += machine.get_active_process().get_quantity()

                    # Calcola in numero di output già prodotto
                    """Da implementare"""

                    # Calcola in numero di input presente in magazzino
                    """Da implementare"""

                    # Aggiunge l'ordine alla lista degli ordini dell'operazione
                    new_operation = MachineOperation(
                        input_shoe_last_variety, output_shoe_last_variety, input_materials, in_production_shoe_lasts)
                    new_operation.append_order(order)

        return operation_list

    def start_machine(self):
        self.__machines_repository.update_machine_state_by_id(self.get_machine_serial(), True)
        """Rimuovi i materiali dal magazzino"""
        """Crea e salva il nuovo processo"""

    def stop_machine(self):
        self.__machines_repository.update_machine_state_by_id(self.get_machine_serial(), False)
        """Termina e rimuovi il processo"""
        """Aggiungi l'output al magazzino"""

    def observe_repositories(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__machines_repository.attach(observer)
        self.__orders_repository.attach(observer)
        self.__storage_repository.attach(observer)
        return observer

    def detach_machine_observer(self, observer: Observer):
        self.__machine.detach(observer)
