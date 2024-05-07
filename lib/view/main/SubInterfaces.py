from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from qfluentwidgets import SingleDirectionScrollArea, FluentIconBase, FluentIcon

from res import Styles


# Widget ereditato da tutte le sotto-interfacce della MainWindow
# noinspection PyPep8Naming
class SubInterfaceWidget(QWidget):

    def __init__(self,
                 name: str,
                 parent_widget: QWidget,
                 svg_icon: FluentIconBase,
                 scrollable: bool = False,
                 scrollable_sidebar: bool = False):
        super().__init__(parent_widget)

        # Base Widget - il widget Base include il frame Header e il widget Body
        self.setObjectName(name.lower().replace(' ', '_'))  # ObjectName unico
        self.setStyleSheet(Styles.BASE_WIDGET)

        # Base Layout
        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)
        self.base_layout.setObjectName("base_layout")
        # self.base_layout.setContentsMargins(0, 32, 0, 0)  # Lascia spazio per la TitleBar

        # Header Frame
        self.header_frame = QFrame(self)
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Plain)
        self.header_frame.setObjectName("header_frame")

        # Header Layout
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setObjectName("header_layout")
        self.header_layout.setContentsMargins(16, 12, 16, 12)
        self.header_layout.setSpacing(16)

        # Header Icon
        self.svg_icon = svg_icon
        self.svg_icon_widget = QSvgWidget(svg_icon.path())
        self.svg_icon_widget.setFixedSize(48, 48)

        # Header Text Layout
        self.header_text_layout = QVBoxLayout(self.header_frame)
        self.header_text_layout.setObjectName("header_text_layout")
        self.header_text_layout.setContentsMargins(0, 0, 0, 0)
        self.header_text_layout.setSpacing(0)

        # Header Title Label
        self.header_title_label = QLabel(self.header_frame)
        self.header_title_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum))
        self.header_title_label.setObjectName("header_title_label")
        self.header_title_label.setStyleSheet(Styles.LABEL_TITLE)

        # Header Subtitle Label
        self.header_subtitle_label = QLabel(self.header_frame)
        self.header_subtitle_label.setObjectName("header_subtitle_label")
        self.header_subtitle_label.setStyleSheet(Styles.LABEL_SUBTITLE)

        # Aggiungo titolo e sottotitolo al layout testuale dell'header
        self.header_text_layout.addWidget(self.header_title_label)
        self.header_text_layout.addWidget(self.header_subtitle_label)

        # Aggiungo l'icona e il layout testuale dell'header al layout dell'header
        self.header_layout.addWidget(self.svg_icon_widget)
        self.header_layout.addLayout(self.header_text_layout)

        # Body Widget - il widget Body include i frame Central e Sidebar
        self.body_widget = QWidget(self)
        self.body_widget.setObjectName("body_widget")

        # Body Layout
        self.body_layout = QHBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.body_layout.setObjectName("body_layout")

        # Central Frame
        self.central_frame = QFrame(self.body_widget)
        self.central_frame.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        self.central_frame.setFrameShape(QFrame.StyledPanel)
        self.central_frame.setFrameShadow(QFrame.Plain)
        self.central_frame.setObjectName("central_frame")

        # Central Layout
        self.central_layout = QVBoxLayout(self.central_frame)
        self.central_layout.setObjectName("central_layout")
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar Frame
        self.sidebar_frame = QFrame(self.body_widget)
        self.sidebar_frame.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        self.sidebar_frame.setFixedWidth(250)
        self.sidebar_frame.setFrameShape(QFrame.StyledPanel)
        self.sidebar_frame.setFrameShadow(QFrame.Plain)
        self.sidebar_frame.setObjectName("sidebar_frame")

        # Sidebar Layout
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setObjectName("sidebar_layout")
        self.sidebar_layout.setContentsMargins(16, 12, 16, 12)

        # Aggiungo i frame centrale e laterale al layout del Body
        if scrollable:
            central_scroll_area = SingleDirectionScrollArea(self.body_widget, Qt.Vertical)
            central_scroll_area.setWidget(self.central_frame)
            central_scroll_area.setSizePolicy(self.central_frame.sizePolicy())
            central_scroll_area.setFrameShape(QFrame.NoFrame)
            central_scroll_area.setWidgetResizable(True)
            central_scroll_area.setObjectName("central_scroll_area")
            self.body_layout.addWidget(central_scroll_area)

        else:
            self.body_layout.addWidget(self.central_frame)

        if scrollable_sidebar:
            sidebar_scroll_area = SingleDirectionScrollArea(self.body_widget, Qt.Vertical)
            sidebar_scroll_area.setWidget(self.sidebar_frame)
            sidebar_scroll_area.setSizePolicy(self.sidebar_frame.sizePolicy())
            sidebar_scroll_area.setFixedWidth(self.sidebar_frame.width())
            sidebar_scroll_area.setFrameShape(QFrame.NoFrame)
            sidebar_scroll_area.setWidgetResizable(True)
            sidebar_scroll_area.setObjectName("sidebar_scroll_area")
            self.body_layout.addWidget(sidebar_scroll_area)

        else:
            self.body_layout.addWidget(self.sidebar_frame)

        # Aggiungo il frame header e il Body al layout di base
        self.base_layout.addWidget(self.header_frame)
        self.base_layout.addWidget(self.body_widget)

    # Imposta il testo del titolo
    def setTitleText(self, text):
        self.header_title_label.setText(text)

    # Imposta il testo del sottotitolo
    def setSubtitleText(self, text):
        self.header_subtitle_label.setText(text)

    # Nascone il sottotitolo
    def hideSubtitle(self):
        self.header_subtitle_label.setHidden(True)

    # Nascone l'header
    def hideHeader(self):
        self.header_frame.setHidden(True)

    # Nascone il sottotitolo
    def hideSidebar(self):
        self.sidebar_frame.setHidden(True)


# Widget per le sotto-interfacce di secondo livello
# noinspection PyPep8Naming
class SubInterfaceChildWidget(SubInterfaceWidget):

    def __init__(self,
                 name: str,
                 parent_interface: SubInterfaceWidget,
                 scrollable: bool = False,
                 scrollable_sidebar: bool = False):
        super().__init__(name, parent_interface, parent_interface.svg_icon, scrollable, scrollable_sidebar)

