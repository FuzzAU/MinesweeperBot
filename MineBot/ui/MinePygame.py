import sys
from ..game import *
from ..game.MineGame import MineGame
from ..game.MineGame import *

try:
    import pygame
    from pygame.locals import *
except:
    print 'Pygame not installed'

# Factor of window to use as margin (on each side)
WINDOW_MARGIN = 0.05
CELL_GAP_FACTOR = 0.1
BLACK_COLOR = pygame.Color(0, 0, 0)
WHITE_COLOR = pygame.Color(255, 255, 255)
BLUE_COLOR = pygame.Color(0, 255, 0)
CELL_COLOR = pygame.Color(255, 0, 0)
BACKGROUND_COLOR = BLACK_COLOR


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
        self.surface = pygame.Surface(self.window.get_size())
        self.surface.convert()

        # We want the screen to be divided up as follows
        #  n x squares
        #  n-1 x gaps between squares (of 10% square width)
        #  5% of screen width to be used as margin
        #
        #  Let:
        #    n be mine count in a certain dimension
        #    cs be cell size
        #    res be the screen resolution in a certain dimension
        #
        #  Therefore
        #  res = n.cs + (n-1).0.1.cs + 0.05.res
        #
        # We want all cells to be squares, so lets find the dimension
        # that allows us to fit everything in using squares
        # depending on the resolution and cell size in each dimension
        square_size_x = ((1 - WINDOW_MARGIN) * self.x_resolution) /\
                        (self.x_cell_count +
                        CELL_GAP_FACTOR * (self.x_cell_count - 1))
        square_size_y = ((1 - WINDOW_MARGIN) * self.y_resolution) /\
                        (self.y_cell_count +
                        CELL_GAP_FACTOR * (self.y_cell_count - 1))

        # The square cell size will be the smallest so that it
        # will fit in the screen
        if square_size_x <= square_size_y:
            square_size = int(square_size_x)
        else:
            square_size = int(square_size_y)
        self.square_size = square_size
        self.gap_size = CELL_GAP_FACTOR * square_size

        # Calculate the size of the field to be drawn with the new square sizes
        display_size_x = self.x_cell_count * square_size +\
                         self.gap_size * (self.x_cell_count - 1)
        display_size_y = self.y_cell_count * square_size +\
                         self.gap_size * (self.y_cell_count - 1)

        self.start_loc_x = (self.x_resolution - display_size_x) / 2
        self.start_loc_y = (self.y_resolution - display_size_y) / 2

        self.grid_left = self.start_loc_x
        self.grid_right = self.start_loc_x + display_size_x
        self.grid_top = self.start_loc_y
        self.grid_bottom = self.start_loc_y + display_size_y

        # Using the square size as the font, render numbers on surface
        # for blitting when needed
        font_surfaces = []
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        drawing_font = pygame.font.Font(default_font, square_size)
        font_surfaces.append(0)
        for i in xrange(1, 9):
            font_surfaces.append(drawing_font.render(str(i), True,\
                                                     CELL_COLOR, BLACK_COLOR))

        self.font_surfaces = font_surfaces

        # Work out drawing offset from corner of box to draw a font surface
        # Assuming (As they seem to be) that all numbers in the font
        # are drawn on the same size surface
        num_surf_size = font_surfaces[1].get_size()
        self.num_draw_offset = ((square_size - num_surf_size[0]) // 2,\
                               (square_size - num_surf_size[1]) // 2)

    def start(self):
        pygame.init()
        fpsClock = pygame.time.Clock()

        # Set up the window
        pygame.display.set_caption('Minesweeper Bot')

        # Main loop for pygame
        while True:
            grid_state = self.game.get_grid_state()

            self.window.fill(BACKGROUND_COLOR)

            self.draw_cells(grid_state)
            self.window.blit(self.surface, (0, 0))
#            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    selected_cell = self.determine_cell_clicked(event.pos)
                    # If this is a left click, we want to unhide the mine
                    if event.button == 1:
                        self.handle_unhide_cell(selected_cell)
                    # For right clicks we want to flag the mine, or unflag it
                    elif event.button == 3:
                        self.handle_flag_cell(selected_cell)

                    self.game.display_grid_state()

                    if(self.game.get_game_state() == GameState.LOST):
                        print 'You lost'

            pygame.display.update()
            fpsClock.tick(30)

    def draw_cells(self, grid_status):
        cell_loc = [int(self.start_loc_x), int(self.start_loc_y)]
        rect = [cell_loc[0], cell_loc[1], self.square_size, self.square_size]

        draw_color = CELL_COLOR
        surface = self.surface

        for x in xrange(0, self.x_cell_count):
            for y in xrange(0, self.y_cell_count):
                # If the cell contains a zero, dont draw anything
                if grid_status[y][x] == '0':
                    draw_color = BLACK_COLOR
                    # Perform the surface drawing
                    surface.fill(draw_color, rect)
                # Draw flagged cells as clue
                elif grid_status[y][x] == 'F':
                    draw_color = BLUE_COLOR
                     # Perform the surface drawing
                    surface.fill(draw_color, rect)
                elif grid_status[y][x] == 'X':
                    draw_color = pygame.Color(255, 255, 0)
                    surface.fill(draw_color, rect)
                # The mine is still hidden, draw it as a square
                elif grid_status[y][x] == '-':
                    draw_color = CELL_COLOR
                    # Perform the surface drawing
                    surface.fill(draw_color, rect)
                # It must be a number, draw it as such
                else:
                    draw_color = BLACK_COLOR
                    surface.fill(draw_color, rect)
                    surface.blit(self.font_surfaces[int(grid_status[y][x])],\
                                 (rect[0] + self.num_draw_offset[0],\
                                 rect[1] + self.num_draw_offset[1]))

                # Move the rectanges start location in Y forward
                rect[1] += int((1 + CELL_GAP_FACTOR) * self.square_size)
            # Reset y start location and increment x location
            rect[1] = cell_loc[1]
            rect[0] += int((1 + CELL_GAP_FACTOR) * self.square_size)

    def handle_unhide_cell(self, selected_cell):
        if selected_cell == -1:
            return
        # Get the underlying game engine to unhide the cell
        self.game.unhide_cell(selected_cell)

        state = self.game.get_grid_state()

#        if game.get_game_state

    def handle_flag_cell(self, selected_cell):
        if selected_cell == -1:
            return

        self.game.toggle_flag_cell(selected_cell)

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
            offset_location = (click_position[0] - self.grid_left +\
                              (self.gap_size // 2),
                              click_position[1] - self.grid_top +\
                              (self.gap_size // 2))

            grid_clicked = (int(offset_location[0] // \
                           (self.square_size + self.gap_size)),
                            int(offset_location[1] // \
                            (self.square_size + self.gap_size)))
            print grid_clicked
        return grid_clicked
