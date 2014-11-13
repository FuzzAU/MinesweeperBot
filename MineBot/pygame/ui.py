from ..game.game import *
from ..bot.bot import MineBot
from ..ui.common import CommonUI

try:
    import pygame
    from pygame.locals import *
except:
    print 'Pygame not installed'
    sys.exit(1)


class MinePygame(CommonUI):
    def __init__(self, x_resolution, y_resolution,
                 x_cell_count, y_cell_count, mine_count):

        # Initiate a MineGame
        self.game = MineGame()
        self.game.init_game(x_cell_count, y_cell_count, mine_count)

        # Initiate an auto-playing MineBot
        self.bot = MineBot(self.game)

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

        # Precalculate elements and locations of objects to be drawn
        self.precalculate_drawing()

        # Using the square size as the font, render numbers on surface
        # for blitting when needed
        font_surfaces = []
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        drawing_font = pygame.font.Font(default_font, self.square_size)

        num_colors = [pygame.Color(255, 122, 122),
                      pygame.Color(128, 255, 0),
                      pygame.Color(0, 0, 255),
                      pygame.Color(255, 255, 0),
                      pygame.Color(255, 128, 0),
                      pygame.Color(128, 0, 255),
                      pygame.Color(255, 0, 128),
                      pygame.Color(255, 61, 61)
                      ]

        font_surfaces.append(0)
        for i in xrange(1, 9):
            font_surfaces.append(drawing_font.render(str(i),
                                 True,
                                 num_colors[i-1],
                                 MinePygame.to_pygcolor(CommonUI.BLACK_COLOR)))

        self.font_surfaces = font_surfaces

        # Work out drawing offset from corner of box to draw a font surface
        # Assuming (As they seem to be) that all numbers in the font
        # are drawn on the same size surface
        num_surf_size = font_surfaces[1].get_size()
        self.num_draw_offset = ((self.square_size - num_surf_size[0]) // 2,
                                (self.square_size - num_surf_size[1]) // 2)

    @staticmethod
    def to_pygcolor(color):
        return pygame.Color(color[0], color[1], color[2])

    def start(self):
        pygame.init()
        fpsClock = pygame.time.Clock()

        # Set up the window
        pygame.display.set_caption('Minesweeper Bot')

        # Main loop for pygame
        while True:
            # Grab the latest state of game
            grid_state = self.game.get_grid_state()
            game_state = self.game.get_game_state()

            self.window.fill(MinePygame.to_pygcolor(CommonUI.BACKGROUND_COLOR))

            # Draw the cells to a surface, and blit it on to the window
            self.paint_game(self.surface)
            self.window.blit(self.surface, (0, 0))

            # Handle events
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

                    if self.game.get_game_state() == GameState.LOST:
                        print 'You lost'
                    if self.game.get_game_state() == GameState.WON:
                        print 'You won'
                elif event.type == KEYDOWN:
                    if event.key == K_a:
                        f = self.bot.auto_flag()
                        print 'Auto-flagged ' + str(f) + ' mines'
                    elif event.key == K_c:
                        c = self.bot.auto_clear()
                        print 'Auto-cleared ' + str(c) + ' cells'
                    elif event.key == K_s:
                        self.bot.auto_step()

            pygame.display.update()
            fpsClock.tick(30)

    def draw_rect(self, context, rectangle, color):
        context.fill(MinePygame.to_pygcolor(color), rectangle)

    def draw_number(self, context, rectangle, color, number):
        # Fill background surface with black first
        context.fill(MinePygame.to_pygcolor(CommonUI.BLACK_COLOR), rectangle)
        context.blit(self.font_surfaces[int(number)],
                     (rectangle[0] + self.num_draw_offset[0],
                     rectangle[1] + self.num_draw_offset[1]))

    def get_window_size(self):
        width, height = self.window.get_size()
        return [width, height]