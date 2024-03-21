from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QValidator, QRegularExpressionValidator, QIntValidator


# Classe che rappresenta una regola di validazione. Essa si traduce in una sottoclasse QValidator e in un messaggio
# testuale di errore. Si può istanziare la classe usando il costruttore principale o uno dei classmethod predefiniti.
# noinspection PyPep8Naming
class ValidationRule:

    def __init__(self, validator: QValidator, error_message: str = "Input non valido"):
        self.validator: QValidator = validator
        self.error_message = error_message

    # Ritorna True se il contenuto è accettabile (QValidator ritorna "2" se il contenuto è "Acceptable")
    def validate(self, text: str) -> bool:
        return self.validator.validate(text) == 2

    # Costruttori secondari ("classmethods")
    @classmethod
    def Required(cls, error_message: str = "Il campo è richiesto"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^.{1,}$"))

        return cls(validator, error_message)

    @classmethod
    def MinLength(cls, min_length: int, error_message: str = None):
        validator = QRegularExpressionValidator(
            QRegularExpression("^.{" + str(min_length) + ",}$"))

        error_message = error_message or f"La lunghezza minima è {min_length} caratteri"

        return cls(validator, error_message)

    @classmethod
    def MaxLength(cls, max_length: int, error_message: str = None):
        validator = QRegularExpressionValidator(
            QRegularExpression("^.{," + str(max_length) + "}$"))

        error_message = error_message or f"La lunghezza massima è {max_length} caratteri"

        return cls(validator, error_message)

    @classmethod
    def Length(cls, min_length: int, max_length: int, error_message: str = None):
        validator = QRegularExpressionValidator(
            QRegularExpression("^{" + str(min_length) + "," + str(max_length) + "}$"))

        error_message = error_message or f"La lunghezza deve essere compresa tra {min_length} è {max_length} caratteri"

        return cls(validator, error_message)

    @classmethod
    def MinValue(cls, min_value: int, error_message: str = None):
        validator = QIntValidator()
        validator.setBottom(min_value)

        error_message = error_message or f"Il valore minimo è {min_value}"

        return cls(validator, error_message)

    @classmethod
    def MaxValue(cls, max_value: int, error_message: str = None):
        validator = QIntValidator()
        validator.setTop(max_value)

        error_message = error_message or f"Il valore massimo è {max_value}"

        return cls(validator, error_message)

    @classmethod
    def Range(cls, min_value: int, max_value: int, error_message: str = None):
        validator = QIntValidator(min_value, max_value)

        error_message = error_message or f"Il valore deve essere compreso tra {min_value} e {max_value}"

        return cls(validator, error_message)

    @classmethod
    def Email(cls, error_message: str = "Il testo non è una email valida"):
        validator = QRegularExpressionValidator(
            QRegularExpression("\\b[A-Za-z0-9àèéìòù._%+-]+@[A-Za-z0-9àèéìòù.-]+\\.[A-Za-z]{2,4}\\b"))

        return cls(validator, error_message)

    @classmethod
    def Name(cls, error_message: str = "Il testo non è un nome valido"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^(?=.{2,40}$)[a-zA-Zàèéìòù]+(?:[-'\\s][a-zA-Zàèéìòù]+)*$"))

        return cls(validator, error_message)

    @classmethod
    def Phone(cls, error_message: str = "Il testo non è un numero di telefono valido"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^[+]? *[0-9][0-9 ]{9,16}$"))

        return cls(validator, error_message)

    @classmethod
    def Numbers(cls, error_message: str = "Il testo può contenere solo numeri"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^[0-9]+$"))

        return cls(validator, error_message)

    @classmethod
    def Address(cls, error_message: str = "Il testo non è un indirizzo valido"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^[a-zA-Z0-9àèéìòù .,'-()]+$"))

        return cls(validator, error_message)

    @classmethod
    def IVANumber(cls, error_message: str = "Il testo deve essere una Partita IVA valida"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^[0-9]{11}$"))

        return cls(validator, error_message)

    @classmethod
    def FiscalCode(cls, error_message: str = "Il testo deve essere un codice fiscale valido"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$"))

        return cls(validator, error_message)

    @classmethod
    def Password(cls, error_message: str = "La password deve essere lunga almeno 6 caratteri"):
        validator = QRegularExpressionValidator(
            QRegularExpression("^\\S{6,}$"))

        return cls(validator, error_message)

    @classmethod
    def RegExp(cls, regex: str, error_message: str = None):
        validator = QRegularExpressionValidator(QRegularExpression(regex))

        if error_message:
            return cls(validator, error_message)
        else:
            return cls(validator)
