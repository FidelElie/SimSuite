from tools.utils import UtilityBase, parametiser, general_utils

class Simulation(UtilityBase):

    def __init__(self, modes):
        self.modes = modes
        self.pick_sim()

    def pick_sim(self):
        # resolves simulation class names into a list (reference to classes)
        classes = [
            general_utils.str_to_class("packages", mode) for mode in self.modes]
        # get parameter data for chosen simulation
        template_data = parametiser.Parametiser(self.modes)
        chosen_parameters = template_data.params

        # ? if data found in template is valid
        if template_data.flag == True:

            # loads the corresponding simulation file
            index = self.modes.index(template_data.mode)
            sim_module = classes[index]
            sim_module = sim_module(**chosen_parameters)
            sim_module.start_sim()
