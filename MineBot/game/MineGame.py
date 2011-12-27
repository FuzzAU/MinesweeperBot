from .InternalCellInfo import InternalCellInfo
from .MineGrid import MineGrid
from .MinePlacer import *
from .MineGridUtils import *
import sys

class GameState:
    WON=1
    PLAYING=2
    LOST=3


class MineGame(object):

    def __init__(self):
        self.state = GameState.PLAYING
        self.populated = False

    def init_game(self, x_size, y_size, mine_count):
        self._grid = MineGrid(x_size, y_size)
        grid = self._grid
        self.mine_count = mine_count

    def populate_grid(self, first_location):
        """
        We want to populate the grid with mines, but
        not allow a mine to be in the first selected cell,
        or any adjacent cells
        This is a common way to start in modern minesweeper games
        """
        grid_indexes = list(self._grid.flat_indexes)
        
        # Take away the first location from the list usable for mine placement
        grid_indexes.remove(first_location)
        # Take away all adjacement cells
        for cell in adjacent_cells(self._grid.size, first_location):
            grid_indexes.remove(cell)

        # Get some random mines to put in to the grid
        mineList = get_random_mines(grid_indexes, self.mine_count)
   
        self._grid.place_mines(mineList)

        self.populated = True
   
        self._grid.display_grid()

    def get_game_state(self):
        return self.state

    def get_grid_state(self):
        size = self._grid.size
        state = [[0 for i in range(size[0])] for j in range(size[1])] 
        for loc in self._grid.flat_indexes:
            state[loc[1]][loc[0]] = self._grid[loc].get_game_char()
        return state

    def display_grid_state(self):
        state = self.get_grid_state()
        for line in state:
            for cell in line:
                sys.stdout.write(cell + ' ')
            sys.stdout.write('\n')

    def unhide_cell(self, location):
        """
        Unhide a cell selected by the player
        """
        # If this is our first click, then populate the grid
        if self.populated == False:
            self.populate_grid(location)
        
        self._grid[location].is_hidden = False
        
        if self._grid[location].has_mine == True:
            self.state = GameState.LOST
    
    def toggle_flag_cell(self, location):
        """
        Toggle the flagged state of a cell
        """
        cell = self._grid[location]
        cell.is_flagged = not cell.is_flagged

        # If cell is already unhidden, it cannot be flagged
        if cell.is_hidden == False:
            cell.is_flagged = False

    def flag_cell(self, location):
        """
        Flag a cell that is suspected of having a mine
        """
        # If cell is already unhidden, it cannot be flagged
        if cell.is_hidden == True:
            self._grid[location].is_flagged = True

    def unflag_cell(self, location):
        """
        Flag a cell that is suspected of having a mine
        """
        self._grid[location].is_flagged = False 

    def display_grid(self):
        self._grid.display_grid()
