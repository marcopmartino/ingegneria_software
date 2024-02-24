from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QGridLayout, QLayout, QSpacerItem, QSizePolicy

from res import Styles
from res.Dimensions import LineEditDimensions, SpacerDimensions


# Classe che estende un QGridLayout, usata per centrare un elemento e gestire il ridimensionamento degli spacers.
# noinspection PyPep8Naming
class FrameLayout(QGridLayout):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Imposta degli Spacers nei quattro lati del frame
    def setSpacers(self,
                   horizontal: int = SpacerDimensions.DEFAULT_PRIMARY,
                   vertical: int = SpacerDimensions.DEFAULT_PRIMARY,
                   h_size_policy: QSizePolicy = QSizePolicy.Preferred,
                   v_size_policy: QSizePolicy = QSizePolicy.Preferred):
        horizontal_spacer = QSpacerItem(horizontal, SpacerDimensions.DEFAULT_SECONDARY, h_size_policy,
                                        QSizePolicy.Minimum)
        vertical_spacer = QSpacerItem(SpacerDimensions.DEFAULT_SECONDARY, vertical, QSizePolicy.Minimum, v_size_policy)
        self.addItem(horizontal_spacer, 1, 0, 1, 1)  # Spacer sinistro
        self.addItem(horizontal_spacer, 1, 2, 1, 1)  # Spacer destro
        self.addItem(vertical_spacer, 2, 1, 1, 1)  # Spacer inferiore
        self.addItem(vertical_spacer, 0, 1, 1, 1)  # Spacer superiore

    '''
    def setSpacers(self,
                   horizontal: int = SpacerDimensions.DEFAULT_PRIMARY,
                   vertical: int = SpacerDimensions.DEFAULT_PRIMARY,
                   size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacers(horizontal, vertical, h_size_policy=size_policy, v_size_policy=size_policy)

    def setSpacers(self,
                   value: int = SpacerDimensions.DEFAULT_PRIMARY,
                   h_size_policy: QSizePolicy = QSizePolicy.Preferred,
                   v_size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacers(horizontal=value, vertical=value, h_size_policy=h_size_policy, v_size_policy=v_size_policy)

    def setSpacers(self,
                   value: int = SpacerDimensions.DEFAULT_PRIMARY,
                   size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacers(horizontal=value, vertical=value, h_size_policy=size_policy, v_size_policy=size_policy)
    '''

    # Imposta un Layout al centro del frame
    def setCentralLayout(self, layout: QLayout):
        self.addLayout(layout, 1, 1, 1, 1)

    # Imposta un Widget al centro del frame
    def setCentralWidget(self, widget: QWidget):
        self.addWidget(widget, 1, 1, 1, 1)
