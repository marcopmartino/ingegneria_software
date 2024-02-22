import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from lib.view.LoginWindow import LoginWindow
from res.Dimensions import FontDimensions

# Main
if __name__ == '__main__':

    # Applicazione
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Default style
    app.setFont(QFont('Helvetica', FontDimensions.DEFAULT))  # Default font

    # Schermata di login
    window = LoginWindow()
    window.show()

    # Esegue l'applicazione
    sys.exit(app.exec())
