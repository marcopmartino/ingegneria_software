from abc import abstractmethod, ABC
from enum import Enum
from typing import Callable

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtWidgets import QTableWidget, QWidget, QFrame, QAbstractItemView, QHeaderView, QStyledItemDelegate, \
    QTableWidgetItem

from lib.mvc.order.model.Order import Order
from lib.mvc.pricecatalog.model.PriceCatalog import PriceCatalog
from lib.utility.Singleton import singleton, Singleton
from lib.validation.FormManager import FormManager
from res import Styles
from res.Dimensions import TableDimensions, FontWeight, FontSize
from res.Strings import PriceCatalogStrings


# StyledItemDelegate per allineare al centro il testo di ogni cella
class AlignCenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenterDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


# Elemento della tabella dotato di nome
# noinspection PyPep8Naming
class NamedTableItem(QTableWidgetItem):
    def __init__(self, name: str, text: str = ''):
        super().__init__(text)
        self.itemName = name

    # Imposta il nome dell'elemento
    def setItemName(self, name: str):
        self.itemName = name


# Widget tabella esteso con una lista di NamedTableItem e nuovi metodi
# noinspection PyPep8Naming
class ExtendedTableWidget(QTableWidget):
    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)
        self.namedItems: list[NamedTableItem] = []

    # Imposta l'altezza di tutte le celle della tabella, header compresi
    def setCellHeight(self, height: int):
        # Imposta l'altezza degli header orizzontali
        self.horizontalHeader().setFixedHeight(height)
        # Imposta l'altezza degli header verticali (e quindi delle righe della tabella)
        self.verticalHeader().setDefaultSectionSize(height)

    # Imposta header orizzontali e numero di colonne
    def setHorizontalHeaders(self, headers: list[str]):
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

    # Nasconde gli header
    def hideHeaders(self):
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

    # Unisce tutte le celle della riga "row" a formare una riga. La riga ha altezza "rowSpan".
    def setRow(self, row: int, rowSpan: int = 1):
        self.setSpan(row, 0, rowSpan, self.columnCount())

    # Unisce tutte le celle della colonna "column" a formare una colonna. La colonna ha larghezza "columnSpan".
    def setColumn(self, column: int, columnSpan: int = 1):
        self.setSpan(0, column, self.rowCount(), columnSpan)

    # Ritorna l'elemento contenuto nella riga "row"
    def rowItem(self, row: int) -> QTableWidgetItem:
        return self.item(row, 0)

    # Ritorna l'elemento contenuto nella colonna "column"
    def columnItem(self, column: int) -> QTableWidgetItem:
        return self.item(0, column)

    # Imposta l'elemento "item" nella riga "row"
    def setRowItem(self, row: int, item: QTableWidgetItem):
        self.setItem(row, 0, item)

    # Imposta l'elemento "item" nella colonna "column"
    def setColumnItem(self, column: int, item: QTableWidgetItem):
        self.setItem(0, column, item)

    # Imposta una riga e l'elemento in essa contenuto
    def setRowAndItem(self, row: int, item: QTableWidgetItem, rowSpan: int = 1):
        self.setRow(row, rowSpan)
        self.setRowItem(row, item)

    # Imposta una colonna e l'elemento in essa contenuto
    def setColumnAndItem(self, column: int, item: QTableWidgetItem, columnSpan: int = 1):
        self.setRow(column, columnSpan)
        self.setRowItem(column, item)

    # Imposta un elemento con nome e lo aggiunge alla lista
    def setNamedItem(self, row: int, column: int, item: NamedTableItem):
        self.setItem(row, column, item)
        self.addNamedItem(item)

    # Aggiunge un elemento con nome alla lista
    def addNamedItem(self, item: NamedTableItem):
        self.namedItems.append(item)


