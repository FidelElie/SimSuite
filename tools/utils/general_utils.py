import os
import sys
import json
import pathlib
import datetime
import webbrowser

SIM_TEMPLATES = str(pathlib.Path("templates/sims"))
FILE_TEMPLATES = str(pathlib.Path("templates/files"))
SAVE_PATH = str(pathlib.Path("params"))
MODULE_PATH = str(pathlib.Path("tools"))
SIM_PATH = str(pathlib.Path("packages"))
DATA_PATH = str(pathlib.Path("data"))
GRAPHS_PATH = str(pathlib.Path("graphs"))

# General Functions

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

def load_file(path, flag = False):
    """Load a file and gets it data"""
    with open(path, "r") as file_data:
        if flag == False:
            data = file_data.readlines()
            del data[0:2]
        else:
            data = file_data.read()
    return data

def load_json_file(path):
    with open(path, "r") as json_file:
        return json.loads(json_file.read())

def write_data(data, file_data, sim_info):
    """Write data from simulations to file"""
    data_file_name = "{} - {} - {}.txt".format(*file_data)
    data_file_path = join_path(DATA_PATH, data_file_name)
    with open(data_file_path, "w") as data_file:
        data_file.write("{}\n".format(sim_info))
        for line in data:
            data_file.write("{}\n".format(line))
    print ("Data succesfully saved as {}".format(data_file_name))

def check_directories():
    if os.path.basename(os.getcwd()) != "SimSuite":
        raise Exception("Please Run Programme From Base Directory")
    if os.path.isdir(DATA_PATH) == False:
        os.mkdir("data")
    if os.path.isdir(GRAPHS_PATH) == False:
        os.mkdir("graphs")
    if os.path.isdir(SIM_TEMPLATES) == False:
        os.mkdir("templates")
    if os.path.isdir(SAVE_PATH) == False:
        os.mkdir("params")

# Template Functions

def copy_template(name):
    try:
        file_name = "{}.json".format(name)
        new_file_name = "{} - {}.json".format(
            name, str(datetime.datetime.utcnow()).replace(":",",").replace("-",","))
        template_path = join_path(SIM_TEMPLATES, file_name)
        params_path = join_path(SAVE_PATH, new_file_name)

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

        file_path = join_path(SIM_TEMPLATES, file_name)
        with open(file_path, "r") as template_f:
            json_data = json.loads(template_f.read())
        return json_data
    except FileNotFoundError:
        print("File Not Found {}".format(file_name))

# Creation Functions

def create_simulation(sim_name):
    # file names
    class_file = "{}.py".format(sim_name.lower())
    json_name = "{}.json".format(sim_name.lower())
    # data for each file

    class_template = load_file(
        join_path(FILE_TEMPLATES, "sim.py"), True).format(sim_name.title())

    json_template = load_json_file(join_path(FILE_TEMPLATES, "params.json"))

    json_template["mode"] = sim_name

    # writing data to files
    with open(join_path(SIM_TEMPLATES, json_name), "w") as new_template:
        new_template.write(json.dumps(json_template, indent=4))

    print ("New Template File {} Created".format(sim_name))

    with open(join_path(SIM_PATH, class_file), "w") as new_sim_class:
        new_sim_class.write(class_template)

    print ("New Class File {} Created".format(sim_name.title()))

def create_module(name):
    class_template = load_file(
        join_path(FILE_TEMPLATES, "module.py"), True).format(name.title())

    file_name = "{}.py".format(name)

    with open(os.path.join(MODULE_PATH, file_name), "w") as new_module:
        new_module.write(class_template)

    print ("New Module {} Created".format(name))

# Command Line Stuff

def command_line_error(name):
    print("Command Line Error: Not Enough Arguements Given for --{} call".format(name.replace("_", "-")))

def print_cl_commands():
    print(load_file(join_path(FILE_TEMPLATES, "commands.txt"), True))

# For Dynamic Packages

def str_to_class(package, name):
    return getattr(sys.modules["{}.{}".format(package, name)], name.title())

def get_py_files(path):
    classes  = []
    for files in os.listdir(path):
        if "__init__" not in files and "__pycache__" not in files and ".pyd" not in files and os.path.isdir(os.path.join(path, files)) == False:
            classes.append(files.replace(".py",""))
    return classes

def get_sim_modes():
    modes = []
    for files in os.listdir(SIM_TEMPLATES):
        if "manifest" not in files:
            modes.append(files.replace(".json", ""))
    return modes
