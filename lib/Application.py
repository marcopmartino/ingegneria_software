from typing import List

from PyQt5.QtWidgets import QApplication

from lib.firebaseData import Firebase
from lib.view.access.AccessWindow import AccessWindow
from lib.view.main.MainWindow import MainWindow


class Application(QApplication):

    def __init__(self, argv: List[str]):
        super().__init__(argv)

        # Inizializzo Firebase
        Firebase.initialize_app()

        # Inizializza le due finestre
        self.main_window: MainWindow = MainWindow()
        self.access_window: AccessWindow = AccessWindow()

        # Imposta la navigazione tra le finestre
        self.access_window.login.connect(self.show_main_window)
        self.main_window.logout.connect(self.show_access_window)

    # Avvia l'applicazione mostrando la schermata di accesso
    def run(self):
        self.access_window.show()

    # Chiude eventuali finestre aperte
    def stop(self):
        if self.main_window:
            self.main_window.hide()
            self.main_window.reset()

        if self.access_window:
            self.access_window.hide()
            self.access_window.reset()

    # Chiude eventuali finestre aperte e poi avvia l'applicazione
    def rerun(self):
        self.stop()
        self.run()

    # Crea e mostra la schermata di accesso
    def show_access_window(self):
        self.main_window.hide()
        self.main_window.reset()
        self.access_window.show()

    # Crea e mostra la schermata principale
    def show_main_window(self):
        self.access_window.hide()
        self.access_window.reset()
        self.main_window.setup()

