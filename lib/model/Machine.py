from abc import abstractmethod, ABC
from datetime import datetime
from math import floor

from lib.model.Order import Order
from lib.model.ShoeLastVariety import ShoeLastVariety, Processing, CompassType, Shoeing, ProductType
from lib.model.StoredItems import MaterialDescription
from lib.utility.ObserverClasses import Observable
from lib.utility.UtilityClasses import DatetimeUtils


class InputMaterial:
    def __init__(self, material_description: MaterialDescription, quantity: int = 1):
        self.__material_description = material_description
        self.__quantity = quantity

    def get_material_description(self) -> MaterialDescription:
        return self.__material_description

    def get_quantity(self) -> int:
        return self.__quantity

    def set_quantity(self, quantity: int) -> None:
        self.__quantity = quantity


class MachineOperationData:
    def __init__(
            self,
            first_order: Order,
            input_shoe_last_variety: ShoeLastVariety,
            output_shoe_last_variety: ShoeLastVariety,
            required_input_materials: list[InputMaterial],
            available_input_materials: list[InputMaterial],
            available_input_shoe_lasts: int,
            in_production_shoe_lasts: int,
            produced_shoe_lasts: int,
    ):
        self.__order_list: list[Order] = [first_order]
        self.__input_shoe_last_variety: ShoeLastVariety = input_shoe_last_variety
        self.__output_shoe_last_variety: ShoeLastVariety = output_shoe_last_variety
        self.__required_input_materials: list[InputMaterial] = required_input_materials
        self.__available_input_materials: list[InputMaterial] = available_input_materials
        self.__available_input_shoe_lasts: int = available_input_shoe_lasts
        self.__in_production_shoe_lasts: int = in_production_shoe_lasts
        self.__produced_shoe_lasts: int = produced_shoe_lasts
        self.__required_shoe_lasts: int = 0
        self.__to_be_produced_shoe_lasts: int = 0
        self.__required_to_start_shoe_lasts: int = 0
        self.__finalized: bool = False

    def finalize(self, machine_capacity: int) -> None:
        if not self.__finalized:

            # Calcola il numero di paia di forme richieste nel complesso
            for order in self.__order_list:
                self.__required_shoe_lasts += order.get_quantity()

            # Calcola il numero di paia da produrre per soddisfare le richieste di tutti gli ordini
            self.__to_be_produced_shoe_lasts = max(0, (self.__required_shoe_lasts - self.__produced_shoe_lasts
                                                       - self.__in_production_shoe_lasts))

            # Determina il minimo numero di paia richieste per poter avviare un processo basato su questa operazione
            self.__required_to_start_shoe_lasts = min(machine_capacity, self.__to_be_produced_shoe_lasts)

            # Aggiorna le quantità richieste di materiali
            for material in self.__required_input_materials:
                material.set_quantity(material.get_quantity() * self.__required_to_start_shoe_lasts)

            # Indica che l'oggetto è stato finalizzato
            self.__finalized = True

    def get_order_list(self) -> list[Order]:
        return self.__order_list

    def append_order(self, order: Order):
        if not self.__finalized:
            self.__order_list.append(order)

    def get_id(self) -> str:
        return self.__order_list[0].get_order_serial()

    def contains_order(self, order_serial: str):
        for order in self.__order_list:
            if order.get_order_serial() == order_serial:
                return True
        return False

    def get_input_shoe_last_variety(self) -> ShoeLastVariety:
        return self.__input_shoe_last_variety

    def get_output_shoe_last_variety(self) -> ShoeLastVariety:
        return self.__output_shoe_last_variety

    def get_required_input_materials(self) -> list[InputMaterial]:
        return self.__required_input_materials

    def get_available_input_materials(self) -> list[InputMaterial]:
        return self.__available_input_materials

    def get_available_input_shoe_lasts(self) -> int:
        return self.__available_input_shoe_lasts

    def get_in_production_shoe_lasts(self) -> int:
        return self.__in_production_shoe_lasts

    def get_produced_shoe_lasts(self) -> int:
        return self.__produced_shoe_lasts

    def get_required_shoe_lasts(self) -> int:
        return self.__required_shoe_lasts

    def get_to_be_produced_shoe_lasts(self) -> int:
        return self.__to_be_produced_shoe_lasts

    def get_required_to_start_shoe_lasts(self) -> int:
        return self.__required_to_start_shoe_lasts


