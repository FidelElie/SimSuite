import numpy as np
from packages.controller import SimulationPlane
from tools.utils import utils

class Reaction(SimulationPlane):
	def __init__(self, dimensions, timesteps):
		super().__init__(dimensions, timesteps)

	#override
	def create_figure(self):
		super().create_figure()

	#override
	def create_cells(self):
		pass

	#override
	def anim_func(self, i):
		pass