from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QLayout, QWidget

from lib.validation.FormField import IFormField, CheckBoxFormField, SpinBoxFormField, ComboBoxFormField, \
    LineEditFormField, DatePickerFormField


# Classe per la gestione delle form. Automatizza il processo di validazione dei campi e di estrazione dei loro dati.
class FormManager(QObject):
    # Segnale emesso quando i dati inseriti nei campi della form cambiano
    dataChanged = pyqtSignal()

    def __init__(self, field_list: list[IFormField] = None, form_token: any = None):
        super().__init__()
        if field_list is None:
            field_list = []  # Lista vuota
        self.field_list: list[IFormField] = field_list
        self.form_token = form_token

    # Ritorna il numero di campi associati al FormManager
    def field_count(self) -> int:
        return len(self.field_list)

    # Imposta un token (termine chiave\dato extra)
    def set_token(self, token: any) -> None:
        self.form_token = token

    # Svuota la lista dei campi associati al FormManager
    def reset_field_list(self) -> None:
        self.field_list = []

    # Esegue il reset dei campi
    def clear_fields(self):
        for field in self.field_list:
            field.clear()

    # Esegue la validazione dei campi. Ritorna True solo se la validazione di ogni campo ha successo.
    def validate(self) -> bool:
        validation_successful: bool = True
        for form_field in self.field_list:
            if not form_field.validate():  # Possibile grazie alle classi adattatrici
                validation_successful = False
        return validation_successful

    # Estrae i dati dai campi sotto forma di dizionario
    def data(self, raw: bool = False) -> dict[str, any]:
        data = {} if raw else {"form_token": self.form_token, "field_count": self.field_count()}
        for form_field in self.field_list:
            data.update(form_field.data_dict())  # Possibile grazie alle classi adattatrici
        return data

    # Aggiunge elementi alla lista dei campi
    def add_fields(self, *form_fields: IFormField):
        for form_field in form_fields:
            form_field.data_changed().connect(lambda: self.dataChanged.emit())
            self.add_field(form_field)

    # Aggiunge un elemento alla lista dei campi
    def add_field(self, form_field: IFormField):
        self.field_list.append(form_field)

    # Aggiunge elementi alla lista dei campi
    def add_objects(self, *objects: QObject):
        for obj in objects:
            self.add_object(obj)

    # Aggiunge un elemento alla lista dei campi
    def add_object(self, obj: QObject):
        match type(obj).__name__:
            case "QCheckBox" | "CheckBox":
                self.add_fields(CheckBoxFormField(obj))
            case "QSpinBox" | "SpinBox":
                self.add_fields(SpinBoxFormField(obj))
            case "QComboBox" | "ComboBox":
                self.add_fields(ComboBoxFormField(obj))
            case "QLineEdit" | "LineEdit" | "SearchLineEdit":
                self.add_fields(LineEditFormField(obj))
            case "DatePicker" | "CustomeDatePicker":
                self.add_fields(DatePickerFormField(obj))

    # Cerca e aggiunge i campi di input figli di un Widget
    def add_widget_fields(self, *widgets: QWidget):
        for widget in widgets:
            for child in widget.children():
                self.add_object(child)

    # Cerca e aggiunge i campi di input contenuti in un Layout
    def add_layout_fields(self, *layouts: QLayout):
        for layout in layouts:
            for index in range(0, layout.count() - 1):
                item = layout.itemAt(index).widget()
                self.add_object(item)

    # Eseguito al click su un pulsante di submit: esegue la validazione, poi chiama una funzione di callback
    def __on_submit(self, callback_success: callable, callback_failure: callable, raw_data: bool):
        print("About to validate")
        if self.validate():
            print("Validation Successful")
            callback_success(self.data(raw_data))
        else:
            print("Validation Failure")
            if callback_failure:  # False se callback_failure è None
                callback_failure(self.data(raw_data))

    # Aggiunge un pulsante di submit connettendo il segnale generato dall'evento di click con il metodo\slot
    # "on_submit", a cui vengono passate le funzioni di callback
    def add_submit_button(self, submit_button: QPushButton, callback_success: callable,
                          callback_failure: callable = None, raw_data: bool = False):
        submit_button.clicked.connect(lambda: self.__on_submit(callback_success, callback_failure, raw_data))

    # Aggiunge un pulsante per la sola estrazione dei dati, che vengono passati a una funzione di callback
    def add_data_button(self, submit_button: QPushButton, callback: callable, raw_data: bool = False):
        submit_button.clicked.connect(lambda: callback(self.data(raw_data)))

    # Aggiunge un pulsante per la sola estrazione del token, che viene passato a una funzione di callback
    def add_token_button(self, submit_button: QPushButton, callback: callable):
        submit_button.clicked.connect(lambda: callback(self.form_token))
