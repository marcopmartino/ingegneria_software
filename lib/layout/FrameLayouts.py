from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QWidget, QGridLayout, QLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout

from lib.widget.Separators import HorizontalSpacer, VerticalSpacer
from res.Dimensions import SpacerDimensions


# Classe astratta per i FrameLayout
# noinspection PyPep8Naming
class IFrameLayout(ABC):

    @abstractmethod
    def setSpacerDimensionsAndPolicies(self, first_value, second_value, first_size_policy, second_size_policy):
        pass

    @abstractmethod
    def setSpacerDimensionsAndPolicy(self, first_value, second_value, size_policy):
        pass

    @abstractmethod
    def setSpacerDimensionAndPolicies(self, value, first_size_policy, second_size_policy):
        pass

    @abstractmethod
    def setSpacerDimensionAndPolicy(self, value, size_policy):
        pass

    @abstractmethod
    def setCentralLayout(self, layout: QLayout):
        pass

    @abstractmethod
    def setCentralWidget(self, widget: QWidget):
        pass


# Metaclassi
class FrameLayoutMeta(type(QGridLayout), type(IFrameLayout)):
    pass


class HFrameLayoutMeta(type(QHBoxLayout), type(IFrameLayout)):
    pass


class VFrameLayoutMeta(type(QVBoxLayout), type(IFrameLayout)):
    pass


