import numpy as np
from packages.controller import SimulationPlane
from tools.utils.general_utils import write_data

class Cahn(SimulationPlane):
    """Class for simulating the Cahn Hilliard system

    - dimensions: x and y dimension of the cells
    - timesteps: number of timesteps for the simulation
    - sim_type: either a visual or full simulation
    - dx_value: dx value
    - M: value of M
    - a_and_b: the value of a and b i.e a = b
    - k: the value of k
    - sig0: the inital value of sigma
    - noise: noise added to the array.
    """
    def __init__(self, dimensions, timesteps, sim_type, dx_value,
                    M, a_and_b, k, sig0, noise):
        """
        Sirs Constuctor
        """
        super().__init__(dimensions, timesteps)
        dt_value = float(dx_value)
        self.sim_type = sim_type
        self.uConstant = float(k) / (float(dx_value) ** 2)
        self.sigConstant = (float(M) * dt_value) / (float(dx_value) ** 2)
        self.a = self.b = float(a_and_b)
        self.sig0 = float(sig0)
        self.noise = float(noise)
        self.k = float(k)

        self.create_cells()
        self.create_figure()

    #override
    def start_sim(self):
        if self.sim_type == "visual":
            self.create_cells()
            self.create_figure()
            super().start_sim()
        else:
            self.start_full_sim()

    #override
    def create_cells(self):
        self.cells = np.random.normal(
            loc=0, scale= self.noise, size=(self.dimensions, self.dimensions))
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                self.cells[i, j] = self.cells[i, j] + self.sig0

    #override
    def create_figure(self):
        super().create_figure()
        self.axes.set_title("Cahn Hilliard Simulation For {} Cells".format(self.dimensions ** 2))
        self.im = self.axes.imshow(self.cells, interpolation = "nearest", animated = True)
        self.fig.colorbar(self.im)

    #override
    def anim_func(self, i):
        self.new_cells = np.copy(self.cells)
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                self.new_cells[i,j] = self.cahn_hilliard(i, j)
        self.cells = np.copy(self.new_cells)
        self.im.set_array(self.cells)
        self.check_sim()
        yield self.im

    def start_full_sim(self):
        self.create_cells()
        self.sim_data = []
        for t in range(self.timesteps):
            self.new_cells = np.copy(self.cells)
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    self.new_cells[i, j] = self.cahn_hilliard(i, j)
            self.cells = np.copy(self.new_cells)
            self.sim_data.append("{}, {}".format(t, self.free_energy()))
            self.check_sim()
        self.finished_sim()

    def cahn_hilliard(self, i, j):
        mew_component = self.sigConstant * (
            # u(i + 1, j; n)
            self.calc_mew(self.i_index(i), j) + \
                # u(i - 1, j; n)
                self.calc_mew(self.d_index(i), j) + \
                    # u(i, j + 1; n)
                    self.calc_mew(i, self.i_index(j)) + \
                        # u(i, j -1; n)
                        self.calc_mew(i, self.d_index(j)) - \
                            # 4u(i, j)
                            4 * self.calc_mew(i, j))
        new_sigma = self.new_cells[i, j] + mew_component

        return new_sigma

    def calc_mew(self, i, j):
        mew_init = - self.a * self.new_cells[i, j] + self.b * (self.new_cells[i, j] ** 3)
        mew_product = - self.uConstant * (
            # sig(i + 1, j; n)
            self.new_cells[self.i_index(i), j] + \
                # sig(i - 1, j; n)
                self.new_cells[self.d_index(i), j] + \
                    # sig(i, j + 1; n)
                    self.new_cells[i, self.i_index(j)] + \
                        # sig(i, j - 1; n)
                        self.new_cells[i, self.d_index(j)] - \
                            # 4sig(i, j, n)
                            4 * self.cells[i, j])
        mew = mew_init + mew_product
        return mew

    def free_energy(self):
        energy = - (self.a / 2) * (sum(sum(self.cells)) ** 2) + \
            (self.a / 4) * (sum(sum(self.cells)) ** 4) + (self.k / 2) * \
                (sum(sum(sum(np.gradient(self.cells)))) ** 2)
        return energy

    #override
    def check_sim(self):
        if self.index % 5 == 0:
            print ("Timesteps Completed: {} out of {}".format(self.index, self.timesteps))
        if self.index == self.timesteps:
            print ("Simulation Completed")
            self.end_simulation()
        self.index += 1

    #override
    def finished_sim(self):
        table_heads = "timesteps, energy"
        timestep_values = [i for i in range(self.timesteps)]
        file_data = ("Cahn", self.dimensions, self.timesteps)
        sim_info = "{} Simulation with {} Cells and {} Timesteps\n{}".format("Cahn Hilliard", self.dimensions ** 2, self.timesteps, table_heads)
        write_data(self.sim_data, file_data, sim_info)
