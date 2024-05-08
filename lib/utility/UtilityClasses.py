import re
from datetime import datetime

from PyQt5.QtCore import QDate


class PhoneFormatter:
    @staticmethod
    def format(phone: str):
        pattern = re.compile(r"^\+39\s[0-9]{3}\s[0-9]{3}\s[0-9]{4}$", re.IGNORECASE)
        if pattern.match(phone):
            print(phone)
            return phone
        else:
            return phone[:3] + ' ' + phone[3:6] + ' ' + phone[6:9] + ' ' + phone[9:]


class PriceFormatter:
    # Converte il prezzo in una stringa con due cifre nella parte decimale
    @staticmethod
    def format(value: float) -> str:
        return f"{value:.2f}".replace(".", ",")

    # Converte il prezzo nel corrispondente valore numerico
    @staticmethod
    def unformat(text: str) -> float:
        return float(text.replace(",", "."))


class SerialNumberFormatter:
    # Converte il valore numerico in una stringa con non meno di quattro caratteri
    @staticmethod
    def format(value: int) -> str:
        return f"{value:04d}"

    # Converte il seriale nel corrispondente valore numerico
    @staticmethod
    def unformat(text: str) -> int:
        return int(text)


class DatetimeUtils:
    # Ritorna la data odierna in formato DD/MM/YYYY
    @staticmethod
    def current_date() -> str:
        return datetime.today().strftime('%d/%m/%Y')

    # Converte una stringa DD/MM/YYYY in un oggetto QDate
    @staticmethod
    def format(dd_mm_yyyy_string: str) -> QDate:
        date_parts: list = dd_mm_yyyy_string.split('/')
        return QDate(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))

    # Converte un oggetto QDate in una stringa DD/MM/YYYY
    @staticmethod
    def unformat(date: QDate) -> str:
        return date.toString('dd/MM/yyyy')
