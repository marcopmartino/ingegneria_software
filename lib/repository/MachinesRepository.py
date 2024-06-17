import threading
from datetime import datetime
from enum import Enum
from time import sleep

from PyQt5.QtCore import QObject

from lib.model.Machine import Machine, Sgrossatore, Tornio, Finitore, Ferratore, Timbratrice, MachineProcess
from lib.model.ShoeLastVariety import ShoeLastVariety, ProductType, Gender, ShoeLastType, PlasticType, CompassType, \
    Shoeing, Processing
from lib.network.MachinesNetwork import MachinesNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta
from lib.utility.UtilityClasses import DatetimeUtils


class MachinesRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        MACHINES_INITIALIZED = 0
        MACHINE_STATE_UPDATED = 1
        THREAD_MACHINE_PROGRESS_UPDATED = 2
        THREAD_MACHINE_STOPPED = 3

    def __init__(self):
        self.__machine_list: list[Machine] = []  # Inizializza la lista dei macchinari
        self.__machine_threads: list[MachineThread] = []  # Inizializza la lista dei thread dei macchinari
        self.__machines_network = MachinesNetwork()
        super().__init__(self.__machines_network.stream)

    def clear(self):
        # Ferma tutti i thread
        for thread in self.__machine_threads:
            thread.stop()

        # Svuota le liste
        self.__machine_list = []
        self.__machine_threads = []

    # Avvia un thread per un macchinario
    def __start_machine_thread(self, machine: Machine):
        # Crea il Thread
        machine_thread = MachineThread(
            machine,

            # Gestisce l'aggiornamento della percentuale di progresso
            lambda: self.notify(Message(MachinesRepository.Event.THREAD_MACHINE_PROGRESS_UPDATED, machine)),

            # Gestisce l'aggiornamento dello stato
            lambda: self.notify(Message(MachinesRepository.Event.THREAD_MACHINE_STOPPED, machine)),

            # Gestisce la rimozione del thread
            lambda: self.__machine_threads.remove(machine_thread)
        )

        # Aggiunge il thread alla lista
        self.__machine_threads.append(machine_thread)

        # Avvia il thread
        machine_thread.start()

    # Usato internamente per istanziare e aggiungere un nuovo macchinario alla lista
    def __instantiate_and_append_machine(self, serial: str, data: any) -> Machine:
        # Istanzia il processo
        process_data = data.get("active_process")
        machine_process = None
        if process_data is not None:
            machine_process = self.__instantiate_machine_process(process_data)

        # Istanza il macchinario
        for machine_class in [Sgrossatore, Tornio, Finitore, Ferratore, Timbratrice]:
            if data["machine_type"] == machine_class.__name__:
                machine = machine_class(serial, data["capacity"], data["is_running"],
                                        data["manufacturer"], machine_process)
                self.__machine_list.append(machine)
                return machine

    # Usato internamente per istanziare un nuovo processo
    # noinspection PyMethodMayBeStatic
    def __instantiate_machine_process(self, data: any) -> MachineProcess:
        return MachineProcess(
            data["operation_id"], self.__instantiate_shoe_last_variety(data["output_shoe_last_variety"]),
            data["quantity"], DatetimeUtils.format_datetime(data["end_datetime"]), data["duration"]
        )

    # Usato internamente per istanziare una nuova varietà di forma
    # noinspection PyMethodMayBeStatic
    def __instantiate_shoe_last_variety(self, data: any) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType(data["product_type"]),
            Gender(data["gender"]), ShoeLastType(data["shoe_last_type"]), PlasticType(data["plastic_type"]),
            data["size"], Processing(data["processing"]), CompassType(data["first_compass_type"]),
            CompassType(data["second_compass_type"]), data["pivot_under_heel"], Shoeing(data["shoeing"]),
            data["iron_tip"], data["numbering_antineck"], data["numbering_lateral"], data["numbering_heel"],
        )

    # Stream handler che aggiorna automaticamente la lista dei macchinari
    def _stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorna la lista dei macchinari così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:

            # Ottenimento\inserimento\eliminazione di macchinari
            case "put":

                # # All'apertura dello Stream, quando viene caricata l'intera lista dei macchinari
                if path == "/":
                    # Se c'è almeno un ordine nella lista
                    if data:
                        for key, value in data.items():
                            # Crea e aggiunge un ordine alla lista di ordini della repository
                            self.__instantiate_and_append_machine(key, value)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(Message(MachinesRepository.Event.MACHINES_INITIALIZED, self.__machine_list))

                        # Avvia i thread per i macchinari
                        for machine in self.__machine_list:
                            # Valuta se iniziare un Thread per aggiornare il progresso del macchinario
                            if machine.is_running():
                                self.__start_machine_thread(machine)

            # Aggiornamento di un macchinario
            case "patch":
                # Estrae il seriale del macchinario dal path
                machine_serial = path.split("/")[1]

                print("Updating machine " + machine_serial)

                # Prende il macchinario corrispondente
                machine = self.get_machine_by_id(machine_serial)

                print("Found machine " + machine.__str__())

                # Estraggo i dati
                is_running: bool = data.get("is_running")

                # Aggiorna lo stato del macchinario
                if is_running:
                    machine_process = self.__instantiate_machine_process(data.get("active_process"))
                    machine.start(machine_process)

                    # Avvia un thread per l'aggiornamento del progresso
                    self.__start_machine_thread(machine)
                else:
                    machine.stop()

                # Prepara il messaggio
                message = Message(MachinesRepository.Event.MACHINE_STATE_UPDATED)

                # Notifica eventuali osservatori del singolo macchinario
                machine.notify(message)

                # Notifica gli osservatori della lista dei macchinari
                message.setData(machine)
                self.notify(message)

            # Terminazione imprevista dello stream
            case "cancel":
                pass

    # Ritorna la lista dei macchinari
    def get_machine_list(self) -> list[Machine]:
        return self.__machine_list

    # Cerca un macchinario in base al suo numero di serie e lo ritorna
    def get_machine_by_id(self, machine_serial: str) -> Machine:
        for machine in self.__machine_list:
            if machine.get_machine_serial() == machine_serial:
                return machine

    # Avvia un macchinario
    def start_machine_by_id(self, machine_serial: str, operation_id: str, shoe_last_variety: ShoeLastVariety,
                            quantity: int, duration: int):
        # Crea un dizionario con i campi del macchinario da aggiornare
        machine_data = dict(
            is_running=True,
            active_process=dict(
                operation_id=operation_id,
                quantity=quantity,
                duration=duration,
                end_datetime=DatetimeUtils.unformat_datetime(
                    DatetimeUtils.add_seconds_to_datetime(datetime.now(), duration)),
                output_shoe_last_variety=dict(
                    product_type=shoe_last_variety.get_product_type().value,
                    gender=shoe_last_variety.get_gender().value,
                    size=shoe_last_variety.get_size(),
                    shoe_last_type=shoe_last_variety.get_shoe_last_type().value,
                    plastic_type=shoe_last_variety.get_plastic_type().value,
                    first_compass_type=shoe_last_variety.get_first_compass_type().value,
                    second_compass_type=shoe_last_variety.get_second_compass_type().value,
                    processing=shoe_last_variety.get_processing().value,
                    shoeing=shoe_last_variety.get_shoeing().value,
                    numbering_antineck=shoe_last_variety.get_numbering_antineck(),
                    numbering_lateral=shoe_last_variety.get_numbering_lateral(),
                    numbering_heel=shoe_last_variety.get_numbering_heel(),
                    iron_tip=shoe_last_variety.get_iron_tip(),
                    pivot_under_heel=shoe_last_variety.get_pivot_under_heel()
                )
            )
        )

        # Aggiorna il macchinario nel database
        self.__machines_network.update(machine_serial, machine_data)

    # Ferma un macchinario
    def stop_machine_by_id(self, machine_serial: str):
        # Crea un dizionario con i campi del macchinario da aggiornare
        machine_data = dict(
            is_running=False,
            active_process=None,
        )

        # Aggiorna il macchinario nel database
        self.__machines_network.update(machine_serial, machine_data)

    def request_to_manage_machine_output(self, machine_id: str):
        self.__machines_network.request_to_manage_machine_output(machine_id)

    def can_manage_machine_output(self, machine_id: str) -> bool:
        return self.__machines_network.can_manage_machine_output(machine_id)


