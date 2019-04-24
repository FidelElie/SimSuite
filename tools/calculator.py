import numpy as np
from tools.utils import UtilityBase, sim_utils

class Calculator(UtilityBase):

    def __init__(self, modes):
        super().__init__(self.calculate_data, None, self.setup)
        self.modes = modes

    def setup(self):
        self.choices = [
            ("gol", self.calculate_speed)
        ]
        self.identifiers = [string[0] for sting in self.choices]
        self.functions = [func[1] for func in self.choices]

    def calculate_data(self, file_name):
        identifier = file_name.replace(".txt", "").lower()
        params = identifier.split(" - ")

        if params[0] in self.identifiers:
            index = self.identifiers.index(params[0])
            self.functions[index](*params)

        if params[0].lower() == "gol":
            self.calculate_speed(params)
        else:
            self.incomp_message()

    def calculate_speed(self, identifier, size, sweeps):
        x_coords, y_coords = sim_utils.get_com_data(self.file_data)
        x_differences = np.diff(x_coords)
        y_differences = np.diff(y_coords)
        vector_diffs = np.hypot(x_differences, y_differences)
        average_speed = np.average(vector_diffs)
        self.print_report(average_speed, size, sweeps)

    def print_report(self, result, size, sweeps):
        if dataset_info[0].lower() == "gol":
            mode = "Game Of Life"
        else:
            mode = dataset_info[0]
        report = \
        """
        Game Of Life Simulation Report

        Simulation Parameters
        ---
        Simulation Mode: {}
        Cell Dimension: {}
        Number of TimeSteps: {}
        ---
        Simulation Results
        ---
        Average Speed Calculated For Glider : {} cells / timestep
        """.format(mode, size, sweeps, result)
        print(report)

