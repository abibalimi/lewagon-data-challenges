# pylint: disable=missing-docstring

def sudoku_validator(grid):
    ok_line = True
    ok_col = True
    ok_block = True
    while ok_line and ok_col and ok_block:
        for i in range(9):
            ok_line = sorted(grid[i]) == sorted([j+1 for j in range(9)])
        for i in range(9):
            col = []
            for j in range(9):
                col.append(grid[j][i])
            ok_col = sorted(col) == sorted([j+1 for j in range(9)])
            col[:] = []
        for k in [0, 1, 2]:
            for m_l in [0, 1, 2]:
                block = []
                for i in range(3):
                    for j in range(3):
                        block.append(grid[m_l*3+i][k*3+j])
                ok_block = sorted(block) == sorted([j+1 for j in range(9)])
                block[:] = []
    return ok_line and ok_col and ok_block
