import pygame, sys
from pygame.locals import *

# Amount of margin to usei ( 1 = 100% )
windowMargin = 0.1
black = pygame.Color( 0,0,0 )
white = pygame.Color( 255, 255, 255 )
bgColor = white

def start( xResolution, yResolution ):
    pygame.init()
    fpsClock = pygame.time.Clock()

    # Set up the window
    window = pygame.display.set_mode( ( xResolution, yResolution ) )
    pygame.display.set_caption( 'Minesweeper Bot' )

    xMargin = int( windowMargin * float( xResolution ) )
    yMargin = int( windowMargin * float( yResolution ) )

    # Calculate where the field is going to be drawn
    fieldBoundBox = ( xMargin, yMargin, xResolution - 2*xMargin, yResolution - 2*yMargin )

    # Calculate where the lines need to be drawn
    lines = calculateCellLines( ( xResolution, yResolution ), fieldBoundBox, 5, 5 )
    
    # Main loop for pygame
    while True:
        window.fill( bgColor )

        pygame.draw.rect( window, black, fieldBoundBox, 3 )

        for l in lines:
            pygame.draw.line( window, black, l[ 0 ], l[ 1 ], 3 )

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick( 30 )

# Calculates where the cell lines need to be drawn
def calculateCellLines( resolution, boundBox, xCellCount, yCellCount ):
    cellLines = []

    xCellSize = int( boundBox[ 2 ] / xCellCount )
    yCellSize = int( boundBox[ 3 ] / yCellCount )

    top = boundBox[ 1 ]    
    bottom = top + boundBox[ 3 ]
    left = boundBox[ 0 ]
    right = left + boundBox[ 2 ]

    # Y lines go from the top of the bound box, to the bottom
    for yCell in range( 1, xCellCount ):
        xL = left + yCell * xCellSize
        cellLines.append( ( ( xL, top ), ( xL, bottom ) ) )

    for xCell in range( 1, yCellCount ):
        yL = top + xCell * yCellSize
        cellLines.append( ( ( left, yL ), ( right, yL ) ) )

    return cellLines
