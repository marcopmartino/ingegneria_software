from lib.model.Machine import Machine, MachineOperationData, InputMaterial, MachineProcess
from lib.model.Order import OrderState, Order
from lib.model.ShoeLastVariety import ShoeLastVariety
from lib.model.StoredItems import AssignedShoeLastVariety
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
        self.__operation_list: list[MachineOperationData] = []

        # Inizializza la lista di operazioni
        self.refresh_operation_list()

    def get_machine(self):
        return self.__machine

    def get_machine_serial(self):
        return self.__machine.get_machine_serial()

    def is_machine_running(self):
        return self.__machine.is_running()

    def get_machine_type(self):
        return self.__machine.__class__.__name__

    # Ottiene le informazioni su tutte le operazioni possibili eseguibili dal macchinario
    def get_operation_list(self) -> list[MachineOperationData]:
        return self.__operation_list

    def get_operation_by_id(self, operation_id: str) -> MachineOperationData:
        for operation in self.__operation_list:
            if operation.get_id() == operation_id:
                return operation

    def get_operation_by_order_serial(self, order_serial: str) -> MachineOperationData:
        for operation in self.__operation_list:
            if operation.contains_order(order_serial):
                return operation

    # Aggiorna le informazioni su tutte le operazioni possibili eseguibili dal macchinario
    def refresh_operation_list(self):

        # Inizializza una lista vuota.
        # L'idea è di raggruppare gli ordini sulla base dell'operazione di cui necessitano (stesso ShoeLastVariety in
        # output); gli ordini relativi allo stesso articolo appariranno insieme, ma anche ordini di articoli diversi se
        # hanno in comune una parte (iniziale) del processo produttivo.
        operation_list: list[MachineOperationData] = []

        # Itera sugli ordini che sono in lavorazione (stato "PROCESSING")
        for order in self.__orders_repository.get_order_list():
            if order.get_state() == OrderState.PROCESSING:
                # Estrae l'articolo dell'ordine
                article = self.__articles_repository.get_article_by_id(order.get_article_serial())

                # Prosegue solo se l'ordine richiede l'esecuzione di questo macchinario
                if self.__machine.is_process_required(article.get_shoe_last_variety()):

                    # Calcola la varietà di forma data in output dal macchinario come parte del processo per giungere
                    # alla varietà desiderata (quella dell'articolo)
                    output_shoe_last_variety = self.__machine.calculate_output_shoe_last_variety(
                        article.get_shoe_last_variety())

                    # Imposta a False una variabile che indica se l'ordine è stato aggiunto al dizionario
                    order_added = False

                    print("Ordine: " + order.get_order_serial())

                    # Itera sugli elementi già presenti nella lista
                    for operation in operation_list:
                        # Aggiunge l'ordine alla lista se l'output dell'operazione coincide con l'output calcolato
                        if operation.get_output_shoe_last_variety().equals(output_shoe_last_variety):
                            operation.append_order(order)
                            order_added = True
                            break

                    # Se l'ordine non è stato aggiunto, crea una nuova OperationData con l'ordine in questione
                    if not order_added:
                        # Calcola la varietà di forma data in input al macchinario come parte del processo per
                        # giungere alla varietà desiderata (quella dell'articolo)
                        input_shoe_last_variety = self.__machine.calculate_input_shoe_last_variety(
                            article.get_shoe_last_variety())

                        # Calcola i materiali in input necessari all'operazione
                        required_input_materials = self.__machine.calculate_input_materials(
                            article.get_shoe_last_variety())

                        # Inizializza una lista vuota per i materiali disponibili
                        available_input_materials: list[InputMaterial] = []

                        # Calcola i materiali in input disponibili
                        for input_material in required_input_materials:
                            material_description = input_material.get_material_description()
                            available_quantity = self.__storage_repository.get_material_by_description(
                                material_description).get_quantity()

                            # Aggiunge la quantità disponibile alla lista
                            available_input_materials.append(InputMaterial(material_description, available_quantity))

                        # Calcola il numero di forme in input presente in magazzino
                        stored_shoe_last_variety = (
                            self.__storage_repository.get_unassigned_product_by_shoe_last_variety(
                                input_shoe_last_variety)
                        )

                        available_input_shoe_lasts = stored_shoe_last_variety.get_quantity() \
                            if stored_shoe_last_variety is not None else 0

                        # Calcola le forme in produzione in macchinari dello stesso tipo
                        in_production_shoe_lasts = 0
                        for machine in self.__machines_repository.get_machine_list():
                            if isinstance(machine, type(self.__machine)) and machine.is_running():
                                in_production_shoe_lasts += machine.get_active_process().get_quantity()

                        # Calcola il numero di forme già prodotto
                        produced_shoe_lasts = 0
                        for product in self.__storage_repository.get_product_list():
                            if ((not isinstance(product, AssignedShoeLastVariety))
                                    and self.__machine.is_compatible_shoe_last_variety(
                                        desired_shoe_last_variety=article.get_shoe_last_variety(),
                                        shoe_last_variety=product.get_shoe_last_variety()
                                    )):
                                produced_shoe_lasts += product.get_quantity()

                        # Crea una nuova operazione e aggiunge l'ordine alla sua lista degli ordini
                        new_operation = MachineOperationData(
                            order,
                            input_shoe_last_variety,
                            output_shoe_last_variety,
                            required_input_materials,
                            available_input_materials,
                            available_input_shoe_lasts,
                            in_production_shoe_lasts,
                            produced_shoe_lasts
                        )

                        # Aggiunge la nuova operazione alla lista
                        operation_list.append(new_operation)

        # Finalizza le operazioni
        for operation in operation_list:
            operation.finalize(self.__machine.get_capacity())

        # Aggiorna la lista di operazioni
        self.__operation_list = operation_list

    # Esegue le operazioni di avvio del macchinario
    def start_machine(self, order_serial: str):
        # Ottiene i dati dell'operazione
        operation_data = self.get_operation_by_order_serial(order_serial)

        # Aggiorna la quantità della forma richiesta in input
        stored_shoe_last_variety = self.__storage_repository.get_unassigned_product_by_shoe_last_variety(
            operation_data.get_input_shoe_last_variety())
        self.__storage_repository.update_product_quantity(
            stored_shoe_last_variety.get_item_id(),
            stored_shoe_last_variety.get_quantity() - operation_data.get_required_to_start_shoe_lasts()
        )

        # Aggiorna le quantità dei materiali richiesti in input
        for input_material in operation_data.get_required_input_materials():
            material = self.__storage_repository.get_material_by_description(input_material.get_material_description())
            self.__storage_repository.update_material_quantity(
                material.get_item_id(),
                material.get_quantity() - input_material.get_quantity()
            )

        # Avvia il macchinario
        self.__machines_repository.start_machine_by_id(
            self.__machine.get_machine_serial(),
            order_serial,
            operation_data.get_output_shoe_last_variety(),
            operation_data.get_required_to_start_shoe_lasts(),
            self.__machine.calculate_duration(operation_data.get_output_shoe_last_variety())
        )

    # Esegue le operazioni di stop del macchinario in caso di emergenza (processo interrotto improvvisamente)
    def emergency_stop_machine(self):
        # Ferma il macchinario
        self.__machines_repository.stop_machine_by_id(self.__machine.get_machine_serial())

    def observe_repositories(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__machines_repository.attach(observer)
        self.__orders_repository.attach(observer)
        self.__storage_repository.attach(observer)
        return observer

    def detach_machine_observer(self, observer: Observer):
        self.__machine.detach(observer)
