from datetime import datetime
from unittest import TestCase

from PyQt5.QtCore import QDate

from lib.utility.UtilityClasses import PriceFormatter, SerialNumberFormatter, DatetimeUtils


class UtilityClassesTestCase(TestCase):

    def test_price_formatter(self) -> None:
        self.assertEqual(PriceFormatter.format(0), "0,00")
        self.assertEqual(PriceFormatter.format(12), "12,00")
        self.assertEqual(PriceFormatter.format(-7), "-7,00")
        self.assertEqual(PriceFormatter.format(23.50), "23,50")
        self.assertEqual(PriceFormatter.format(-105.99), "-105,99")
        self.assertEqual(PriceFormatter.format(3.125), "3,12")

        self.assertEqual(PriceFormatter.unformat("0,00"), 0)
        self.assertEqual(PriceFormatter.unformat("12,00"), 12)
        self.assertEqual(PriceFormatter.unformat("-7,00"), -7)
        self.assertEqual(PriceFormatter.unformat("23,50"), 23.50)
        self.assertEqual(PriceFormatter.unformat("-105,99"), -105.99)

    def test_serial_number_formatter(self) -> None:
        self.assertEqual(SerialNumberFormatter.format(0), "0000")
        self.assertEqual(SerialNumberFormatter.format(1), "0001")
        self.assertEqual(SerialNumberFormatter.format(23), "0023")
        self.assertEqual(SerialNumberFormatter.format(780), "0780")
        self.assertEqual(SerialNumberFormatter.format(2174), "2174")
        self.assertEqual(SerialNumberFormatter.format(32783), "32783")

        self.assertEqual(SerialNumberFormatter.unformat("0000"), 0)
        self.assertEqual(SerialNumberFormatter.unformat("0001"), 1)
        self.assertEqual(SerialNumberFormatter.unformat("0023"), 23)
        self.assertEqual(SerialNumberFormatter.unformat("0780"), 780)
        self.assertEqual(SerialNumberFormatter.unformat("2174"), 2174)
        self.assertEqual(SerialNumberFormatter.unformat("32783"), 32783)

    def test_date_formatter(self) -> None:
        self.assertEqual(DatetimeUtils.format("12/03/2024"), QDate(2024, 3, 12))
        self.assertEqual(DatetimeUtils.format("04/06/2023"), QDate(2023, 6, 4))
        self.assertEqual(DatetimeUtils.format("21/12/1998"), QDate(1998, 12, 21))

        self.assertEqual(DatetimeUtils.unformat(QDate(2024, 3, 12)), "12/03/2024")
        self.assertEqual(DatetimeUtils.unformat(QDate(2023, 6, 4)), "04/06/2023")
        self.assertEqual(DatetimeUtils.unformat(QDate(1998, 12, 21)), "21/12/1998")


