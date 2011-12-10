import unittest
from MineBot import *


class MineGameTests(unittest.TestCase):

    def testCellInfoUniqueness(self):
        # This is a regression test
        g = game.MineGame.MineGame()
        g.InitGame(5, 5, 8)
        self.assertEquals(len(g.Cells()), 25)
        self.assertEquals(len(set(g.Cells())), 25)
