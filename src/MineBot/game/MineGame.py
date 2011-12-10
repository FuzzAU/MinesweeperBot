import CellInfo 
import MinePlacer
import sys

class MineGame(object):

    mineGrid = []

    def InitGame( self, xSize, ySize, numberOfMines ):
        # Andrew: How do i make it so i dont have to type CellInfo.CellInfo
        # I want to import all of the module's contents
        self.mineGrid = [ [ CellInfo.CellInfo() ] * ySize for x in xrange( xSize ) ]

        MinePlacer.placeMines( self.mineGrid, numberOfMines )

    def DisplayGrid( self ):
        for line in self.mineGrid:
            for cell in line:
                sys.stdout.write( cell.GetChar() + ' ' )
            sys.stdout.write('\n')
