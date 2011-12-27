from .PlayerCellInfo import PlayerCellInfo


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
        if self.has_mine == True:
            cell_char = 'X'
        else:
            cell_char = str(self._adjacent_mines)
        return cell_char
