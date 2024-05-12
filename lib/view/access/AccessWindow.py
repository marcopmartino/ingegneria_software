from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy

from lib.controller.AccessController import AccessController
from lib.layout.FrameLayouts import FrameLayout
from lib.view.access.LoginView import LoginView
from lib.view.access.SignUpView import SignUpView
from res import Styles
from res.Strings import Config


class AccessWindow(QMainWindow):
    login = pyqtSignal()

    def __init__(self):
        super(AccessWindow, self).__init__()

        # Controller
        self.controller = AccessController()

        # Finestra
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.setObjectName("access_window")
        self.resize(1000, 600)
        self.setStyleSheet(Styles.ACCESS)

        # Widget più esterno - Inizializzazione
        self.outerWidget = QWidget(self)
        self.outerWidget.setObjectName("outer_widget")

        # Widget più esterno - Layout
        self.outerFrameLayout = FrameLayout(self.outerWidget)
        self.outerFrameLayout.setObjectName("outer_layout")
        self.outerFrameLayout.setSpacerDimensionsAndPolicy(140, 80, QSizePolicy.Expanding)

        # Pone il Widget più esterno come Widget di base della finestra
        self.setCentralWidget(self.outerWidget)

        # Crea le due possibili viste del Widget interno con la form
        self.loginWidget = LoginView(self.outerWidget)
        self.signUpWidget = SignUpView(self.outerWidget)

        # Mostra la form di login
        self.show_login_form()

    # Mostra la form di login
    def show_login_form(self):
        self.signUpWidget.setHidden(True)
        self.update_ui(self.loginWidget)  # Per posizionare la form prima di mostrarla
        self.loginWidget.setHidden(False)

    # Mostra la form di registrazione
    def show_sign_up_form(self):
        self.loginWidget.setHidden(True)
        self.update_ui(self.signUpWidget)  # Per posizionare la form prima di mostrarla
        self.signUpWidget.setHidden(False)

    # Aggiorna la UI con un widget AccessView (login o registrazione)
    def update_ui(self, widget: QWidget):
        # Pone il Widget interno al centro del frame esterno
        self.outerFrameLayout.setCentralWidget(widget)

    # Mostra la schermata principale dopo aver fatto il login o la registrazione
    def show_main_window(self):
        self.login.emit()

    # Esegue il reset della finestra
    def reset(self):
        self.show_login_form()
        self.loginWidget.form_manager.clear_fields()
        self.signUpWidget.form_manager.clear_fields()
