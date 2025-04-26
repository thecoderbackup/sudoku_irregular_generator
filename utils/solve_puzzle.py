import utils.constants as consts
import copy
import utils.irregular_sudoku_utils as utils
from collections import defaultdict

def get_region_cells(target_region_id, regions_map):
    cells = []
    for r in range(consts.N):
        for c in range(consts.N):
            if regions_map[r][c] == target_region_id:
                cells.append((r, c))
    return cells

def get_peers(r, c, regions_map):
    peers = set()
    region_id = regions_map[r][c]
    for i in range(consts.N):
        if i != c: peers.add((r, i))
        if i != r: peers.add((i, c))
    for r_reg, c_reg in get_region_cells(region_id, regions_map):
        if (r_reg, c_reg) != (r, c):
            peers.add((r_reg, c_reg))
    return peers

def initialize_candidates(grid, regions_map):
    candidates = [[set(range(1, consts.N + 1)) for _ in range(consts.N)] for _ in range(consts.N)]
    all_peers = {}

    for r in range(consts.N):
        for c in range(consts.N):
            all_peers[(r,c)] = get_peers(r,c, regions_map)
            if grid[r][c] != 0:
                val = grid[r][c]
                candidates[r][c] = set() 
                for pr, pc in all_peers[(r,c)]:
                     candidates[pr][pc].discard(val)
    return candidates, all_peers

def update_candidates(r, c, num, candidates, all_peers):
    candidates[r][c] = set() 
    affected_cells = []
    for pr, pc in all_peers[(r,c)]:
        if num in candidates[pr][pc]:
            candidates[pr][pc].discard(num)
            affected_cells.append((pr,pc))
    return affected_cells

def track_candidate_eliminations(grid, r, c, candidates, regions_map):
    """
    Analisa por que cada candidato foi eliminado para a célula (r,c)
    Retorna um dicionário que mapeia cada número eliminado para as células que o bloqueiam
    """
    blocked_by = {num: [] for num in range(1, consts.N + 1)}
    region_id = regions_map[r][c]
    
    for col in range(consts.N):
        if col != c and grid[r][col] != 0:
            blocked_by[grid[r][col]].append(("linha", (r, col)))
    
    for row in range(consts.N):
        if row != r and grid[row][c] != 0:
            blocked_by[grid[row][c]].append(("coluna", (row, c)))
    
    for row in range(consts.N):
        for col in range(consts.N):
            if regions_map[row][col] == region_id and (row != r or col != c) and grid[row][col] != 0:
                blocked_by[grid[row][col]].append(("região", (row, col)))
    
    return blocked_by

def explain_naked_single(grid, r, c, regions_map, candidates):
    """
    Explica detalhadamente por que um Naked Single foi encontrado na célula (r,c)
    """
    if grid[r][c] != 0:
        return f"A célula ({r},{c}) já está preenchida com {grid[r][c]}"
    
    num = list(candidates[r][c])[0] 
    blocked_by = track_candidate_eliminations(grid, r, c, candidates, regions_map)
    
    explanation = f"Naked Single {num} na célula ({r},{c}) porque:\n"
    
    for blocked_num in range(1, consts.N + 1):
        if blocked_num != num:
            blockers = blocked_by[blocked_num]
            if blockers:
                explanation += f"  - Número {blocked_num} é bloqueado por: "
                by_type = defaultdict(list)
                for block_type, pos in blockers:
                    by_type[block_type].append(pos)
                
                details = []
                for block_type, positions in by_type.items():
                    pos_str = ", ".join([f"({p[0]},{p[1]})" for p in positions])
                    details.append(f"{block_type} nas células {pos_str}")
                
                explanation += "; ".join(details) + "\n"
    
    explanation += f"Portanto, o único número possível é {num}."
    return explanation

def solve_step_by_step_with_details(puzzle_grid, regions_map):
    grid = copy.deepcopy(puzzle_grid)
    candidates, all_peers = initialize_candidates(grid, regions_map)
    steps_log = []
    explanations = []
    
    iteration = 0
    max_iterations = consts.N * consts.N * consts.N

    while iteration < max_iterations:
        iteration += 1
        progress_made = False

        found_naked_single = False
        for r in range(consts.N):
            for c in range(consts.N):
                if grid[r][c] == 0 and len(candidates[r][c]) == 1:
                    num = list(candidates[r][c])[0]
                    
                    if utils.is_valid(grid, num, (r, c), regions_map): 
                        explanation = explain_naked_single(grid, r, c, regions_map, candidates)
                        grid[r][c] = num
                        steps_log.append(((r, c), num, "Naked Single"))
                        explanations.append(explanation)
                        update_candidates(r, c, num, candidates, all_peers)
                        progress_made = True
                        found_naked_single = True 
                        break
                    else:
                        print(f"ERRO LÓGICO: Naked Single {num} em ({r},{c}) não é válido.")
                        return steps_log, grid, False, explanations
            if found_naked_single:
                break

        if progress_made:
            continue

        found_hidden_single = False
        for unit_type in ["Row", "Col", "Region"]:
            for unit_index in range(consts.N): 
                
                if unit_type == "Row": unit_cells = [(unit_index, c) for c in range(consts.N)]
                elif unit_type == "Col": unit_cells = [(r, unit_index) for r in range(consts.N)]
                else: unit_cells = get_region_cells(unit_index, regions_map)

                for num_to_check in range(1, consts.N + 1):
                    possible_placements = []
                    for r_cell, c_cell in unit_cells:
                        if grid[r_cell][c_cell] == 0 and num_to_check in candidates[r_cell][c_cell]:
                            possible_placements.append((r_cell, c_cell))
                    
                    if len(possible_placements) == 1:
                        r, c = possible_placements[0]
                        
                        if grid[r][c] == 0:
                            if utils.is_valid(grid, num_to_check, (r, c), regions_map):
                                explanation = f"Hidden Single {num_to_check} na célula ({r},{c}) porque é o único lugar na {unit_type} {unit_index} onde esse número pode estar."
                                grid[r][c] = num_to_check
                                steps_log.append(((r, c), num_to_check, f"Hidden Single ({unit_type} {unit_index})"))
                                explanations.append(explanation)
                                update_candidates(r, c, num_to_check, candidates, all_peers)
                                progress_made = True
                                found_hidden_single = True
                                break
                            else:
                                print(f"ERRO LÓGICO: Hidden Single {num_to_check} em ({r},{c}) não é válido.")
                                return steps_log, grid, False, explanations
                
                if found_hidden_single:
                    break
            
            if found_hidden_single:
                break

        if progress_made:
            continue

        if not progress_made:
            break 

    is_solved = utils.find_empty(grid) is None
    if not is_solved and iteration == max_iterations:
         print("ADVERTÊNCIA: Limite de iteraçoes.")
         
    return steps_log, grid, is_solved, explanations