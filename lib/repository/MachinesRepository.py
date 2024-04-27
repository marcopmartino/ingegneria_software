from enum import Enum

from lib.model.Machine import Machine
from lib.network.MachineNetwork import MachineNetwork
from lib.utility.ObserverClasses import Observable, Message
from lib.utility.Singleton import ObservableSingleton


class MachinesRepository(Observable, metaclass=ObservableSingleton):
    class Event(Enum):
        MACHINE_STOPPED = 0
        MACHINE_STARTED = 1

    def __init__(self):
        super().__init__()
        self.__machine_list: list[Machine] = []  # Inizializza la lista dei macchinari
        self.__machine_network = MachineNetwork()
        self.__machine_network.stream(self.__stream_handler)

    # Usato internamente per istanziare e aggiungere un nuovo macchinario alla lista
    def __instantiate_and_append_machine(self, serial: str, data: any) -> Machine:
        order = Machine(
            serial, data["machine_type"], data["is_running"], data["capacity"]
        )
        self.__machine_list.append(order)
        return order

    # Stream handler che aggiorna automaticamente la lista dei macchinari
    def __stream_handler(self, message):
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorna la lista dei macchinari così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"]
        match message["event"]:

            # Ottenimento\inserimento\eliminazione di macchinari
            case "put":

                # All'avvio del programma, quando viene caricata l'intera lista dei macchinari
                if path == "/":
                    # Se c'è almeno un ordine nella lista
                    if data:
                        for key, value in data.items():
                            # Crea e aggiunge un ordine alla lista di ordini della repository
                            self.__instantiate_and_append_machine(key, value)

                        # Notifica gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
                        self.notify(message)

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
