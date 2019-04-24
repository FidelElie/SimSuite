import os
import sys
import json
import pathlib
import datetime
import webbrowser

TEMPLATEPATH = str(pathlib.Path("templates"))
SAVEPATH = str(pathlib.Path("params"))
MODULEPATH = str(pathlib.Path("tools"))
SIMPATH = str(pathlib.Path("packages"))
DATAPATH = str(pathlib.Path("data"))
GRAPHSPATH = str(pathlib.Path("graphs"))

def pick_parameter(identifier, iterable = None):
        """Picks parameters based on list of options or integer"""
        while True:
            if iterable != None:
                list_options(iterable)
                try:
                    chosen_option = int(input(
                        "Please Enter Number Corresposing To Chosen Option For {}: ".format(identifier.title())))
                except (ValueError, UnboundLocalError):
                    print("Please enter a valid integer")
                else:
                    if chosen_option < 1 or chosen_option > len(iterable):
                        print("Please enter a valid integer")
                    else:
                        break
        return iterable[chosen_option - 1]

def returnGraphConfigs(fig_call):
    """Returns general figure configurations for matplotlib"""
    anim_fig = {
        "font.family": "Courier New",
        "axes.titlesize": 22,
        "axes.titlepad": 8.0,
        "axes.labelsize": 15,
        "axes.labelpad": 8.0,
        "figure.autolayout": True,
    }
    subplot_fig = {
        "font.family": "Courier New",
        "figure.titlesize": 22,
        "axes.titlesize": 18,
        "axes.titlepad": 8.0,
        "axes.labelsize": 15,
        "axes.labelpad": 8.0,
    }
    if fig_call == "anim":
        fig_params = anim_fig
    elif fig_call == "subplots":
        fig_params = subplot_fig
    return (fig_params)

def list_options(iterable):
    """List options from a iterable with numbers"""
    for i, item in enumerate(iterable, 1):
        print("{}. {}".format(i, item.title())),

def get_directory_contents(dir_path):
    """Lists the directory contents"""
    return os.listdir(dir_path)

def join_path(dir_path, file_name):
    return os.path.join(dir_path, file_name)

def load_file(path):
    """Load a file and gets it data"""
    with open(path, "r") as file_data:
        data = file_data.readlines()
        del data[0:2]
    return data

def load_json_file(path):
    with open(path, "r") as json_file:
        return json.loads(json_file.read())

def write_data(data, file_data, sim_info):
    """Write data from simulations to file"""
    data_file_name = "{} - {} - {}.txt".format(*file_data)
    data_file_path = join_path(DATAPATH, data_file_name)
    with open(data_file_path, "w") as data_file:
        data_file.write("{}\n".format(sim_info))
        for line in data:
            data_file.write("{}\n".format(line))
    print ("Data succesfully saved as {}".format(data_file_name))

def check_directories():
    if os.path.isdir(DATAPATH) == False:
        os.mkdir("data")
    if os.path.isdir(GRAPHSPATH) == False:
        os.mkdir("graphs")
    if os.path.isdir(TEMPLATEPATH) == False:
        os.mkdir("templates")
    if os.path.isdir(SAVEPATH) == False:
        os.mkdir("params")

def copy_template(name):
    try:
        file_name = "{}.json".format(name)
        new_file_name = "{} - {}.json".format(
            name, str(datetime.datetime.utcnow()).replace(":",",").replace("-",","))
        template_path = join_path(TEMPLATEPATH, file_name)
        params_path = join_path(SAVEPATH, new_file_name)

        with open(template_path, "r") as template_f:
            copy_data = template_f.read()

        with open(params_path, "w") as template_f:
            template_f.write(copy_data)

        print("Template For {} Simulation Saved".format(name.title()))
    except FileNotFoundError:
        print("File Not Found {}".format(file_name))

def load_template(name):
    try:
        file_name = "{}.json".format(name)

        file_path = join_path(TEMPLATEPATH, file_name)
        with open(file_path, "r") as template_f:
            json_data = json.loads(template_f.read())
        return json_data
    except FileNotFoundError:
        print("File Not Found {}".format(file_name))

def create_simulation(sim_name):
    # file names
    class_file = "{}.py".format(sim_name.lower())
    json_name = "{}.json".format(sim_name.lower())
    # data for each file
    class_template = "import numpy as np\nfrom packages.controller import SimulationPlane\nfrom tools.utils import utils\n\nclass {}(SimulationPlane):\n\tdef __init__(self, dimensions, timesteps):\n\t\tsuper().__init__(dimensions, timesteps)\n\n\t#override\n\tdef create_figure(self):\n\t\tsuper().create_figure()\n\n\t#override\n\tdef create_cells(self):\n\t\tpass\n\n\t#override\n\tdef anim_func(self, i):\n\t\tpass".format(sim_name.title())

    data_string = "\t\"mode\": \"{}\",\n\t\"dimensions\": \"null\",\n\t\"timesteps\": \"null\",\n\t\"default_values\":[]".format(sim_name)
    data = "{{\n{}\n}}".format(data_string)

    # writing data to files
    with open(os.path.join(TEMPLATEPATH, json_name), "w") as new_template:
        new_template.write(data)

    print ("New Template File {} Created".format(sim_name))

    with open(os.path.join(SIMPATH, class_file), "w") as new_sim_class:
        new_sim_class.write(class_template)

    print ("New Class File {} Created".format(sim_name.title()))

def create_module(name):
    template_string = "import numpy as np\nfrom tools.utils import UtilityBase,utils\n\nclass {}(UtilityBase):\n\tdef __init__(self):\n\t\tsuper().__init__()".format(name.title())

    file_name = "{}.py".format(name)

    with open(os.path.join(MODULEPATH, file_name), "w") as new_module:
        new_module.write(template_string)
    print ("New Module {} Created".format(name))

def get_sim_modes():
    modes = []
    for files in os.listdir(TEMPLATEPATH):
        if "manifest" not in files:
            modes.append(files.replace(".json",""))
    return modes

def str_to_class(package, name):
    return getattr(sys.modules["{}.{}".format(package, name)], name.title())

def get_py_files(path):
    classes  = []
    for files in os.listdir(path):
        if "__init__" not in files and "__pycache__" not in files and ".pyd" not in files and os.path.isdir(os.path.join(path, files)) == False:
            classes.append(files.replace(".py",""))
    return classes

def command_line_error(name):
    print("Command Line Error: Not Enough Arguements Given for --{} call".format(name.replace("_", "-")))

def open_readme():
    print("Opening README in default browser")
    webbrowser.open("README.html")

def print_cl_commands():
    commands_str = "--new-template <arguement>: creates new template file\n--new-simulation <arguement>: creates new simulation and corresponding template file\n--new-module <arguement>: creates new module\n--shortcut <arguement>: jumps to module\n--readme: opens the programme readme\n--help-commands: displays command line call syntax (You Just Called It)"
    print(commands_str)
