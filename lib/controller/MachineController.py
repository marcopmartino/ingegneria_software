from lib.model.Machine import Machine
from lib.repository.MachinesRepository import MachinesRepository
from lib.utility.ObserverClasses import Observer, AnonymousObserver


class MachineController:
    def __init__(self, machine: Machine):
        super().__init__()

        # Repositories
        self.__machines_repository: MachinesRepository = MachinesRepository()

        # Models
        self.__machine: Machine = machine

    def get_machine(self):
        return self.__machine

    def get_machine_serial(self):
        return self.__machine.get_machine_serial()

    def is_machine_running(self):
        return self.__machine.is_running()

    def get_machine_type(self):
        return self.__machine.get_machine_type()

    def start_machine(self):
        self.__machines_repository.update_machine_state_by_id(self.get_machine_serial(), True)

    def stop_machine(self):
        self.__machines_repository.update_machine_state_by_id(self.get_machine_serial(), False)

    def observe_machine(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__machine.attach(observer)
        return observer

    def detach_machine_observer(self, observer: Observer):
        self.__machine.detach(observer)
