from .CellInfo import CellInfo
import MinePlacer
import sys

class MineGame(object):

    mineGrid = []

    def InitGame( self, xSize, ySize, numberOfMines ):
        self.mineGrid = [ [ CellInfo() ] * ySize for x in xrange( xSize ) ]

        MinePlacer.placeMines( self.mineGrid, numberOfMines )

    def DisplayGrid( self ):
        for line in self.mineGrid:
            for cell in line:
                sys.stdout.write( cell.GetChar() + ' ' )
            sys.stdout.write('\n')
