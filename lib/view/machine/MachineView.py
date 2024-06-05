from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHeaderView, QProgressBar, \
    QAbstractItemView
from qfluentwidgets import BodyLabel

from lib.controller.MachineController import MachineController
from lib.model.Machine import Machine, MachineOperationData, InputMaterial
from lib.model.Order import OrderState
from lib.model.ShoeLastVariety import ProductType
from lib.model.StoredItems import MaterialDescription
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.OrdersRepository import OrdersRepository
from lib.repository.StorageRepository import StorageRepository
from lib.utility.ObserverClasses import Message, Observer
from lib.utility.TableAdapters import SingleRowTableAdapter, TableAdapter
from lib.view.main.SubInterfaces import SubInterfaceWidget, SubInterfaceChildWidget
from lib.utility.gui.widget.CustomPushButton import CustomPushButton
from lib.utility.gui.widget.Separators import VerticalSpacer, HorizontalLine
from lib.utility.gui.widget.TableWidgets import SingleRowStandardTable, StandardTable
from res import Styles
from res.Dimensions import FontSize, FontWeight


class MachineView(SubInterfaceChildWidget):

    # Eseguito alla chiusura della finestra (dopo la chiamata "self.close()")
    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.controller.detach_observer(self.observer)  # Rimuove l'osservatore dal macchinario

    def __init__(self, parent_widget: SubInterfaceWidget, machine: Machine):
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

        # Tabella dettagli macchinario
        self.machine_table = SingleRowStandardTable(self.central_frame)
        self.machine_table_adapter = MachineDetailsAdapter(self.machine_table)
        headers = ["Capienza massima", "Fabbricato da"]
        self.machine_table.setFixedWidth(400)
        self.machine_table.setHeaders(headers)
        self.machine_table.setColumnWidth(0, 200)
        self.machine_table.setColumnWidth(1, 200)
        self.machine_table_adapter.setData(self.controller.get_machine())

        # Titolo tabella informazioni operazione
        self.operation_info_title = QLabel(self.controller.get_machine().OPERATION_NAME)
        self.operation_info_subtitle = QLabel("Informazioni sull'operazione")
        self.operation_info_title.setFont(font)
        self.operation_info_title.setContentsMargins(16, 16, 16, 0)
        self.operation_info_subtitle.setContentsMargins(16, 0, 16, 8)

        # Tabella informazioni operazione
        self.operation_info_table = StandardTable(self.central_frame)
        self.operation_info_table.setSelectionMode(QAbstractItemView.NoSelection)  # Disabilita la selezione
        self.operation_info_table_adapter = MachineOperationAdapter(self.operation_info_table)
        headers = ["Input", "Output", "Caratteristiche acquisite"]
        self.operation_info_table.setHeaders(headers)
        self.operation_info_table_adapter.setData(self.controller.get_machine().OPERATION_INFO)

        # Aggiorno l'altezza della tabella
        total_height = 40
        for row in range(self.operation_info_table.rowCount()):
            total_height += self.operation_info_table.rowHeight(row)
        self.operation_info_table.setFixedHeight(total_height)

        # Titolo tabella lista operazioni disponibili
        self.operation_list_title = QLabel(f"Lista operazioni")
        self.operation_list_subtitle = QLabel("Lista delle operazioni necessarie al completamento degli ordini")
        self.operation_list_title.setFont(font)
        self.operation_list_title.setContentsMargins(16, 16, 16, 0)
        self.operation_list_subtitle.setContentsMargins(16, 0, 16, 8)

        # Tabella lista operazioni disponibili
        self.operation_list_table = StandardTable(self.central_frame)
        self.operation_list_table_adapter = MachineOperationListAdapter(self.operation_list_table)
        headers = ["Id", "Input", "Output", "Ordini di interesse"]
        self.operation_list_table.setHeaders(headers)
        self.operation_list_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.operation_list_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.operation_list_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.operation_list_table.setColumnWidth(3, 150)
        self.operation_list_table.verticalScrollBar().setDisabled(True)  # Disabilita lo scroll per la tabella
        self.operation_list_table_adapter.hideKeyColumn()
        self.operation_list_table_adapter.onSelection(lambda operation_id: self.refresh_sidebar(operation_id))

        # Label che indica che la tabella con la lista delle operazioni è vuota
        font = QFont()
        font.setPointSize(FontSize.FLUENT_DEFAULT)
        font.setBold(True)
        self.empty_table_label = QLabel(self.central_frame)
        self.empty_table_label.setObjectName("empty_storage_label")
        self.empty_table_label.setText("Non ci sono operazioni da eseguire")
        self.empty_table_label.setFixedHeight(150)
        self.empty_table_label.setFont(font)

        # Popola il layout centrale in modo da allineare i Widget in alto
        # Usare "setAlignment" non funziona poiché va in conflitto con la SizePolicy del "central_layout"
        self.inner_central_layout = QVBoxLayout(self.central_frame)
        self.inner_central_layout.addWidget(self.machine_details_title)
        self.inner_central_layout.addWidget(self.machine_details_subtitle)
        self.inner_central_layout.addWidget(self.machine_table)
        self.inner_central_layout.addWidget(self.operation_info_title)
        self.inner_central_layout.addWidget(self.operation_info_subtitle)
        self.inner_central_layout.addWidget(self.operation_info_table)
        self.inner_central_layout.addWidget(self.operation_list_title)
        self.inner_central_layout.addWidget(self.operation_list_subtitle)
        self.inner_central_layout.addWidget(self.operation_list_table)
        self.inner_central_layout.addWidget(self.empty_table_label, alignment=Qt.AlignJustify)
        self.inner_central_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_central_layout.setSpacing(0)
        self.central_layout.addLayout(self.inner_central_layout)
        self.central_layout.addItem(VerticalSpacer(size_policy=QSizePolicy.Expanding))  # Costringe i widget in alto

        # Sidebar -----------------------------------

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
        self.select_operation_label = BodyLabel(
            text="Seleziona un'operazione per vedere ulteriori dettagli ed eseguirla")
        self.select_operation_label.setFont(small_font)
        self.select_operation_label.setWordWrap(True)
        self.select_operation_label.setFixedHeight(70)
        self.select_operation_label.setContentsMargins(0, 0, 0, 8)
        self.select_operation_label.setAlignment(Qt.AlignCenter)

        # Label "Operazione"
        self.operation_label = QLabel("Dettagli operazione")
        self.operation_label.setFont(big_font)

        # Sezione Output
        self.output_info_label = QLabel("Info output")
        self.output_info_label.setFont(big_bold_font)
        self.output_info_label.setContentsMargins(0, 6, 0, 2)

        self.output_required_label = QLabel("Richieste: ")
        self.output_required_label.setFont(small_bold_font)

        self.output_required_by_order_label = QLabel()
        self.output_required_by_order_label.setFont(small_font)
        self.output_required_by_order_label.setContentsMargins(0, 0, 0, 2)

        self.output_produced_label = QLabel("Prodotte: ")
        self.output_produced_label.setFont(small_bold_font)

        self.output_in_production_label = QLabel("In produzione: ")
        self.output_in_production_label.setFont(small_bold_font)

        self.output_to_be_produced_label = QLabel("Da produrre: ")
        self.output_to_be_produced_label.setFont(small_bold_font)

        # Sezione Input
        self.input_info_label = QLabel("Disponibilità input")
        self.input_info_label.setFont(big_bold_font)
        self.input_info_label.setContentsMargins(0, 6, 0, 2)

        # Lista con le Input Label
        self.input_labels = []

        # Sezione Richiesti
        self.required_for_start_label = QLabel("Richiesti per l'avvio")
        self.required_for_start_label.setFont(big_bold_font)
        self.required_for_start_label.setContentsMargins(0, 6, 0, 0)

        # Lista con le Required Label
        self.required_labels = []

        # Sezione Avvio\Gestione operazione
        self.start_machine_button = CustomPushButton.cyan(text="Avvia macchinario", point_size=FontSize.FLUENT_DEFAULT)
        self.start_machine_button.clicked.connect(lambda: {
            self.start_machine_button.setDisabled(True),
            self.controller.start_machine(self.operation_list_table_adapter.getSelectedItemKey())
        })

        self.operation_completed_label = BodyLabel(
            text="Operazione completata. Controlla i macchinari delle fasi successive.")
        self.operation_completed_label.setFont(small_font)
        self.operation_completed_label.setWordWrap(True)
        self.operation_completed_label.setAlignment(Qt.AlignCenter)
        self.operation_completed_label.setFixedHeight(80)
        self.operation_completed_label.setContentsMargins(0, 16, 0, 12)

        self.insufficient_input_label = BodyLabel(
            text="Input insufficiente per l'avvio del macchinario.")
        self.insufficient_input_label.setFont(small_font)
        self.insufficient_input_label.setWordWrap(True)
        self.insufficient_input_label.setAlignment(Qt.AlignCenter)
        self.insufficient_input_label.setFixedHeight(60)
        self.insufficient_input_label.setContentsMargins(0, 16, 0, 12)

        self.operation_progress_label = QLabel("Progresso operazione")
        self.operation_progress_label.setAlignment(Qt.AlignCenter)
        self.operation_progress_label.setContentsMargins(0, 12, 0, 6)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(Styles.PROGRESS_BAR)
        self.progress_bar.setValue(0)

        self.percentage_progress_label = QLabel()
        self.percentage_progress_label.setAlignment(Qt.AlignCenter)
        self.percentage_progress_label.setContentsMargins(0, 6, 0, 0)

        self.emergency_stop_button = CustomPushButton.red(text="Ferma macchinario")
        self.emergency_stop_button.setContentsMargins(0, 6, 0, 0)
        self.emergency_stop_button.clicked.connect(lambda: {
            self.emergency_stop_button.setDisabled(True),
            self.controller.emergency_stop_machine()
        })

        self.running_machine_layout = QVBoxLayout()
        self.running_machine_layout.setContentsMargins(0, 0, 0, 0)
        self.running_machine_layout.setSpacing(4)

        self.emergency_stop_label = BodyLabel(
            text="Fermare il macchinario solo in caso di emergenza. I materiali in lavorazione finiranno negli scarti.")
        self.emergency_stop_label.setFont(small_font)
        self.emergency_stop_label.setWordWrap(True)
        self.emergency_stop_label.setAlignment(Qt.AlignCenter)
        self.emergency_stop_label.setFixedHeight(110)
        self.emergency_stop_label.setContentsMargins(0, 12, 0, 16)

        # Widget e layout con le informazioni dell'operazione selezionata
        self.operation_details_widget = QWidget(self.sidebar_frame)
        self.operation_details_widget.setContentsMargins(0, 0, 0, 0)
        self.operation_details_widget.setHidden(True)

        self.operation_layout = QVBoxLayout(self.operation_details_widget)
        self.operation_layout.setAlignment(Qt.AlignTop)
        self.operation_layout.setContentsMargins(0, 0, 0, 0)
        self.operation_layout.setSpacing(0)

        # Aggiungo i widget al layout dell'operazione
        self.operation_layout.addWidget(self.operation_label)

        self.operation_layout.addWidget(self.output_info_label)
        self.operation_layout.addWidget(self.output_required_label)
        self.operation_layout.addWidget(self.output_required_by_order_label)
        self.operation_layout.addWidget(self.output_produced_label)
        self.operation_layout.addWidget(self.output_in_production_label)
        self.operation_layout.addWidget(self.output_to_be_produced_label)

        self.operation_layout.addSpacerItem(VerticalSpacer(6, QSizePolicy.Fixed))
        self.operation_layout.addWidget(HorizontalLine())

        self.operation_layout.addWidget(self.input_info_label)

        field_count = 9

        for number in range(field_count):
            label = QLabel()
            label.setFont(small_bold_font)
            label.setHidden(True)
            self.input_labels.append(label)
            self.operation_layout.addWidget(label)

        self.operation_layout.addSpacerItem(VerticalSpacer(6, QSizePolicy.Fixed))
        self.operation_layout.addWidget(HorizontalLine())

        self.operation_layout.addWidget(self.required_for_start_label)

        for number in range(field_count):
            label = QLabel()
            label.setFont(small_bold_font)
            label.setHidden(True)
            self.required_labels.append(label)
            self.operation_layout.addWidget(label)

        self.operation_layout.addSpacerItem(VerticalSpacer(12, QSizePolicy.Fixed))

        self.running_machine_layout.addWidget(self.operation_progress_label)
        self.running_machine_layout.addWidget(self.progress_bar)
        self.running_machine_layout.addWidget(self.percentage_progress_label)
        self.running_machine_layout.addSpacerItem(VerticalSpacer(16, QSizePolicy.Fixed))
        self.running_machine_layout.addWidget(self.emergency_stop_button)
        self.running_machine_layout.addWidget(self.emergency_stop_label)

        self.operation_layout.addWidget(self.start_machine_button)
        self.operation_layout.addWidget(self.operation_completed_label)
        self.operation_layout.addWidget(self.insufficient_input_label)
        self.operation_layout.addLayout(self.running_machine_layout)

        # Aggiungo i Widget al layout della sidebar
        self.sidebar_layout.setSpacing(0)

        self.sidebar_layout.addWidget(self.select_operation_label, alignment=Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.operation_details_widget, alignment=Qt.AlignTop)

        # Observer ------------------------------

        # Callback per l'observer
        def update_machine_view(message: Message):
            data = message.data()
            match message.event():
                case OrdersRepository.Event.ORDER_STATE_UPDATED:
                    if data.get_state() == OrderState.PROCESSING or data.get_state() == OrderState.COMPLETED:
                        self.refresh_machine_view()
                case StorageRepository.Event.PRODUCT_CREATED | StorageRepository.Event.PRODUCT_UPDATED \
                     | StorageRepository.Event.MATERIAL_UPDATED:
                    self.refresh_machine_view()
                case MachinesRepository.Event.MACHINE_STATE_UPDATED:
                    if data.get_machine_serial() == self.controller.get_machine_serial():
                        # Abilita\disabilita i pulsanti in base al nuovo stato del macchinario
                        self.start_machine_button.setDisabled(self.controller.is_machine_running())
                        self.emergency_stop_button.setEnabled(self.controller.is_machine_running())

                        # Imposta a 0% la barra di progresso
                        self.progress_bar.setValue(0)

                        # Imposta a 0% il testo che mostra la percentuale di progresso
                        self.percentage_progress_label.setText("0%")
                    self.refresh_machine_view()
                case MachinesRepository.Event.THREAD_MACHINE_PROGRESS_UPDATED:
                    if data.get_machine_serial() == self.controller.get_machine_serial():
                        self.refresh_progress()

        # Imposta l'observer
        # Usando i segnali il codice è eseguito sul Main Thread, evitando il crash dell'applicazione
        # (per esempio, l'apertura o la chiusura di finestre da un Thread secondario causa il crash dell'applicazione)
        self.messageReceived.connect(update_machine_view)
        self.observer: Observer = self.controller.observe_repositories(self.messageReceived.emit)

        # Aggiorna la vista
        self.refresh_machine_view()

        # Se il macchinario è in funzione
        if self.controller.is_machine_running():
            # Aggiorna il progresso
            self.refresh_progress()

    # Aggiorna i dettagli delle operazioni e la vista
    def refresh_machine_view(self):

        # Aggiorna i dati sulle operazioni e la tabella
        def refresh_operation_list_and_table():
            # Aggiorna i dati sulle operazioni
            self.controller.refresh_operation_list()

            # Aggiorna la tabella con i dati delle nuove operazioni
            self.refresh_operation_list_table()

        # Aggiorna la vista e seleziona la nuova operazione corrispondente a quella precedente l'aggiornamento
        def refresh_machine_view_and_select_operation(order_serial: str):
            # Aggiorna i dati sulle operazioni e la tabella
            refresh_operation_list_and_table()

            # Cerca la nuova operazione che corrisponde a quella precedente (stesso ordine associato)
            operation = self.controller.get_operation_by_order_serial(order_serial)

            # Se l'operazione è ancora presente nella lista
            if operation is not None:
                # Seleziona la nuova operazione nella tabella
                self.update_selected_row(operation.get_id())

                # Aggiorna la sidebar con i dati della nuova operazione che corrisponde a quella precedente
                self.refresh_sidebar(operation.get_id())

            else:
                # Nasconde i dettagli dell'operazione nella sidebar
                self.operation_details_widget.setHidden(True)

        # Esegue l'aggiornamento
        if self.controller.is_machine_running():
            # Disabilita la tabella con le operazioni (per non permettere di modificare la selezione e la sidebar)
            self.operation_list_table.setDisabled(True)

            # Prende la chiave dell'operazione corrente (seriale del primo ordine associato all'operazione corrente)
            operation_id = self.controller.get_machine().get_active_process().get_operation_id()

            # Aggiorna la vista e seleziona la nuova operazione corrispondente a quella precedente l'aggiornamento
            refresh_machine_view_and_select_operation(operation_id)

        else:
            # Abilita la tabella con la lista di operazioni
            self.operation_list_table.setEnabled(True)

            if self.operation_list_table.isRowSelected():
                # Prende la chiave dell'operazione corrente (seriale del primo ordine associato all'operazione corrente)
                operation_id = self.operation_list_table_adapter.getSelectedItemKey()

                # Aggiorna la vista e seleziona la nuova operazione corrispondente a quella precedente l'aggiornamento
                refresh_machine_view_and_select_operation(operation_id)

            else:
                # Aggiorna i dati sulle operazioni e la tabella
                refresh_operation_list_and_table()

                # Nasconde i dettagli dell'operazione
                self.operation_details_widget.setHidden(True)

                # Mostra la label di selezione di un'operazione
                self.select_operation_label.setHidden(False)

    # Aggiorna la riga selezionata della tabella in base all'id dell'operazione
    def update_selected_row(self, operation_id: str):
        # Individua la riga in cui l'operazione di trova
        operation_row = self.operation_list_table_adapter.getRowIndexByKey(operation_id)

        # Seleziona la riga della tabella
        self.operation_list_table.selectRow(operation_row)

    # Aggiorna la tabella
    def refresh_operation_list_table(self):
        # Aggiorna i dati della tabella
        self.operation_list_table_adapter.setData(self.controller.get_operation_list())

        # Aggiorna l'altezza della tabella
        table_height = self.operation_list_table.horizontalHeader().height()

        for row_index in range(self.operation_list_table.rowCount()):
            table_height += self.operation_list_table.rowHeight(row_index)

        self.operation_list_table.setFixedHeight(table_height)

        # Controlla se la tabella con la lista delle operazioni è vuota; se lo è, mostra la label che informa di ciò
        self.check_empty_table()

    # Aggiorna il progresso del processo
    def refresh_progress(self):
        progress_percentage = self.controller.get_machine().get_active_process().get_progress_percentage()
        self.progress_bar.setValue(progress_percentage)
        self.percentage_progress_label.setText(f"{str(progress_percentage)}%")

    # Aggiorna la sidebar
    def refresh_sidebar(self, operation_id: str):
        # Assegna testo e mostra le label dei materiali con le quantità
        def setup_labels(label_list: list[QLabel], shoe_last_quantity: int, material_list: list[InputMaterial]):

            # Nasconde tutte le label e reimposta il loro stile
            for label_ in label_list:
                label_.setStyleSheet("")
                label_.setHidden(True)

            # Imposta la label delle forme
            product_type_string = \
                "Abbozzi" if self.controller.get_machine_type() in (
                    "Sgrossatore", "Tornio", "Finitore") else "Forme"
            shoe_last_label = label_list[0]
            shoe_last_label.setText(f"{product_type_string}: {shoe_last_quantity}")
            shoe_last_label.setHidden(False)

            # Imposta una label dei materiali
            def setup_material_label(index__: int, text: str):
                label__ = label_list[index__]
                label__.setText(f"{text}: {material.get_quantity()}")
                label__.setHidden(False)

            for material in material_list:
                match material.get_material_description():
                    case MaterialDescription.BUSSOLA_STANDARD:
                        setup_material_label(1, "Bussole")
                    case MaterialDescription.BUSSOLA_RINFORZATA:
                        setup_material_label(2, "Bussole rinforzate")
                    case MaterialDescription.PIASTRA_CORTA | MaterialDescription.PIASTRA_MEDIA | \
                         MaterialDescription.PIASTRA_LUNGA:
                        setup_material_label(3, "Piastre")
                    case MaterialDescription.PIASTRA_PUNTA:
                        setup_material_label(4, "Piastre punta")
                    case MaterialDescription.PERNO:
                        setup_material_label(5, "Perni")
                    case MaterialDescription.MOLLA:
                        setup_material_label(6, "Molle")
                    case MaterialDescription.GANCIO_ALFA | MaterialDescription.GANCIO_TENDO:
                        setup_material_label(7, "Ganci")
                    case MaterialDescription.INCHIOSTRO:
                        setup_material_label(8, "Inchiostro")

        # Ottiene i dati dell'operazione
        operation_data = self.controller.get_operation_by_id(operation_id)

        # Sezione Output -----------------------------------

        # Imposta le stringhe sulle quantità complessive
        self.output_required_label.setText(f"Richieste: {operation_data.get_required_shoe_lasts()}")
        self.output_produced_label.setText(f"Prodotte: {operation_data.get_produced_shoe_lasts()}")
        self.output_in_production_label.setText(f"In produzione: {operation_data.get_in_production_shoe_lasts()}")
        self.output_to_be_produced_label.setText(f"Da produrre: {operation_data.get_to_be_produced_shoe_lasts()}")

        # Imposta la stringa con le quantità richieste divise per ordine
        required_by_order_string = ""
        for order in operation_data.get_order_list():
            required_by_order_string += f"Ordine {order.get_order_serial()}: {str(order.get_quantity())}\n"

        required_by_order_string = required_by_order_string[:-1]  # Rimuove gli ultimi due caratteri
        self.output_required_by_order_label.setText(required_by_order_string)

        # Sezione Input -----------------------------------

        # Assegna testo e mostra le label di con le quantità disponibili di materiali
        setup_labels(self.input_labels, operation_data.get_available_input_shoe_lasts(),
                     operation_data.get_available_input_materials())

        # Sezione Richiesti -----------------------------------

        # Assegna testo e mostra le label di con le quantità richieste per l'avvio di materiali
        setup_labels(self.required_labels, operation_data.get_required_to_start_shoe_lasts(),
                     operation_data.get_required_input_materials())

        # Estrae la quantità da una label dei materiali
        def extract_quantity(label_: QLabel) -> int:
            return int(label_.text().split(": ")[1])

        # Variabile che indica se il macchinario può essere avviato
        can_start_machine: bool = True

        # Colora il testo di rosso se la quantità disponibile non è sufficiente all'avvio
        for index in range(len(self.input_labels)):
            input_label = self.input_labels[index]
            if not input_label.isHidden():
                required_label = self.required_labels[index]
                if extract_quantity(input_label) < extract_quantity(required_label):
                    can_start_machine = False
                    input_label.setStyleSheet(Styles.ERROR_LABEL)
                    required_label.setStyleSheet(Styles.ERROR_LABEL)

        # Gestisce il caso speciale dell'inchiostro indelebile (uso non quantificabile automaticamente)
        required_ink_label = self.required_labels[-1]
        if not required_ink_label.isHidden():
            # Rimuove la quantità richiesta dalla label per l'inchiostro richiesto
            required_ink_label.setText(required_ink_label.text()[:-3])

            input_ink_label = self.input_labels[-1]
            if extract_quantity(input_ink_label) == 0:
                can_start_machine = False
                input_ink_label.setStyleSheet(Styles.ERROR_LABEL)
                required_ink_label.setStyleSheet(Styles.ERROR_LABEL)

        # Ottiene lo stato del macchinario
        is_running = self.controller.is_machine_running()

        # Determina se l'operazione è stata completata
        is_operation_completed = operation_data.get_to_be_produced_shoe_lasts() == 0

        # Mostra o nasconde la progress bar e le label relative
        self.operation_progress_label.setHidden(not is_running)
        self.progress_bar.setHidden(not is_running)
        self.percentage_progress_label.setHidden(not is_running)

        # Mostra o nasconde il pulsante e la label per lo stop del macchinario
        self.emergency_stop_button.setHidden(not is_running)
        self.emergency_stop_label.setHidden(not is_running)

        # Mostra o nasconde il pulsante per l'avvio del macchinario
        self.start_machine_button.setHidden(is_running)

        # Abilita o disabilita il pulsante per l'avvio del macchinario
        self.start_machine_button.setEnabled(can_start_machine and not is_operation_completed)

        # Mostra o nasconde la label che informa che l'operazione è completata
        self.operation_completed_label.setHidden(not is_operation_completed)

        # Mostra o nasconde la label che informa che i materiali immagazzinati sono insufficienti
        self.insufficient_input_label.setHidden(can_start_machine)

        # Mostra i dettagli dell'operazione
        self.operation_details_widget.setHidden(False)

        # Nasconde la label di selezione di un'operazione
        self.select_operation_label.setHidden(True)

    # Controlla se la tabella con la lista delle operazioni è vuota; se lo è, mostra la label che informa di ciò
    def check_empty_table(self):
        if self.operation_list_table.isEmpty():
            self.empty_table_label.setVisible(True)
            self.operation_list_table.setVisible(False)
        else:
            self.empty_table_label.setVisible(False)
            self.operation_list_table.setVisible(True)


