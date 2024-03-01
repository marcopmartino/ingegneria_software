from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import QPushButton, QWidget


# noinspection PyPep8Naming
class LoadingPushButton(QPushButton):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Avvia l'animazione di caricamento
    @QtCore.pyqtSlot()
    def start(self):
        if hasattr(self, "_movie"):
            self.__movie.start()

    # Termina l'animazione di caricamento
    @QtCore.pyqtSlot()
    def stop(self):
        if hasattr(self, "_movie"):
            self.__movie.stop()
            self.setIcon(QIcon())  # Esegue il reset dell'icona del pulsante

    # Imposta l'animazione di caricamento
    def setGif(self, filename):
        if not hasattr(self, "_movie"):
            self.__movie = QMovie(self)
            self.__movie.setFileName(filename)
            self.__movie.frameChanged.connect(self.on_frameChanged)  # Eseguito quando il frame cambia
            if self.__movie.loopCount() != -1:
                self.__movie.finished.connect(self.start)  # Riavvia l'animazione al suo termine
        self.stop()

    @QtCore.pyqtSlot(int)
    def on_frameChanged(self, frameNumber):
        self.setIcon(QIcon(self.__movie.currentPixmap()))
