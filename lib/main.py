import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from lib.view.Access.AccessWindow import AccessWindow
from lib.view.Main.MainWindow import MainWindow
from res.Dimensions import FontSize

# Main
if __name__ == '__main__':

    # Impostazioni applicazione
    # Abilita lo scaling automatico in base alla densità di pixel (DPI) del monitor
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Applicazione
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Default style
    app.setFont(QFont('Helvetica', FontSize.DEFAULT))  # Default font

    # Schermata di login
    window = AccessWindow()
    # window = MainWindow()
    window.show()

    # Esegue l'applicazione
    sys.exit(app.exec())
