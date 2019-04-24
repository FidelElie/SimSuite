from tools.utils import general_utils

class ParseArg(object):

    def __init__(self, arguement, modes, modules):
        self.arguement = arguement
        self.modes = modes
        self.modules = modules
        self.intialiseCommands()
        self.check_arguements()

    def intialiseCommands(self):
        self.commands = [
            ("--new-template", "template", self.create_template),
            ("--new-simulation", "new", self.new_simulation),
            ("--new-module", "new", self.new_module),
            ("--shortcut", None, self.shortcut),
            ("--readme", "docs", general_utils.open_readme),
            ("--help-commands", "help", general_utils.print_cl_commands)]
        self.calls = [command[0] for command in self.commands]
        self.flags = [flag[1] for flag in self.commands]
        self.functions = [function[2] for function in self.commands]

    def check_arguements(self):
        if len(self.arguement) != 1:
            self.check()
        else:
            self.shortcut_flag = "none"

    def check(self):
        if self.arguement[1] in self.calls:
            index = self.calls.index(self.arguement[1])
            self.shortcut_flag = self.flags[index]
            self.functions[index]()
        else:
            print("Command Line Error: Invalid Command Given\nCall 'python main.py --help-commands' to see supported commands")
            self.shortcut_flag = "error"

    def create_template(self):
        try:
            if self.arguement[2].lower() in self.modes:
                general_utils.copy_template(self.arguement[2])
            else:
                print ("Command Line Error: Invalid Simulation Given\nSupported Simulations: {}".format(",".join(self.modes)))
        except IndexError:
            general_utils.command_line_error(self.create_template.__name__)

    def shortcut(self):
        try:
            if self.arguement[2].lower() in self.modules:
                self.shortcut_flag = self.arguement[2].lower()
            else:
                print ("Command Line Error: Invalid Module name Given\nSupported Modules: {}".format(",".join(self.modules)))
        except IndexError:
            general_utils.command_line_error(self.shortcut.__name__)

    def new_simulation(self):
        try:
            new_sim_name = self.arguement[2]
            general_utils.create_simulation(new_sim_name)
        except IndexError:
           general_utils.command_line_error(self.new_simulation.__name__)

    def new_module(self):
        try:
            new_module_name = self.arguement[2]
            general_utils.create_module(new_module_name)
        except IndexError:
            general_utils.command_line_error(self.new_module.__name__)
