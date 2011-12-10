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
        self.PerformMineCount()

    def PerformMineCount(self):
        for x in xrange(len(self.mineGrid)):
            for y in xrange(len(self.mineGrid[0])):
                self.CountAdjacentMines(x,y)

    def CountAdjacentMines(self, mineX, mineY):
        cell = self.mineGrid[mineX][mineY]
        # Maybe I need to make the mine grid something smarter???
        size = ( len(self.mineGrid), len(self.mineGrid[0]) )
        for xAdj in xrange(mineX-1, mineX+2):
            # Do bounds check for X
            if (xAdj < 0) | (xAdj > size[0] - 1):
                continue
            for yAdj in xrange(mineY-1, mineY+2):
                # Do bounds check for Y
                if (yAdj < 0) | (yAdj > size[1] - 1):
                    continue
                testCell = self.mineGrid[xAdj][yAdj]
                if testCell.hasMine == True:
                    cell.surroundingMines += 1 

    def DisplayGrid(self):
        for line in self.mineGrid:
            for cell in line:
                sys.stdout.write(cell.GetChar() + ' ')
            sys.stdout.write('\n')
