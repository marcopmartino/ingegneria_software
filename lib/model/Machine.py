from lib.utility.ObserverClasses import Observable


class Machine(Observable):

    def __init__(self, machine_serial: str, machine_type: str, __is_running: bool, capacity: int):
        super(Machine, self).__init__()
        self.__machine_serial = machine_serial
        self.__machine_type = machine_type
        self.__is_running = __is_running
        self.__capacity = capacity

    def get_machine_serial(self) -> str:
        return self.__machine_serial

    def get_machine_type(self) -> str:
        return self.__machine_type

    def is_running(self) -> bool:
        return self.__is_running

    def get_capacity(self) -> int:
        return self.__capacity

    def start(self) -> None:
        self.__is_running = True

    def stop(self) -> None:
        self.__is_running = False
