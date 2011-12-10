import random

# Generate a list of all cells in a grid of sizeX by sizeY
def generateList( sizeX, sizeY ):
    cellList = []
    for x in range( 0, sizeX ):
        for y in range( 0, sizeY ):
            cellList.append( [ x,y ] )
    return cellList
    
# For debugging, print a list of all cells in the provided list
def printCellList( cellList ):
    for cell in cellList:
        print cell
    
# Will generate random mine locations from the provided list of cells
def getRandomMines( cellList, numberOfMines ):
    mineLocations = []
    cellListCopy = cellList
    
    for mineNum in range( 0, numberOfMines ):
        randIndex = random.randint( 0, len( cellListCopy ) - 1 )
        mineLocations.append( cellListCopy.pop( randIndex ) )
    
    return mineLocations

# Place random mines inside the mine grid provided
def placeMines( mineGrid, numberOfMines ):
    xSize = len( mineGrid )
    ySize = len( mineGrid[0] ) # Andrew: is there a better way of doing this?

    cellList = generateList( xSize, ySize )
    mineList = getRandomMines( cellList, numberOfMines )

    for mine in mineList:
        cell = mineGrid[ mine[0] ][ mine[1] ]
        cell.hasMine = True
