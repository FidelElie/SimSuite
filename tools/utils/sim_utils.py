import numpy as np

"""
Icing Model Utility Functions
---
determine_flip_state: determines if the state should be flipped
filp_array_state: flips the state
determine_energy_change: calculates the change of energy
get_icing_data: gets data back from an icing model
calculate_total_energy: calculates the total energy of the array
determine_energy: determines energy of a given cell
calculate_total_mag: calcualtes the total magnetisation of the array
"""

def determine_flip_state(energy_change, tempurature):
    """Determines the flip state of a state in icing model"""
    if energy_change < 0:
        flip_state = True
    else:
        random_number = np.random.uniform(0, 1)
        probability_p = np.exp(- energy_change / float(tempurature))
        if random_number <= probability_p:
            flip_state = True
        else:
            flip_state = False
    return flip_state

def flip_array_state(array_state):
    """Flips state in icing model"""
    if array_state == 1:
        array_state = -1
    else:
        array_state = 1
    return array_state

def determine_energy_change(member_state, neighbours):
    """Determines energy change of state in icing model"""
    energy_change = 2 * sum(neighbours) * member_state
    return energy_change

def get_icing_data(file_data, size):
    """Gets data from icing model file"""
    temps = [float(data.split(",")[0]) for data in file_data]
    energy = [float(data.split(",")[1]) for data in file_data]
    mags = [float(data.split(",")[2]) for data in file_data]
    amounts = np.arange(min(temps), max(temps), 0.1)
    averageEnergy = []
    averageMags = []
    suceptibility = []
    specificHeat = []
    # loops over the tempuratures for sorting of data values
    for i in range(len(amounts)):
        tempEnergy = []
        tempMags = []
        # loops over all tempurature values to sort the values for averaging
        for j in range(len(temps)):
            if temps[j] == amounts[i]:
                tempEnergy.append(energy[j])
                tempMags.append(mags[j])
        # work out average energies
        averageEnergy.append(sum(tempEnergy) / len(tempEnergy))
        averageMags.append(sum(tempMags) / len(tempMags))
        # work out variance of the averages
        sucAmount = np.var(averageMags) / \
            (temps[i] * int(size) ** 2)
        specAmount = np.var(averageEnergy) / \
            (temps[i] ** 2 * int(size) ** 2)
        suceptibility.append(sucAmount)
        specificHeat.append(specAmount)
    icing_list = [averageEnergy, averageMags, suceptibility, specificHeat]
    return icing_list, amounts

def determine_energy(cells, coordinate):
    """Determines energy of state in the icing model"""
    row = coordinate[0]
    col = coordinate[1]
    member = cells[row, col]
    top = cells[row - 1 if row - 1 >= 0 else len(cells) - 1, col]
    bottom = cells[row + 1 if row + 1 <= len(cells) -1 else 0, col]
    right = cells[row, col - 1 if col - 1 >= 0 else len(cells) - 1]
    left = cells[row, col + 1 if col + 1 <= len(cells) - 1 else 0]
    nieghbours = [top, bottom, right, left]
    energy = - sum(nieghbours) * member
    return energy

def calculate_total_energy(cells):
    """Calulates the toal energy of the system"""
    energies = np.empty((len(cells), len(cells)))
    for i in range(len(cells)):
        for j in range(len(cells)):
            energies[i, j] = determine_energy(cells, (i, j))
    energy = np.sum(energies)
    return energy

def calculate_total_mag(cells):
    """Calculates the toal magnetisation of the system"""
    magnetisation = abs(np.sum(cells))
    return magnetisation
# -----------------------------------------------------------------
"""
Game Of Life Utility Functions
"""
GOLSTRUCTS = {
    "static": np.array(
        [
            [0, 1, 0],
            [1, 0, 1],
            [1, 0, 1],
            [0, 1, 0]
        ]
        ),
    "blinker": np.array(
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]
        ),
    "toad": np.array(
        [
            [1, 1, 1, 0],
            [0, 1, 1, 1]
        ]
        ),
    "glider": np.array(
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
        ),
    "pulsar": np.array(
        [
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        ]
    ),
    "beacon": np.array(
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]
    ),
    "gun": np.vstack(
        [
            [0] * 24 + [1] + [0] * 11,
            [0] * 22 + [1, 0, 1] + [0] * 11,
            [0] * 12 + [1, 1] + [0] * 6 + [1, 1] + [0] * 12 + [1, 1],
            [0] * 11 + [1, 0, 0, 0, 1] + [0] * 4 + [1, 1] + [0] * 12 + [1, 1],
            [1, 1] + [0] * 8 + [1] + [0] * 5 + [1] + [0] * 3 + [1, 1] + [0] * 14,
            [1, 1] + [0] * 8 + [1, 0, 0, 0, 1, 0, 1, 1] + [0] * 4 + [1, 0, 1] + [0] * 11,
            [0] * 10 + [1] + [0] * 5 + [1] + [0] * 7 + [1] + [0] * 11,
            [0] * 11 + [1, 0, 0, 0, 1] + [0] * 20,
            [0] * 12 + [1, 1] + [0] * 22,
        ]
    ),
    "pentadecon": np.array(
        [
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 0 ,0]
        ]
    ),
    "heavyglider": np.array(
        [
            [0, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0]
        ]
    )
}

def return_gol_structures(struct_name):
    return GOLSTRUCTS[struct_name]

def get_com_data(file_data):
    x_coordinate = [float(data.split(",")[0]) for data in file_data]
    y_coordinate = [float(data.split(",")[1]) for data in file_data]
    return np.asarray(x_coordinate), np.asarray(y_coordinate)

# -----------------------------------------------------------------
"""
SIRS Utility Functions
---
get_infection_data : sorts data from sirs data sets
"""
def get_infection_data(file_data, identifier):
    if identifier == "Half":
        iprob_data = np.asarray([float(x.split(",")[0]) for x in file_data])
        avgI = np.asarray([float(x.split(",")[1]) for x in file_data])
        errors = np.asarray([float(x.split(",")[2]) for x in file_data])
        data = [iprob_data, avgI, errors]
    elif identifier == "Cut":
        p1_data = np.asarray([float(x.split(",")[0]) for x in file_data])
        p3_data = np.asarray([float(x.split(",")[1]) for x in file_data])
        varI = np.asarray([float(x.split(",")[2]) for x in file_data])
        data = [p1_data, varI]
    else:
        p1_data = np.asarray([float(x.split(",")[0]) for x in file_data])
        p3_data = np.asarray([float(x.split(",")[1]) for x in file_data])
        avgI = np.asarray([float(x.split(",")[2]) for x in file_data])
        data = [p1_data, p3_data, avgI]
    return data

# -----------------------------------------------------------------------------
def get_cahn_data(file_data):
    timesteps = np.asarray([float(x.split(",")[0]) for x in file_data])
    energy = np.asarray([float(x.split(",")[1]) for x in file_data])
    data = [timesteps, energy]

    return data
