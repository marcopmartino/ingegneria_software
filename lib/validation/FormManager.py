from PyQt5.QtWidgets import QPushButton

from lib.validation.FormField import IFormField


# Classe per la gestione delle form. Automatizza il processo di validazione dei campi e di estrazione dei loro dati.
class FormManager:

    def __init__(self, field_list: list[IFormField] = None, form_token: any = None):
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

    # Esegue la validazione dei campi. Ritorna True solo se la validazione di ogni campo ha successo.
    def validate(self) -> bool:
        validation_successful: bool = True
        for form_field in self.field_list:
            validation_successful = form_field.validate()  # Possibile grazie alle classi adattatrici
        return validation_successful

    # Estrae i dati dai campi sotto forma di dizionario
    def data(self) -> dict[str, any]:
        data = {"form_token": self.form_token, "field_count": self.field_count()}
        for form_field in self.field_list:
            data.update(form_field.data_dict())  # Possibile grazie alle classi adattatrici
        return data

    # Aggiunge elementi alla lista dei campi
    def add_fields(self, *form_fields: IFormField):
        for form_field in form_fields:
            self.field_list.append(form_field)

    # Eseguito al click su un pulsante di submit: esegue la validazione, poi chiama una funzione di callback
    def on_submit(self, callback_success, callback_failure):
        print("About to validate")
        if self.validate():
            print("Validation Successful")
            callback_success(self.data())
        else:
            print("Validation Failure")
            if callback_failure:  # False se callback_failure è None
                callback_failure(self.data())

    # Aggiunge un pulsante di submit connettendo il segnale generato dall'evento di click con il metodo\slot
    # "on_submit", a cui vengono passate le funzioni di callback
    def add_submit_button(self, submit_button: QPushButton, callback_success: callable,
                          callback_failure: callable = None):
        submit_button.clicked.connect(lambda: self.on_submit(callback_success, callback_failure))

    # Aggiunge un pulsante per la sola estrazione dei dati, che vengono passati a una funzione di callback
    def add_data_button(self, submit_button: QPushButton, callback: callable):
        submit_button.clicked.connect(lambda: callback(self.data()))
