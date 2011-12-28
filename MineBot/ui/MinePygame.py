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
CELL_COLOR = pygame.Color(255,0,0)
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
        square_size_x = ( (1 - WINDOW_MARGIN) * self.x_resolution) / (self.x_cell_count + CELL_GAP_FACTOR*(self.x_cell_count - 1))
        square_size_y = ( (1 - WINDOW_MARGIN) * self.y_resolution) / (self.y_cell_count + CELL_GAP_FACTOR*(self.y_cell_count - 1))

        print 'square_size_x: ' + str(square_size_x)
        print 'square_size_y: ' + str(square_size_y)

        # The square cell size will be the smallest so that it will fit in the screen
        if square_size_x <= square_size_y:
            square_size = square_size_x
        else:
            square_size = square_size_y
        self.square_size = square_size

        # Calculate the size of the field to be drawn with the new square sizes
        display_size_x = self.x_cell_count * square_size + 0.1 * square_size * (self.x_cell_count - 1)
        display_size_y = self.y_cell_count * square_size + 0.1 * square_size * (self.y_cell_count - 1)

        self.start_loc_x = (self.x_resolution - display_size_x) / 2
        self.start_loc_y = (self.y_resolution - display_size_y) / 2

    def start(self):
        pygame.init()
        fpsClock = pygame.time.Clock()

        # Set up the window
        pygame.display.set_caption('Minesweeper Bot')

        # Main loop for pygame
        while True:
            self.window.fill(BACKGROUND_COLOR)

            self.draw_cells()
            self.window.blit(self.surface, (0,0))
            pygame.display.flip()

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

    def draw_cells(self):
        cell_loc = [self.start_loc_x, self.start_loc_y]
        rect = [cell_loc[0], cell_loc[1], self.square_size, self.square_size]
        
        for x in xrange(0, self.x_cell_count):
            for y in xrange(0, self.y_cell_count):
                self.surface.fill(CELL_COLOR, rect)
                rect[1] += (1 + CELL_GAP_FACTOR) * self.square_size
            
            rect[1] = cell_loc[1]
            rect[0] += (1 + CELL_GAP_FACTOR) * self.square_size

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
            offset_location = (click_position[0] - self.grid_left,
                             click_position[1] - self.grid_top)
            grid_clicked = (offset_location[0] // self.x_cell_size,
                            offset_location[1] // self.y_cell_size)

        return grid_clicked
