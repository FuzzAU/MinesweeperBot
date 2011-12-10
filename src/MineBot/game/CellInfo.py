
class CellInfo(object):
  hasMine = False
  surroundingMines = 0

  def __init__( self ):
    self.hasMine = False
    self.surroundingMines = 0

  # Get an ASCII character representation of this cell
  def GetChar( self ):
    cellChar = '0'
    if self.hasMine == True:
        cellChar = 'X'
    else:
        cellChar = str( self.surroundingMines )
    return cellChar
