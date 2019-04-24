import numpy as np
from packages.controller import SimulationPlane
from tools.utils import sim_utils

class Reaction(SimulationPlane):
    def __init__(self, dimensions, timesteps, k, sigma, dt):
        super().__init__(dimensions, timesteps)
        self.k = k
        self.sigma = sigma
        self.dt = dt

    #override
    def start_sim(self):
        self.create_cells()
        self.create_figure()
        super().start_sim()

    #override
    def create_figure(self):
        super().create_figure()
        self.axes.set_title("Reaction-Diffusion Simulation For {} Cells".format(self.dimensions ** 2))
        self.im = self.axes.imshow(self.cells, interpolation = "nearest", animated = True)
        self.fig.colorbar(self.im)
    #override
    def create_cells(self):
        self.cells = np.random.uniform(low=-0.1, high=0.1, size=(self.dimensions, self.dimensions))
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                self.cells[i, j] += 0.5
    #override
    def anim_func(self, i):
        self.new_cells = np.copy(self.cells)
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                self.new_cells[i, j] = self.reaction_procedure(i, j)
        self.cells = np.copy(self.new_cells)
        self.im.set_array(self.cells)
        self.check_sim()
        yield self.im

    def reaction_procedure(self, i , j):
        laplacian = self.dt * (
            self.cells[self.i_index(i), j] + \
                self.cells[self.d_index(i), j] + \
                    self.cells[i, self.i_index(j)] + \
                        self.cells[i, self.d_index(j)] - \
                            4 * self.cells[i, j]
        )
        constants = self.dt * self.calc_row(i, j) - self.k * self.cells[i, j]
        new_value = laplacian + constants
        print (new_value)
        return new_value

    def calc_row(self, i , j):
        i_component = i - (self.dimensions / 2)
        j_component = j - (self.dimensions / 2)
        mag_r  = np.sqrt(i_component ** 2 + j_component ** 2)
        row = np.exp(-(mag_r ** 2) / (self.sigma ** 2))
        print(row)
        return row

