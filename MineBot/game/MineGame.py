from .InternalCellInfo import InternalCellInfo
from .MineGrid import MineGrid
from .MinePlacer import *
import sys

class GameState:
    WON=1
    PLAYING=2
    LOST=3


class MineGame(object):

    def __init__(self):
        self.state = GameState.PLAYING

    def init_game(self, x_size, y_size, mine_count):
        self._grid = MineGrid(x_size, y_size)
        grid = self._grid

        # Get some random mines to put in to the grid
        mineList = get_random_mines(grid.flat_indexes, mine_count)
        grid.place_mines(mineList)

    def get_game_state(self):
        size = self._grid.size
        state = [[0 for i in range(size[0])] for j in range(size[1])] 
        for loc in self._grid.flat_indexes:
            state[loc[0]][loc[1]] = self._grid[loc].get_game_char()
        return state

    def display_game_state(self):
        state = self.get_game_state()
        for line in state:
            for cell in line:
                sys.stdout.write(cell + ' ')
            sys.stdout.write('\n')

    def unhide_cell(self, location):
        """
        Unhide a cell selected by the player
        """
        grid[location].is_hidden = False
        
        if grid[location].has_mine == True:
            self.state = GameState.LOST
    
    def flag_cell(self, location):
        """
        Flag a cell that is suspected of having a mine
        """
        grid[location].is_flagged = True

    def unflag_cell(self, location):
        """
        Flag a cell that is suspected of having a mine
        """
        grid[location].is_flagged = False 

    def display_grid(self):
        self._grid.display_grid()
