from abc import abstractmethod, ABC

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QCheckBox, QButtonGroup, QSpinBox

from lib.layout.LineEditLayout import LineEditLayout, LineEditCompositeLayout
from lib.validation.ValidationRule import ValidationRule
from res.Dimensions import ValidationDimensions

# Lunghezza di default per il testo in input
DEFAULT_MAX_LENGTH = ValidationDimensions.DEFAULT_MAX_LENGTH


# Implementazione del pattern Adapter: vogliamo che un Client possa lavorare facilmente con i campi della form,
# per esempio ciclando una lista dei campi per validarli ed estrarne i dati senza preoccuparsi di che tipo di campi
# si tratti. A questo scopo definiamo una serie di classi "wrapper" dei campi di input di Qt che fungono da adattatori.

# Classi Target (interfacce\classi astratte per le classi Adapter)
# Classe astratta che rappresenta un generico campo di una form
class IFormField(ABC):

    # Il costruttore prende come argomento il solo campo di input (un oggetto di tipo QObject)
    # Il campo di input è un QObject per poter includere i ButtonGroup
    def __init__(self, input_field: QObject):
        self.input_field: QObject = input_field

    # Ritorna il nome del campo
    def field_name(self) -> str:
        return self.input_field.objectName().split("_")[0]  # Nome dell'oggetto fino al primo "_"

    # Ritorna il dato\contenuto del campo.
    # Questo è il primo metodo adattato: è possibile estrarre il dato del campo indipendentemente dal tipo
    @abstractmethod
    def data(self) -> any:
        pass

    # Ritorna il nome del campo con il dato in esso contenuto sotto forma di dizionario
    def data_dict(self) -> dict[str: any]:
        return {self.field_name(): self.data()}

    # Esegue la validazione del campo.
    # Questo è il secondo metodo adattato: è possibile validare un campo indipendentemente dal tipo, anche se in realtà
    # è privo di validazione (per assenza di necessità o di possibilità)
    def validate(self) -> bool:
        # Trattandosi di un campo non necessariamente\non possibilmente validabile, esso passa sempre la validazione
        return True


