import numpy as np
from tools.utils import sim_utils
from packages.controller import SimulationPlane

class {}(SimulationPlane):
    def __init__(self, dimensions, timesteps):
        super().__init__(dimensions, timesteps)

    #override
    def start_sim(self):
        # override to add different simulation types visual or full
        super().start_sim()

    #override
    def create_figure(self):
        super().create_figure()
        self.im = self.axes.imshow(self.cells, interpolation = "nearest", animated = True)
        self.fig.colorbar(self.im)

    #override
    def create_cells(self):
        """
        self.cells = np.random.normal(
            size=(self.dimensions, self.dimensions)) # loc and scale for noise
        self.cells = np.random.uniform(
            size=self.dimensions, self.dimensions) # high or low
        """
        pass

    #override
    def anim_func(self, i):
        yield self.im



