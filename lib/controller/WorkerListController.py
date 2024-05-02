from lib.firebaseData import Firebase
from lib.model import Staff
from lib.repository.UsersRepository import UsersRepository


class WorkerListController:
    def __init__(self):
        super().__init__()
        self.__workers_repository = UsersRepository()

    def observe_worker_list(self, callback: callable):
        self.__workers_repository.observe(callback)

    # Ritorna un ordine in base all'id
    def get_worker_by_id(self, uid: str) -> Staff:
        return self.__workers_repository.get_user_by_id(uid).get_dict()

    # Ritorna la lista di ordini filtrata
    def get_worker_list(self) -> list[Staff]:
        return self.__workers_repository.get_user_list(role="worker")

    def create_worker(self, data, password):
        return self.__workers_repository.create_user(data, password)

