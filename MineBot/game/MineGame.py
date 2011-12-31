from .InternalCellInfo import InternalCellInfo
from .MineGrid import MineGrid
from .MinePlacer import *
from .MineGridUtils import *
import sys
from copy import copy

class GameState(object):
    WON = 1
    PLAYING = 2
    LOST = 3


class MineGame(object):

    def __init__(self):
        self.state = GameState.PLAYING
        self.populated = False

        # Keep a list of unopened cells (to assist in speedy auto-evaluation)
        self.unopened_cells = []
        # Keep a list of opened cells, that are non-zero (to assist in speed auto-evaluation)
        self.opened_cells = []

    def init_game(self, x_size, y_size, mine_count):
        self._grid = MineGrid(x_size, y_size)
        self.mine_count = mine_count

        # The list of unopened cells will initially be all possible cells
        self.unopened_cells = copy(self._grid.flat_indexes) 

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
        for cell in adjacent_indexes(self._grid.size, first_location):
            grid_indexes.remove(cell)

        # Get some random mines to put in to the grid
        mineList = get_random_mines(grid_indexes, self.mine_count)
        # Place the mines
        self._grid.place_mines(mineList)
        # Mark the grid as populated
        self.populated = True

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
        sys.stdout.write('\n')
        for line in state:
            for cell in line:
                sys.stdout.write(cell + ' ')
            sys.stdout.write('\n')

        sys.stdout.write('\n')

    def unhide_cell(self, location):
        """
        Unhide a cell selected by the player
        """
        # If this is our first click, then populate the grid
        if self.populated == False:
            self.populate_grid(location)

        cell = self._grid[location]
        # Unhide the selected cell
        cell.is_hidden = False
        
        # When this mine is unhidden, remove it from the unopened cells list
        try:
            self.unopened_cells.remove(location)
        except ValueError:
            pass

        cell.is_flagged = False 

        # If this cell was a mine, the game is lost
        if cell.has_mine == True:
            self.state = GameState.LOST

        # If the cell has 0 surrounding mines, auto-unhide the
        # surrounding mines
        elif cell.count_adjacent_mines() == 0:
            self.auto_unhide(location)
        else:
            # This cell was opened, so print out the opened cells
            self.opened_cells.append(location)

        win = self.check_for_win()
        if win == True:
            self.state = GameState.WON

    def check_for_win(self):
        """
        Check to see if the game is in a winning state

        A winning state is when all the non-mine cells are unhidden
        """
        grid = self._grid
        # When the number of cells still flagged is == number
        # of mines, this is a win
        still_flagged = sum([grid[(x, y)].is_hidden for x in\
                            xrange(0, grid.size[0]) for y in\
                            xrange(0, grid.size[1])])

        if still_flagged == self.mine_count:
            return True
        else:
            return False

    def auto_unhide(self, location):
        """
        Automatically unhide all cells around a cell marked
        with 0 surrounding mines
        """
        unhide_list = [location]
        while len(unhide_list) > 0:
            cell = unhide_list.pop()
            self._grid[cell].is_hidden = False

            for cell_ind in adjacent_indexes(self._grid.size, cell):
                # If one oef the cells we try and unhide is also zero
                # then push it to the list to have its neighbours
                # unhidden too
                adj_cell = self._grid[cell_ind]
                try:
                    self.unopened_cells.remove(cell_ind)
                except ValueError:
                    pass

                if (adj_cell.count_adjacent_mines() == 0)\
                   & (adj_cell.is_hidden == True):
                    unhide_list.append(cell_ind)
                elif (adj_cell.count_adjacent_mines() != 0)\
                   & (adj_cell.is_hidden == True):
                    self.opened_cells.append(cell_ind)

                # Unhide this, and all surrounding cells
                adj_cell.is_hidden = False

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
