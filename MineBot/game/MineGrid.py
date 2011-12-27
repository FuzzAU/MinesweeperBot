from .InternalCellInfo import InternalCellInfo
from .MineGridUtils import *
import sys


class MineGrid(object):

    def __init__(self, x_size, y_size):
        """
        Initialize a new mine grid
        """
        self._mine_grid = []
        self.size = (x_size, y_size)
        self.flat_indexes = [(x, y) for x in xrange(0, x_size)\
                                   for y in xrange(0, y_size)]

        for j in xrange(y_size):
            row = []
            for i in xrange(x_size):
                row.append(InternalCellInfo())
            self._mine_grid.append(row)

    def __getitem__(self, location):
        """
        Access a specific location in the grid

        We want to access as (x,y)
        The first index in our grid is actually the row, and is hence y
        so we access as (location[1], location[0])
        """
        return self._mine_grid[location[1]][location[0]]

    def place_mines(self, mine_list):
        """
        Mine list should be formed as [(x1,y1), (x2,y2)]
        """
        for cell in [self[x] for x in mine_list]:
            cell.has_mine = True

        self.__update_adjacency__()

    def __update_adjacency__(self):
        """
        Updates the adjacent mine fields of each cell after mines are placed
        """
        for loc in self.flat_indexes:
            adj = adjacent_cells(self.size, loc)
            x = sum(self[i].has_mine for i in adj)
            self[loc]._adjacent_mines = sum(self[i].has_mine for i in adj)

    def display_grid(self):
        for line in self._mine_grid:
            for cell in line:
                sys.stdout.write(cell.get_char() + ' ')
            sys.stdout.write('\n')
