import sys
import time
import matplotlib.pyplot as plt
from matplotlib import animation
from tools.utils import general_utils

class SimulationPlane(object):
    """ Base Class for implementing a cell simulation environment
    dimensions: x and y dimension of the cells
    timesteps: number of timesteps for the simulation
    """
    index = 0
    def __init__(self, dimensions, timesteps):
        """
        SimulationPlane Constuctor

        Dimensions : The Dimensions of the given cell.
        Timesteps: The Number of timesteps or sweeps for a given simulation.
        """
        self.dimensions = int(dimensions)
        self.timesteps = int(timesteps)

    def create_figure(self):
        """ Creates the figure elements for the simulations """
        self.fig = plt.figure()
        self.axes = plt.axes()
        self.axes.set_xlabel("Cells In X (Columns)")
        self.axes.set_ylabel("Cells In Y (Rows)")
        self.axes.set_xlim(0, self.dimensions - 1)
        self.axes.set_ylim(0, self.dimensions - 1)

    def start_sim(self):
        """ Starts tha simulation by calling the animation (only mehtod that has to be called directly in classes) """
        self.anim = animation.FuncAnimation(self.fig, self.anim_func, frames = self.timesteps, interval = 1, blit=True)
        plt.show()

    def check_sim(self):
        """ Check simulation to see if the amout of timesteps were reached """
        if self.index % 5 == 0:
            print ("Timesteps Completed: {} out of {}".format(self.index, self.timesteps))
        if self.index == self.timesteps:
            print ("Simulation Completed")
            self.end_simulation()
        self.index += 1

    def check_nieghbours(self, coordinate):
        """Used to find the neighbours of a cell"""
        row = coordinate[0]
        cols = coordinate[1]
        member = self.cells[row, cols]
        top = self.cells[self.d_index(row), cols]
        bottom = self.cells[self.i_index(row), cols]
        right = self.cells[row, self.i_index(cols)]
        left = self.cells[row, self.d_index(cols)]
        nieghbours = [left, right, top, bottom]
        return member, nieghbours

    def check_all_nieghbours(self, coordinate):
        """Used to find all neighbours even diagonal members"""
        row = coordinate[0]
        cols = coordinate[1]
        member = self.cells[row, cols]
        top = self.cells[self.d_index(row), cols]
        bottom = self.cells[self.i_index(row), cols]
        right = self.cells[row, self.i_index(cols)]
        left = self.cells[row, self.d_index(cols)]
        top_right = self.cells[self.d_index(row), self.i_index(cols)]
        top_left = self.cells[self.d_index(row), self.d_index(cols)]
        bottom_right = self.cells[self.i_index(row), self.i_index(cols)]
        bottom_left = self.cells[self.i_index(row), self.d_index(cols)]
        nieghbours = [top, bottom, right, left, top_right, top_left, bottom_right, bottom_left]
        return member, nieghbours

    def d_index(self, coord):
        """Decrease index number in array in up or right directions"""
        return coord - 1 if coord - 1 >= 0 else self.dimensions - 1

    def i_index(self, coord):
        """Increase index number in array in down or left directions"""
        return coord + 1 if coord + 1 <= self.dimensions - 1 else 0

    def end_simulation(self):
        time.sleep(1)
        print("Ending Programme")
        time.sleep(0.5)
        sys.exit()

    @staticmethod
    def plot_data(graph, data ,title, x_label, y_label):
        if graph == "Contour":
            plt.contourf(data)
            plt.colorbar()
        elif graph == "Standard":
            x_data = [x.split(",")[0] for x in data]
            y_data = [y.split(",")[1] for y in data]
            plt.plot(x_data, y_data)
        elif graph == "Imshow":
            plt.imshow(data)
        elif graph == "Quiver":
            plt.quiver(data[0], data[1], data[2], data[3])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

        plt.show()


    def warning_message(self):
        if self.timesteps < 99:
            print ("Runtime Warning: There is not enough steps for equilibrium to be reached, so no data will be recorded. Restart progamme with higher sweep number to get data.")

    def create_cells(self):
        """ Base Method Needs To Be Re-implemented in sub classes
        Used for creating the simulation cell object and more figure configurations
        """
        raise NotImplementedError(
            "create_cells function not reimplemented from base class")

    def anim_func(self, i):
        """ Base Method Needs To Be Re-implemented in sub classes
        Used for the animation function
        """
        raise NotImplementedError(
            "anim_func function not reimplemented from base class")

    def finished_sim(self):
        """ Base Method Needs To Be Re-implemneted in sub classes
        Used to finish up and do final calculations and maniuplations
        """
        raise NotImplementedError(
            "finished_sim function not reimplemented form base class")
