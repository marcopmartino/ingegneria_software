import re
from datetime import datetime


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


class DatetimeUtils:
    # Ritorna la data odierna in formato DD/MM/YYYY
    @staticmethod
    def current_date() -> str:
        return datetime.today().strftime('%d/%m/%Y')