# Tabella standard usata nell'applicazione
# noinspection PyPep8Naming
class StandardTable(ExtendedTableWidget):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

        # Tabella
        self.setStyleSheet(Styles.STANDARD_TABLE)  # Stile
        self.setFrameStyle(QFrame.NoFrame)  # Nasconde la linea di contorno esterna
        self.setShowGrid(False)  # Nasconde la griglia interna
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Imposta la selezione per righe anziché celle
        self.setSelectionMode(QAbstractItemView.SingleSelection)  # Imposta la seleziona singola anziché multipla
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Impedisce di modificare da tastiera le celle
        self.setSortingEnabled(True)  # Abilita l'ordinamento automatico delle righe in base ai valori di una colonna

        # Header
        self.verticalHeader().hide()  # Nasconde gli header verticali (laterali sinistri)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Abilita il ridimensionamento automatico

        # Celle
        self.setCellHeight(TableDimensions.DEFAULT_CELL_HEIGHT)  # Imposta l'altezza di cella
        self.setItemDelegate(AlignCenterDelegate(self))  # Imposta l'allineamento al centro per il testo delle celle


# noinspection PyPep8Naming
class SimpleTableAdapter(ABC):

    def __init__(self, table: QTableWidget):
        super().__init__()

        self.table: QTableWidget = table
        self.key_column: int = 0

    @abstractmethod
    def adaptData(self, element: any) -> list[str]:
        pass

    def setKeyColumn(self, column_index: int):
        self.key_column = column_index

    def hideKeyColumn(self):
        self.table.hideColumn(self.key_column)

    def showKeyColumn(self):
        self.table.showColumn(self.key_column)

    def getSelectedItemKey(self) -> str:
        return self.table.item(self.table.currentRow(), self.key_column).text()

    def removeRowByKey(self, key: str):
        for row in range(self.table.rowCount()):
            if self.table.item(row, self.key_column).text() == key:
                self.table.removeRow(row)
                break

    def setData(self, data: list[any]):
        self.table.setRowCount(len(data))

        for row in range(0, self.table.rowCount()):
            element: list = self.adaptData(data[row])

            for column in range(0, self.table.columnCount()):
                self.table.setItem(row, column, QTableWidgetItem(element[column]))

    def addData(self, data: list[any]):
        row_count: int = self.table.rowCount()
        self.table.setRowCount(row_count + len(data))

        index: int = 0
        for row in range(row_count, self.table.rowCount()):
            element: list = self.adaptData(data[index])

            for column in range(0, self.table.columnCount()):
                self.table.setItem(row, column, QTableWidgetItem(element[column]))

            index += 1

    def updateData(self, data: list[any]):
        for element in data:
            element: list = self.adaptData(element)
            key_column: int = self.key_column
            element_key: str = element[key_column]

            for row in range(0, self.table.rowCount()):
                if self.table.item(row, key_column).text() == element_key:
                    for column in range(0, self.table.columnCount()):
                        self.table.setItem(row, column, QTableWidgetItem(element[column]))

                    break

    def updateDataColumns(self, data: list[any], columns: list[int]):
        for element in data:
            element: list = self.adaptData(element)
            key_column: int = self.key_column
            element_key: str = element[key_column]

            for row in range(0, self.table.rowCount()):
                if self.table.item(row, key_column).text() == element_key:
                    for column in columns:
                        self.table.setItem(row, column, QTableWidgetItem(element[column]))

                    break


# noinspection PyPep8Naming
class AdvancedTableAdapter(SimpleTableAdapter, ABC):

    def __init__(self, table: QTableWidget, form_manager: FormManager):
        super().__init__(table)

        self.form_manager: FormManager = form_manager

    @abstractmethod
    def filterData(self, data: list[any], filters: dict[str, any]) -> list[any]:
        pass

    def setData(self, data: list[any]):
        super().setData(self.filterData(data, self.form_manager.data()))

    def addData(self, data: list[any]):
        super().addData(self.filterData(data, self.form_manager.data()))


