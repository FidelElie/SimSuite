from tools.utils import UtilityBase, general_utils

class Creator(UtilityBase):

    def __init__(self, modes):
        super().__init__()
        self.modes = modes
        self.initialise_choices(
        )
        self.create_object()

    def initialise_choices(self):
        self.choices = [
            ("Create Template", self.create_template),
            ("Create Simulation", self.create_simulation),
            ("Create Module", self.create_module)
            ]
        self.choice_stings = [string[0] for string in self.choices]
        self.functions = [function[1] for function in self.choices]

    def create_object(self):
        while True:
            choice = general_utils.pick_parameter("What To Create?", self.choice_stings)

            index = self.choice_stings.index(choice)

            self.functions[index]()

            yes_or_no = general_utils.pick_parameter("Stop {}".format(self.get_subclass_name()), self.choice_iterable).lower()
            if yes_or_no == "yes":
                print("{} Finished\n".format(self.get_subclass_name()))
                break
            else:
                print("Picking new template file\n")

    def create_template(self):
        template = general_utils.pick_parameter(
            "Template File", self.modes)
        general_utils.copy_template(template)

    def create_simulation(self):
        sim_name = input("Name Of New Simulation: ")
        general_utils.create_simulation(sim_name)

    def create_module(self):
        module_name = input("Name Of New Module: ")
        general_utils.create_module(module_name)
