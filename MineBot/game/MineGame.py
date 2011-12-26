from .CellInfo import CellInfo
import MinePlacer
import sys


class MineGame(object):

    def __init__(self):
        self.mine_grid = []

    def cells(self):
        """
        Return a flattened list of cells
        """
        res = []
        for row in self.mine_grid:
            for item in row:
                res.append(item)
        return res

    def init_game(self, x_size, y_size, mine_count):
        for j in xrange(y_size):
            row = []
            for i in xrange(x_size):
                row.append(CellInfo())
            self.mine_grid.append(row)

        MinePlacer.place_mines(self.mine_grid, mine_count)
        self.perform_mine_count()

    def perform_mine_count(self):
        for x in xrange(len(self.mine_grid)):
            for y in xrange(len(self.mine_grid[0])):
                self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x_mine, y_mine):
        cell = self.mine_grid[x_mine][y_mine]
        # Maybe I need to make the mine grid something smarter???
        grid_size = (len(self.mine_grid), len(self.mine_grid[0]))
        for xadj in xrange(x_mine - 1, x_mine + 2):
            # Do bounds check for X
            if (xadj < 0) | (xadj > grid_size[0] - 1):
                continue
            for yadj in xrange(y_mine - 1, y_mine + 2):
                # Do bounds check for Y
                if (yadj < 0) | (yadj > grid_size[1] - 1):
                    continue
                test_cell = self.mine_grid[xadj][yadj]
                if test_cell.has_mine == True:
                    cell.surrounding_mines += 1

    def display_grid(self):
        for line in self.mine_grid:
            for cell in line:
                sys.stdout.write(cell.get_char() + ' ')
            sys.stdout.write('\n')
