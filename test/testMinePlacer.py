import unittest
from MineBot import *


class MinePlacementTests(unittest.TestCase):

    def test_grid(self):
        cells = MinePlacer.generate_list(5, 5)
        # Make sure we get the right number back
        self.assertEquals(len(cells), 25)
        # Choose a couple of random samples, and make sure they are right
        self.assertEquals(cells[0], (0, 0))
        self.assertEquals(cells[-1], (4, 4))

    def test_no_random_mines(self):
        cells = MinePlacer.generate_list(5, 5)
        mines = MinePlacer.get_random_mines(cells, 0)
        self.assertEquals(len(mines), 0)

    def test_too_many_random_mines(self):
        cells = MinePlacer.generate_list(5, 5)
        mines = MinePlacer.get_random_mines(cells, 50)
        self.assertEquals(len(mines), 25)

    def test_mine_cells_unique(self):
        # This test is stochastic, but the probability of failing
        # is exceptionally low, provided that the code works as
        # designed

        cells = MinePlacer.generate_list(5, 5)
        mines = MinePlacer.get_random_mines(cells, 25)
        # sanity test
        self.assertEquals(len(mines), 25)

        # NB. a mine is a list ATM, list are not hashable
        #     so we transform them into tuples which can
        #     be hashed
        mines = [tuple(mine) for mine in mines]
        mines = set(mines)
        self.assertEquals(len(mines), 25)
