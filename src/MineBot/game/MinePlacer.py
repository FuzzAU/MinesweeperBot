import random

def generateList( sizeX, sizeY ):
    """
    Generate a list of all cells in a grid of sizeX by sizeY
    """
    cellList = []
    for x in range( 0, sizeX ):
        for y in range( 0, sizeY ):
            cellList.append( [ x,y ] )
    return cellList
    

def printCellList( cellList ):
    """
    Prints a list of cells

    For debugging, print a list of all cells in the provided list
    """
    for cell in cellList:
        print cell

def getRandomMines( cellList, numberOfMines ):
    """
    Will generate random mine locations from the provided list of cells
    """
    mineLocations = []
    cellListCopy = cellList
    
    for mineNum in range( 0, numberOfMines ):
        randIndex = random.randint( 0, len( cellListCopy ) - 1 )
        mineLocations.append( cellListCopy.pop( randIndex ) )
    
    return mineLocations

def placeMines( mineGrid, numberOfMines ):
    """
    Place random mines inside the mine grid provided
    """
    xSize = len( mineGrid )
    ySize = len( mineGrid[0] ) # Andrew: is there a better way of doing this?

    cellList = generateList( xSize, ySize )
    mineList = getRandomMines( cellList, numberOfMines )

    for mine in mineList:
        cell = mineGrid[ mine[0] ][ mine[1] ]
        cell.hasMine = True
