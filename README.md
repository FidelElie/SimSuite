# SimSuite
What started off as school assignment has been rolled into one. Three checkpoints, 6 simulations condensed into one programme for learning, style points and exam ease.

## Motivation
This programme arose from a rewrite of my first checkpoint (out of 3) leading to eureka moment where I noticed that there are a lot of similarities between many different simulations. So why not
create a system that would reuse code, for the animation, saving and loading the datasets and all the other process that were required. I wanted it be easily expandable because who knows what the
exam will require, it will also have to be easy to yse

## Features
* Option To Choose From Many Different Simulations Models.
* Change Parameters Through Easy To Use Templates.
* Easy Steps To Add New Simulations To The Programme.
* Directories to hold resulting graphs and datasets.
* Graph Various functions for simulation datasets.
* Calculate quantities from the simulation datasets.

## Prerequisites
* [Python 3](https://www.python.org/downloads/)
* [Numpy](http://www.numpy.org/)
* [Matplotlib](https://matplotlib.org/)

## Installation
Install python and both of the dependencies and run the **main.py** file located in the root directory.

*Note: ensure that directory you are running the programme from is the root of the programme. This needs to be ensured if running from text editors or there is a possibility that file paths will not be resolved properly.*

## Usage
### Simulation Module
As of writing ths README there are six different simulations to choose from:

* Icing Model Using Glauber Dynamics
* Icing Model Using Kawasaki Dynamics
* Game of Life
* SIRS
* Cahn Hilliard
* Poisson

The sole method of using the programme is through template files (check [Using Template](###Using-Templates) for detailed usage). The process consists of:

1. Choosing which simulation you would like to use from the list above.
2. Choosing the cell dimension and time-steps for the simulation.
3. Choosing parameters that are specific to that simulation.

This will give you any of the simulations on offer whether they are visual ones plotted in matplotlib or full ones that result in dataset creation.

### Using Templates
The template files (located in the [template](template/) file directory) are simply a json file containing a dictionary that is parsed directly to python after being chosen at runtime.

```json
{
    "mode": "glauber",
    "dimensions": "null",
    "timesteps": "null",
    "sim_type": "null",
    "tempurature": "null"
}
```
*The code snippet above shows the base json template file for the icing model simulation using glauber dynamics.*

Each of the keys of the json object are the parameters for a given simulation. They are parsed directly - using `class(**dictionary)` - to the constructor of their corresponding class file (This information only really matters if you are looking to extend the program check [here](##Extending) for more details.)

The template files are generated through the use of the creator module or through a command line call (see [here](###Command-Line) for details). The parameters can then be edited to the desired values for each and can then be loaded into programme upon choosing the simulation module.

### More on Parameters
Most of the parameters will be self-explanatory as they will be required for changing the behavior of the chosen simulation. However, some are a bit more vague in their implementation and should be explained to add clarity:

* percentage: is the percentage of dead cells in the game of life.
* struct_mode: is used to add a specific structure into the game of life.
* sim_type: used in many simulations to determine whether the 'visual' or 'full' simulation is called.
* dyn_mode: used in sirs simulation to change the propagation dynamics.
* prob: percentage chance values for each of the free simulation states (Susceptible, Infected, Recovered)

The valid data formats for different parameters are given in [Mitigating Errors](###Mitigating-Errors) section.

### Special Parameters
A special parameter is one that results in different simulation behavior defined by the programme using a different defined function to carry out the task or enables extra steps in the existing simulation function. Usually these special parameters are used to start simulations that will result in the creation of datasets specific to a certain required quantity. The current special parameters values are:

* *"half"* and *"cut"* for the dyn_mode parameter in the **SIRS** simulation will result in different full simulations. Cut, deals with the variance of infected sites in the simulation and half, deals with the the average infected population against a changing probability of immunity.
* *"glider"* for the struct_mode parameter in the **Game of Life** simulation will result in constant calculations of the centre of mass of said structure. All of this data will be saved to a file at the end of the simulation.

### Mitigating Errors
The template system was created in an effort to decrease the risk of entering invalid data which will be parsed into the programme. Much of these processes are error handled in the code, but it is difficult to forsee them all. As a result instituting a intuitive system and enforcing the correct data types is important. So to make sure here are the data types for each of the parameters:

* dimensions: integer > 0.
* timesteps: integer > 0.
* sim_type: str takes value of 'visual' or 'full'.
* tempurature: int between 1 and 5
* struct_mode: str takes values of 'static', 'blinker', 'toad', 'glider', 'pulsar', 'beacon', 'gun', 'pentadecon', 'heavyglider' and 'none' (no structure added).
* dyn_mode: str takes values of 'cyclic', 'absorbing', 'half', 'dynamic', 'cut' and 'none' (default start state)
* prob: list (array object in json terms) of length 3.
* *cahn simulation*: all values other than the default first three are floating point numbers.
* sim_type (*poisson simulation*): 'jacobi' or 'gauss'
* *poisson simulation*: all other values than default three are floating point numbers.

### Command Line
Command line calls are used in the programme for utility and convenience. They can be used to create new files and quickly start a module etc. They are not used to parse parameters to the simulation. However, if you forget this fact it should not be a problem and the arguments will be ignored.

| Command                     | [arguement]                                            | Explanation                                                                                     |
|-----------------------------|--------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| --new-template [arguement]  | Current: sirs, cahn, glauber, kawasaki, gol or poisson | Will create a base template file from the desired  template denoted with a timestamp in commas. |
| --shortcut [arguement]      | Currently: simulation, grapher, creator or calculator. | Will jump to which ever module was chosen and skip this initial program choice.                 |
| --new-simulation [arguement]| Desired Name Of Simulation                             | Creates components for defining a new simulation.                                               |
| --new-module [arguement]    | Desired Name of Module                                 | Will create a module for utility purposes                                                       |
| --readme                    | N/A                                                    | Will open this readme in your favorite web browser.                                             |
| --help-commands             | N/A                                                    | Quick Overview of the command line commands printed to the command line                         |

### Other Modules

* Grapher: provides functions to plot various graphs from the saved datasets generated by the programme.
* Creator: an in program module that allows the creation of new template, new simulation and new module files.
* Calculator: provides functions to calculate different quantities.

## Extending
### Procedure
The extension of the programme with more simulations can be completed by following these steps:

1. Create a simulation class file and template file by using the create module or `--new-simulation arguement` command line call. THis will create a template json file with mandatory fields for you to enter and add to and a simulation python class file for the simulation to be coded into.
2. Add default values to the json file.
3. Profit.

Your new simulation will automatically be imported into the *[main.py](main.py)* file so there is no need to mess around with the imports.

This procedure leaves a lot of flexibility in defining simulations and gives a parent class that adds convenience for implementing functions such as an animation. As this process has already been implemented into the base class to be called from a method.

### Using The Functions
Some of the methods provided by simulationPlane are convenience functions but they are also used for structure and guidance on implementing specific structures into your simulation. For example: if you want a visualisation for your simulation, then the create_figure method will have to be called to create the figure object, a create_cells method can be overridden to create the cells for the simulation and finally the anim_func method is overridden to hold all your simulation code for the process. The start_sim function is the only thing called and as you can see from the snippet below start_sim can be called to start the simulation in main.py.

```python
def start_sim(self):
    """ Starts the simulation by calling the animation."""
    self.anim = animation.FuncAnimation(self.fig, self.anim_func, frames = self.timesteps, interval = 10, blit=True)
    plt.show()
```
*This method can be used to get a quick matplotlib animation going (which can take hours if your don't know what you're doing or are just unlucky)*
You can also consider overriding the start_sim method if there is say a visual and a full simulation that is to be completed in the simulation. An example of this is shown below for the glauber simulation.

```python
 def start_sim(self):
    """Re-implemented from base class
    Starts the full simulation or visual simulation
    """
    if self.sim_type.lower() == "visual":
        self.create_cells()
        self.create_figure()
        super().start_sim()
    else:
        self.tempurature = np.arange(1, 3, 0.1)
        self.start_full_sim()

```
*The super class method of start sim is called for the visual simulation and another method is called otherwise in the full simulation*

Below is a list of methods and their purposes for created purposes in the parent class.

| Method Name    | Use                                                                                                           |
|----------------|---------------------------------------------------------------------------------------------------------------|
| create_figure  | create the **self.fig** object required for animation, as well as adding goodies.                             |
| start_sim      | start the visual simulation animation function by calling **self.anim**.                                      |
| check_sim      | useful for stopping visual simulation after alloted time-steps.                                               |
| end_simulation | used to end simulation by calling **sys.exit()**.                                                             |
| anim_func      | used for creating the looping animation, simulation code is called here (has to be overridden for animation). |
| create_cells   | used for creating the cells object **self.cells**, used in all simulation pathways (visual or full)           |
| finished_sim   | used for post simulation actions such as saving the dataset to a file and whatever else is required.          |

The neighbour (check_neighbours and check_all_neighbours methods are used my specific simulation and can be be reused if applicable.

### The Other Modules
The other three modules' functionality can be extended in a similar way to eachother. This is achieved by adding tuples to the `self.choices` instance variable located within in the respective class. There is only one notable difference between the creator class and the others. The string taken in as the first index is an arbitrary string for the creator to show what the function will do. Whereas the other two's first index is the lowercase of the dataset file name (e.g sirshalf for SIRSHalf etc). The second index is a reference to the function that should be called upon that being the desired choice.
```python
self.choices = [
        ("Create Template", self.create_template),
        ("Create Simulation", self.create_simulation),
        ("Create Module", self.create_module)
]
```
*This is what the instance variable looks like now with its three different option in the [creator](tools/creator.py) class.*
```python
self.choices = [
            ("kawasaki", self.icing_plots),
            ("glauber", self.icing_plots),
            ("sirs", self.aver_plot),
]
```
*Extract of the `self.choices` instance variable within the [grapher](tools/grapher.py) class showing the difference between this and the creator module above.*

### Considerations
#### Taming Templates
When creating a simulation, care has to be taken to ensure that the parameters, given in the class file match up to those of the parameters in the corresponding json file. The code snippets below illustrate this.

```json
{
    "mode": "gol",
    "dimensions": "null",
    "timesteps": "null",
    "percentage": "null",
    "struct_mode": "null"
}
```
*json file for the Game Of Life simulation: [gol.json](templates/gol.json)*
```python
def __init__(self, dimensions, timesteps, percentage, struct_mode):
    """
    GameOfLife Constructor
    """
    super().__init__(dimensions, timesteps)
    self.percentage = percentage
    self.struct_mode = struct_mode
```
*constructor from the game of life class file: [gol.py](packages/gol.py)*

Notice that all the variable names match each-other in both files. This is paramount to allow the dictionary taken from the template to be parsed
into the simulation constructor without any hassle. This is done process is completed in the *[main.py](main.py)* file with the lines:
```python
sim_module = sim_module(**chosen_parameters)  # calls simulation class and passes its parameters
sim_module.start_sim()  # starts the simulation.
```
*this start any of the simulations and gives them their chosen parameters*
The double asterisk will unpack the parameters based on their keys in the dictionary. Simply put it will try and match up the dictionary keys
with constructor variable names. It is great for sorting but requires a bit of extra care as to not have an exception raised.

#### All About Utility
The *[general_utils.py](tools/utils/general_utils.py)* and *[sim_utils](tools/utils/sim_utils.py)* files located in the [tools/utils](tools/utils) directory contains many functions that do various tasks. *general_utils* has functions that perform file operations and easily have their uses throughout the programme and *sim_utils* has functions specifically tailored to a given simulation.

## License
Please check the license by clicking [here](LICENSE.md).

## Acknowledgments
* Python for being great.
* Modelling and Visualisation for being a great course.
