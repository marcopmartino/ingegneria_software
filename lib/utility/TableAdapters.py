from abc import ABC, abstractmethod
from typing import Callable

from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from lib.validation.FormManager import FormManager
from lib.widget.TableWidgets import ExtendedTableWidget, SingleRowStandardTable, StandardTable


# Classe astratta rappresentante un adattatore per tabelle. Si tratta di un'interfaccia per interagire con una tabella
# che facilita l'inserimento, l'aggiornamento e la rimozione di dati
# noinspection PyPep8Naming
class ITableAdapter(ABC):
    def __init__(self, table: ExtendedTableWidget):
        super().__init__()

        # La tabella da adattare
        self.table: ExtendedTableWidget = table

    # Converte un oggetto in una lista di stringhe da mostrare nelle celle di una riga della tabella
    @abstractmethod
    def adaptData(self, element: any) -> list[str]:
        pass

    # Popola la tabella con nuovi dati - imposta i QTableWidgetItem
    @abstractmethod
    def setData(self, data: any):
        pass

    # Aggiorna la tabella con nuovi dati - agisce sui QTableWidgetItem precedentemente impostati
    @abstractmethod
    def updateData(self, data: any):
        pass


# Adapter per tabelle composta da una sola riga
# noinspection PyPep8Naming
class SingleRowTableAdapter(ITableAdapter, ABC):
    def __init__(self, table: ExtendedTableWidget):
        super().__init__(table)

    # Costruttore secondario che crea e assegna automaticamente una tabella all'Adapter
    @classmethod
    def autoSetup(cls, table_parent: QWidget = None):
        instance = cls(SingleRowStandardTable(table_parent))
        return instance, instance.table

    # Popola la tabella con nuovi dati - imposta i QTableWidgetItem
    def setData(self, data: any):
        data: list[str] = self.adaptData(data)
        for column in range(self.table.columnCount()):
            self.table.setColumnItem(column, QTableWidgetItem(data[column]))

    # Aggiorna i dati di una riga della tabella - agisce sui QTableWidgetItem già impostati
    def updateData(self, data: any):
        data: list[str] = self.adaptData(data)
        for column in range(self.table.columnCount()):
            self.table.columnItem(column).setText(data[column])

    # Aggiorna i dati di alcune colonne di una riga della tabella - agisce sui QTableWidgetItem già impostati
    def updateDataColumns(self, data: any, columns: list[int]):
        data: list[str] = self.adaptData(data)
        for column in columns:
            self.table.columnItem(column).setText(data[column])


