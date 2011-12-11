import unittest
from MineBot import *


class MineGameTests(unittest.TestCase):

    def test_cell_info_uniqueness(self):
        # This is a regression test
        g = game.MineGame.MineGame()
        g.init_game(5, 5, 8)
        self.assertEquals(len(g.cells()), 25)
        self.assertEquals(len(set(g.cells())), 25)

    def test_mine_placement(self):
        # Create a game with 10 mines in it
        game = MineGame.MineGame()
        game.init_game(5, 5, 10)
   
        # Make sure we actually gave 10 mines in there
        mines = sum( cell.has_mine == True for cell in game.cells())
        
        self.assertEquals(mines, 10)
 
