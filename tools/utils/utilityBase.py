from tools.utils import general_utils

class UtilityBase(object):
    file_data = None
    choice_iterable = ["Yes", "No"]

    def __init__(self, data_function = None, create_function = None, setup_function = None):
        self.data_function = data_function
        self.create_function = create_function
        self.setup_function = setup_function
        if self.data_function != None or self.create_function != None:
            self.pick_file()

    def pick_file(self):
        """User can pick what file they would like to plot"""
        if self.setup_function != None:
            self.setup_function()
        while True:
            if self.create_function != None:
                self.create_function()
            file_list = general_utils.get_directory_contents(
                general_utils.DATAPATH)
            if len(file_list) < 1:
                print ("No files present please do simulations to get files")
                break
            else:
                chosen_file = general_utils.pick_parameter("Dataset", file_list)
                self.file_data = general_utils.load_file(
                    general_utils.join_path(
                    general_utils.DATAPATH, chosen_file))
                self.data_function(chosen_file)
            yes_or_no = general_utils.pick_parameter("Stop {}".format(self.get_subclass_name()), self.choice_iterable).lower()
            if yes_or_no == "yes":
                print("{} Finished\n".format(self.get_subclass_name()))
                break
            else:
                print("Picking Another Data Set\n")

    def plot_data(self):
        raise NotImplementedError("plot_data function is used without being reimplemented within the sub class")

    def calculate_data(self):
        raise NotImplementedError("calculate_data function is used without being reimplemented within the sub class")

    @classmethod
    def get_subclass_name(cls):
        return str(cls.__name__).title()

    @staticmethod
    def incomp_message():
        print("Error dataset chosen does not have a supported mode")


