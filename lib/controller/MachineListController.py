from threading import Thread
from time import sleep

from lib.model.Machine import Machine
from lib.repository.MachinesRepository import MachinesRepository
from lib.repository.StorageRepository import StorageRepository


class MachineListController:
    def __init__(self):
        super().__init__()
        self.__machines_repository = MachinesRepository()
        self.__storage_repository = StorageRepository()

    # Imposta un osservatore per la repository
    def observe_machine_list(self, callback: callable):
        self.__machines_repository.observe(callback)

    # Ritorna un macchinario in base al suo nome seriale
    def get_machine_by_id(self, machine_serial: str) -> Machine:
        return self.__machines_repository.get_machine_by_id(machine_serial)

    # Ritorna la lista di macchinari filtrata
    def get_machine_list(self, filters: dict[str, any]) -> list[Machine]:
        return self.filter_machines(filters, *self.__machines_repository.get_machine_list())

    # Filtra una lista di macchinari
    # noinspection PyMethodMayBeStatic
    def filter_machines(self, filters: dict[str, any], *machines: Machine) -> list[Machine]:

        # Inizializzo alcune variabili e funzioni per ottimizzare il filtraggio dei macchinari

        # Parametri di filtro scelti dall'utente
        search_text: str = filters["searchbox"]  # Testo inserito nel SearchBox per filtrare in base al nome
        allowed_states: list[bool] = []  # Stati dei macchinari da mostrare
        allowed_types: list[str] = []  # Tipi di macchinari da mostrare

        # In base ai parametri di filtro, determina se uno stato di un macchinario è ammesso o meno
        def append_state_if_allowed(filter_key: str, state_name: bool):
            if filters[filter_key]:
                allowed_states.append(state_name)

        # Eseguo la funzione per tutti gli stati possibili
        append_state_if_allowed("running", True)
        append_state_if_allowed("available", False)

        # In base ai parametri di filtro, determina se un tipo di macchinario è ammesso o meno
        def append_type_if_allowed(filter_key: str, type_name: str):
            if filters[filter_key]:
                allowed_types.append(type_name)

        # Eseguo la funzione per tutti i tipi possibili
        append_type_if_allowed("sgrossatore", "Sgrossatore")
        append_type_if_allowed("tornio", "Tornio")
        append_type_if_allowed("finitore", "Finitore")
        append_type_if_allowed("ferratore", "Ferratore")
        append_type_if_allowed("timbratrice", "Timbratrice")

        # Numero di stati ammessi
        allowed_states_count: int = len(allowed_states)

        # Numero di tipi ammessi
        allowed_types_count: int = len(allowed_types)

        # Inizializzo la lista degli elementi da ritornare
        filtered_machine_list: list[Machine] = []

        # Se nessuno stato o tipo è ammesso, la lista dei macchinari da mostrare è quella vuota
        if allowed_states_count or allowed_types_count:

            # Filtra la lista degli ordini
            for machine in machines:

                # Se il testo di ricerca è vuoto viene saltato il filtro sul nome del macchinario
                if search_text:
                    if search_text.lower() not in machine.get_machine_serial().lower():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo del macchinario
                if allowed_types_count != 5:
                    if machine.__class__.__name__ not in allowed_types:
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato del macchinario
                if allowed_states_count != 2:
                    if machine.is_running() not in allowed_states:
                        continue

                filtered_machine_list.append(machine)

        return filtered_machine_list

    def stop_machine(self, machine: Machine) -> None:
        # Bisogna tenere conto che altri utenti potrebbero star osservando lo stesso macchinario: in tal caso più
        # utenti andrebbero ad agire sul database, eseguendo più volte l'incremento della quantità immagazzinata. Per
        # questo motivo ogni dipendente in ascolto richiede di occuparsi dell'aggiornamento dei dati. Ogni richiesta
        # sovrascrive la precedente, per cui sarà il più ritardatario a occuparsene.

        # Richiede di poter aggiornare lo stop del macchinario
        self.__machines_repository.request_to_manage_machine_output(machine.get_machine_serial())

        # Esegue le modifiche ai dati
        def execute_updates():

            # Ottiene la varietà di forma e la quantità in output
            output_shoe_last_variety = machine.get_active_process().get_output_shoe_last_variety()
            output_quantity = machine.get_active_process().get_quantity()

            # Cerca i prodotti immagazzinati della varietà di forma in output
            stored_shoe_last_variety = self.__storage_repository.get_unassigned_product_by_shoe_last_variety(
                output_shoe_last_variety)

            # Se non esistono prodotti immagazzinati dello stesso tipo di quelli in output...
            if stored_shoe_last_variety is None:
                # ...crea un nuovo prodotto con la quantità in output
                self.__storage_repository.create_unassigned_product(output_shoe_last_variety, output_quantity)

            # Altrimenti...
            else:
                # ...aggiorna la quantità della forma in output
                self.__storage_repository.update_product_quantity(
                    stored_shoe_last_variety.get_item_id(),
                    stored_shoe_last_variety.get_quantity() + output_quantity
                )

            # Ferma il macchinario
            self.__machines_repository.stop_machine_by_id(machine.get_machine_serial())

        # Il seguente thread serve a dare tempo a tutti gli utenti di effettuare la richiesta, e al thread di
        # aggiornamento del progresso del macchinario di essere chiuso ed eliminato definitivamente

        # Avvia il thread
        Thread(target=lambda: {
            # Tempo di attesa in secondi
            sleep(3),

            # Controlla se l'utente corrente puà eseguire le modifiche. Se sì, le esegue
            execute_updates() if self.__machines_repository.can_manage_machine_output(machine.get_machine_serial())
            else None
        }).start()