class MachineProcess:
    # Il seriale di un ordine è usato per identificare l'operazione la cui esecuzione ha generato questo processo,
    # poiché è impossibile che un ordine sia legato a operazioni diverse di uno stesso macchinario.
    def __init__(self, operation_id: str, output_shoe_last_variety: ShoeLastVariety, quantity: int,
                 end_datetime: datetime, duration: int):
        super().__init__()
        self.__operation_id: str = operation_id  # Seriale del primo ordine associato all'operazione
        self.__output_shoe_last_variety: ShoeLastVariety = output_shoe_last_variety
        self.__quantity: int = quantity
        self.__end_datetime: datetime = end_datetime
        self.__duration: int = duration  # In secondi
        self.__progress_percentage: int = 0

    def get_operation_id(self) -> str:
        return self.__operation_id

    def get_output_shoe_last_variety(self) -> ShoeLastVariety:
        return self.__output_shoe_last_variety

    def get_quantity(self) -> int:
        return self.__quantity

    def get_progress_percentage(self) -> int:
        return self.__progress_percentage

    def refresh_progress_percentage(self) -> None:
        timediff_seconds = DatetimeUtils.calculate_time_difference(self.__end_datetime, datetime.now())
        self.__progress_percentage = floor((float(self.__duration - timediff_seconds) / self.__duration) * 100)

    def get_end_datetime(self) -> datetime:
        return self.__end_datetime

    def get_duration(self) -> int:
        return self.__duration


