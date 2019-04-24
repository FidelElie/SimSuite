import numpy as np
from tools.utils import sim_utils
from packages.controller import SimulationPlane
from tools.utils.general_utils import write_data

class Gol(SimulationPlane):
    """ Class for simulating the Game Of Life system

    dimensions: x and y dimension of the cells

    timesteps: number of timesteps for the simulation

    percentage: The Percentage of dead cells to be put in the array

    struct_mode: For inserting cells structures into an empty cell array
    """
    def __init__(self, dimensions, timesteps, percentage, struct_mode):
        """
        GameOfLife Constructor
        """
        super().__init__(dimensions, timesteps)
        self.percentage = percentage
        self.struct_mode = struct_mode
        self.create_cells()
        self.create_figure()

    def create_cells(self):
        """Create Cell Array and adds more data to figure object"""
        if self.struct_mode == None or self.struct_mode == "none":
            self.percentage = int(self.percentage) / 100
            probabilities = [1 - self.percentage, self.percentage]
            self.cells = np.random.choice([1, 0], size = (self.dimensions, self.dimensions), p = probabilities)
        else:
            self.cells = np.zeros(shape= (self.dimensions, self.dimensions))
            self.structure_injection()
        self.new_cells = np.copy(self.cells)

    def create_figure(self):
        """ Reimplemented from base class

        Creates base figure elements that are required for visual sim
        """
        super().create_figure()
        self.axes.set_title("The Game Of Life For {} Cells".format(self.dimensions ** 2))
        self.im = self.axes.imshow(self.cells, animated=True)

    def structure_injection(self):
        """ Puts known game of life strucutres into cell array """
        gol_structure = sim_utils.return_gol_structures(self.struct_mode)
        x = len(gol_structure[0])
        y = len(gol_structure[:,0])
        for row in range(x):
            for col in range(y):
                self.cells[col, row] = gol_structure[col, row]
        if self.struct_mode == "glider":
            self.com_values = []

    def anim_func(self, i):
        """ Repimplemented from base class

        Used for visual simulation of game of life
        """
        self.gol_procedure()
        self.cells = np.copy(self.new_cells)
        self.im.set_array(self.cells)
        self.check_sim()
        if self.struct_mode == "glider":
            self.check_centre_of_mass()
        yield self.im

    def check_sim(self):
        if self.index % 5 == 0:
            print ("Timesteps Completed: {} out of {}".format(self.index, self.timesteps))
        if self.index == self.timesteps:
            print ("Simulation Completed")
            if self.struct_mode == "glider":
                self.finished_sim()
            self.end_simulation()
        self.index += 1

    def gol_procedure(self):
        """ Does the game of life picking procedure """
        for rows in range(self.dimensions):
            for cols in range(self.dimensions):
                coordinate = (rows, cols)
                member, nieghbours = super().check_all_nieghbours(coordinate)
                live_sum = sum(nieghbours)
                number = self.check_life(member, live_sum)
                if self.new_cells[rows, cols] != number:
                    self.new_cells[rows, cols] = number

    def check_life(self, member, live_sum):
        if member == 1:
            if live_sum < 2 or live_sum > 3:
                return 0
            else:
                return 1
        else:
            if live_sum == 3:
                return 1
            else:
                return 0

    def check_centre_of_mass(self):
        """Checks the Center of mass for a given glider structure"""
        x, y = np.nonzero(self.cells)
        com_x = np.average(x)
        com_y = np.average(y)
        self.com_values.append("{},{}".format(com_x, com_y))

    def finished_sim(self):
        """ For Finishing the Sim """
        if self.struct_mode == "glider":
            sim_info = "Game Of Life Simulation of {} Cells and {} Timesteps\ncomX,comY".format(self.dimensions ** 2, self.timesteps)
            sim_data = ["GoL", self.dimensions, self.timesteps]
            write_data(self.com_values, sim_data, sim_info)

