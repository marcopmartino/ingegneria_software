import sys

from PyQt5.QtCore import Qt, QLibraryInfo, QLocale, QTranslator
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

    # Installo un traduttore per il testo predefinito nei componenti Qt (QDialog, QMessageBox etc.)
    translator = QTranslator(app)
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load('qtbase_it', path)
    app.installTranslator(translator)

    # Esegue l'applicazione
    app.run()

    # Avvia il ciclo degli eventi da cui uscirà solo alla chiusura dell'applicazione
    sys.exit(app.exec())
