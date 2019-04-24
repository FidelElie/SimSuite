import numpy as np
from packages.controller import SimulationPlane
from tools.utils.general_utils import write_data

class Sirs(SimulationPlane):
    """Class for simulating the SIRS system

    dimensions: x and y dimension of the cells

    timesteps: number of timesteps for the simulation

    dyn_mode: different developing states either 'none', absorbing', 'dynamic', 'cyclic' or 'half'

    sim_type: simulation dyn_mode either 'visual' or 'full'

    prob: probabilities that are given for p2 if none all probs are 1
    """
    def __init__(self, dimensions, timesteps, sim_type, dyn_mode, prob):
        """
        Sirs Constuctor
        """
        super().__init__(dimensions, timesteps)
        self.sim_type = sim_type
        self.dyn_mode = dyn_mode
        self.probalbilities = prob

    def create_cells(self):
        """ Create Cell Array and adds more data to figure object """
        self.cells = np.random.choice([1, 0, -1], size=(self.dimensions, self.dimensions))
        if self.dyn_mode != "none":
            self.prob_by_mode()
        else:
            if self.probalbilities == None:
                self.probalbilities = [1, 1, 1]
            else:
                self.probalbilities = [float(prob) for prob in self.probalbilities]

    def prob_by_mode(self):
        # TODO get the correct probabilities for these points
        if self.dyn_mode == "half":
            self.probalbilities = [0.5, 0.5, 0.5]
        elif self.dyn_mode == "dynamic":
            self.probalbilities = [0, 1, 0]
        elif self.dyn_mode == "absorbing":
            self.probalbilities = [0.4, 1, 1]
        elif self.dyn_mode == "cyclic":
            self.probalbilities = [0.8, 0.1, 0.01]

    def create_figure(self):
        """ Reimplemented from base class
        Creates base figure elements that are required for visual sim
        """
        super().create_figure()
        self.axes.set_title("SIRS Simulation For {} Cells".format(self.dimensions ** 2))
        self.im = self.axes.imshow(self.cells, interpolation="nearest", animated=True)
        self.fig.colorbar(self.im)

    def start_sim(self):
        """ Re-implemented from base class
        Runs either the visual simulation with matplotlib or full without
        """
        if self.sim_type == "visual":
            self.create_cells()
            self.create_figure()
            super().start_sim()
        else:
            if self.dyn_mode == "half":
                self.start_half_sim()
            elif self.dyn_mode == "cut":
                self.start_cut_sim()
            else:
                self.start_full_sim()

    def start_full_sim(self):
        """Runs the full simulation procedure"""
        self.sim_data = []
        p1_amounts = np.arange(0, 1.05, 0.05)
        p3_amounts = np.arange(0, 1.05, 0.05)
        for prob1 in range(len(p1_amounts)):
            for prob2 in range(len(p3_amounts)):
                print ("Probabilities - p1 : {}, p3 : {}".format(p1_amounts[prob1], p3_amounts[prob2]))
                self.probalbilities = [p1_amounts[prob1], 0.5, p3_amounts[prob2]]
                self.create_cells()
                average_data = []
                for sweep in range(self.timesteps):
                    for i in range(self.dimensions ** 2):
                        self.sirs_procedure()
                    if sweep % 10 == 0:
                        print ("Sweep {} out of {}".format(sweep, self.timesteps))
                    if sweep % 10 == 0 and sweep > 99:
                        average_data.append(self.caculate_averages())
                avg_i = np.average([x[0] for x in average_data])
                self.sim_data.append("{},{},{}".format(p1_amounts[prob1], p3_amounts[prob2], avg_i))
        self.finished_sim("SIRS")

    def start_cut_sim(self):
        self.sim_data = []
        p1_amounts = np.arange(0.2, 0.52, 0.02)
        p3_amounts = np.arange(0.2, 0.52, 0.02)
        for prob1 in range(len(p1_amounts)):
            for prob2 in range(len(p3_amounts)):
                print ("Probability p1 : {}".format(p1_amounts[prob1]))
                self.probalbilities = [p1_amounts[prob1], 0.5, p3_amounts[prob2]]
                print(self.probalbilities)
                self.create_cells()
                average_data = []
                for sweep in range(self.timesteps):
                    for i in range(self.dimensions ** 2):
                        self.sirs_procedure()
                    if sweep % 10 == 0:
                        print ("Sweep {} out of {}".format(sweep, self.timesteps))
                    if sweep % 10 == 0 and sweep > 99:
                        average_data.append(self.caculate_averages())
                avg_var = np.average([x[1] for x in average_data])
                self.sim_data.append("{},{},{}".format(p1_amounts[prob1], p3_amounts[prob2], avg_var))
        self.finished_sim("SIRSCut")

    def start_half_sim(self):
        self.sim_data = []
        immune_prob = np.arange(0, 1.01, 0.01)
        for i in immune_prob:
            immune_data = []
            print ("Immune Probability: : {}".format(i))
            prob_vals = (1 - i) /3
            # Creating a certain immune population
            probabilities = [i, prob_vals, prob_vals, prob_vals]
            self.cells = np.random.choice([2, 1, 0, -1], size=(self.dimensions, self.dimensions), p=probabilities)
            self.probalbilities = [0.5, 0.5, 0.5]
            for sweep in range(self.timesteps):
                for j in range(self.dimensions ** 2):
                    self.sirs_procedure()
                if sweep % 10 == 0:
                    print ("Sweep {} out of {}".format(sweep,self.timesteps))
                if sweep % 10 == 0 and sweep > 99:
                    immune_data.append(self.caculate_averages())
            # Get average Intensity
            avg_i = np.average([x[0] for x in immune_data])
            dev_i = np.std([x[0] for x in immune_data])
            self.sim_data.append("{},{},{}".format(i, avg_i, dev_i))
        self.finished_sim("SIRSHalf")

    def caculate_averages(self):
        """Calculate averages of the infected sites"""
        infected_sites = (self.cells == -1).sum()
        infected_avg = infected_sites / (self.dimensions ** 2)
        infected_var = (infected_sites ** 2 - infected_avg ** 2) / self.dimensions ** 2
        return infected_avg, infected_var

    def anim_func(self, i):
        """ Re-implemented from base class
        Method for doing the SIRS simulation procedure over N sweeps
        """
        for i in range(self.dimensions ** 2):
            self.sirs_procedure()
        self.im.set_array(self.cells)
        self.check_sim()
        yield self.im

    def sirs_procedure(self):
        """Does the SIRS picking procedure"""
        random_row = np.random.randint(0, self.dimensions)
        random_cols = np.random.randint(0, self.dimensions)
        coordinate = (random_row, random_cols)
        c_agent, nieghbour_a = super().check_nieghbours(coordinate)
        self.determine_state(coordinate, c_agent, nieghbour_a)

    def determine_state(self, coordinate, c_agent, nieghbour_a):
        """ Determine the state of an agent based on neighbours and prob"""
        random_numb = np.random.uniform()
        # ! Infection Clause
        if (c_agent == 0):
            if (-1 in nieghbour_a):
                if random_numb < self.probalbilities[0]:
                    self.cells[coordinate[0], coordinate[1]] = -1
        # ! Recovery Clause
        elif (c_agent == -1):
            if random_numb < self.probalbilities[1]:
                self.cells[coordinate[0], coordinate[1]] = 1
        # ! Suceptible Clause
        elif (c_agent == 1) :
            if random_numb < self.probalbilities[2]:
                self.cells[coordinate[0], coordinate[1]] = 0


    def finished_sim(self, identifier):
        # TODO check that the correct information is being saved
        """For Finishing the Sim"""
        if identifier == "SIRS":
            tables_heads = "p1, p3, avgI"
        elif identifier == "SIRSHalf":
            tables_heads = "iProb, avgI, devI"
        elif identifier == "SIRSCut":
            tables_heads = "p1, varI"

        sim_info = "{} Simulation with {} Cells and {} TimeSteps\n{}".format(identifier, self.dimensions ** 2, self.timesteps, tables_heads)
        file_data = (identifier, self.dimensions, self.timesteps)
        write_data(self.sim_data, file_data, sim_info)