# Tabella usata per rappresentare i listini prezzi
# noinspection PyPep8Naming
class PriceCatalogTable(ExtendedTableWidget):

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

        # Tabella
        self.setStyleSheet(Styles.PRICE_CATALOG_TABLE)  # Stile
        self.setFrameStyle(QFrame.NoFrame)  # Nasconde la linea di contorno esterna
        self.setShowGrid(True)  # Mostra la griglia interna
        self.setSelectionMode(QAbstractItemView.NoSelection)  # Impedisce la selezione di celle
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Impedisce di modificare da tastiera le celle
        self.setSortingEnabled(False)  # Disabilita il sorting automatico delle righe in base ai valori di una colonna
        self.setColumnCount(7)  # Imposta il numero di colonne della tabella

        # Header
        self.verticalHeader().hide()  # Nasconde gli header verticali (laterali sinistri)
        self.horizontalHeader().hide()  # Nasconde gli header orizzontali (superiori)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Abilita il ridimensionamento automatico

        # Celle
        self.setCellHeight(TableDimensions.DEFAULT_CELL_HEIGHT)  # Imposta l'altezza di cella
        self.setItemDelegate(AlignCenterDelegate(self))  # Imposta l'allineamento al centro per il testo delle celle

    # Aggiorna tutti i NamedTableItem in base alla corrispondenza tra i nomi degli item e le chiavi di un dict
    def updateAllNamedItems(self, data: dict):
        for item in self.namedItems:
            item.setText(PriceCatalog.price_format(data[item.itemName]))

    # Aggiorna un NamedTableItem cercandolo in base al nome
    def updateNamedItem(self, name, value):
        for item in self.namedItems:
            if item.itemName == name:
                item.setText(PriceCatalog.price_format(value))
                break


# Singleton con i font e i brush usati nelle PriceListTableSection
class PriceCatalogTableStyle(metaclass=Singleton):

    def __init__(self):
        self.primary_bold_font = QFont()
        self.primary_bold_font.setWeight(FontWeight.BOLD)
        self.primary_bold_font.setPointSize(FontSize.DEFAULT)

        self.secondary_bold_font = QFont()
        self.secondary_bold_font.setWeight(FontWeight.BOLD)
        self.secondary_bold_font.setPointSize(FontSize.TABLE_HEADER)

        self.italic_font = QFont()
        self.italic_font.setItalic(True)
        self.italic_font.setPointSize(FontSize.DEFAULT)

        self.blue_brush = QBrush(QColor(0, 95, 184))
        self.red_brush = QBrush(QColor(207, 0, 0))
        self.green_brush = QBrush(QColor(70, 142, 35))
        self.brown_brush = QBrush(QColor(92, 64, 51))


# Classe che rappresenta una sezione di una PriceListTable
class PriceCatalogTableSection(ABC):
    def __init__(self, rows):
        self.rows: int = rows  # Numero di righe occupate dalla sezione

    # Metodo che traccia la sezione su una PriceListTable "table" a partire dalla riga "start_row"
    @abstractmethod
    def draw(self, table: PriceCatalogTable, start_row: int = 0):
        pass


# Sezione costituita da una riga titolo e una riga sottotitolo.
class TitleAndSubtitleSection(PriceCatalogTableSection):
    def __init__(self, title_text: str, subtitle_text: str):
        super().__init__(2)
        self.title_text: str = title_text
        self.subtitle_text: str = subtitle_text

    def draw(self, table: PriceCatalogTable, start_row: int = 0):
        # Righe
        title_row = start_row
        subtitle_row = start_row + 1

        # Titolo
        table.setRowAndItem(title_row, QTableWidgetItem(self.title_text))
        table.rowItem(title_row).setFont(PriceCatalogTableStyle().primary_bold_font)

        # Sottotitolo
        table.setRowAndItem(subtitle_row, QTableWidgetItem(self.subtitle_text))
        table.rowItem(subtitle_row).setFont(PriceCatalogTableStyle().italic_font)


