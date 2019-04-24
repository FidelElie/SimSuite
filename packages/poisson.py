import numpy as np
from packages.controller import SimulationPlane
from tools.utils.general_utils import write_data

class Poisson(SimulationPlane):
    """ Poisson Simulation Class

     - dimensions : size of simulation
    - timesteps : duration of simulation
    - poi_type: jacobi or guass
    - dx_value: dx value
    - e0: epsilon naught
    - noise: noise added to the simulation
    - limit: limit of convergence
    """
    def __init__(self, dimensions, timesteps, poi_type, charge_type, quantities, dx_value,  limit):
        super().__init__(dimensions, timesteps)
        self.poi_type = poi_type
        self.charge_type = charge_type
        self.quantities = quantities
        self.dx_value = dx_value
        self.limit = limit

    #override
    def create_cells(self):
        """ Create Simulation Cells For The Simulation To Take Place"""
        self.cells = np.zeros(
            (self.dimensions, self.dimensions, self.dimensions))

    #override
    def start_sim(self):
        """Starts The Simulation"""
        self.create_p()
        self.create_cells()
        self.sim_data = []
        if self.poi_type == "jacobi":
            sim_function = self.jacobi
        else:
            sim_function = self.gauss_seidel
            self.cellsList = []

        for self.t in range(self.timesteps):
            sim_function()
        self.finished_sim()

    def create_p(self):
        self.p = np.zeros((self.dimensions, self.dimensions, self.dimensions))

        if self.quantities == "magnetic":
            for i in range(0, self.dimensions):
                self.p[0, 0, i]
        elif self.charge_type == "point":
            self.p[int(self.dimensions / 2), int(self.dimensions / 2), int(self.dimensions / 2)] = 1
        else:
            for i in range(0, self.dimensions):
                self.p[int(self.dimensions / 2), int(self.dimensions / 2), i] = 1

    def jacobi(self):
        self.new_cells = np.copy(self.cells)
        for i in range(1, self.dimensions - 1):
            for j in range(1, self.dimensions - 1):
                for k in range(1, self.dimensions - 1):
                    self.new_cells[i, j, k] = self.jacobi_procedure(i, j, k)
        self.check_sim()
        self.cells = np.copy(self.new_cells)

    def gauss_seidel(self):
        self.gauss_procdeure()
        if len(self.cellsList) >= 2:
            self.new_cells = self.cellsList[self.t - 1]
            self.check_sim()
        self.cellsList.append(self.cells)

    def jacobi_procedure(self, i, j, k, variable = None):
        sigma = (1 / 6) * (
            self.cells[self.i_index(i), j, k] + \
                self.cells[self.d_index(i), j, k] + \
                    self.cells[i, self.i_index(j), k] + \
                        self.cells[i, self.d_index(j), k] + \
                            self.cells[i, j, self.i_index(k)] + \
                                self.cells[i, j, self.d_index(k)] +\
                                    self.p[i, j, k] * (self.dx_value ** 2))
        return sigma

    def gauss_procdeure(self):
        for i in range(1, self.dimensions - 1):
            for j in range(1, self.dimensions - 1):
                for k in range(1, self.dimensions - 1):
                    self.cells[i,j,k] = (1 / 2)  * \
                        (self.cells[self.i_index(i), j, k] + \
                        self.cells[self.d_index(i), j, k] + \
                            self.cells[i, self.i_index(j), k] + \
                                self.cells[i, self.d_index(j), k] + \
                                    self.cells[i, j, self.i_index(k)] + \
                                        self.cells[i, j, self.d_index(k)] +
                                            (self.dx_value ** 2) * self.p[i,j, k])

    def difference(self, array1, array2):
        """ Calculates the difference between two arrays """
        difference = np.sum(array2.flatten() - array1.flatten()) / np.sum(array2.flatten())
        return difference

    #override
    def check_sim(self):
        if self.index % 5 == 0:
            print ("Timesteps Completed: {} out of {}".format(self.index, self.timesteps))
        if self.difference(self.cells , self.new_cells) <= self.limit:
            print("Convergence Limit Reached")
            self.finished_sim()
            self.end_simulation()
        self.index += 1

    #override
    def finished_sim(self):
        self.contour_data = [self.cells[int(self.dimensions / 2)], self.p[int(self.dimensions / 2)]]
        if self.quantities == "electric":
            gradients = self.get_gradients()
            x = np.arange(0, self.dimensions, 1)
            y = np.flip(x)
            data = [x, y, gradients[:,:,1], gradients[:,:,0]]
            self.plot_data("Quiver", data, "Quiver Plot of the electric field for Poisson Simulation", "X", "Y")

        elif self.quantities == "charges":
            self.plot_data("Contour", self.contour_data[0],  "Contour Plot of the Field For Poisson Simulation", "X", "Y")
            # self.plot_data("Imshow", self.contour_data[0], "X", "Y", "Contour Plot of the Field For Poisson Simulation")
            self.plot_data("Contour", self.contour_data[1], "Contour Plot of the Charge Distribution For Poisson Simulation", "X", "Y")

        elif self.quantities == "magnetic":
            gradients = self.get_gradients()
            x = np.arange(0, self.dimensions, 1)
            y = np.arange(0, self.dimensions, 1)
            data = [x, y, gradients[:,:,1], gradients[:,:,0]]
            self.plot_data("Quiver", data, "Quiver Plot of magnetic field for Poisson Simulation", "X", "Y")

    def get_gradients(self):
        grads_shape = self.contour_data[0].shape + (2,)
        gradients = np.zeros(grads_shape)
        for i in range(1, self.dimensions - 1):
            for j in range(1, self.dimensions - 1):
                gradients[i, j] = [self.contour_data[0][self.i_index(i), j] - self.contour_data[0][self.d_index(i), j], self.contour_data[0][i, self.d_index(j)] - self.contour_data[0][i, self.i_index(j)]]
        return gradients

