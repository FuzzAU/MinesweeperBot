import random
import copy
import numpy


def get_random_mines(cell_list, mine_count):
    """
    Will generate random mine locations from the provided list of cells
    """
    # TODO - JY to consider `random.shuffle` and list slicing
    cell_list_copy = copy.deepcopy(cell_list)

    numpy.random.shuffle(cell_list_copy)
    return cell_list_copy[:mine_count]
