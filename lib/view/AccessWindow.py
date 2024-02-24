from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy

from lib.layout.FrameLayout import FrameLayout
from lib.view.AccessView import AccessView
from lib.view.LoginView import LoginView
from lib.view.SignUpView import SignUpView
from res import Styles
from res.Strings import Config


class AccessWindow(QMainWindow):

    def __init__(self):
        super(AccessWindow, self).__init__()

        # Finestra
        self.setWindowTitle(Config.APPLICATION_NAME)
        self.setObjectName("main_window")
        self.resize(1000, 600)
        self.setStyleSheet(Styles.ACCESS)

        # Widget più esterno - Inizializzazione
        self.outerWidget = QWidget(self)
        self.outerWidget.setObjectName("outer_widget")

        # Widget più esterno - Layout
        self.outerFrameLayout = FrameLayout(self.outerWidget)
        self.outerFrameLayout.setObjectName("outer_layout")
        self.outerFrameLayout.setSpacers(140, 80, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Pone il frame esterno come Widget di base della finestra
        self.setCentralWidget(self.outerWidget)

        # Crea il frame interno con la form
        self.loginWidget = LoginView()
        self.signUpWidget = SignUpView()

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
        self.update_ui(self.signUpWidget) # Per posizionare la form prima di mostrarla
        self.signUpWidget.setHidden(False)

    # Aggiorna la UI con un widget AccessView (login o registrazione)
    def update_ui(self, widget: QWidget):
        # Pone il frame interno al centro del frame esterno
        self.outerFrameLayout.setCentralWidget(widget)
