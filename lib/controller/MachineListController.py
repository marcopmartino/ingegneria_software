from lib.model.Machine import Machine
from lib.repository.MachinesRepository import MachinesRepository


class MachineListController:
    def __init__(self):
        super().__init__()
        self.__machines_repository = MachinesRepository()

    # Imposta un osservatore per la repository
    def observe_machine_list(self, callback: callable):
        self.__machines_repository.observe(callback)

    # Ritorna un ordine in base all'id
    def get_machine_by_id(self, order_id: str) -> Machine:
        return self.__machines_repository.get_machine_by_id(order_id)

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
                    if search_text not in machine.get_machine_serial():
                        continue

                # Se tutti i tipi sono ammessi viene saltato il filtro sul tipo del macchinario
                if allowed_types_count != 5:
                    if machine.get_machine_type() not in allowed_types:
                        continue

                # Se tutti gli stati sono ammessi viene saltato il filtro sullo stato del macchinario
                if allowed_states_count != 2:
                    if machine.is_running() not in allowed_states:
                        continue

                filtered_machine_list.append(machine)

        return filtered_machine_list
