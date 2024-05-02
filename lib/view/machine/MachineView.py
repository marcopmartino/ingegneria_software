from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCloseEvent, QFont, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHeaderView, QScrollArea, QProgressBar
from qfluentwidgets import PrimaryPushButton, ProgressBar

from lib.controller.MachineController import MachineController
from lib.model.Machine import Machine
from lib.repository.MachinesRepository import MachinesRepository
from lib.utility.ObserverClasses import Message, Observer
from lib.utility.TableAdapters import SingleRowTableAdapter, TableAdapter
from lib.view.main.BaseWidget import BaseWidget
from lib.widget.Separators import VerticalSpacer, HorizontalLine
from res import Colors, Styles
from res.Dimensions import FontSize, FontWeight


class MachineView(BaseWidget):
    messageReceived = pyqtSignal(Message)

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.controller.detach_machine_observer(self.observer)  # Rimuove l'osservatore dal macchinario

    def __init__(self, parent_widget: QWidget, machine: Machine):
        # Controller
        self.controller: MachineController = MachineController(machine)

        # Inizializzo il widget di base
        super().__init__(f"machine_{self.controller.get_machine_serial()}_view", parent_widget, True, True)

        # Titolo e sottotitolo
        self.setTitleText(self.controller.get_machine_serial())
        self.setSubtitleText(self.controller.get_machine_type())

        # Titolo tabella dettagli macchinario
        font = QFont()
        font.setPointSize(FontSize.TITLE)
        self.machine_details_title = QLabel(self.controller.get_machine_type())
        self.machine_details_subtitle = QLabel("Informazioni sul macchinario")
        self.machine_details_title.setFont(font)
        self.machine_details_title.setContentsMargins(16, 16, 16, 0)
        self.machine_details_subtitle.setContentsMargins(16, 0, 16, 8)

        # Dettagli ordine
        self.machine_table_adapter, self.machine_table = MachineDetailsAdapter.autoSetup(self)
        headers = ["Capienza massima", "Durata di un ciclo"]
        self.machine_table.setFixedWidth(400)
        self.machine_table.setHeaders(headers)
        self.machine_table.setColumnWidth(0, 200)
        self.machine_table.setColumnWidth(1, 200)
        self.machine_table_adapter.setData(self.controller.get_machine())

        # Titolo tabella dettagli operazione
        self.operation_details_title = QLabel("")
        self.operation_details_subtitle = QLabel("Informazioni sull'operazione")
        self.operation_details_title.setFont(font)
        self.operation_details_title.setContentsMargins(16, 16, 16, 0)
        self.operation_details_subtitle.setContentsMargins(16, 0, 16, 8)

        # Tabella dell'operazione
        self.operation_details_table_adapter, self.operation_details_table = MachineOperationAdapter.autoSetup(self)
        headers = ["Input", "Output", "Caratteristiche acquisite"]
        self.operation_details_table.setHeaders(headers)
        # self.article_table_adapter_main.setData(article)

        # Titolo tabella lista operazioni
        self.operation_list_title = QLabel(f"Lista operazioni")
        self.operation_list_subtitle = QLabel("Lista delle operazioni necessarie al completamento degli ordini")
        self.operation_list_title.setFont(font)
        self.operation_list_title.setContentsMargins(16, 16, 16, 0)
        self.operation_list_subtitle.setContentsMargins(16, 0, 16, 8)

        # Tabella lista operazioni
        self.operation_list_table_adapter, self.operation_list_table = MachineOperationListAdapter.autoSetup(self)
        headers = ["Input", "Output", "Ordini di interesse"]
        self.operation_list_table.setHeaders(headers)
        # self.article_table_adapter_main.setData(article)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.machine_details_title)
        self.inner_central_layout.addWidget(self.machine_details_subtitle)
        self.inner_central_layout.addWidget(self.machine_table)
        self.inner_central_layout.addWidget(self.operation_details_title)
        self.inner_central_layout.addWidget(self.operation_details_subtitle)
        self.inner_central_layout.addWidget(self.operation_details_table)
        self.inner_central_layout.addWidget(self.operation_list_title)
        self.inner_central_layout.addWidget(self.operation_list_subtitle)
        self.inner_central_layout.addWidget(self.operation_list_table)
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addLayout(self.inner_central_layout)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))  # Costringe i widget in alto

        # Sidebar

        # Sidebar Fonts
        big_bold_font = QFont()
        big_bold_font.setPointSize(FontSize.SUBTITLE - 1)
        big_bold_font.setWeight(FontWeight.BOLD)
        small_bold_font = QFont()
        small_bold_font.setPointSize(FontSize.FLUENT_DEFAULT)
        small_bold_font.setWeight(FontWeight.BOLD)
        big_font = QFont()
        big_font.setPointSize(FontSize.SUBTITLE)
        small_font = QFont()
        small_font.setPointSize(FontSize.SMALL)

        # Label che indica di selezionare un'operazione dalla lista per visualizzare maggiori dettagli
        self.select_operation_label = QLabel("Seleziona un'operazione per vedere ulteriori dettagli ed eseguirla")
        self.select_operation_label.setFont(small_font)
        self.select_operation_label.setWordWrap(True)
        self.select_operation_label.setFixedHeight(70)
        self.select_operation_label.setContentsMargins(0, 0, 0, 8)
        self.select_operation_label.setAlignment(Qt.AlignCenter)

        # Label "Operazione"
        self.operation_label = QLabel("Dettagli operazione")
        self.operation_label.setFont(big_font)

        self.first_horizontal_line = HorizontalLine(color=Colors.BLACK)

        # Sezione Output
        self.output_info_label = QLabel("Info output")
        self.output_info_label.setFont(big_bold_font)
        self.output_info_label.setContentsMargins(0, 6, 0, 2)

        self.output_required_label = QLabel("Richieste: ")
        self.output_required_label.setFont(small_bold_font)

        self.output_produced_label = QLabel("Prodotte: ")
        self.output_produced_label.setFont(small_bold_font)

        self.output_in_production_label = QLabel("In produzione: ")
        self.output_in_production_label.setFont(small_bold_font)

        self.output_to_be_produced_label = QLabel("Da produrre: ")
        self.output_to_be_produced_label.setFont(small_bold_font)
        self.output_to_be_produced_label.setContentsMargins(0, 0, 0, 6)

        self.second_horizontal_line = HorizontalLine()

        # Sezione Input
        self.input_info_label = QLabel("Disponibilità input")
        self.input_info_label.setFont(big_bold_font)
        self.input_info_label.setContentsMargins(0, 6, 0, 2)

        self.third_horizontal_line = HorizontalLine()

        # Sezione Avvio\Gestione operazione
        self.required_for_start_label = QLabel("Richiesti per l'avvio")
        self.required_for_start_label.setFont(big_bold_font)
        self.required_for_start_label.setContentsMargins(0, 6, 0, 2)

        self.operation_progress_label = QLabel("Progresso operazione")
        #self.operation_progress_label.setAlignment(Qt.AlignCenter)
        self.operation_progress_label.setFont(big_font)
        self.operation_progress_label.setContentsMargins(0, 12, 0, 6)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(Styles.PROGRESS_BAR)
        self.progress_bar.setValue(35)

        self.percentage_progress_label = QLabel("[XX% completata]")
        self.percentage_progress_label.setAlignment(Qt.AlignCenter)
        self.percentage_progress_label.setContentsMargins(0, 6, 0, 0)

        self.remaining_time_label = QLabel("[remaining time]")
        self.remaining_time_label.setAlignment(Qt.AlignCenter)
        self.remaining_time_label.setContentsMargins(0, 2, 0, 16)

        self.emergency_stop_button = PrimaryPushButton(text="Ferma macchinario")

        self.emergency_stop_label = QLabel(
            "Fermare il macchinario solo in caso di emergenza. I materiali in lavorazione finiranno negli scarti.")
        self.emergency_stop_label.setFont(small_font)
        self.emergency_stop_label.setWordWrap(True)
        self.emergency_stop_label.setAlignment(Qt.AlignCenter)
        self.emergency_stop_label.setFixedHeight(110)
        self.emergency_stop_label.setContentsMargins(0, 12, 0, 16)

        # Aggiungo i Widget al Layout
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setSpacing(0)
        self.sidebar_layout.addWidget(self.select_operation_label)
        self.sidebar_layout.addWidget(self.operation_label)
        self.sidebar_layout.addWidget(self.first_horizontal_line)
        self.sidebar_layout.addWidget(self.output_info_label)
        self.sidebar_layout.addWidget(self.output_produced_label)
        self.sidebar_layout.addWidget(self.output_required_label)
        self.sidebar_layout.addWidget(self.output_in_production_label)
        self.sidebar_layout.addWidget(self.output_to_be_produced_label)
        self.sidebar_layout.addWidget(self.second_horizontal_line)
        self.sidebar_layout.addWidget(self.input_info_label)
        self.sidebar_layout.addWidget(self.third_horizontal_line)
        self.sidebar_layout.addWidget(self.required_for_start_label)
        self.sidebar_layout.addWidget(self.operation_progress_label)
        self.sidebar_layout.addWidget(self.progress_bar)
        self.sidebar_layout.addWidget(self.percentage_progress_label)
        self.sidebar_layout.addWidget(self.remaining_time_label)
        self.sidebar_layout.addWidget(self.emergency_stop_button)
        self.sidebar_layout.addWidget(self.emergency_stop_label)

        # Callback per l'observer
        def update_machine_view(message: Message):
            match message.event():
                case MachinesRepository.Event.MACHINE_STOPPED:
                    pass
                case MachinesRepository.Event.MACHINE_STARTED:
                    pass

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_machine_view)
        self.observer: Observer = self.controller.observe_machine(self.messageReceived.emit)


# TableAdapters
class MachineDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, machine: Machine) -> list[str]:
        return [
            f"{machine.get_capacity()} paia",
            ""
        ]


class MachineOperationAdapter(TableAdapter):
    def adaptData(self, machine: Machine) -> list[str]:
        return [
            "",
            "",
            ""
        ]


class MachineOperationListAdapter(TableAdapter):
    def adaptData(self, machine: Machine) -> list[str]:
        return [
            "",
            "",
            ""
        ]
