import sys

try:
    import pygame
    from pygame.locals import *
except:
    print 'Pygame not installed'

# Amount of margin to usei (1 = 100%)
WINDOW_MARGIN = 0.1
BLACK_COLOUR = pygame.Color(0, 0, 0)
WHITE_COLOR = pygame.Color(255, 255, 255)
BACKGROUND_COLOR = WHITE_COLOR

def start(x_resolution, y_resolution):
    pygame.init()
    fpsClock = pygame.time.Clock()

    # Set up the window
    window = pygame.display.set_mode((x_resolution, y_resolution))
    pygame.display.set_caption('Minesweeper Bot')

    x_margin = int(WINDOW_MARGIN * float(x_resolution))
    y_margin = int(WINDOW_MARGIN * float(y_resolution))

    # Calculate where the field is going to be drawn
    xClip = x_resolution - (2 * x_margin)
    yClip = y_resolution - (2 * y_margin)
    field_bound_box = (x_margin, y_margin, xClip, yClip)

    # Calculate where the lines need to be drawn
    lines = calculate_cell_lines((x_resolution, y_resolution), field_bound_box, 5, 5)

    # Main loop for pygame
    while True:
        window.fill(BACKGROUND_COLOR)

        pygame.draw.rect(window, BLACK_COLOUR, field_bound_box, 3)

        for l in lines:
            pygame.draw.line(window, BLACK_COLOUR, l[0], l[1], 3)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #elif event.type == MOUSEBUTTONUP:
            #    selected_cell = determine_cell_clicked( event.pos )
            #    print 'Clicked cell: ' + str(selected_cell)

        pygame.display.update()
        fpsClock.tick(30)


def calculate_cell_lines(resolution, bound_box, x_cell_count, y_cell_count):
    """
    Calculates where the cell lines need to be drawn
    """

    cell_lines = []

    x_cell_size = int(bound_box[2] / x_cell_count)
    y_cell_size = int(bound_box[3] / y_cell_count)

    top = bound_box[1]
    bottom = top + bound_box[3]
    left = bound_box[0]
    right = left + bound_box[2]

    # Y lines go from the top of the bound box, to the bottom
    for yCell in range(1, x_cell_count):
        xL = left + yCell * x_cell_size
        cell_lines.append(((xL, top), (xL, bottom)))

    for xCell in range(1, y_cell_count):
        yL = top + xCell * y_cell_size
        cell_lines.append(((left, yL), (right, yL)))

    return cell_lines
