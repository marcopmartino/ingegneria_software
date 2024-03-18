from typing import List

from PyQt5.QtWidgets import QApplication

from lib.mvc.access.view.AccessWindow import AccessWindow
from lib.mvc.main.view.MainWindow import MainWindow


class Application(QApplication):

    def __init__(self, argv: List[str]):
        super().__init__(argv)

        # Inizializzo lo stato
        self.state = "NOT_RUNNING"

        # Inizializza a None le due finestre
        self.main_window = None
        self.access_window = None

    # Avvia l'applicazione mostrando la schermata di accesso
    def run(self):
        self.access_window = AccessWindow()
        self.access_window.login.connect(self.show_main_window)
        self.access_window.show()

        # Aggiorno lo stato
        self.state = "RUNNING"

    # Chiude eventuali finestre aperte
    def stop(self):
        if self.main_window:
            self.main_window.close()

        if self.access_window:
            self.access_window.close()

        # Aggiorno lo stato
        self.state = "STOPPED"

    # Chiude eventuali finestre aperte e poi avvia l'applicazione
    def rerun(self):
        self.stop()
        self.run()

    # Crea e mostra la schermata di accesso
    def show_access_window(self):
        self.access_window = AccessWindow()
        self.access_window.login.connect(self.show_main_window)
        self.main_window.close()
        self.access_window.show()

    # Crea e mostra la schermata principale
    def show_main_window(self):
        self.main_window = MainWindow()
        self.main_window.logout.connect(self.show_access_window)
        self.access_window.close()
        self.main_window.show()