# noinspection PyPep8Naming
class TableAdapter(ITableAdapter, ABC):

    def __init__(self, table: ExtendedTableWidget):
        super().__init__(table)

        # Indica quale colonna contiene la chiave dei dati mostrati nelle righe della tabella
        self.__key_column: int = 0

        # Dizionario che associa tipi di QTableWidgetItem a colonne della tabella
        # Usato per impostare QTableWidgetItem personalizzati in determinate colonne
        self.__column_item_class_dict: dict[int, type(QTableWidgetItem)] = dict()

    # Costruttore secondario che crea e assegna automaticamente una tabella all'Adapter
    @classmethod
    def autoSetup(cls, table_parent: QWidget = None):
        instance = cls(StandardTable(table_parent))
        return instance, instance.table

    # Eseguito alla selezione di una cella (o di una riga se si usa una StandardTable con impostazioni predefinite)
    def onSelection(self, callback: Callable[[str], any]):
        self.table.cellClicked.connect(lambda: callback(self.getSelectedItemKey()))

    # Eseguito al doppio click su una cella (o su una riga se si usa una StandardTable con impostazioni predefinite)
    def onDoubleClick(self, callback: Callable[[str], any]):
        self.table.cellDoubleClicked.connect(lambda: callback(self.getSelectedItemKey()))

    # Imposta la colonna che contiene la chiave dei dati mostrati nelle righe della tabella
    def setKeyColumn(self, column_index: int):
        self.__key_column = column_index

    # Nasconde la colonna che contiene la chiave dei dati mostrati nelle righe della tabella
    def hideKeyColumn(self):
        self.table.hideColumn(self.__key_column)

    # Mostra la colonna che contiene la chiave dei dati mostrati nelle righe della tabella
    def showKeyColumn(self):
        self.table.showColumn(self.__key_column)

    # Ritorna la chiave dell'elemento mostrato in una riga
    def getItemKey(self, row: int) -> str:
        return self.table.item(row, self.__key_column).text()

    # Ritorna le chiavi degli elementi mostrati in ogni riga
    def getItemKeys(self) -> list[str]:
        keys: list[str] = []

        for row in range(self.table.rowCount()):
            keys.append(self.getItemKey(row))

        return keys

    # Ritorna la chiave dell'elemento mostrato nella riga attualmente selezionata
    def getSelectedItemKey(self) -> str:
        return self.getItemKey(self.table.currentRow())

    # Ritorna l'indice della riga dell'elemento con la chiave cercata
    def getRowIndexByKey(self, key: str):
        for row in range(self.table.rowCount()):
            if self.table.item(row, self.__key_column).text() == key:
                return row

    # Rimuove la riga rappresentante l'elemento con la chiave cercata
    def removeRowByKey(self, key: str):
        for row in range(self.table.rowCount()):
            if self.table.item(row, self.__key_column).text() == key:
                self.table.removeRow(row)
                break

    # Ritorna il tipo di classe QTableWidgetItem assegnata alla colonna "column"
    def getColumnItemClass(self, column: int) -> type(QTableWidgetItem):
        return self.__column_item_class_dict.get(column, QTableWidgetItem)

    # Assegna il tipo di classe QTableWidgetItem "item_type" alla colonna "column"
    def setColumnItemClass(self, column: int, item_type: type(QTableWidgetItem)):
        self.__column_item_class_dict.update({column: item_type})

    # Eseguita successivamente all'aggiornamento di una riga della tabella
    def _onRowUpdated(self, row_data: list[str], row: int) -> None:
        pass

    # Popola la tabella con nuovi dati - imposta i QTableWidgetItem
    def setData(self, data: list[any]):
        self.table.setSortingEnabled(False)  # Disabilita il sorting mentre la tabella viene modificata
        self.table.clearContents()  # Svuota la tabella
        self.table.setRowCount(len(data))

        for row in range(0, self.table.rowCount()):
            element: any = data[row]
            adapted_element: list = self.adaptData(element)

            for column in range(0, self.table.columnCount()):
                self.table.setItem(row, column, self.getColumnItemClass(column)(adapted_element[column]))

            self._onRowUpdated(adapted_element, row)

        self.table.setSortingEnabled(True)  # Abilita il sorting una volta finito di modificare la tabella

        # Se il sorting è attivo mentre vengono aggiunte righe alla tabella, la riga viene ordinata automaticamente
        # non appena la cella oggetto di ordinamento viene popolata. Ciò può comportare lo spostamento della nuova
        # riga in un altro punto della tabella, e una delle vecchie righe prende il suo posto in fondo alla tabella.
        # Le celle successive a quella oggetto di ordinamento della riga che è appena stata spostata in fondo vengono
        # sovrascritte, mentre le celle successive della nuova riga rimangono vuote.

    def addData(self, data: any):
        self.table.setSortingEnabled(False)  # Disabilita il sorting mentre la tabella viene modificata
        adapted_data: list = self.adaptData(data)
        row_count: int = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        for column in range(0, self.table.columnCount()):
            self.table.setItem(row_count, column, self.getColumnItemClass(column)(adapted_data[column]))

        self._onRowUpdated(adapted_data, row_count)
        self.table.setSortingEnabled(True)  # Abilita il sorting una volta finito di modificare la tabella

    # Aggiorna i dati di una riga della tabella - agisce sui QTableWidgetItem già impostati
    def updateData(self, data: any):
        self.table.setSortingEnabled(False)  # Disabilita il sorting mentre la tabella viene modificata
        data: list = self.adaptData(data)
        key_column: int = self.__key_column
        data_key: str = data[key_column]

        for row in range(0, self.table.rowCount()):
            if self.table.item(row, key_column).text() == data_key:
                for column in range(0, self.table.columnCount()):
                    self.table.item(row, column).setText(data[column])

                self._onRowUpdated(data, row)
                break

        self.table.setSortingEnabled(True)  # Abilita il sorting una volta finito di modificare la tabella

    # Aggiorna i dati di alcune colonne di una riga della tabella - agisce sui QTableWidgetItem già impostati
    def updateDataColumns(self, data: list, columns: list[int]):
        self.table.setSortingEnabled(False)  # Disabilita il sorting mentre la tabella viene modificata
        data: list = self.adaptData(data)
        key_column: int = self.__key_column
        data_key: str = data[key_column]

        for row in range(0, self.table.rowCount()):
            if self.table.item(row, key_column).text() == data_key:
                for column in columns:
                    self.table.item(row, column).setText(data[column])

                self._onRowUpdated(data, row)
                break

        self.table.setSortingEnabled(True)  # Abilita il sorting una volta finito di modificare la tabella
