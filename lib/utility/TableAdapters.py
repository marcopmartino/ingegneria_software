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


# noinspection PyPep8Naming
class TableAdapter(ITableAdapter, ABC):

    def __init__(self, table: ExtendedTableWidget):
        super().__init__(table)

        self.key_column: int = 0

    @classmethod
    def autoSetup(cls, table_parent: QWidget = None):
        instance = cls(StandardTable(table_parent))
        return instance, instance.table

    def onSelection(self, callback: Callable[[str], any]):
        self.table.cellClicked.connect(lambda: callback(self.getSelectedItemKey()))

    def setKeyColumn(self, column_index: int):
        self.key_column = column_index

    def hideKeyColumn(self):
        self.table.hideColumn(self.key_column)

    def showKeyColumn(self):
        self.table.showColumn(self.key_column)

    def getItemKey(self, row: int) -> str:
        return self.table.item(row, self.key_column).text()

    def getItemKeys(self) -> list[str]:
        keys: list[str] = []

        for row in range(self.table.rowCount()):
            keys.append(self.getItemKey(row))

        return keys

    def getSelectedItemKey(self) -> str:
        return self.getItemKey(self.table.currentRow())

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
class AdvancedTableAdapter(TableAdapter, ABC):

    def __init__(self, table: ExtendedTableWidget, form_manager: FormManager):
        super().__init__(table)

        self.form_manager: FormManager = form_manager

    @classmethod
    def autoSetupWithFormManager(cls, form_manager: FormManager, table_parent: QWidget = None):
        instance = cls(StandardTable(table_parent), form_manager)
        return instance, instance.table

    @abstractmethod
    def filterData(self, data: list[any], filters: dict[str, any]) -> list[any]:
        pass

    def setData(self, data: list[any]):
        super().setData(self.filterData(data, self.form_manager.data()))

    def addData(self, data: list[any]):
        super().addData(self.filterData(data, self.form_manager.data()))