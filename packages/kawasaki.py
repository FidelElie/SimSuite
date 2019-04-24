import numpy as np
from packages.controller import SimulationPlane
from tools.utils.general_utils import write_data
from tools.utils import sim_utils

class Kawasaki(SimulationPlane):
    """ Class for simulating the Kawasaki dynamics for Icing Model

    dimensions: x and y dimension of the cells

    timesteps: number of timesteps for the simulation

    tempurature: between 1 and 5

    sim_type: simulation mode either 'visual' or 'full'
    """
    def __init__(self, dimensions, timesteps, tempurature, sim_type):
        """
        Glauber Constructor
        ---
        Tempurature: The Unitary tempurature of the system
        Mode: The sim_type for either a visual or full simulation
        """
        super().__init__(dimensions, timesteps)
        self.tempurature = tempurature
        self.sim_type = sim_type

    # override
    def create_cells(self):
        "Overriden from base class"
        self.cells = np.random.choice(
            [1, -1], size=(self.dimensions, self.dimensions))

    # override
    def create_figure(self):
        """ Reimplemented from base class
        Creates base figure elements that are required for visual sim
        """
        super().create_figure()
        self.axes.set_title(
            "Kawasaki Simulation For {} Cells".format(self.dimensions ** 2))
        self.im = self.axes.imshow(
            self.cells, interpolation="nearest", animated=True)
        self.fig.colorbar(self.im)

    # override
    def start_sim(self):
        """Re-implemented from base class
        Runs either the visual simulation with matplotlib or full without
        """
        if self.sim_type.lower() == "visual":
            self.create_cells()
            self.create_figure()
            super().start_sim()
        else:
            self.tempurature = np.arange(1, 3, 0.1)
            self.start_full_sim()

    def start_full_sim(self):
        """Runs full simulation procedure"""
        self.warning_message()
        self.avg_qauntities = []
        for temp in self.tempurature:
            self.create_cells()
            print ("Current Tempurature: {0:.1f}".format(temp))
            for  i in range(self.timesteps):
                if i % 10 == 0:
                    print("Current Sweep: {} out of {}".format(int(i), int(self.timesteps)))
                for j in range(self.dimensions ** 2):
                    self.kawasaki_procedure(temp)
                if i >= 99 and i % 10 == 0:
                    self.calculate_averages(temp)
        self.finished_sim()

    def calculate_averages(self, tempurature):
        """ Calculate average energies and magnetisation of the system """
        average_energy = sim_utils.calculate_total_energy(self.cells)
        average_mag = sim_utils.calculate_total_mag(self.cells)
        self.avg_qauntities.append("{},{},{}".format(str(tempurature), str(average_energy), str(average_mag)))

    # override
    def anim_func(self, i):
        """ Repimplemented from base class
        Used for visual simulation of kawasaki dynamics
        """
        for i in range(self.dimensions ** 2):
            self.kawasaki_procedure(self.tempurature)
        self.im.set_array(self.cells)
        self.check_sim()
        yield self.im

    def kawasaki_procedure(self, temp):
        """Does the Kawasaki Procedure for the icing model"""
        i_random_row = np.random.randint(0, self.dimensions)
        i_random_col = np.random.randint(0, self.dimensions)
        j_random_row = np.random.randint(0, self.dimensions)
        j_random_col = np.random.randint(0, self.dimensions)
        if (i_random_row != j_random_row)  and (i_random_col != j_random_col):
            i_coordinate = (i_random_row, i_random_col)
            j_coordinate = (j_random_row, j_random_col)
            if self.cells[i_coordinate[0], i_coordinate[1]] != self.cells[j_coordinate[0], j_coordinate[1]]:
                i_energy_change = self.check_nieghbours(i_coordinate)
                j_energy_change = self.check_nieghbours(j_coordinate)
                i_outcome = sim_utils.determine_flip_state(i_energy_change, temp)
                j_outcome = sim_utils.determine_flip_state(j_energy_change, temp)
                if i_outcome == True and j_outcome == True:
                    new_i_state = sim_utils.flip_array_state(self.cells[i_coordinate[0], j_coordinate[1]])
                    new_j_state = sim_utils.flip_array_state(self.cells[j_coordinate[0], j_coordinate[1]])
                    self.cells[i_coordinate[0], i_coordinate[1]] = new_i_state
                    self.cells[j_coordinate[0], j_coordinate[1]] = new_j_state

    # override
    def check_nieghbours(self, coordinate):
        """ Re-implemented from base class
        Method for checking the closest neighbours in kawasaki simulation.
        """
        member, neighbours = super().check_nieghbours(coordinate)
        energyChange = sim_utils.determine_energy_change(member, neighbours)
        return energyChange

    # override
    def finished_sim(self):
        """ Method for finishing the simulation """
        sim_info = "Kawasaki Simulation of {} Cells and {} TimeSteps\ntemp,avgEnergy,avgMag".format(self.dimensions ** 2, self.timesteps)
        file_parameters = ["Kawasaki", self.dimensions, self.timesteps]
        write_data(self.avg_qauntities, file_parameters, sim_info)
