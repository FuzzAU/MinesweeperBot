from .CellInfo import CellInfo
import MinePlacer
import sys


class MineGame(object):

    def __init__(self):
        self.mineGrid = []

    def Cells(self):
        """
        Return a flattened list of cells
        """
        res = []
        for row in self.mineGrid:
            for item in row:
                res.append(item)
        return res

    def InitGame(self, xSize, ySize, numberOfMines):
        # TODO - JY to remove following line after experimenting with
        #        MineGameTests.testCellInfoUniqueness
        #self.mineGrid = [[CellInfo()] * ySize for x in xrange(xSize)]
        for j in xrange(ySize):
            row = []
            for i in xrange(xSize):
                row.append(CellInfo())
            self.mineGrid.append(row)

        MinePlacer.placeMines(self.mineGrid, numberOfMines)

    def DisplayGrid(self):
        for line in self.mineGrid:
            for cell in line:
                sys.stdout.write(cell.GetChar() + ' ')
            sys.stdout.write('\n')
