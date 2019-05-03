import sys
from tools import *
from packages import *
from tools.utils import general_utils, parseArg

def main():
    # checks that all folders are present for programme
    general_utils.check_directories()

    # gets name of module python files tools/utils
    modules = general_utils.get_py_files(general_utils.MODULE_PATH)

    # resolves module class names into a list (references to classes)
    module_class = [general_utils.str_to_class("tools", module) for module in modules]

    # gets the simulation mode names from the template files
    modes = general_utils.get_sim_modes()

    # parses arguements from the command line
    flag = parseArg.ParseArg(sys.argv, modes, modules).shortcut_flag

    # checks what module was chosen if applicable
    module_mode = general_utils.pick_parameter("Module", modules) if flag == "none" else flag

    # loads the chosen module
    if module_mode in modules:
        index = modules.index(module_mode)
        module = module_class[index](modes)

if __name__ == '__main__':
    main()
