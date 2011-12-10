import random
import copy


def generateList(sizeX, sizeY):
    """
    Generate a list of all cells in a grid of sizeX by sizeY
    """
    cellList = []
    for x in range(0, sizeX):
        for y in range(0, sizeY):
            cellList.append([x, y])
    return cellList


def printCellList(cellList):
    """
    Prints a list of cells

    For debugging, print a list of all cells in the provided list
    """
    for cell in cellList:
        print cell


def getRandomMines(cellList, numberOfMines):
    """
    Will generate random mine locations from the provided list of cells
    """
    # TODO - JY to consider `random.shuffle` and list slicing
    mineLocations = []
    cellListCopy = copy.deepcopy(cellList)
    for mineNum in xrange(min(numberOfMines, len(cellList))):
        randIndex = random.randint(0, len(cellListCopy) - 1)
        mineLocations.append(cellListCopy.pop(randIndex))
    return mineLocations


def placeMines(mineGrid, numberOfMines):
    """
    Place random mines inside the mine grid provided
    """
    xSize = len(mineGrid)
    ySize = len(mineGrid[0]) # No better way to do this without better grid structure

    cellList = generateList(xSize, ySize)
    mineList = getRandomMines(cellList, numberOfMines)

    for mine in mineList:
        cell = mineGrid[mine[0]][mine[1]]
        cell.hasMine = True


