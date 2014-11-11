from PySide.QtCore import *
from PySide.QtGui import *

from game import GameWindow

# Minimum size of a board is 3 squares
BOARD_MINIMUM = 3
# Minimum size of a board is 50 squares
BOARD_MAXIMUM = 50
# Start by suggesting a board size of 10 to the user
BOARD_START_VALUE = 10
# Number of mines will default to this factor multiplied by the number
# of square on the board
MINE_COUNT_FACTOR = 0.15


class SizeDialog(QWidget):
    """ Dialog to ask user what size game they wish to play """

    def __init__(self, exit_handler):
        """ Initialise window and build form components """

        QWidget.__init__(self)

        # Create game interface
        self.game = GameWindow()
        # Store reference to handler that will allow us to request an exit
        self.exit_handler = exit_handler

        # Set up window
        self.setWindowTitle('Minesweeper')
        self.setMinimumWidth(300)

        # Use a vertical box layout for the dialog
        self.layout = QVBoxLayout()

        # Insert label explaining function of form
        self.select_label = QLabel('Select size of Minesweeper board')
        self.select_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.select_label)

        # User form layout for spin boxes as it provides ability to add label
        self.form_layout = QFormLayout()

        # Create spin boxes to represent the size of the minesweeper board
        # that the user wants
        self.x_size = QSpinBox()
        self.x_size.setRange(BOARD_MINIMUM, BOARD_MAXIMUM)
        self.x_size.setSingleStep(1)
        self.x_size.setValue(BOARD_START_VALUE)
        self.form_layout.addRow('Width:', self.x_size)

        self.y_size = QSpinBox()
        self.y_size.setRange(BOARD_MINIMUM, BOARD_MAXIMUM)
        self.y_size.setSingleStep(1)
        self.y_size.setValue(BOARD_START_VALUE)
        self.form_layout.addRow('Height:', self.y_size)

        # Create a box so that the user can specify the number of
        # mines on the board
        self.mine_count = QSpinBox()
        self.update_mine_count()
        self.form_layout.addRow('Mines:', self.mine_count)

        # When user changes the size of the board we need to update
        # the mine count
        self.x_size.valueChanged.connect(self.on_size_changed)
        self.y_size.valueChanged.connect(self.on_size_changed)

        # Add the form layout to base layout
        self.layout.addLayout(self.form_layout)

        self.button_box = QHBoxLayout()
        # Button to start new game
        self.start_button = QPushButton('Start Game', self)
        self.start_button.clicked.connect(self.on_start)
        # Button to exit application
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.on_exit)
        # Add buttons to button layout
        self.button_box.addWidget(self.start_button)
        self.button_box.addWidget(self.exit_button)

        self.layout.addLayout(self.button_box)
        # Set window layout to the vertical layout
        self.setLayout(self.layout)

    def update_mine_count(self):
        """ Update the number of mines in the game based on the number of
            squares on the board
        """
        board_squares = self.x_size.value() * self.y_size.value()
        num_mines = int(board_squares * MINE_COUNT_FACTOR)
        # Maximum number of mines is the number of squares on the board
        # Minimum is 1 mine, so there is an actual game
        self.mine_count.setRange(1, board_squares)
        self.mine_count.setSingleStep(1)
        # Set the value of the mines count spin box to the suggested value
        self.mine_count.setValue(num_mines)

    @Slot()
    def on_size_changed(self):
        self.update_mine_count()

    @Slot()
    def on_start(self):
        """ Start a minesweeper game with the parameters given in this form """
        self.game.show()
        self.hide()

    @Slot()
    def on_exit(self):
        """ Exit the game """
        self.exit_handler.exit()