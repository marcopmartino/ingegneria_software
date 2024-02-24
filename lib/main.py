import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from lib.view.AccessWindow import AccessWindow
from res.Dimensions import FontSize

# Main
if __name__ == '__main__':

    # Applicazione
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Default style
    app.setFont(QFont('Helvetica', FontSize.DEFAULT))  # Default font

    # Schermata di login
    window = AccessWindow()
    window.show()

    # Esegue l'applicazione
    sys.exit(app.exec())
