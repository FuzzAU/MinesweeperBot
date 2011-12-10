
class CellInfo(object):
    def __init__( self ):
        self.hasMine = False
        self.surroundingMines = 0

    def GetChar( self ):
        """
        Get an ASCII character representation of this cell
        """
        cellChar = '0'
        if self.hasMine == True:
            cellChar = 'X'
        else:
            cellChar = str( self.surroundingMines )
        return cellChar
