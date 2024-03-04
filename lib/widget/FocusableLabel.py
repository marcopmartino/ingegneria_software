from PyQt5.QtWidgets import QWidget, QLabel


# QLabel che mostra una sottolineatura al passaggio del puntatore del mouse su di essa
# noinspection PyPep8Naming
class FocusableLabel(QLabel):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Imposta il font di default della Label
    def setDefaultFont(self):
        font = self.font()
        font.setUnderline(False)
        self.setFont(font)

    # Modifica il font aggiungendo la sottolineatura
    def setOnHoverFont(self):
        font = self.font()
        font.setUnderline(True)
        self.setFont(font)

    # Funzione eseguita quando il mouse viene spostato sopra la Label
    def enterEvent(self, event):
        super().enterEvent(event)
        self.setOnHoverFont()  # Sottolineato

    # Funzione eseguita quando il mouse viene spostato fuori dalla Label
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setDefaultFont()  # Non sottolineato
