from abc import abstractmethod, ABC
from enum import Enum


# Classe astratta Osservatore
# noinspection PyPep8Naming
class Observer(ABC):

    # Metodo eseguito alla ricezione di notifiche
    @abstractmethod
    def onNotificationReceived(self, message):
        pass


# Osservatore anonimo - è necessario definire la funzione di callback da eseguire alla ricezione di notifiche
class AnonymousObserver(Observer):
    def __init__(self, callback: callable):
        self.__callback = callback

    def onNotificationReceived(self, message):
        self.__callback(message)


# Classe base Osservabile
# noinspection PyPep8Naming
class Observable:

    def __init__(self):
        self.__observers: list[Observer] = []

    # Aggiunge un osservatore anonimo alla lista
    def observe(self, callback: callable) -> Observer:
        observer = AnonymousObserver(callback)
        self.__observers.append(observer)
        return observer

    # Se non già presente, aggiunge un osservatore alla lista
    def attach(self, observer: Observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    # Se presente, rimuove un osservatore dalla lista
    def detach(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    # Svuota la lista degli osservatori
    def detachAll(self):
        self.__observers.clear()

    # Notifica gli osservatori dei cambiamenti
    def notify(self, message):
        for observer in self.__observers:
            observer.onNotificationReceived(message)


# Classe di utilità rappresentante un messaggio che può essere inviato da un Observable come notifica
# noinspection PyPep8Naming
class Message:
    def __init__(self, event: Enum, data: any = None):
        self.__event: Enum = event
        self.__data: any = data

    def event(self) -> Enum:
        return self.__event

    def data(self) -> any:
        return self.__data

    def setData(self, data: any):
        self.__data = data