class MachineThread(QObject):

    def __init__(
            self,
            machine: Machine,
            on_progress_changed: callable,
            on_machine_stopped: callable,
            on_thread_stopped: callable
    ):
        super().__init__()
        self.__machine: Machine = machine
        self.__keep_alive: bool = True
        self.__thread: threading.Thread | None = None
        self.__on_progress_changed: callable = on_progress_changed
        self.__on_machine_stopped: callable = on_machine_stopped
        self.__on_thread_stopped: callable = on_thread_stopped

    def start(self):
        self.__thread = threading.Thread(target=self.__run)
        self.__thread.start()

    def stop(self):
        if self.__thread.is_alive():
            self.__keep_alive = False

    def __run(self):
        # Flag
        self.__keep_alive = True

        while self.__keep_alive:
            sleep(2)  # Periodicità dell'esecuzione in secondi

            # Ottiene il processo in esecuzione
            active_process = self.__machine.get_active_process()

            # Il processo può diventare None in caso di stop d'emergenza
            if active_process is not None:
                # Calcola la nuova percentuale
                active_process.refresh_progress_percentage()

                # La percentuale supera 100 se il datetime corrente è successivo a quello di fine
                if active_process.get_progress_percentage() < 100:
                    self.__on_progress_changed()

                    print(f"Aggiorno il progresso di {self.__machine.get_machine_serial()}: "
                          f"{active_process.get_progress_percentage()}%")

                else:
                    # Modifica la flag per uscire dal ciclo (processo completato)
                    self.__keep_alive = False
                    self.__on_machine_stopped()

                    print(f"Fine processo {self.__machine.get_machine_serial()}")

            else:
                # Modifica la flag per uscire dal ciclo (processo fermato d'emergenza)
                self.__keep_alive = False

        try:
            self.__on_thread_stopped()

            print(f"Fine thread {self.__machine.get_machine_serial()}")

            return  # Termina il thread

        # Può verificarsi se il thread tenta di rimuoversi da MachinesRepository dopo un clear della repository
        except ValueError:
            print(f"Eccezione thread {self.__machine.get_machine_serial()}")

            return  # Termina il thread
