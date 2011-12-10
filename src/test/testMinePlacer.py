import unittest
from MineBot import *


class MinePlacementTests( object ):

    def testPlacement(self):
        cells = MinePlacer.generateList(5, 5)
        # Make sure we get the right number back
        self.assertEquals(len(cells), 25)
        # Choose a couple of random samples, and make sure they are right
        self.assertEquals(cells[0], [0, 0])
        self.assertEquals(cells[-1], [4, 4])

#def test():
#    myList = MinePlacer.generateList(5, 5)
#    MinePlacer.printCellList(myList)
#    mines = MinePlacer.placeMines(myList, 10)
#    print 'Mines:'
#    MinePlacer.printCellList(mines)
