from ..game.game import *
from ..bot.bot import MineBot
from abc import ABCMeta, abstractmethod


class CommonUI(object):

    WINDOW_MARGIN = 0.05
    CELL_GAP_FACTOR = 0.1
    # Factor of window to use as margin (on each side)
    DEFAULT_RESOLUTION = [800, 600]
    MINIMUM_RESOLUTION = 300
    # Factor of window to use as margin (on each side)
    BLACK_COLOR = [0, 0, 0]
    FLAGGED_COLOR = [0, 255, 0]
    CELL_COLOR = [255, 0, 0]
    MINE_COLOR = [255, 255, 0]
    BACKGROUND_COLOR = BLACK_COLOR

    def __init__(self):
        self.game = MineGame()
        self.x_cell_count = 0
        self.y_cell_count = 0

        # Initialise the bot with the current game
        self.bot = MineBot(self.game)

    def handle_unhide_cell(self, selected_cell):
        if selected_cell == -1:
            return

        # Get the underlying game engine to unhide the cell
        self.game.unhide_cell(selected_cell)

        state = self.game.get_grid_state()

    def handle_flag_cell(self, selected_cell):
        if selected_cell == -1:
            return

        self.game.toggle_flag_cell(selected_cell)

    @abstractmethod
    def draw_rect(self, context, rectangle, color):
        """
        Draw a filled rectangle in the underlying UI framework
        :param context: drawing context supplied by framework
        :param rectangle: list (of size 4) of rectangle base
                          co-ordinates and size
        :param color: list (of size 3) of RGB colors
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def draw_number(self, context, rectangle, color, number):
        """
        Draw some text in the underlying UI framework
        :param context: drawing context supplied by framework
        :param rectangle: list (of size 4) of rectangle base
                          co-ordinates and size
        :param color: list (of size 3) of RGB colors
        :param number: number to draw at supplied location
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_window_size(self):
        """
        Get the size of the window from the underlying UI framework
        :return: list (of size 2) of window width and height
        """
        raise NotImplementedError()

    def paint_game(self, context):
        # Grab the latest state of game
        grid_state = self.game.get_grid_state()

        cell_loc = [int(self.start_loc_x), int(self.start_loc_y)]
        rect = [cell_loc[0], cell_loc[1], self.square_size, self.square_size]

        for x in xrange(0, self.x_cell_count):
            for y in xrange(0, self.y_cell_count):
                # If the cell contains a zero, don't draw anything
                if grid_state[y][x] == '0':
                    self.draw_rect(context, rect, CommonUI.BACKGROUND_COLOR)
                # Draw flagged cells as clue
                elif grid_state[y][x] == 'F':
                    self.draw_rect(context, rect, CommonUI.FLAGGED_COLOR)
                # This is a mine :(
                elif grid_state[y][x] == 'X':
                    self.draw_rect(context, rect, CommonUI.MINE_COLOR)
                # The mine is still hidden, draw it as a square
                elif grid_state[y][x] == '-':
                    self.draw_rect(context, rect, CommonUI.CELL_COLOR)
                # It must be a number, draw it as such
                else:
                    self.draw_number(context, rect, CommonUI.CELL_COLOR,
                                     grid_state[y][x])

                # Move the rectangles start location in Y forward
                rect[1] += int((1 + CommonUI.CELL_GAP_FACTOR) *
                               self.square_size)
            # Reset y start location and increment x location
            rect[1] = cell_loc[1]
            rect[0] += int((1 + CommonUI.CELL_GAP_FACTOR) * self.square_size)

    def precalculate_drawing(self):
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
        windowsize = self.get_window_size()
        square_size_x = ((1 - CommonUI.WINDOW_MARGIN) * windowsize[0]) /\
                        (self.x_cell_count +
                            CommonUI.CELL_GAP_FACTOR * (self.x_cell_count - 1))
        square_size_y = ((1 - CommonUI.WINDOW_MARGIN) * windowsize[1]) /\
                        (self.y_cell_count +
                            CommonUI.CELL_GAP_FACTOR * (self.y_cell_count - 1))

        # The square cell size will be the smallest so that it
        # will fit in the screen
        if square_size_x <= square_size_y:
            square_size = int(square_size_x)
        else:
            square_size = int(square_size_y)

        self.square_size = square_size
        self.gap_size = CommonUI.CELL_GAP_FACTOR * square_size

        # Calculate the size of the field to be drawn with the new square sizes
        display_size_x = self.x_cell_count * square_size +\
            self.gap_size * (self.x_cell_count - 1)
        display_size_y = self.y_cell_count * square_size +\
            self.gap_size * (self.y_cell_count - 1)

        self.start_loc_x = (windowsize[0] - display_size_x) / 2
        self.start_loc_y = (windowsize[1] - display_size_y) / 2

        self.grid_left = self.start_loc_x
        self.grid_right = self.start_loc_x + display_size_x
        self.grid_top = self.start_loc_y
        self.grid_bottom = self.start_loc_y + display_size_y

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
            offset_location = (click_position[0] - self.grid_left +
                               (self.gap_size // 2),
                               click_position[1] - self.grid_top +
                               (self.gap_size // 2))

            grid_clicked = (int(offset_location[0] //
                            (self.square_size + self.gap_size)),
                            int(offset_location[1] //
                            (self.square_size + self.gap_size)))
        return grid_clicked
