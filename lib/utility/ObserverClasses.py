from abc import abstractmethod, ABC


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


# Classe astratta Osservabile
class Observable(ABC):

    def __init__(self):
        self.__observers: list[Observer] = []

    # Aggiunge un osservatore anonimo alla lista
    def observe(self, callback: callable):
        self.__observers.append(AnonymousObserver(callback))

    # Se non già presente, aggiunge un osservatore alla lista
    def attach(self, observer: Observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    # Se presente, rimuove un osservatore dalla lista
    def detach(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    # Notifica gli osservatori dei cambiamenti
    def notify(self, message):
        for observer in self.__observers:
            observer.onNotificationReceived(message)
