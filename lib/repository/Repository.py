from abc import abstractmethod, ABC

from pyrebase.pyrebase import Stream

from lib.utility.ObserverClasses import Observable


class Repository(Observable, ABC):
    def __init__(self):
        super().__init__()
        self._stream: Stream | None = None  # Visibilità "protected"

    # Apre uno stream di dati (lo Stream creato va salvato nella proprietà "_stream")
    @abstractmethod
    def open_stream(self):
        pass

    # Chiude lo stream di dati
    def close_stream(self):
        if self._stream is not None:
            self._stream.close()
