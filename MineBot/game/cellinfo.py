

class PlayerCellInfo(object):
    """
    Representation of what a player knows about a specific game cell
    Lack's any hidden internal game state information
    """

    def __init__(self):
        self.is_hidden = True
        self._adjacent_mines = 0
        self.is_flagged = False

    def count_adjacent_mines(self):
        """
        Returns the number of adjacent mines to this cell
        If this is a hidden cell, the the number zero will be returned
        """
        if(self.is_hidden):
            return 0
        else:
            return self._adjacent_mines

    def get_game_char(self):
        """
        Get an ASCII character representation of this cell
        """
        cell_char = '0'
        if self.is_flagged:
            cell_char = 'F'
        elif self.is_hidden:
            cell_char = '-'
        # Only show a mine when it is not hidden and unflagged.
        elif self.has_mine:
            cell_char = 'X'
        else:
            cell_char = str(self._adjacent_mines)
        return cell_char


class InternalCellInfo(PlayerCellInfo):

    def __init__(self):
        self.has_mine = False
        PlayerCellInfo.__init__(self)

    def count_adjacent_mines(self):
        return self._adjacent_mines

    def get_char(self):
        """
        Get an ASCII character representation of this cell
        """
        cell_char = '0'
        if self.has_mine:
            cell_char = 'X'
        else:
            cell_char = str(self._adjacent_mines)
        return cell_char
