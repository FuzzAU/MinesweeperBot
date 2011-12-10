from MineBot import *


def test():
    myList = MinePlacer.generateList(5, 5)
    MinePlacer.printCellList(myList)
    mines = MinePlacer.placeMines(myList, 10)
    print 'Mines:'
    MinePlacer.printCellList(mines)
