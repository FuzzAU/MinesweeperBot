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
def placeMines( cellList, numberOfMines ):
    mineLocations = []
    cellListCopy = cellList
    
    for mineNum in range( 0, numberOfMines ):
        randIndex = random.randint( 0, len( cellListCopy ) - 1 )
        mineLocations.append( cellListCopy.pop( randIndex ) )
    
    return mineLocations