class Machine(Observable, ABC):
    OPERATION_NAME: str
    OPERATION_INFO: list[list[str]]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool, manufacturer: str,
                 active_process: MachineProcess = None):
        super(Machine, self).__init__()
        self.__machine_serial = machine_serial
        self.__capacity = capacity
        self.__is_running = is_running
        self.__manufacturer = manufacturer
        self.__active_process = active_process

    def get_machine_serial(self) -> str:
        return self.__machine_serial

    def get_capacity(self) -> int:
        return self.__capacity

    def is_running(self) -> bool:
        return self.__is_running

    def get_manufacturer(self) -> str:
        return self.__manufacturer

    def get_active_process(self) -> MachineProcess:
        return self.__active_process

    def start(self, process: MachineProcess) -> None:
        self.__active_process = process
        self.__is_running = True

    def stop(self) -> None:
        self.__active_process = None
        self.__is_running = False

    @staticmethod
    @abstractmethod
    def is_process_required(desired_shoe_last_variety: ShoeLastVariety) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def is_compatible_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety,
                                        shoe_last_variety: ShoeLastVariety) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def calculate_input_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety) -> ShoeLastVariety:
        pass

    @staticmethod
    @abstractmethod
    def calculate_output_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety) -> ShoeLastVariety:
        pass

    @staticmethod
    @abstractmethod
    def calculate_input_materials(desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        pass

    @staticmethod
    @abstractmethod
    def calculate_duration(desired_shoe_last_variety: ShoeLastVariety) -> int:
        pass


class Sgrossatore(Machine):
    OPERATION_NAME = "Sgrossatura"
    OPERATION_INFO = [["Abbozzo", "Abbozzo sgrossato", "Taglia"]]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool, manufacturer: str,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, manufacturer, active_process)

    @staticmethod
    def is_process_required(desired_shoe_last_variety: ShoeLastVariety) -> bool:
        return True

    @staticmethod
    def is_compatible_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety,
                                        shoe_last_variety: ShoeLastVariety) -> bool:
        return (shoe_last_variety.get_product_type() != ProductType.ABBOZZO and
                shoe_last_variety.get_gender() == desired_shoe_last_variety.get_gender() and
                shoe_last_variety.get_shoe_last_type() == desired_shoe_last_variety.get_shoe_last_type() and
                shoe_last_variety.get_size() == desired_shoe_last_variety.get_size())

    @staticmethod
    def calculate_input_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.ABBOZZO,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),
        )

    @staticmethod
    def calculate_output_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.ABBOZZO_SGROSSATO,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),
        )

    @staticmethod
    def calculate_input_materials(desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        return []

    @staticmethod
    def calculate_duration(desired_shoe_last_variety: ShoeLastVariety) -> int:
        return 120


class Tornio(Machine):
    OPERATION_NAME = "Tornitura"
    OPERATION_INFO = [
        ["Abbozzo sgrossato\nPerno (x2)\nMolla per cuneo", "Abbozzo sgrossato con\nlavorazione cuneo",
         "Lavorazione cuneo"],
        ["Abbozzo sgrossato\nPerno (x2)\nGancio per snodo alfa", "Abbozzo sgrossato con\nlavorazione snodo alfa",
         "Lavorazione snodo alfa"],
        ["Abbozzo sgrossato\nPerno (x3)\nGancio per snodo tendo", "Abbozzo sgrossato con\nlavorazione snodo tendo",
         "Lavorazione snodo tendo"],
    ]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool, manufacturer: str,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, manufacturer, active_process)

    @staticmethod
    def is_process_required(desired_shoe_last_variety: ShoeLastVariety) -> bool:
        return desired_shoe_last_variety.get_processing() != Processing.NESSUNA

    @staticmethod
    def is_compatible_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety,
                                        shoe_last_variety: ShoeLastVariety) -> bool:
        return (Sgrossatore.is_compatible_shoe_last_variety(desired_shoe_last_variety, shoe_last_variety) and
                shoe_last_variety.get_processing() == desired_shoe_last_variety.get_processing())

    @staticmethod
    def calculate_input_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.ABBOZZO_SGROSSATO,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            Processing.NESSUNA
        )

    @staticmethod
    def calculate_output_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.ABBOZZO_SGROSSATO,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),
        )

    @staticmethod
    def calculate_input_materials(desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        match desired_shoe_last_variety.get_processing():
            case Processing.CUNEO:
                return [
                    InputMaterial(MaterialDescription.PERNO, 2),
                    InputMaterial(MaterialDescription.MOLLA)
                ]
            case Processing.SNODO_ALFA:
                return [
                    InputMaterial(MaterialDescription.PERNO, 2),
                    InputMaterial(MaterialDescription.GANCIO_ALFA)
                ]
            case Processing.SNODO_TENDO:
                return [
                    InputMaterial(MaterialDescription.PERNO, 3),
                    InputMaterial(MaterialDescription.GANCIO_TENDO)
                ]

    @staticmethod
    def calculate_duration(desired_shoe_last_variety: ShoeLastVariety) -> int:
        match desired_shoe_last_variety.get_processing():
            case Processing.CUNEO:
                return 240
            case Processing.SNODO_ALFA:
                return 300
            case Processing.SNODO_TENDO:
                return 360


class Finitore(Machine):
    OPERATION_NAME = "Finitura"
    OPERATION_INFO = [["Abbozzo sgrossato (con o senza lavorazione)\nBussola", "Forma finita",
                       "Bussola\nSeconda bussola\n(opzionale - richiede Bussola)\nPerno sotto tallone\n(opzionale - "
                       "richiede Perno)"]]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool, manufacturer: str,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, manufacturer, active_process)

    @staticmethod
    def is_process_required(desired_shoe_last_variety: ShoeLastVariety) -> bool:
        return True

    @staticmethod
    def is_compatible_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety,
                                        shoe_last_variety: ShoeLastVariety) -> bool:
        return (Tornio.is_compatible_shoe_last_variety(desired_shoe_last_variety, shoe_last_variety) and
                shoe_last_variety.get_product_type() != ProductType.ABBOZZO_SGROSSATO and
                shoe_last_variety.get_first_compass_type() == desired_shoe_last_variety.get_first_compass_type() and
                shoe_last_variety.get_second_compass_type() == desired_shoe_last_variety.get_second_compass_type() and
                shoe_last_variety.get_pivot_under_heel() == desired_shoe_last_variety.get_pivot_under_heel())

    @staticmethod
    def calculate_input_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.ABBOZZO_SGROSSATO,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing()
        )

    @staticmethod
    def calculate_output_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.FORMA_FINITA,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),

            desired_shoe_last_variety.get_first_compass_type(),
            desired_shoe_last_variety.get_second_compass_type(),
            desired_shoe_last_variety.get_pivot_under_heel(),
        )

    @staticmethod
    def calculate_input_materials(desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        input_materials = []
        standard_compass_quantity = 0
        reinforced_compass_quantity = 0

        match desired_shoe_last_variety.get_first_compass_type():
            case CompassType.STANDARD:
                standard_compass_quantity += 1
            case CompassType.RINFORZATA:
                reinforced_compass_quantity += 1

        match desired_shoe_last_variety.get_second_compass_type():
            case CompassType.STANDARD:
                standard_compass_quantity += 1
            case CompassType.RINFORZATA:
                reinforced_compass_quantity += 1

        if desired_shoe_last_variety.get_pivot_under_heel():
            input_materials.append(InputMaterial(MaterialDescription.PERNO))

        input_materials.append(InputMaterial(MaterialDescription.BUSSOLA_STANDARD, standard_compass_quantity))

        if reinforced_compass_quantity != 0:
            input_materials.append(InputMaterial(MaterialDescription.BUSSOLA_RINFORZATA, reinforced_compass_quantity))

        return input_materials

    @staticmethod
    def calculate_duration(desired_shoe_last_variety: ShoeLastVariety) -> int:
        duration = 300

        if desired_shoe_last_variety.get_second_compass_type() != CompassType.NESSUNA:
            duration += 60

        if desired_shoe_last_variety.get_pivot_under_heel():
            duration += 60

        return duration


class Ferratore(Machine):
    OPERATION_NAME = "Ferratura"
    OPERATION_INFO = [
        ["Forma finita\nPiastra sottile corta", "Forma finita con tacco ferrato",
         "Ferratura \"tacco\"\nPunta ferrata (opzionale -\nrichiede Piastra per punta)"],
        ["Forma finita\nPiastra sottile media", "Forma finita mezza ferrata",
         "Ferratura \"mezza\"\nPunta ferrata (opzionale -\nrichiede Piastra per punta)"],
        ["Forma finita\nPiastra sottile lunga", "Forma finita tutta ferrata",
         "Ferratura \"tutta\"\nPunta ferrata (opzionale -\nrichiede Piastra per punta)"],
    ]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool, manufacturer: str,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, manufacturer, active_process)

    @staticmethod
    def is_process_required(desired_shoe_last_variety: ShoeLastVariety) -> bool:
        return (desired_shoe_last_variety.get_shoeing() != Shoeing.NESSUNA) or desired_shoe_last_variety.get_iron_tip()

    @staticmethod
    def is_compatible_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety,
                                        shoe_last_variety: ShoeLastVariety) -> bool:
        return (Finitore.is_compatible_shoe_last_variety(desired_shoe_last_variety, shoe_last_variety) and
                shoe_last_variety.get_shoeing() == desired_shoe_last_variety.get_shoeing() and
                shoe_last_variety.get_iron_tip() == desired_shoe_last_variety.get_iron_tip())

    @staticmethod
    def calculate_input_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.FORMA_FINITA,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),

            desired_shoe_last_variety.get_first_compass_type(),
            desired_shoe_last_variety.get_second_compass_type(),
            desired_shoe_last_variety.get_pivot_under_heel(),

            Shoeing.NESSUNA,
            False
        )

    @staticmethod
    def calculate_output_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.FORMA_FINITA,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),

            desired_shoe_last_variety.get_first_compass_type(),
            desired_shoe_last_variety.get_second_compass_type(),
            desired_shoe_last_variety.get_pivot_under_heel(),

            desired_shoe_last_variety.get_shoeing(),
            desired_shoe_last_variety.get_iron_tip()
        )

    @staticmethod
    def calculate_input_materials(desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        input_materials = []

        match desired_shoe_last_variety.get_shoe_last_type():
            case Shoeing.TACCO_FERRATO:
                input_materials.append(InputMaterial(MaterialDescription.PIASTRA_CORTA))
            case Shoeing.MEZZA_FERRATA:
                input_materials.append(InputMaterial(MaterialDescription.PIASTRA_MEDIA))
            case Shoeing.TUTTA_FERRATA:
                input_materials.append(InputMaterial(MaterialDescription.PIASTRA_LUNGA))

        if desired_shoe_last_variety.get_iron_tip():
            input_materials.append(InputMaterial(MaterialDescription.PIASTRA_PUNTA))

        return input_materials

    @staticmethod
    def calculate_duration(desired_shoe_last_variety: ShoeLastVariety) -> int:
        duration = 0

        match desired_shoe_last_variety.get_processing():
            case Shoeing.TACCO_FERRATO:
                duration = 120
            case Shoeing.MEZZA_FERRATA:
                duration = 180
            case Shoeing.TUTTA_FERRATA:
                duration = 240

        if desired_shoe_last_variety.get_iron_tip():
            duration += 60

        return duration


class Timbratrice(Machine):
    OPERATION_NAME = "Numeratura"
    OPERATION_INFO = [["Forma finita\nInchiostro indelebile", "Forma numerata",
                       "Codice seriale completo\nSegno anticollo (opzionale)\nSegno laterale (opzionale)\n"
                       "Segno sotto tallone (opzionale)"]]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool, manufacturer: str,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, manufacturer, active_process)

    @staticmethod
    def is_process_required(desired_shoe_last_variety: ShoeLastVariety) -> bool:
        return True

    @staticmethod
    def is_compatible_shoe_last_variety(desired_shoe_last_variety: ShoeLastVariety,
                                        shoe_last_variety: ShoeLastVariety) -> bool:
        return shoe_last_variety.equals(desired_shoe_last_variety)

    @staticmethod
    def calculate_input_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            ProductType.FORMA_FINITA,
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),

            desired_shoe_last_variety.get_first_compass_type(),
            desired_shoe_last_variety.get_second_compass_type(),
            desired_shoe_last_variety.get_pivot_under_heel(),

            desired_shoe_last_variety.get_shoeing(),
            desired_shoe_last_variety.get_iron_tip()
        )

    @staticmethod
    def calculate_output_shoe_last_variety(desired_shoe_last_variety) -> ShoeLastVariety:
        return desired_shoe_last_variety

    @staticmethod
    def calculate_input_materials(desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        return [InputMaterial(MaterialDescription.INCHIOSTRO, 0)]  # Quantità di inchiostro non calcolabile

    @staticmethod
    def calculate_duration(desired_shoe_last_variety: ShoeLastVariety) -> int:
        duration = 30

        if desired_shoe_last_variety.get_numbering_antineck():
            duration += 15

        if desired_shoe_last_variety.get_numbering_lateral():
            duration += 15

        if desired_shoe_last_variety.get_numbering_heel():
            duration += 15

        return duration
