from abc import abstractmethod, ABC
from typing import Callable

from pyrebase.pyrebase import Stream

from lib.utility.ObserverClasses import Observable


class Repository(Observable, ABC):
    def __init__(self, stream_source: callable) -> None:
        super().__init__()

        # Funzione che fornisce lo stream
        self.__stream_source: Callable[[Callable[[any], None]], Stream] = stream_source

        # Stream
        self.__stream: Stream | None = None  # Visibilità "protected"

    # Apre uno stream di dati (lo Stream creato viene salvato nella proprietà "__stream")
    def open_stream(self):
        self.close_stream()  # Per assicurarci che ci sia un solo stream aperto
        self.__stream = self.__stream_source(self._stream_handler)  # Apro e salvo un nuovo stream

    # Chiude lo stream di dati
    def close_stream(self):
        if self.__stream is not None:
            self.__stream.close()
            self.__stream = None

    # Callback per lo stream
    @abstractmethod
    def _stream_handler(self, message):
        pass