# Sezione costituita da un Header orizzontale (superiore) a due livelli, uno per riga. Il primo livello ha tre colonne,
# e ogni colonna è divisa in due sottocolonne (3 x 2 = 6 colonne in totale).
class SixColumnsHeaderSection(PriceCatalogTableSection):
    def __init__(self, corner_text: str, header_texts: list[str], subheader_texts: list[str]):
        super().__init__(2)
        self.corner_text: str = corner_text
        self.header_texts: list[str] = header_texts
        self.subheader_texts: list[str] = subheader_texts

    def draw(self, table: PriceCatalogTable, start_row: int = 0):
        # Righe
        header_row = start_row
        subheader_row = start_row + 1

        # Font
        secondary_bold_font = PriceCatalogTableStyle().secondary_bold_font

        # Brush
        blue_brush = PriceCatalogTableStyle().blue_brush
        red_brush = PriceCatalogTableStyle().red_brush
        green_brush = PriceCatalogTableStyle().green_brush

        # Angolo dell'Header
        table.setSpan(header_row, 0, 2, 1)
        table.setItem(header_row, 0, QTableWidgetItem(self.corner_text))
        table.item(header_row, 0).setFont(secondary_bold_font)

        # Header primo livello - Prima colonna
        table.setSpan(header_row, 1, 1, 2)
        table.setItem(header_row, 1, QTableWidgetItem(self.header_texts[0]))
        table.item(header_row, 1).setFont(secondary_bold_font)
        table.item(header_row, 1).setForeground(blue_brush)

        # Header primo livello - Seconda colonna
        table.setSpan(header_row, 3, 1, 2)
        table.setItem(header_row, 3, QTableWidgetItem(self.header_texts[1]))
        table.item(header_row, 3).setFont(secondary_bold_font)
        table.item(header_row, 3).setForeground(red_brush)

        # Header primo livello - Terza colonna
        table.setSpan(header_row, 5, 1, 2)
        table.setItem(header_row, 5, QTableWidgetItem(self.header_texts[2]))
        table.item(header_row, 5).setFont(secondary_bold_font)
        table.item(header_row, 5).setForeground(green_brush)

        # Header secondo livello - Primo sottolivello di ogni Header di primo livello
        table.setItem(subheader_row, 1, QTableWidgetItem(self.subheader_texts[0]))
        table.item(subheader_row, 1).setFont(secondary_bold_font)
        table.item(subheader_row, 1).setForeground(blue_brush)
        table.setItem(subheader_row, 3, QTableWidgetItem(self.subheader_texts[0]))
        table.item(subheader_row, 3).setFont(secondary_bold_font)
        table.item(subheader_row, 3).setForeground(red_brush)
        table.setItem(subheader_row, 5, QTableWidgetItem(self.subheader_texts[0]))
        table.item(subheader_row, 5).setFont(secondary_bold_font)
        table.item(subheader_row, 5).setForeground(green_brush)

        # Header secondo livello - Secondo sottolivello di ogni Header di primo livello
        table.setItem(subheader_row, 2, QTableWidgetItem(self.subheader_texts[1]))
        table.item(subheader_row, 2).setFont(secondary_bold_font)
        table.setItem(subheader_row, 4, QTableWidgetItem(self.subheader_texts[1]))
        table.item(subheader_row, 4).setFont(secondary_bold_font)
        table.setItem(subheader_row, 6, QTableWidgetItem(self.subheader_texts[1]))
        table.item(subheader_row, 6).setFont(secondary_bold_font)


# Sezione con header verticale (laterali sinistro) costituita dai sei colonne di dati.
class SixColumnsDataSection(PriceCatalogTableSection):
    def __init__(self, left_header_texts: list[str], data_names: list[list[str]]):
        super().__init__(len(left_header_texts))
        self.left_headers: list[str] = left_header_texts
        self.data_names: list[list[str]] = data_names  # Nomi dei NamedTableItem

    def draw(self, table: PriceCatalogTable, start_row: int = 0):

        # Righe
        first_data_row = start_row
        last_data_row = start_row + self.rows

        # Fone
        secondary_bold_font = PriceCatalogTableStyle().secondary_bold_font

        # Brush
        blue_brush = PriceCatalogTableStyle().blue_brush
        red_brush = PriceCatalogTableStyle().red_brush
        green_brush = PriceCatalogTableStyle().green_brush

        # Itera sulle righe
        iteration: int = 0
        for row in range(first_data_row, last_data_row):

            # Imposta l'Header sinistro della riga
            table.setItem(row, 0, QTableWidgetItem(self.left_headers[iteration]))
            table.item(row, 0).setFont(secondary_bold_font)

            # Itera sulle colonne di una riga
            for column in range(1, 7):  # Da 1 a 6

                # Imposta un NamedTableItem per la cella della riga
                table.setNamedItem(row, column, NamedTableItem(self.data_names[iteration][column - 1]))

            # Colora il testo della prima, terza e quinta colonna di dati
            table.item(row, 1).setForeground(blue_brush)
            table.item(row, 3).setForeground(red_brush)
            table.item(row, 5).setForeground(green_brush)

            iteration += 1


