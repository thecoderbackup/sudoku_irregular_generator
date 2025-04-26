import random
import copy
import utils.constants as consts
import utils.irregular_sudoku_utils as utils

def count_solutions(grid, regions_map):
    count = [0] 
    grid_copy = copy.deepcopy(grid) 
    def solve_and_count():
        find = utils.find_empty(grid_copy)
        if not find:
            count[0] += 1
            return count[0] > 1 
        row, col = find
        for num in range(1, consts.N + 1):
            if utils.is_valid(grid_copy, num, (row, col), regions_map):
                grid_copy[row][col] = num
                
                if solve_and_count():
                    grid_copy[row][col] = 0
                    return True 

                grid_copy[row][col] = 0 
            if count[0] > 1: 
                return True   
        return False
    solve_and_count()
    return count[0]

def create_puzzle(solved_grid, regions_map, min_clues=6, max_clues=8):
    if not solved_grid:
        return None

    puzzle_grid = copy.deepcopy(solved_grid)
    N_puzzle = len(puzzle_grid)
    
    all_positions = [(r, c) for r in range(N_puzzle) for c in range(N_puzzle)]
    random.shuffle(all_positions)

    target_clues = random.randint(min_clues, max_clues)
    cells_to_remove = (N_puzzle * N_puzzle) - target_clues
    
    removed_count = 0
    for r, c in all_positions:
        if puzzle_grid[r][c] == 0:
            continue

        original_value = puzzle_grid[r][c]
        puzzle_grid[r][c] = 0 
        num_solutions = count_solutions(puzzle_grid, regions_map)

        if num_solutions != 1:
            puzzle_grid[r][c] = original_value
        else:
            removed_count += 1
            if removed_count >= cells_to_remove:
                break 

    return puzzle_grid