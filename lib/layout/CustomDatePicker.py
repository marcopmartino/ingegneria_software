from PyQt5.QtCore import QDate
from qfluentwidgets import DatePicker
from qfluentwidgets.components.date_time.date_picker import MonthFormatter


# noinspection PyPep8Naming
class CustomDatePicker(DatePicker):

    def __init__(self):
        super().__init__()
        self.MONTH = self.tr('Mese')
        self.YEAR = self.tr('Anno')
        self.DAY = self.tr('Giorno')

    def setDateFormat(self, format=None):
        self.clearColumns()
        y = QDate.currentDate().year()
        self.dayIndex = 0
        self.monthIndex = 1
        self.yearIndex = 2

        monthFormatter = MonthFormatter()
        monthFormatter.months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                                 "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
        self.setMonthFormatter(monthFormatter)

        self.addColumn(self.DAY, range(1, 32), 80,
                       formatter=self.dayFormatter())
        self.addColumn(self.MONTH, range(1, 13),
                       100, formatter=self.monthFormatter())
        self.addColumn(self.YEAR, range(y - 100, y + 101),
                       80, formatter=self.yearFormatter())

    def panelInitialValue(self):
        if any(self.value()):
            return self.value()

        date = QDate.currentDate()
        y = self.encodeValue(self.yearIndex, date.year())
        m = self.encodeValue(self.monthIndex, date.month())
        d = self.encodeValue(self.dayIndex, date.day())
        return [d, m, y]
