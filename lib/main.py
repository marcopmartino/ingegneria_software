import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from lib.Application import Application
from res.Dimensions import FontSize

# main
if __name__ == '__main__':
    # Impostazioni applicazione
    # Abilita lo scaling automatico in base alla densità di pixel (DPI) del monitor
    Application.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    Application.setAttribute(Qt.AA_EnableHighDpiScaling)
    Application.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Applicazione
    app = Application(sys.argv)
    app.setStyle('Fusion')  # Default style
    app.setFont(QFont('Helvetica', FontSize.DEFAULT))  # Default font

    # Esegue l'applicazione
    app.run()

    # Avvia il ciclo degli eventi e si bloccherà fino alla chiusura dell'applicazione
    sys.exit(app.exec())
