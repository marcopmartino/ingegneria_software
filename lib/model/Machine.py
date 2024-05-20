from abc import abstractmethod, ABC

from lib.model.Order import Order
from lib.model.ShoeLastVariety import ShoeLastVariety, Processing, CompassType, Shoeing, ProductType
from lib.model.StoredItems import MaterialDescription
from lib.utility.ObserverClasses import Observable


class InputMaterial:
    def __init__(self, material_description: MaterialDescription, quantity: int = 1):
        self.__material_description = material_description
        self.__quantity = quantity

    def get_material_description(self) -> MaterialDescription:
        return self.__material_description

    def get_quantity(self) -> int:
        return self.__quantity


class MachineOperation:
    def __init__(self, input_shoe_last_variety: ShoeLastVariety, output_shoe_last_variety: ShoeLastVariety,
                 input_materials: list[InputMaterial], first_order: Order):
        self.__input_shoe_last_variety: ShoeLastVariety = input_shoe_last_variety
        self.__output_shoe_last_variety: ShoeLastVariety = output_shoe_last_variety
        self.__input_materials: list[InputMaterial] = input_materials
        self.__order_list: list[Order] = [first_order]
        self.__in_production_shoe_lasts: int = 0
        self.__produced_shoe_lasts: int = 0

    def append_order(self, order: Order):
        self.__order_list.append(order)

    def get_id(self) -> str:
        return self.__order_list[0].get_order_serial()

    def get_input_shoe_last_variety(self) -> ShoeLastVariety:
        return self.__input_shoe_last_variety

    def get_output_shoe_last_variety(self) -> ShoeLastVariety:
        return self.get_output_shoe_last_variety()

    def get_input_materials(self) -> list[InputMaterial]:
        return self.__input_materials

    def get_order_list(self) -> list[Order]:
        return self.__order_list

    def get_in_production_shoe_lasts(self) -> int:
        return self.__in_production_shoe_lasts

    def set_in_production_shoe_lasts(self, in_production_shoe_lasts: int):
        self.__in_production_shoe_lasts = in_production_shoe_lasts

    def get_produced_shoe_lasts(self) -> int:
        return self.__produced_shoe_lasts

    def set_produced_shoe_lasts(self, produced_shoe_lasts: int):
        self.__produced_shoe_lasts = produced_shoe_lasts

    def get_required_shoe_lasts(self) -> int:
        total_required = 0
        for order in self.__order_list:
            total_required += order.get_quantity()
        return total_required


class MachineProcess:
    # Il seriale di un ordine è usato per identificare l'operazione la cui esecuzione ha generato questo processo,
    # poiché è impossibile che un ordine sia legato a operazioni diverse di uno stesso macchinario.
    def __init__(self, order_serial: str, quantity: int, end_datetime: str):
        super().__init__()
        self.__order_serial = order_serial
        self.__quantity = quantity
        self.__end_datetime = end_datetime

    def get_operation_id(self) -> str:
        return self.__order_serial

    def get_quantity(self) -> int:
        return self.__quantity

    def get_end_datetime(self) -> str:
        return self.__end_datetime


