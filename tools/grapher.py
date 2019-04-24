import numpy as np
import matplotlib.pyplot as plt
from tools.utils import UtilityBase, general_utils, sim_utils

class Grapher(UtilityBase):

    def __init__(self, modes):
        self.modes = modes
        super().__init__(self.plot_data, self.create_figure, self.setup)

    def setup(self):
        self.choices = [
            ("kawasaki", self.icing_plots),
            ("glauber", self.icing_plots),
            ("sirs", self.aver_plot),
            ("sirshalf", self.immune_plot),
            ("sirscut", self.var_plot),
            ("cahn", self.cahn_plot)
            ]
        self.identifiers = [string[0] for string in self.choices]
        self.functions = [func[1] for func in self.choices]

    def create_figure(self):
        """Creates figure for plotting and subplotting"""
        self.figure = plt.figure()

    def plot_data(self, file_name):
        """Plots the data based on simulations chosen"""
        identifier = file_name.replace(".txt","").lower()
        print (identifier)
        params = identifier.split(" - ")

        if params[0] in self.identifiers:
            index = self.identifiers.index(params[0])
            self.functions[index](*params)
        else:
            self.incomp_message()

    def icing_plots(self, identifier, size, sweeps):
        """Sorts and plots data for icing model datasets"""
        icing_list, amounts = sim_utils.get_icing_data(self.file_data, size)
        plot_titles = ["Average Energy Against Tempurature", "Average Magnetisation Against Tempurature", "Suceptibility Against Tempurature", "Specific Heat Against Tempurature"]
        plot_xlabel = "Tempurature"
        plot_ylabels = ["Average Energy", "Average Magnetisation", "Suceptibility", "Specific Heat"]
        mode = identifier
        figure_title = "Data for the {} Sim With {} Cells and {} Sweeps".format(mode.title() ,int(size) ** 2, sweeps)
        self.figure.suptitle(figure_title)
        for i in range(len(icing_list)):
            ax = self.figure.add_subplot(2, 2, i + 1)
            ax.plot(amounts, icing_list[i])
            ax.set_xlabel(plot_xlabel)
            ax.set_ylabel(plot_ylabels[i])
            ax.set_title(plot_titles[i])
        plt.show()

    def aver_plot(self, indentifier, size, sweeps):
        contour_list = sim_utils.get_infection_data(self.file_data, "Full")
        p1_vals = list(set(contour_list[0]))
        p3_vals = list(set(contour_list[1]))
        avg_vals = contour_list[2].reshape(len(p1_vals), len(p3_vals))
        plot_xlabel = "p1"
        plot_ylabel = "p3"
        plot_title = "Contour Plot Showing The Averages Of Suceptible Cells"
        self.figure.suptitle(plot_title)
        plt.xlabel(plot_xlabel)
        plt.ylabel(plot_ylabel)
        plt.contourf(avg_vals)
        plt.show()

    def var_plot(self, identifier, size, sweeps):
        contour_list = sim_utils.get_infection_data(self.file_data, "Cut")
        p1_vals = list(set(contour_list[0]))
        p3_vals = list(set(contour_list[0]))
        var_vals = contour_list[1].reshape(len(p1_vals), len(p3_vals))
        plot_xlabel = "p1"
        plot_ylabel = "p3"
        plot_title = "Contour Plot Showing The Variance of Suceptible Cells"
        self.figure.suptitle(plot_title)
        plt.xlabel(plot_xlabel)
        plt.ylabel(plot_ylabel)
        plt.contourf(var_vals)
        plt.show()

    def immune_plot(self, identifier, size, sweeps):
        immune_list = sim_utils.get_infection_data(self.file_data, "Half")
        immune_prob = immune_list[0]
        avgI = immune_list[1]
        error_data = immune_list[2]
        plot_title = "Plot Showing Immune Probabbilities Against The Average Infection Number"
        self.figure.suptitle(plot_title)
        plt.xlabel("Immune Probabilities")
        plt.ylabel("Average Infection")
        plt.errorbar(immune_list[0], immune_list[1], yerr=immune_list[2])
        plt.show()

    def cahn_plot(self, identifier, size, sweeps):
        energy_list = sim_utils.get_cahn_data(self.file_data)
        timesteps = energy_list[0]
        energies = energy_list[1]
        plot_title = "Plot Showing The Free Energy Against Timesteps For The Cahn Hilliard Simulation"
        self.figure.suptitle(plot_title)
        plt.xlabel("Timesteps")
        plt.ylabel("Energy")
        plt.plot(energy_list[0], energy_list[1])
        plt.show()
