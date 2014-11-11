from PySide.QtCore import *
from PySide.QtGui import *


BOARD_MINIMUM = 3
BOARD_MAXIMUM = 50
BOARD_START_VALUE = 10

class SizeDialog(QWidget):
    """ Dialog to ask user what size game they wish to play """

    def __init__(self, exit_handler):
        """ Initialise window and build form components """

        QWidget.__init__(self)
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

        # Create spin boxes to represent the size of the minesweeper board that the user wants  
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

    @Slot()
    def on_start(self):
        """ Start a minesweeper game with the parameters given in this form """
        print 'Start'

    @Slot()
    def on_exit(self):
        """ Exit the game """
        self.exit_handler.exit()