

def adjacent_cells(size, location):
    """
    Get adjacent sell indexes for a given cell on the Minesweeper grid
    Based heavily on Andrew Walker's adjacent cells function from gist-1459561
    """
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            nx = location[0] + i
            ny = location[1] + j
            if nx >= 0 and nx < size[0] and ny >= 0 and ny < size[1]:
                res.append((nx, ny))
    return res
