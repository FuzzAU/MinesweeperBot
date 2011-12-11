

class CellInfo(object):

    def __init__(self):
        self.has_mine = False
        self.surrounding_mines = 0

    def get_char(self):
        """
        Get an ASCII character representation of this cell
        """
        cell_char = '0'
        if self.has_mine == True:
            cell_char = 'X'
        else:
            cell_char = str(self.surrounding_mines)
        return cell_char
