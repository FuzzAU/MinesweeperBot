import random
import copy


def generate_list(size_x, size_y):
    """
    Generate a list of all cells in a grid of sizeX by sizeY
    """
    cell_list = []
    for x in range(0, size_x):
        for y in range(0, size_y):
            cell_list.append([x, y])
    return cell_list


def print_cell_list(cell_list):
    """
    Prints a list of cells

    For debugging, print a list of all cells in the provided list
    """
    for cell in cell_list:
        print cell


def get_random_mines(cell_list, mine_count):
    """
    Will generate random mine locations from the provided list of cells
    """
    # TODO - JY to consider `random.shuffle` and list slicing
    mine_locations = []
    cell_list_copy = copy.deepcopy(cell_list)
    for mineNum in xrange(min(mine_count, len(cell_list))):
        rand_index = random.randint(0, len(cell_list_copy) - 1)
        mine_locations.append(cell_list_copy.pop(rand_index))
    return mine_locations


def place_mines(mine_grid, mine_count):
    """
    Place random mines inside the mine grid provided
    """
    x_size = len(mine_grid)
    # No better way to do this without better grid structure
    y_size = len(mine_grid[0])

    cell_list = generate_list(x_size, y_size)
    mine_list = get_random_mines(cell_list, mine_count)

    for mine in mine_list:
        cell = mine_grid[mine[0]][mine[1]]
        cell.has_mine = True
