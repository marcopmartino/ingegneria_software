from abc import ABC, abstractmethod
from typing import Callable

from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from lib.validation.FormManager import FormManager
from lib.widget.TableWidgets import ExtendedTableWidget, SingleRowStandardTable, StandardTable


# noinspection PyPep8Naming
class ITableAdapter(ABC):
    def __init__(self, table: ExtendedTableWidget):
        super().__init__()

        self.table: ExtendedTableWidget = table

    @abstractmethod
    def adaptData(self, element: any) -> list[str]:
        pass

    @abstractmethod
    def setData(self, data: any):
        pass

    @abstractmethod
    def updateData(self, data: any):
        pass


# noinspection PyPep8Naming
class SingleRowTableAdapter(ITableAdapter, ABC):
    def __init__(self, table: ExtendedTableWidget):
        super().__init__(table)

    @classmethod
    def autoSetup(cls, table_parent: QWidget = None):
        instance = cls(SingleRowStandardTable(table_parent))
        return instance, instance.table

    # Inserisce i dati nella riga della tabella
    def setData(self, data: any):
        data: list[str] = self.adaptData(data)
        for column in range(self.table.columnCount()):
            self.table.setColumnItem(column, QTableWidgetItem(data[column]))

    # Aggiorna i dati della riga della tabella
    def updateData(self, data: any):
        data: list[str] = self.adaptData(data)
        for column in range(self.table.columnCount()):
            self.table.columnItem(column).setText(data[column])

    def updateDataColumns(self, data: any, columns: list[int]):
        data: list[str] = self.adaptData(data)
        for column in columns:
            self.table.columnItem(column).setText(data[column])


# noinspection PyPep8Naming
class TableAdapter(ITableAdapter, ABC):

    def __init__(self, table: ExtendedTableWidget):
        super().__init__(table)

        self.__key_column: int = 0
        self.__column_item_class_dict: dict[int, type(QTableWidgetItem)] = dict()

    @classmethod
    def autoSetup(cls, table_parent: QWidget = None):
        instance = cls(StandardTable(table_parent))
        return instance, instance.table

    def onSelection(self, callback: Callable[[str], any]):
        self.table.cellClicked.connect(lambda: callback(self.getSelectedItemKey()))

    def onDoubleClick(self, callback: Callable[[str], any]):
        self.table.cellDoubleClicked.connect(lambda: callback(self.getSelectedItemKey()))

    def setKeyColumn(self, column_index: int):
        self.__key_column = column_index

    def hideKeyColumn(self):
        self.table.hideColumn(self.__key_column)

    def showKeyColumn(self):
        self.table.showColumn(self.__key_column)

    def getItemKey(self, row: int) -> str:
        return self.table.item(row, self.__key_column).text()

    def getItemKeys(self) -> list[str]:
        keys: list[str] = []

        for row in range(self.table.rowCount()):
            keys.append(self.getItemKey(row))

        return keys

    def getSelectedItemKey(self) -> str:
        return self.getItemKey(self.table.currentRow())

    def getRowIndexByKey(self, key: str):
        for row in range(self.table.rowCount()):
            if self.table.item(row, self.__key_column).text() == key:
                return row

    def removeRowByKey(self, key: str):
        for row in range(self.table.rowCount()):
            if self.table.item(row, self.__key_column).text() == key:
                self.table.removeRow(row)
                break

    def isTableEmpty(self):
        if self.table.rowCount() != 0:
            return False
        else:
            return True

    def getColumnItemClass(self, column: int) -> type(QTableWidgetItem):
        return self.__column_item_class_dict.get(column, QTableWidgetItem)

    def setColumnItemClass(self, column: int, item_type: type(QTableWidgetItem)):
        self.__column_item_class_dict.update({column: item_type})

    def setData(self, data: list[any]):
        self.table.setRowCount(len(data))

        for row in range(0, self.table.rowCount()):
            element: list = self.adaptData(data[row])

            for column in range(0, self.table.columnCount()):
                self.table.setItem(row, column, self.getColumnItemClass(column)(element[column]))

    def addData(self, data: any):
        data: list = self.adaptData(data)
        row_count: int = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        for column in range(0, self.table.columnCount()):
            self.table.setItem(row_count, column, self.getColumnItemClass(column)(data[column]))

    def updateData(self, data: any):
        data: list = self.adaptData(data)
        key_column: int = self.__key_column
        data_key: str = data[key_column]

        for row in range(0, self.table.rowCount()):
            if self.table.item(row, key_column).text() == data_key:
                for column in range(0, self.table.columnCount()):
                    self.table.item(row, column).setText(data[column])

                break

    def updateDataColumns(self, data: list, columns: list[int]):
        data: list = self.adaptData(data)
        key_column: int = self.__key_column
        data_key: str = data[key_column]

        for row in range(0, self.table.rowCount()):
            if self.table.item(row, key_column).text() == data_key:
                for column in columns:
                    self.table.item(row, column).setText(data[column])

                break
