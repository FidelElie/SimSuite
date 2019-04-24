from tools.utils import general_utils

class Parametiser(object):
    # FIXME Not Dynamic, have to add sim info manually

    manifest = general_utils.load_json_file(general_utils.join_path(general_utils.SIM_TEMPLATES, "manifest.json"))

    params = {}
    sim_mode = None
    flag = True

    def __init__(self, modes):
        self.modes = modes
        self.load_template()


    def load_template(self):
        print ("\nChoosing template file")
        files = general_utils.get_directory_contents(general_utils.SAVE_PATH)
        if len(files) == 0:
            print(
                "No template files present, use creator module to create file")
            self.flag = False
        else:
            chosen_file = general_utils.pick_parameter("Template File", files)

            file_path = general_utils.join_path(
                general_utils.SAVE_PATH, chosen_file)

            self.params = general_utils.load_json_file(file_path)

            self.mode =  self.params["mode"]
            self.default_values = self.params["default_values"]
            del self.params["mode"]
            del self.params["default_values"]

        if self.flag != False:
            self.check_template()

    def check_template(self):
        if len(self.params) != len(self.default_values):
            print ("Template Error: Number of default Values do not match the amount of modifiable parameters")
            self.flag = False
        else:
            for i, keys in enumerate(self.params):
                if self.params[keys] == None:
                    self.params[keys] = self.default_values[i]
                    continue
                else:
                    try:
                        if self.params[keys] not in self.manifest["discrete"][keys]:
                            self.flag = False
                    except KeyError:
                        continue

                if self.flag == False:
                    self.error_message(keys)
                    break

            if self.flag != False:
                for i, keys in enumerate(self.params):
                    try:
                        if keys in self.manifest["datatyped"]:
                            self.flag = self.check_datatypes(self.params[keys], self.manifest[keys])
                    except KeyError:
                        continue

                    if self.flag == False:
                        self.error_message(keys)
                        break


    def error_message(self, parameter):
        print("Template Error: parameter given not supported for {}".format(parameter))

    @staticmethod
    def check_datatypes(data, rule):
        if isinstance(rule, list) == True:
            rule = len(rule)
            if rule == len(data):
                outcome = True
            else:
                outcome = False
        else:
            rule = rule.split(" ")
            # TODO fix the use of eval
            try:
                eval(rule[0])(data)
            except ValueError:
                outcome = False
            else:
                outcome = True
            if len(rule) > 1:
                low, high = rule.split("-")[0], rule.split("-")[1]
                if data < low or data > high:
                    outcome = False
                else:
                    outcome = True
        return outcome