# Classe astratta che rappresenta un campo validabile di una form
# noinspection PyPep8Naming
class IValidatableFormField(IFormField, ABC):

    # Il costruttore prende come argomento il solo campo di input (un oggetto di tipo QWidget)
    def __init__(self, input_field: QWidget):
        super().__init__(input_field)

    # Costruttore secondario che istanzia la classe impostando il campo e il validatore
    @classmethod
    def FieldAndValidator(cls, input_field: QWidget, validator: QValidator, max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(input_field)
        new_instance.set_validator(validator, max_length)
        return new_instance

    # Costruttore secondario che istanzia la classe impostando il campo e il validatore di una ValidationRule
    @classmethod
    def FieldAndRule(cls, input_field: QWidget, validation_rule: ValidationRule, max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(input_field)
        new_instance.set_validation_rule(validation_rule, max_length)
        return new_instance

    # Esegue la validazione del campo
    def validate(self):
        try:
            # Ritorna True se il contenuto è accettabile (QValidator ritorna "2" se il contenuto è "Acceptable")
            return self.validator().validate(self.data(), 0) == 2
        except TypeError:  # Errore causato dall'assenza di un QValidator associato
            print(f"Errore: Validatore non assegnato per \"{self.field_name()}\"")
            return True

    # Ritorna il validatore associato al campo
    def validator(self) -> QValidator:
        return self.input_field.validator()

    # Imposta come QValidator quello di una ValidationRule, e la lunghezza massima del testo in input
    def set_validation_rule(self, validation_rule: ValidationRule, max_length: int = DEFAULT_MAX_LENGTH):
        self.set_validator(validation_rule.validator, max_length)

    # Imposta un QValidator che eseguirà la validazione e la lunghezza massima del testo in input
    def set_validator(self, validator: QValidator, max_length: int = DEFAULT_MAX_LENGTH):
        self.input_field.setValidator(validator)
        self.input_field.setMaxLength(max_length)


# Classe astratta che rappresenta un campo validabile di una form minuto di una campo di errore
# noinspection PyPep8Naming
class ICompositeFormField(IValidatableFormField, ABC):

    # Il costruttore prende come argomenti il campo di input (un QWidget) e il campo di errore (una QLabel)
    def __init__(self, input_field: QWidget, error_label: QLabel):
        super().__init__(input_field)
        self.error_label: QLabel = error_label

    # Costruttore secondario che istanzia la classe impostando i campi e il validatore
    @classmethod
    def FieldsAndValidator(cls, input_field: QWidget, error_label: QLabel, validator: QValidator,
                           max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(input_field, error_label)
        new_instance.set_validator(validator, max_length)
        return new_instance

    # Costruttore secondario che istanzia la classe impostando i campi e il validatore di una ValidationRule
    @classmethod
    def FieldsAndRule(cls, input_field: QWidget, error_label: QLabel, validation_rule: ValidationRule,
                      max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(input_field, error_label)
        new_instance.set_validation_rule(validation_rule, max_length)
        return new_instance

    # Esegue la validazione del campo. Mostra il campo di errore solo se la validazione non ha successo.
    def validate(self):
        if super().validate():
            self.hide_error_message()
            return True
        else:
            self.show_error_message()
            return False

    # Imposta il validatore, il messaggio di errore e la lunghezza massima del testo in input
    def set_validation_rule(self, validation_rule: ValidationRule, max_length: int = DEFAULT_MAX_LENGTH):
        super().set_validation_rule(validation_rule, max_length)
        self.set_error_message(validation_rule.error_message)

    # Imposta il messaggio di errore
    def set_error_message(self, error_message: str):
        self.error_label.setText(error_message)

    # Mostra il campo di errore
    def show_error_message(self):
        self.error_label.setHidden(False)

    # Nasconde il campo di errore
    def hide_error_message(self):
        self.error_label.setHidden(True)


# Classi Adapter
# Classe adattatrice per QComboBox
class ComboBoxFormField(IFormField):

    def __init__(self, combo_box: QComboBox):
        super().__init__(combo_box)

    def data(self):
        return self.input_field.currentText()


# Classe adattatrice per QCheckBox
class CheckBoxFormField(IFormField):

    def __init__(self, check_box: QCheckBox):
        super().__init__(check_box)

    def data(self):
        return self.input_field.isChecked()


# Classe adattatrice per QSpinBox
class SpinBoxFormField(IFormField):
    def __init__(self, spin_box: QSpinBox):
        super().__init__(spin_box)

    def data(self):
        return self.input_field.value()


# Classe adattatrice per QButtonGroup
class RadioGroupFormField(IFormField):
    def __init__(self, radio_group: QButtonGroup):
        super().__init__(radio_group)

    def data(self):
        return self.input_field.checkedButton().text()


# Classe adattatrice per QLabel
class LabelFormField(IFormField):
    def __init__(self, label: QLabel):
        super().__init__(label)

    def data(self):
        return self.input_field.text()


# Classe adattatrice per QLineEdit senza validatore
# noinspection PyPep8Naming
class LineEditFormField(IFormField):
    def __init__(self, line_edit: QLineEdit):
        super().__init__(line_edit)

    def data(self):
        return self.input_field.text()

    # Costruttore secondario che istanza la classe impostando il QLineEdit di un LineEditLayout
    @classmethod
    def Layout(cls, line_edit_layout: LineEditLayout):
        return cls(line_edit_layout.line_edit)

    # Costruttore secondario che istanza la classe impostando il QLineEdit di un LineEditLayout, e la lunghezza
    # massima del testo in input
    @classmethod
    def LayoutAndLength(cls, line_edit_layout: LineEditLayout, max_length: int = DEFAULT_MAX_LENGTH):
        line_edit_layout.line_edit.setMaxLength(max_length)
        return cls(line_edit_layout.line_edit)


# Classe adattatrice per QLineEdit con validatore
# noinspection PyPep8Naming
class LineEditValidatableFormField(IValidatableFormField, LineEditFormField):
    def __init__(self, line_edit: QLineEdit):
        super().__init__(line_edit)

    # Costruttore secondario che istanza la classe impostando il QLineEdit di un LineEditLayout, un QValidator, e la
    # lunghezza massima del testo in input
    @classmethod
    def LayoutAndValidator(cls, line_edit_layout: LineEditLayout, validator: QValidator,
                           max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(line_edit_layout.line_edit)
        new_instance.set_validator(validator, max_length)
        return new_instance

    # Costruttore secondario che istanza la classe impostando il QLineEdit di un LineEditLayout, un QValidator di una
    # ValidationRule, e la lunghezza massima del testo in input
    @classmethod
    def LayoutAndRule(cls, line_edit_layout: LineEditLayout, validation_rule: ValidationRule,
                      max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(line_edit_layout.line_edit)
        new_instance.set_validation_rule(validation_rule, max_length)
        return new_instance

    # Esegue la validazione del testo in input
    def validate(self):
        return self.input_field.hasAcceptableInput()


# Classe adattatrice per QLineEdit con validatore e campo di errore
# noinspection PyPep8Naming
class LineEditCompositeFormField(ICompositeFormField, LineEditFormField):
    def __init__(self, line_edit: QLineEdit, error_label: QLabel):
        super().__init__(line_edit, error_label)

    # Costruttore secondario che istanza la classe impostando il QLineEdit e la QLabel di errore di un LineEditLayout
    @classmethod
    def Layout(cls, line_edit_layout: LineEditCompositeLayout):
        return cls(line_edit_layout.line_edit, line_edit_layout.error_label)

    # Costruttore secondario che istanza la classe impostando il QLineEdit e la QLabel di errore di un LineEditLayout,
    # e la lunghezza massima del testo in input
    @classmethod
    def LayoutAndLength(cls, line_edit_layout: LineEditCompositeLayout, max_length: int = DEFAULT_MAX_LENGTH):
        line_edit_layout.line_edit.setMaxLength(max_length)
        return cls(line_edit_layout.line_edit, line_edit_layout.error_label)

    # Costruttore secondario che istanza la classe impostando il QLineEdit e la QLabel di errore di un LineEditLayout,
    # un QValidator, e la lunghezza massima del testo in input
    @classmethod
    def LayoutAndValidator(cls, line_edit_layout: LineEditCompositeLayout, validator: QValidator,
                           max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(line_edit_layout.line_edit, line_edit_layout.error_label)
        new_instance.set_validator(validator, max_length)
        return new_instance

    # Costruttore secondario che istanza la classe impostando il QLineEdit e la QLabel di errore di un LineEditLayout,
    # il QValidator di una ValidationRule, e la lunghezza massima del testo in input
    @classmethod
    def LayoutAndRule(cls, line_edit_layout: LineEditCompositeLayout, validation_rule: ValidationRule,
                      max_length: int = DEFAULT_MAX_LENGTH):
        new_instance = cls(line_edit_layout.line_edit, line_edit_layout.error_label)
        new_instance.set_validation_rule(validation_rule, max_length)
        return new_instance

    # Esegue la validazione del testo in input. Mostra il campo di errore solo se la validazione non ha successo.
    def validate(self):
        if self.input_field.hasAcceptableInput():
            self.hide_error_message()
            return True
        else:
            self.show_error_message()
            return False
