import sys
from PySide.QtCore import *
from PySide.QtGui import *

from size_dialog import *


class MinePySide(object):

    def __init__(self):
        # Create qt application
        self._app = QApplication(sys.argv)
        # Create the dialog for selecting size
        self._size_dialog = SizeDialog(self)

    def start(self):
    	# Show dialog to allow user to select grid size and start new game
        self._size_dialog.show()
        # Qt main loop will run until _app exit is called
        sys.exit(self._app.exec_())

    def exit(self):
    	# Request end of qt main loop
    	self._app.exit()
