from PySide.QtCore import *
from PySide.QtGui import *

from ..game.game import *
from ..bot.bot import MineBot
from ..ui.common import CommonUI


class GameWindow(QWidget, CommonUI):
    # Create a signal to allow notification when the window is closing
    closing = Signal()

    def __init__(self):
        # Must initialise like this to allow signal/slots to work
        # As per: http://qt-project.org/wiki/Signals_and_Slots_in_PySide
        super(GameWindow, self).__init__()

        # Set up window
        self.setWindowTitle('Minesweeper')
        # Set resolution to default size
        self.resize(CommonUI.DEFAULT_RESOLUTION[0], CommonUI.DEFAULT_RESOLUTION[1])
        # Set window minimum sizes
        self.setMinimumWidth(CommonUI.MINIMUM_RESOLUTION)
        self.setMinimumHeight(CommonUI.MINIMUM_RESOLUTION)

        # ## Set up pens for drawing ###
        # Create drawing pen with no width to allow filling without border
        self.rect_pen = QPen(GameWindow.toQColor(CommonUI.BACKGROUND_COLOR), 0, Qt.SolidLine)
        self.text_pen = QPen(GameWindow.toQColor(CommonUI.CELL_COLOR), 0, Qt.SolidLine)

        # Move window to centre of screen (doesn't work well on multi-monitor)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def startGame(self, grid_size, mine_count):
        """ Start a new game

        Create a new game with the provided grid size and number of mines
        """

        # Initialise a new game
        self.game = MineGame()
        self.game.init_game(grid_size[0], grid_size[1], mine_count)
        # Store grid size requested by user
        self.x_cell_count = grid_size[0]
        self.y_cell_count = grid_size[1]

        # Initialise the bot with the current game
        self.bot = MineBot(self.game)

    def paintEvent(self, event):
        p = QPainter()

        p.begin(self)

        # Draw black background
        p.setBrush(GameWindow.toQColor(CommonUI.BACKGROUND_COLOR))
        p.drawRect(0, 0, self.size().width(), self.size().height())

        # Paint the game grid
        self.precalculateDrawing()
        self.paintGame(p)

        # Clean up painter
        p.end()
        del p

    @staticmethod
    def toQColor(color):
        """
        Create a Qt QColor object from a list of RGB components
        :param color: list (of size 3) of RGB components
        :return: QColor object representing supplied colour
        """
        return QColor(color[0], color[1], color[2])

    @staticmethod
    def toQRect(rect):
        """
        Create a Qt QRect object from rectangle information
        :param rect: list of rectangle start co-ordinates and size
        :return: QRect object representing supplied rectangle
        """
        return QRect(rect[0], rect[1], rect[2], rect[3])

    def drawRect(self, context, rectangle, color):
        context.setPen(self.rect_pen)
        context.setBrush(GameWindow.toQColor(color))
        context.drawRect(GameWindow.toQRect(rectangle))

    def drawNumber(self, context, rectangle, color, number):
        context.setPen(self.text_pen)
        context.setBrush(GameWindow.toQColor(color))
        context.drawText(GameWindow.toQRect(rectangle), Qt.AlignCenter, number)

    def getWindowSize(self):
        return [self.size().width(), self.size().height()]

    def mousePressEvent(self, event):
        event.accept()
        # Calculate which cell has been selected
        selected_cell = self.determine_cell_clicked([int(event.x()), int(event.y())])

        # If this is a left click, we want to unhide the mine
        if event.button() == Qt.LeftButton:
            self.handle_unhide_cell(selected_cell)
        # For right clicks we want to flag the mine, or unflag it
        elif event.button() == Qt.RightButton:
            self.handle_flag_cell(selected_cell)

        self.update()

        # Check if player has lost of won the game
        game_state = self.game.get_game_state()
        if game_state == GameState.WON:
            QMessageBox.information(self, "Winner", "Congratulations, you won :-)")
            self.hide()
            self.closing.emit()
        elif game_state == GameState.LOST:
            QMessageBox.information(self, "Boo", "Too bad, you lost :-(")
            self.hide()
            self.closing.emit()

    def closeEvent(self, event):
        """ Close the game window and go back to dialog to show size """
        self.closing.emit()

