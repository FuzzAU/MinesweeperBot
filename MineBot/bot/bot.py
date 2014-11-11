import sys
from ..game.gridutils import *


class MineBot(object):
    """
    Function to assist with automatically playing minesweeper

    TODO: I need to find a better way for the bot to interact
          with the game's grid...
    """

    def __init__(self, game):
        self.game = game

    def auto_step(self):
        flagged = 1
        cleared = 1
        print 'Taking auto step...'
        while (flagged + cleared) > 0:
            flagged = self.auto_flag()
            cleared = self.auto_clear()
            print 'F: ' + str(flagged) + '\tC: ' + str(cleared)
        print 'Auto step complete'

    def auto_flag(self):
        """
        Automatically flag all mines that are obviously flaggable
        """
        game = self.game
        # Keep track of how many mines were flagged during this
        # functions run
        flagged = 0

        # Go through each of the opened cells and
        # work out if the number of surrounding cells still hidden
        # is the same as the number if surrounding cells specified
        # by the game
        for cell_ind in game.opened_cells:
            cell = self.game._grid[cell_ind]
            adj = adjacent_cells(self.game._grid, cell_ind)

            # Count the number of hidden fields in the adjacent cells
            hidden_adj = sum(adj_cell.is_hidden for adj_cell in adj)

            # If they do match, then flag each of the unflagged cells
            if hidden_adj == cell.count_adjacent_mines():
                for adj_cell in adj:
                    if adj_cell.is_hidden and (adj_cell.is_flagged is False):
                        adj_cell.is_flagged = True
                        flagged += 1

        return flagged

    def auto_clear(self):
        """
        Automatically clear the cells surrounding a cell that has
        flagged the same number of flags as the number of specified mines
        """
        game = self.game
        grid = game._grid

        cleared = 0

        # This is a once run operation, unlike autoflag
        # For each opened cell, check the number of flagged
        for cell_ind in game.opened_cells:
            cell = grid[cell_ind]
            adj_indexes = adjacent_indexes(grid.size, cell_ind)

            # Count the number of flagged cells
            flagged_adj = sum(grid[ind].is_flagged for ind in adj_indexes)

            if flagged_adj == cell.count_adjacent_mines():
                for adj in adj_indexes:
                    adj_cell = grid[adj]
                    if (adj_cell.is_hidden) and\
                       (adj_cell.is_flagged is False):
                        game.unhide_cell(adj)
                        cleared += 1
        return cleared
