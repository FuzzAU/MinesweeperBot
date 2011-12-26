

class PlayerCellInfo(object):
    """
    Representation of what a player knows about a specific game cell
    Lack's any hidden internal game state information
    """

    def __init__(self):
        self.is_hidden = True
        self._adjacent_mines = 0
        self.is_flagged = False

    def get_adjacent_mines(self):
        """
        Returns the number of adjacent mines to this cell
        If this is a hidden cell, the the number zero will be returned
        """
        if(self.is_hidden == True):
            return 0
        else:
            return self._adjacent_mines

    def get_char(self):
        """
        Get an ASCII character representation of this cell
        """
        cell_char = '0'
        if self.is_flagged == True:
            cell_char = 'F'
        else:
            cell_char = str(self._adjacent_mines)
        return cell_char
