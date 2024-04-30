class ProcessTemplate:
    def __init__(self, process_input: dict[str, int], process_output: dict[str, int], acquired_features: list[str]):
        self.__process_input = process_input
        self.__process_output = process_output
        self.__acquired_features = acquired_features


class Process:
    def __init__(self, process_input: dict[str, int], process_output: dict[str, int], acquired_features: list[str], 
                 finish_datetime: str):
        super().__init__(process_input, process_output, acquired_features)
        self.__finish_datetime: str = finish_datetime