# Sezione con Header verticale (laterali sinistro) a due livelli, e una colonna di dati. Ogni HorizontalTreeSection
# rappresenta un solo elemento di primo livello con le sue foglie. Non ha header orizzontale (superiore).
class HorizontalTreeSection(PriceCatalogTableSection):
    def __init__(self, root_text: str, leaves_text: list[str], data_names: list[str], first_free: bool = False):
        super().__init__(len(leaves_text))
        self.root_text: str = root_text  # Testo dell'header di primo livello (radice)
        self.leaves_text: list[str] = leaves_text  # Testo degli header di secondo livello (foglie)
        self.data_names: list[str] = data_names  # Nomi dei NamedTableItem (uno per ogni header di secondo livello)
        self.first_free: bool = first_free  # Indica se il primo item è gratuito (senza prezzo)

    def draw(self, table: PriceCatalogTable, start_row: int = 0):

        # Righe
        first_data_row = start_row
        last_data_row = start_row + self.rows

        # Font
        secondary_bold_font = PriceCatalogTableStyle().secondary_bold_font

        # Brush
        brown_brush = PriceCatalogTableStyle().brown_brush

        # Header di primo livello
        table.setSpan(first_data_row, 0, 4, 2)
        table.setItem(first_data_row, 0, QTableWidgetItem(self.root_text))
        table.item(first_data_row, 0).setFont(secondary_bold_font)

        # Itera sulle righe
        iteration: int = 0
        for row in range(first_data_row, last_data_row):

            # Header di secondo livello
            table.setSpan(row, 2, 1, 3)
            table.setItem(row, 2, QTableWidgetItem(self.leaves_text[iteration]))

            # Cella con l'importo
            table.setSpan(row, 5, 1, 2)
            if self.first_free:
                if not iteration:
                    table.setItem(row, 5, QTableWidgetItem(PriceCatalogStrings.FREE))
                else:
                    table.setNamedItem(row, 5, NamedTableItem(self.data_names[iteration-1]))
            else:
                table.setNamedItem(row, 5, NamedTableItem(self.data_names[iteration]))
            table.item(row, 5).setForeground(brown_brush)

            iteration += 1


# Classe per la costruzione di PriceListTable tramite PriceListTableSection
class PriceCatalogTableBuilder:
    def __init__(self, table_parent: QWidget = None):
        self.__table_parent: QWidget = table_parent  # QWidget genitore della tabella
        self.__sectionList: list[PriceCatalogTableSection] = []  # Sezioni che compongono la tabella
        self.__row_count: int = 0  # Numero di righe della tabella

    # Aggiunge sezioni alla lista e incrementa il numero totale di righe della tabella
    def add_sections(self, *sections: PriceCatalogTableSection):
        for section in sections:
            self.__sectionList.append(section)
            self.__row_count += section.rows

    # Costruisce la tabella
    def build(self) -> PriceCatalogTable:

        # Crea una nuova PriceListTable e imposta il numero di righe
        table = PriceCatalogTable(self.__table_parent)
        table.setRowCount(self.__row_count)

        row_cursor: int = 0  # Cursore che scorre le righe della tabella sezione dopo sezione

        for section in self.__sectionList:
            section.draw(table, row_cursor)  # Traccio la sezione
            row_cursor += section.rows  # Aggiorno il cursore

        return table
