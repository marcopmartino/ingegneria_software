from lib.model.Worker import Worker
from lib.network.UsersNetwork import UsersNetwork
from lib.utility.ObserverClasses import Observable
from lib.utility.Singleton import ObservableSingleton


class WorkerList(Observable, metaclass=ObservableSingleton):

    def __init__(self):
        super().__init__()
        self.__worker_list: list[Worker] = []
        UsersNetwork.stream(self.__stream_handler)

    # Usato internamente per aggiungere un ordine alla lista
    def __append_worker(self, uid: str, data: any):
        self.__worker_list.append(Worker(
            uid, data["name"], data["CF"], data["birth_date"], data["mail"],
            data["phone"]))

    def __edit_worker(self, path: str, key: str, data: any):

        for index, worker in enumerate(self.__worker_list):
            if worker.uid == path[1]:
                match key:
                    case 'name':
                        worker.name = data
                    case 'CF':
                        worker.CF = data
                    case 'birth_data':
                        worker.birth_date = data
                    case 'phone':
                        worker.phone = data
                    case 'mail':
                        worker.mail = data
                break

    def __remove_worker(self, path: str):
        for index, worker in enumerate(self.__worker_list):
            if worker.uid == path[1]:
                self.delete(worker.mail)
                self.__worker_list.remove(worker)
                break

    # Stream handler che aggiorna automaticamente la lista degli operai
    def __stream_handler(self, message):
        print("1")
        for key in message.keys():
            print(f"{key}: {message[key]}")

        # Aggiorno la lista degli ordini così che client diversi possano accedere alla stessa versione aggiornata dei
        # dati (grazie al pattern Singleton)
        data = message["data"]
        path = message["path"].split("/")
        if data is not None:
            match message["event"]:
                case "put":
                    # All'avvio del programma, quando viene caricata l'intera lista di operai
                    for key, value in data.items():
                        if type(value) is not dict and key != 'role':
                            continue
                        role = value['role'] if type(value) is dict else value
                        if role in ('worker', 'manager'):
                            self.__append_worker(key, value)
                case "patch":
                    # Quando viene modificato un elemento tramite form apposito
                    for key, value in data.items():
                        self.__edit_worker(path, key, value)
                case "cancel": pass
        else:
            # Eliminazione operaio
            self.__remove_worker(path)

        # Notifico gli osservatori così che possano aggiornarsi (grazie al pattern Observer)
        message["notifier"] = "WorkerList"
        self.notify(message)

    # Ritorna la lista  degli operai
    def get(self) -> list[Worker]:
        return self.__worker_list

    # Cerca un operaio in base alla mail e lo ritorna
    def get_by_id(self, mail: str) -> Worker:
        for worker in self.__worker_list:
            if worker.mail == mail:
                return worker

    # Salva un nuovo operaio nel database.
    @staticmethod
    def add(worker: Worker) -> str:
        # Converte l'operaio in dizionario
        worker_dict = vars(worker)
        # Salva l'operaio nel database e ne ritorna l'id
        return UsersNetwork.create(worker_dict)

    @staticmethod
    def delete(email: str):
        UsersNetwork.delete_by_email(email)