# Classe che estende un QGridLayout, usata per centrare un elemento e gestire il ridimensionamento degli spacers.
# noinspection PyPep8Naming
class FrameLayout(QGridLayout, IFrameLayout, metaclass=FrameLayoutMeta):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Imposta degli Spacers nei quattro lati del frame, specificando dimensioni e comportamento
    # Specifica dimensioni e comportamento separatamente per spacer orizzontali e verticali
    def setSpacerDimensionsAndPolicies(self,
                                       horizontal: int = SpacerDimensions.DEFAULT_PRIMARY,
                                       vertical: int = SpacerDimensions.DEFAULT_PRIMARY,
                                       h_size_policy: QSizePolicy = QSizePolicy.Preferred,
                                       v_size_policy: QSizePolicy = QSizePolicy.Preferred):
        horizontal_spacer = HorizontalSpacer(horizontal, h_size_policy)
        vertical_spacer = VerticalSpacer(vertical, v_size_policy)
        self.addItem(horizontal_spacer, 1, 0, 1, 1)  # Spacer sinistro
        self.addItem(horizontal_spacer, 1, 2, 1, 1)  # Spacer destro
        self.addItem(vertical_spacer, 2, 1, 1, 1)  # Spacer inferiore
        self.addItem(vertical_spacer, 0, 1, 1, 1)  # Spacer superiore

    # Specifica dimensioni separatamente per spacer orizzontali e verticali
    def setSpacerDimensionsAndPolicy(self,
                                     horizontal: int = SpacerDimensions.DEFAULT_PRIMARY,
                                     vertical: int = SpacerDimensions.DEFAULT_PRIMARY,
                                     size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(horizontal, vertical, h_size_policy=size_policy, v_size_policy=size_policy)

    # Specifica comportamento separatamente per spacer orizzontali e verticali
    def setSpacerDimensionAndPolicies(self,
                                      value: int = SpacerDimensions.DEFAULT_PRIMARY,
                                      h_size_policy: QSizePolicy = QSizePolicy.Preferred,
                                      v_size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(horizontal=value, vertical=value, h_size_policy=h_size_policy,
                                            v_size_policy=v_size_policy)

    # Specifica dimensioni e comportamento per tutti gli spacer
    def setSpacerDimensionAndPolicy(self,
                                    value: int = SpacerDimensions.DEFAULT_PRIMARY,
                                    size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(horizontal=value, vertical=value, h_size_policy=size_policy,
                                            v_size_policy=size_policy)

    # Imposta un Layout al centro del frame
    def setCentralLayout(self, layout: QLayout):
        self.addLayout(layout, 1, 1, 1, 1)

    # Imposta un Widget al centro del frame
    def setCentralWidget(self, widget: QWidget):
        self.addWidget(widget, 1, 1, 1, 1)


# Classe che estende un QHBoxLayout, usata per centrare un elemento e gestire il ridimensionamento degli spacers.
# noinspection PyPep8Naming
class HFrameLayout(QHBoxLayout, IFrameLayout, metaclass=HFrameLayoutMeta):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Imposta degli Spacers a sinistra e a destra del frame, specificando dimensioni e comportamento
    # Specifica dimensioni e comportamento separatamente per spacer sinistro e destro
    def setSpacerDimensionsAndPolicies(self,
                                       left: int = SpacerDimensions.DEFAULT_PRIMARY,
                                       right: int = SpacerDimensions.DEFAULT_PRIMARY,
                                       l_size_policy: QSizePolicy = QSizePolicy.Preferred,
                                       r_size_policy: QSizePolicy = QSizePolicy.Preferred):
        left_spacer = HorizontalSpacer(left, l_size_policy)
        right_spacer = HorizontalSpacer(right, r_size_policy)
        self.insertItem(0, left_spacer)  # Spacer sinistro
        self.insertItem(2, right_spacer)  # Spacer destro

    # Specifica dimensioni separatamente per spacer sinistro e destro
    def setSpacerDimensionsAndPolicy(self,
                                     left: int = SpacerDimensions.DEFAULT_PRIMARY,
                                     right: int = SpacerDimensions.DEFAULT_PRIMARY,
                                     size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(left, right, l_size_policy=size_policy,
                                            r_size_policy=size_policy)

    # Specifica comportamento separatamente per spacer sinistro e destro
    def setSpacerDimensionAndPolicies(self,
                                      value: int = SpacerDimensions.DEFAULT_PRIMARY,
                                      l_size_policy: QSizePolicy = QSizePolicy.Preferred,
                                      r_size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(left=value, right=value, l_size_policy=l_size_policy,
                                            r_size_policy=r_size_policy)

    # Specifica dimensioni e comportamento per tutti gli spacer
    def setSpacerDimensionAndPolicy(self,
                                    value: int = SpacerDimensions.DEFAULT_PRIMARY,
                                    size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(left=value, right=value, l_size_policy=size_policy,
                                            r_size_policy=size_policy)

    # Imposta un Layout al centro del frame
    def setCentralLayout(self, layout: QLayout):
        self.insertLayout(1, layout)

    # Imposta un Widget al centro del frame
    def setCentralWidget(self, widget: QWidget):
        self.insertWidget(1, widget)


# Classe che estende un QVBoxLayout, usata per centrare un elemento e gestire il ridimensionamento degli spacers.
# noinspection PyPep8Naming
class VFrameLayout(QVBoxLayout, IFrameLayout, metaclass=VFrameLayoutMeta):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

    # Imposta degli Spacers a sinistra e a destra del frame, specificando dimensioni e comportamento
    # Specifica dimensioni e comportamento separatamente per spacer superiore e inferiore
    def setSpacerDimensionsAndPolicies(self,
                                       top: int = SpacerDimensions.DEFAULT_PRIMARY,
                                       bottom: int = SpacerDimensions.DEFAULT_PRIMARY,
                                       t_size_policy: QSizePolicy = QSizePolicy.Preferred,
                                       b_size_policy: QSizePolicy = QSizePolicy.Preferred):
        top_spacer = VerticalSpacer(top, t_size_policy)
        bottom_spacer = VerticalSpacer(bottom, b_size_policy)
        self.insertItem(0, top_spacer)  # Spacer superiore
        self.insertItem(2, bottom_spacer)  # Spacer inferiroe

    # Specifica dimensioni separatamente per spacer superiore e inferiore
    def setSpacerDimensionsAndPolicy(self,
                                     top: int = SpacerDimensions.DEFAULT_PRIMARY,
                                     bottom: int = SpacerDimensions.DEFAULT_PRIMARY,
                                     size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(top, bottom, t_size_policy=size_policy,
                                            b_size_policy=size_policy)

    # Specifica comportamento separatamente per spacer superiore e inferiore
    def setSpacerDimensionAndPolicies(self,
                                      value: int = SpacerDimensions.DEFAULT_PRIMARY,
                                      t_size_policy: QSizePolicy = QSizePolicy.Preferred,
                                      b_size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(top=value, bottom=value, t_size_policy=t_size_policy,
                                            b_size_policy=b_size_policy)

    # Specifica dimensioni e comportamento per tutti gli spacer
    def setSpacerDimensionAndPolicy(self,
                                    value: int = SpacerDimensions.DEFAULT_PRIMARY,
                                    size_policy: QSizePolicy = QSizePolicy.Preferred):
        self.setSpacerDimensionsAndPolicies(top=value, bottom=value, t_size_policy=size_policy,
                                            b_size_policy=size_policy)

    # Imposta un Layout al centro del frame
    def setCentralLayout(self, layout: QLayout):
        self.insertLayout(1, layout)

    # Imposta un Widget al centro del frame
    def setCentralWidget(self, widget: QWidget):
        self.insertWidget(1, widget)
