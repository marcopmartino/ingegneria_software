from enum import Enum

from lib.model.Machine import Machine, Sgrossatore, Tornio, Finitore, Ferratore, Timbratrice
from lib.network.MachinesNetwork import MachinesNetwork
from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Message
from lib.utility.Singleton import RepositoryMeta


class MachinesRepository(Repository, metaclass=RepositoryMeta):
    class Event(Enum):
        MACHINES_INITIALIZED = 0
        MACHINE_STOPPED = 1
        MACHINE_STARTED = 2

    def __init__(self):
        self.__machine_list: list[Machine] = []  # Inizializza la lista dei macchinari
        self.__machines_network = MachinesNetwork()
        super().__init__(self.__machines_network.stream)

    def clear(self):
        self.__machine_list = []

    # Usato internamente per istanziare e aggiungere un nuovo macchinario alla lista
    def __instantiate_and_append_machine(self, serial: str, data: any) -> Machine:
        for machine_class in [Sgrossatore, Tornio, Finitore, Ferratore, Timbratrice]:
            if data["machine_type"] == machine_class.__name__:
                machine = machine_class(serial, data["capacity"], data.get("is_running", False),
                                        data.get("cycle_counter", 0), data.get("active_process"))
                self.__machine_list.append(machine)
                return machine

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

                # Aggiorna l'ordine nella lista
                if is_running:
                    machine.start()  # Aggiorna lo stato del macchinario
                    message = Message(MachinesRepository.Event.MACHINE_STARTED)  # Prepara il messaggio
                else:
                    machine.stop()  # Aggiorna lo stato del macchinario
                    message = Message(MachinesRepository.Event.MACHINE_STOPPED)  # Prepara il messaggio

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

    # Aggiorna lo stato di un macchinario
    def update_machine_state_by_id(self, machine_serial: str, is_running: bool):

        # Crea un dizionario con i campi del macchinario da aggiornare
        machine_data = dict(
            is_running=is_running
        )
        # Salva l'ordine nel database e ne ritorna l'id
        return self.__order_network.update(machine_serial, machine_data)