# TableAdapters
class MachineDetailsAdapter(SingleRowTableAdapter):
    def adaptData(self, machine: Machine) -> list[str]:
        return [
            f"{machine.get_capacity()} paia",
            f"{machine.get_manufacturer()}"
        ]


class MachineOperationAdapter(TableAdapter):
    def adaptData(self, operation_info: list[str]) -> list[str]:
        return operation_info

    # Adatta l'altezza di cella al numero di righe del testo contenuto
    def _onRowUpdated(self, row_data: list[str], row: int) -> None:
        max_extra_lines = 0
        for string in row_data:
            extra_lines = string.count("\n")
            if extra_lines > max_extra_lines:
                max_extra_lines = extra_lines
        self.table.setRowHeight(row, 40 + 20 * max_extra_lines)


class MachineOperationListAdapter(TableAdapter):
    def adaptData(self, operation_data: MachineOperationData) -> list[str]:
        # Ottiene la quantità di paia necessarie ad avviare il processo basato su questa operazione
        process_quantity = operation_data.get_required_to_start_shoe_lasts()

        # Stabilisce se mostrare le quantità richieste
        show_required_quantities: bool = operation_data.get_to_be_produced_shoe_lasts() > 0

        # Determina il testo da mostrare nella prima colonna
        input_string = (f"{operation_data.get_input_shoe_last_variety().get_description()}"
                        + (f" (x{str(process_quantity)})" if show_required_quantities else ""))

        for input_material in operation_data.get_required_input_materials():
            input_string += (f"\n{input_material.get_material_description().value}"
                             + (f" (x{str(input_material.get_quantity())})" if show_required_quantities else ""))

        if operation_data.get_output_shoe_last_variety().get_product_type() == ProductType.FORMA_NUMERATA:
            input_string = input_string[:-4]  # Rimuove la quantità dall'Inchiostro indelebile "(x0)"

        # Determina il testo da mostrare nella seconda colonna
        output_string = (f"{operation_data.get_output_shoe_last_variety().get_description()}"
                         + (f" (x{str(process_quantity)})" if show_required_quantities else ""))

        # Determina il testo da mostrare nella terza colonna
        order_string = ""
        for order in operation_data.get_order_list():
            order_string += f"{order.get_order_serial()}, "

        order_string = order_string[:-2]  # Rimuove gli ultimi due caratteri

        return [
            operation_data.get_id(),
            input_string,
            output_string,
            order_string
        ]

    # Adatta l'altezza di cella al numero di righe del testo contenuto
    def _onRowUpdated(self, row_data: list[str], row: int) -> None:
        max_extra_lines = 0

        # Prima colonna
        second_row_data_strings = row_data[1].split("\n")  # Bisogna tenere conto degli endline presenti
        for second_row_data_string in second_row_data_strings:
            string_length = len(second_row_data_string)
            extra_lines = string_length // 25

            if extra_lines > max_extra_lines:
                max_extra_lines = extra_lines

        # Seconda colonna
        string_length = len(row_data[2])
        extra_lines = string_length // 25

        if extra_lines > max_extra_lines:
            max_extra_lines = extra_lines

        # Terza colonna
        string_length = len(row_data[3])
        extra_lines = string_length // 10

        if extra_lines > max_extra_lines:
            max_extra_lines = extra_lines

        self.table.setRowHeight(row, 40 + 20 * max_extra_lines)
