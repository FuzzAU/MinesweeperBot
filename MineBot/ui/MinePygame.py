import sys
from ..game import *
from ..game.MineGame import MineGame

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


class MinePygame(object):
    def __init__(self, x_resolution, y_resolution,
                 x_cell_count, y_cell_count, mine_count):

        # Initiate a MineGame
        self.game = MineGame()
        self.game.init_game(x_cell_count, y_cell_count, mine_count)

        # Store resolution, cell count and mine count
        self.x_resolution = x_resolution
        self.y_resolution = y_resolution
        self.x_cell_count = x_cell_count
        self.y_cell_count = y_cell_count
        self.mine_count = mine_count

        # Create a blank pygame canvas
        self.window = pygame.display.set_mode((x_resolution, y_resolution))

        # Calculate the margin widths
        self.x_margin = int(WINDOW_MARGIN * float(x_resolution))
        self.y_margin = int(WINDOW_MARGIN * float(y_resolution))

        # Calculate where the field is going to be drawn
        self.x_clip = self.x_resolution - (2 * self.x_margin)
        self.y_clip = self.y_resolution - (2 * self.y_margin)
        self.field_bound_box = (self.x_margin, self.y_margin,
                                self.x_clip, self.y_clip)

        # Calculate the size of the cells in X & Y dimensions
        # To make them square, the X dimension will match the Y-dimension
        self.y_cell_size = int(self.field_bound_box[3] / self.y_cell_count)
        self.x_cell_size = int(self.field_bound_box[2] / self.x_cell_count)

        self.grid_top = self.field_bound_box[1]
        self.grid_bottom = self.grid_top + self.field_bound_box[3]
        self.grid_left = self.field_bound_box[0]
        self.grid_right = self.grid_left + self.field_bound_box[2]

    def start(self):
        pygame.init()
        fpsClock = pygame.time.Clock()

        # Set up the window
        pygame.display.set_caption('Minesweeper Bot')

        # Calculate where the lines need to be drawn
        lines = self.calculate_cell_lines()

        # Main loop for pygame
        while True:
            self.window.fill(BACKGROUND_COLOR)

            pygame.draw.rect(self.window, BLACK_COLOUR,
                             self.field_bound_box, 3)

            for l in lines:
                pygame.draw.line(self.window, BLACK_COLOUR, l[0], l[1], 3)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    selected_cell = self.determine_cell_clicked(event.pos)
                    print 'Clicked cell: ' + str(selected_cell)

            pygame.display.update()
            fpsClock.tick(30)

    def calculate_cell_lines(self):
        """
        Calculates where the cell lines need to be drawn
        """

        cell_lines = []

        # Y lines go from the top of the bound box, to the bottom
        for y_cell in range(1, self.x_cell_count):
            xL = self.grid_left + y_cell * self.x_cell_size
            cell_lines.append(((xL, self.grid_top), (xL, self.grid_bottom)))

        for x_cell in range(1, self.y_cell_count):
            yL = self.grid_top + x_cell * self.y_cell_size
            cell_lines.append(((self.grid_left, yL), (self.grid_right, yL)))

        return cell_lines

    def determine_cell_clicked(self, click_position):
        # Make sure the click was inside the grid
        if (click_position[0] < self.grid_left)\
            | (click_position[0] > self.grid_right):
            grid_clicked = -1
        elif (click_position[1] < self.grid_top) |\
            (click_position[1] > self.grid_bottom):
            grid_clicked = -1
        else:
            # Offset the clicked position back to the origin and divide
            # divide the cell sizes to find which grid was clicked
            offset_location = (click_position[0] - self.grid_left,
                             click_position[1] - self.grid_top)
            grid_clicked = (offset_location[0] // self.x_cell_size,
                            offset_location[1] // self.y_cell_size)

        return grid_clicked
