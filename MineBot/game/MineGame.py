from .InternalCellInfo import InternalCellInfo
from .MineGrid import MineGrid
from .MinePlacer import *
import sys


class MineGame(object):

    def init_game(self, x_size, y_size, mine_count):
        self._grid = MineGrid(x_size, y_size)
        grid = self._grid

        # Get some random mines to put in to the grid
        mineList = get_random_mines(grid.flat_indexes, mine_count)
        grid.place_mines(mineList)

    def display_grid(self):
        self._grid.display_grid()
