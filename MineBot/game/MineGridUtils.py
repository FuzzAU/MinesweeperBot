

def adjacent_indexes(size, location):
    """
    Get adjacent cell indexes for a given cell on the Minesweeper grid
    Based heavily on Andrew Walker's adjacent cells function from gist-1459561
    """
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # The current cell (middle) should be included in the adjacency list
            if (i == 0) & (j == 0):
                continue
            nx = location[0] + i
            ny = location[1] + j
            if nx >= 0 and nx < size[0] and ny >= 0 and ny < size[1]:
                res.append((nx, ny))
    return res

def adjacent_cells(grid, location):
    """
    Get all of the actual cell objects in the grid that are adjacent to the location
    provided
    """
    adj_cells = adjacent_indexes(grid.size, location)
    res = [grid[x] for x in adj_cells]
    
    return res