class Machine(Observable, ABC):
    OPERATION_NAME: str
    OPERATION_INFO: list[list[str]]
    INPUT_PRODUCT_TYPE: ProductType
    OUTPUT_PRODUCT_TYPE: ProductType

    def __init__(self, machine_serial: str, capacity: int, is_running: bool = False, cycle_counter: int = 0,
                 active_process: MachineProcess = None):
        super(Machine, self).__init__()
        self.__machine_serial = machine_serial
        self.__capacity = capacity
        self.__is_running = is_running
        self.__cycle_counter = cycle_counter
        self.__active_process = active_process

    def get_machine_serial(self) -> str:
        return self.__machine_serial

    def get_capacity(self) -> int:
        return self.__capacity

    def is_running(self) -> bool:
        return self.__is_running

    def get_cycle_counter(self) -> int:
        return self.__cycle_counter

    def get_active_process(self) -> MachineProcess:
        return self.__active_process

    def start(self, process: MachineProcess) -> None:
        self.__active_process = process
        self.__is_running = True

    def stop(self) -> None:
        self.__is_running = False
        self.__cycle_counter += 1
        self.__active_process = None

    @abstractmethod
    def calculate_input_shoe_last_variety(self, desired_shoe_last_variety: ShoeLastVariety) -> ShoeLastVariety:
        pass

    @abstractmethod
    def calculate_output_shoe_last_variety(self, desired_shoe_last_variety: ShoeLastVariety) -> ShoeLastVariety:
        pass

    @abstractmethod
    def calculate_input_materials(self, desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        pass

    @abstractmethod
    def calculate_duration(self, desired_shoe_last_variety: ShoeLastVariety) -> int:
        pass


class Sgrossatore(Machine):
    OPERATION_NAME = "Sgrossatura"
    OPERATION_INFO = [["Abbozzo", "Abbozzo sgrossato", "Taglia"]]

    def __init__(self, machine_serial: str, capacity: int, is_running: bool = False, cycle_counter: int = 0,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, cycle_counter, active_process)

    def calculate_input_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),
        )

    def calculate_output_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),
        )

    def calculate_input_materials(self, desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        return []

    def calculate_duration(self, desired_shoe_last_variety: ShoeLastVariety) -> int:
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

    def __init__(self, machine_serial: str, capacity: int, is_running: bool = False, cycle_counter: int = 0,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, cycle_counter, active_process)

    def calculate_input_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            Processing.NESSUNA
        )

    def calculate_output_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),
        )

    def calculate_input_materials(self, desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
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

    def calculate_duration(self, desired_shoe_last_variety: ShoeLastVariety) -> int:
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

    def __init__(self, machine_serial: str, capacity: int, is_running: bool = False, cycle_counter: int = 0,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, cycle_counter, active_process)

    def calculate_input_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing()
        )

    def calculate_output_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),

            desired_shoe_last_variety.get_first_compass_type(),
            desired_shoe_last_variety.get_second_compass_type(),
            desired_shoe_last_variety.get_pivot_under_heel(),
        )

    def calculate_input_materials(self, desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        input_materials = []
        standard_compass_quantity = 0
        reinforced_compass_quantity = 0

        match desired_shoe_last_variety.get_first_compass_type():
            case CompassType.STANDARD:
                standard_compass_quantity += 60
            case CompassType.RINFORZATA:
                reinforced_compass_quantity += 60

        match desired_shoe_last_variety.get_second_compass_type():
            case CompassType.STANDARD:
                standard_compass_quantity += 60
            case CompassType.RINFORZATA:
                reinforced_compass_quantity += 60

        if desired_shoe_last_variety.get_pivot_under_heel():
            input_materials.append(MaterialDescription.PERNO)

        input_materials.append(InputMaterial(MaterialDescription.BUSSOLA_STANDARD, standard_compass_quantity))

        if reinforced_compass_quantity != 0:
            input_materials.append(InputMaterial(MaterialDescription.BUSSOLA_RINFORZATA, reinforced_compass_quantity))

        return input_materials

    def calculate_duration(self, desired_shoe_last_variety: ShoeLastVariety) -> int:
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

    def __init__(self, machine_serial: str, capacity: int, is_running: bool = False, cycle_counter: int = 0,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, cycle_counter, active_process)

    def calculate_input_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
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

    def calculate_output_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
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

    def calculate_input_materials(self, desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        input_materials = []

        match desired_shoe_last_variety.get_shoe_last_type():
            case Shoeing.TACCO_FERRATO:
                input_materials.append(InputMaterial(MaterialDescription.PIASTRA_CORTA))
            case Shoeing.MEZZA_FERRATA:
                input_materials.append(InputMaterial(MaterialDescription.PIASTRA_MEDIA))
            case Shoeing.TUTTA_FERRATA:
                input_materials.append(InputMaterial(MaterialDescription.PIASTRA_LUNGA))

        if desired_shoe_last_variety.get_iron_tip():
            input_materials.append(MaterialDescription.PIASTRA_PUNTA)

        return input_materials

    def calculate_duration(self, desired_shoe_last_variety: ShoeLastVariety) -> int:
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

    def __init__(self, machine_serial: str, capacity: int, is_running: bool = False, cycle_counter: int = 0,
                 active_process: MachineProcess = None):
        super().__init__(machine_serial, capacity, is_running, cycle_counter, active_process)

    def calculate_input_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
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

    def calculate_output_shoe_last_variety(self, desired_shoe_last_variety) -> ShoeLastVariety:
        return ShoeLastVariety(
            desired_shoe_last_variety.get_gender(),
            desired_shoe_last_variety.get_shoe_last_type(),
            desired_shoe_last_variety.get_plastic_type(),

            desired_shoe_last_variety.get_size(),

            desired_shoe_last_variety.get_processing(),

            desired_shoe_last_variety.get_first_compass_type(),
            desired_shoe_last_variety.get_second_compass_type(),
            desired_shoe_last_variety.get_pivot_under_heel(),

            desired_shoe_last_variety.get_shoeing(),
            desired_shoe_last_variety.get_iron_tip(),

            desired_shoe_last_variety.get_numbering_antineck(),
            desired_shoe_last_variety.get_numbering_lateral(),
            desired_shoe_last_variety.get_numbering_heel()
        )

    def calculate_input_materials(self, desired_shoe_last_variety: ShoeLastVariety) -> list[InputMaterial]:
        return []

    def calculate_duration(self, desired_shoe_last_variety: ShoeLastVariety) -> int:
        duration = 30

        if desired_shoe_last_variety.get_numbering_antineck():
            duration += 15

        if desired_shoe_last_variety.get_numbering_lateral():
            duration += 15

        if desired_shoe_last_variety.get_numbering_heel():
            duration += 15

        return duration
