import random
import utils.constants as consts

def find_empty(grid):
    for r in range(consts.N):
        for c in range(consts.N):
            if grid[r][c] == 0:
                return (r, c)
    return None

def is_valid(grid, num, pos, regions_map):
    row, col = pos
    region_id = regions_map[row][col]
    if num in grid[row]:
        return False
    if num in [grid[i][col] for i in range(consts.N)]:
        return False
    for r in range(consts.N):
        for c in range(consts.N):
            if regions_map[r][c] == region_id and grid[r][c] == num:
                return False
    return True

def solve_irregular_sudoku(grid, regions_map):
    find = find_empty(grid)
    if not find:
        return True
    else:
        row, col = find
    numbers_to_try = list(range(1, consts.N + 1))
    random.shuffle(numbers_to_try)

    for num in numbers_to_try:
        if is_valid(grid, num, (row, col), regions_map):
            grid[row][col] = num
            if solve_irregular_sudoku(grid, regions_map):
                return True
            grid[row][col] = 0
    return False