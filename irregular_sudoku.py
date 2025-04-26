import random
import utils.irregular_sudoku_utils as utils
import utils.create_puzzle as puzzle
import utils.solve_puzzle as solver
import utils.constants as consts
import utils.write_utils as write
import copy
import os, sys
import argparse
from collections import defaultdict, deque


def generate_irregular_sudoku(regions_map):
    grid = [[0] * consts.N for _ in range(consts.N)]
    if utils.solve_irregular_sudoku(grid, regions_map):
        return grid
    else:
        return None
    
def printOrWrite(text, file=None):
    if file:
        file.write(text + "\n")
    else:
        print(text)

def print_grid_with_borders(grid, regions, file=None):
    N = len(grid)
    Ht = 2*N + 1
    Wd = 2*N + 1

    h_edge = [[False]*Wd for _ in range(Ht)]
    v_edge = [[False]*Wd for _ in range(Ht)]
    
    def R(r, c):
        return regions[r][c] if 0 <= r < N and 0 <= c < N else None
    
    grid_output = []
    for r in range(N):
        for c in range(N):
            val = R(r, c)
            if val != R(r-1, c):
                i = 2*r
                for j in range(2*c, 2*c+3):
                    h_edge[i][j] = True
            if val != R(r+1, c):
                i = 2*r + 2
                for j in range(2*c, 2*c+3):
                    h_edge[i][j] = True
            if val != R(r, c-1):
                j = 2*c
                for i2 in range(2*r, 2*r+3):
                    v_edge[i2][j] = True
            if val != R(r, c+1):
                j = 2*c + 2
                for i2 in range(2*r, 2*r+3):
                    v_edge[i2][j] = True
    
    for i in range(Ht):
        line = ""
        for j in range(Wd):
            if i % 2 == 1 and j % 2 == 1:
                strNumber = str(grid[i//2][j//2])
                if strNumber == '0' :
                    line += 'X'
                else:
                    line += str(grid[i//2][j//2])
            elif i % 2 == 1 and j % 2 == 0:
                line += '║' if v_edge[i][j] else ' '
            elif i % 2 == 0 and j % 2 == 1:
                line += '═' if h_edge[i][j] else ' '
            else:
                up    = (i > 0               and v_edge[i-1][j])
                down  = (i < Ht-1           and v_edge[i+1][j])
                left  = (j > 0               and h_edge[i][j-1])
                right = (j < Wd-1           and h_edge[i][j+1])
                if   up and down and left and right: ch = '╬'
                elif up and down and left:          ch = '╣'
                elif up and down and right:         ch = '╠'
                elif left and right and up:         ch = '╩'
                elif left and right and down:       ch = '╦'
                elif down and right:                ch = '╔'
                elif down and left:                 ch = '╗'
                elif up and right:                  ch = '╚'
                elif up and left:                   ch = '╝'
                elif up or down:                    ch = '║'
                elif left or right:                 ch = '═'
                else:                               ch = ' '
                line += ch

        printOrWrite(line, file)
        grid_output.append(line)
    return grid_output

def in_bounds(r,c):
    return 0 <= r < consts.N and 0 <= c < consts.N

def build_random_spanning_tree(nodes):
    """
    Cria uma árvore geradora aleatória sobre 'nodes' 
    (conjunto de tuplas (r,c)), usando Prim aleatório.
    Retorna um dict adjacente {u: [v,w,...], ...}.
    """
    nodes = set(nodes)
    start = random.choice(tuple(nodes))
    tree_adj = defaultdict(list)
    in_tree = {start}
    frontier = [(start, nbr) 
                for dr,dc in consts.NEIGHBORS 
                for nbr in [(start[0]+dr, start[1]+dc)] 
                if nbr in nodes]
    while frontier:
        u,v = random.choice(frontier)
        frontier.remove((u,v))
        if v in in_tree:
            continue

        tree_adj[u].append(v)
        tree_adj[v].append(u)
        in_tree.add(v)

        for dr,dc in consts.NEIGHBORS:
            w = (v[0]+dr, v[1]+dc)
            if w in nodes and w not in in_tree:
                frontier.append((v,w))
    return tree_adj

def collect_component(start, forbidden, tree_adj):
    """
    Retorna o conjunto de nós alcançáveis a partir de 'start' sem usar
    o nó 'forbidden' (ou seja, cortando a aresta (start,forbidden)).
    """
    comp = set()
    dq = deque([start])
    comp.add(start)
    while dq:
        u = dq.popleft()
        for w in tree_adj[u]:
            if w not in comp and w != forbidden:
                comp.add(w)
                dq.append(w)
    return comp

def generate_regions_layout(max_attempts=1000):
    all_nodes = [(r,c) for r in range(consts.N) for c in range(consts.N)]
    for _ in range(max_attempts):
        remaining = set(all_nodes)
        regions_map = [[None]*consts.N for _ in range(consts.N)]
        ok = True

        for region_id in range(consts.NUM_GROUPS - 1):
            tree_adj = build_random_spanning_tree(remaining)
            edges = []
            for u, nbrs in tree_adj.items():
                for v in nbrs:
                    if u < v: 
                        edges.append((u,v))
            random.shuffle(edges)

            found = False
            total = len(remaining)
            for u,v in edges:
                comp_u = collect_component(u, v, tree_adj)
                size_u = len(comp_u)
                if size_u == consts.GROUP_SIZE or total - size_u == consts.GROUP_SIZE:
                    if size_u == consts.GROUP_SIZE:
                        block = comp_u
                    else:
                        block = remaining - comp_u
                    found = True
                    break
            if not found:
                ok = False
                break

            for (r,c) in block:
                regions_map[r][c] = region_id
            remaining -= block

        if not ok:
            continue

        last_id = consts.NUM_GROUPS - 1
        for (r,c) in remaining:
            regions_map[r][c] = last_id
        return regions_map

    return None

def generate_puzzle_solution(seed=None, min_clues=6, max_clues=8, output_file=None, verbose=True):
    """
    Gera um puzzle completo com solução e passos, salvando em um arquivo se especificado.
    Retorna um dicionário com todas as informações do puzzle.
    """
    if seed is not None:
        random.seed(seed)
    
    result = {
        "seed": seed,
        "grid_output": [],
        "steps_output": [],
        "solved_completely": False,
        "is_featured": False
    }
    
    original_stdout = sys.stdout
    if output_file:
        sys.stdout = output_file
    
    if verbose:
        print("Gerando Sudoku Irregular 5x5 com Bordas...")

    chosen_regions = generate_regions_layout(500)
    if not chosen_regions:
        if verbose:
            print("Falha ao gerar layout de regiões após muitas tentativas.")
        if output_file:
            sys.stdout = original_stdout
        return None

    solved_grid = generate_irregular_sudoku(chosen_regions)
    if not solved_grid:
        if verbose:
            print("Falha ao gerar o Sudoku para o layout de regiões fornecido.")
        if output_file:
            sys.stdout = original_stdout
        return None
    
    if verbose:
        print("Sudoku Gerado:")
    result["full_solution"] = solved_grid
    result["regions"] = chosen_regions
    
    if output_file:
        result["grid_output"] = print_grid_with_borders(solved_grid, chosen_regions, output_file)
    else:
        result["grid_output"] = print_grid_with_borders(solved_grid, chosen_regions)
    
    if verbose:
        print("\nMapa das Regiões Usadas (0-4):")
        for row in chosen_regions:
            print(" ".join(map(str, row)))
    
    if verbose:
        print(f"\nCriando puzzle com {min_clues}-{max_clues} pistas...")
    
    puzzle_grid = puzzle.create_puzzle(solved_grid, chosen_regions, min_clues=min_clues, max_clues=max_clues)
    if not puzzle_grid:
        if verbose:
            print("Falha ao criar puzzle com número adequado de pistas.")
        if output_file:
            sys.stdout = original_stdout
        return None
    
    result["puzzle_grid"] = puzzle_grid
    
    if verbose:
        print(f"\nSudoku Puzzle ({min_clues}-{max_clues} pistas):")
    
    if output_file:
        result["puzzle_output"] = print_grid_with_borders(puzzle_grid, chosen_regions, output_file)
    else:
        result["puzzle_output"] = print_grid_with_borders(puzzle_grid, chosen_regions)
    
    if verbose:
        print("\nResolvendo passo a passo com técnicas básicas...")
    
    grid_for_steps = copy.deepcopy(puzzle_grid)
    steps, final_grid, solved_by_basic, explanations = solver.solve_step_by_step_with_details(grid_for_steps, chosen_regions)
    
    result["steps"] = steps
    result["explanations"] = explanations
    result["final_grid"] = final_grid
    result["solved_by_basic"] = solved_by_basic
    
    if not steps:
        if verbose:
            print("Não foi possível aplicar passos lógicos básicos (o Sudoku já está resolvido ou é inválido?).")
    else:
        current_step_grid = copy.deepcopy(puzzle_grid)
        if output_file:
            print_grid_with_borders(current_step_grid, chosen_regions, output_file)
        else:
            print_grid_with_borders(current_step_grid, chosen_regions)
        
        if verbose:
            print("-" * (2*consts.N+1))
        
        for i, step_info in enumerate(steps):
            (r, c), num, technique = step_info
            step_description = f"Passo {i+1}: Colocar {num} em ({r},{c}) - Técnica: {technique}"
            result["steps_output"].append(step_description)
            result["steps_output"].append(explanations[i])
            
            if verbose:
                print(step_description)
                print(explanations[i]) 
            
            if current_step_grid[r][c] == 0:
                current_step_grid[r][c] = num
            else:
                warning = f"  Advertência: A célula ({r},{c}) já estava preenchida antes do passo {i+1}"
                result["steps_output"].append(warning)
                if verbose:
                    print(warning)
            
            if output_file:
                grid_display = print_grid_with_borders(current_step_grid, chosen_regions, output_file)
            else:
                grid_display = print_grid_with_borders(current_step_grid, chosen_regions)
            
            result["steps_output"].extend(grid_display)
            
            if verbose:
                print("-" * (2*consts.N+1))
    
    if solved_by_basic:
        result["solved_completely"] = True
        if verbose:
            print("Sudoku resolvido completamente usando técnicas básicas!")
    elif utils.find_empty(final_grid) is not None:
        if verbose:
            print("O Sudoku não pôde ser resolvido completamente apenas com Singles (Naked/Hidden).")
            print("Técnicas mais avançadas ou backtracking são necessárias.")
            print("\nEstado final alcançado com técnicas básicas:")
        
        if output_file:
            result["final_state"] = print_grid_with_borders(final_grid, chosen_regions, output_file)
        else:
            result["final_state"] = print_grid_with_borders(final_grid, chosen_regions)
    else:
        result["solved_completely"] = True
        if verbose:
            print("O solver parou, mas a grade final parece estar completa.")
        
        if output_file:
            result["final_state"] = print_grid_with_borders(final_grid, chosen_regions, output_file)
        else:
            result["final_state"] = print_grid_with_borders(final_grid, chosen_regions)
    
    if output_file:
        sys.stdout = original_stdout
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Gerador e Solucionador de Sudoku Irregular 5x5")
    parser.add_argument("-s", "--ShowSteps", help="Solve Puzzle", action='store_true')
    parser.add_argument("-c", "--CreatePuzzle", help="Create Puzzle", action='store_true')
    parser.add_argument("-m", "--MultiPuzzle", help="Generate multiple puzzles", type=int, default=0)
    parser.add_argument("-f", "--Featured", help="Select a featured puzzle for README", action='store_true')
    parser.add_argument("--min-clues", help="Minimum number of clues", type=int, default=6)
    parser.add_argument("--max-clues", help="Maximum number of clues", type=int, default=8)
    parser.add_argument("--seed", help="Random seed for reproducibility", type=int, default=None)
    args = parser.parse_args()

    if args.MultiPuzzle > 0:
        if not os.path.exists("solucoes"):
            os.makedirs("solucoes")
        
        puzzles = []
        print(f"Gerando {args.MultiPuzzle} puzzles diferentes...")
        
        for i in range(args.MultiPuzzle):
            seed = args.seed + i if args.seed is not None else random.randint(1, 100000)
            output_file_path = f"solucoes/puzzle_{i+1}.txt"
            print(f"Gerando puzzle {i+1}/{args.MultiPuzzle} (seed: {seed})...")
            
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                puzzle_result = generate_puzzle_solution(
                    seed=seed,
                    min_clues=args.min_clues,
                    max_clues=args.max_clues,
                    output_file=output_file,
                    verbose=True
                )
            
            if puzzle_result:
                puzzles.append(puzzle_result)
                print(f"Puzzle {i+1} salvo em {output_file_path}")
            else:
                print(f"Falha ao gerar puzzle {i+1}. Tentando novamente com nova seed...")
                i -= 1
        
        if args.Featured and puzzles:
            puzzles_solved = [p for p in puzzles if p["solved_completely"]]
            featured = None
            
            if puzzles_solved:
                featured = max(puzzles_solved, key=lambda p: len(p["steps"]))
            else:
                featured = max(puzzles, key=lambda p: len(p["steps"]))
            
            featured["is_featured"] = True
            
            readme_content = write.create_readme_content(featured)
            with open("README.md", 'w', encoding='utf-8') as readme_file:
                readme_file.write(readme_content)
            
            print(f"README.md criado com o puzzle em destaque (seed: {featured['seed']})")
        
        return
    
    print("Gerando Sudoku Irregular 5x5 com Bordas...")

    chosen_regions = generate_regions_layout(500) 

    solved_grid = generate_irregular_sudoku(chosen_regions)

    if not solved_grid:
        print("Falha ao gerar o Sudoku para o layout de regiões fornecido.")
        return
    
    print("Sudoku Gerado:")
    print_grid_with_borders(solved_grid, chosen_regions)

    print("\nMapa das Regiões Usadas (0-4):")
    for row in chosen_regions:
        print(" ".join(map(str, row)))

    if not args.CreatePuzzle: 
        return
    
    print(f"\nCriando puzzle com {args.min_clues}-{args.max_clues} pistas...")
    puzzle_grid = puzzle.create_puzzle(solved_grid, chosen_regions, 
                                      min_clues=args.min_clues, 
                                      max_clues=args.max_clues)

    if not puzzle_grid: 
        return

    print(f"\nSudoku Puzzle ({args.min_clues}-{args.max_clues} pistas):")
    print_grid_with_borders(puzzle_grid, chosen_regions)

    if not args.ShowSteps: 
        return

    print("\nResolvendo passo a passo com técnicas básicas...")

    grid_for_steps = copy.deepcopy(puzzle_grid)
    steps, final_grid, solved_by_basic, explanations = solver.solve_step_by_step_with_details(grid_for_steps, chosen_regions)

    if not steps:
        print("Não foi possível aplicar passos lógicos básicos (o Sudoku já está resolvido ou é inválido?).")
    else:
        current_step_grid = copy.deepcopy(puzzle_grid)
        print_grid_with_borders(current_step_grid, chosen_regions)
        print("-" * (2*consts.N+1))
        for i, step_info in enumerate(steps):
            (r, c), num, technique = step_info
            print(f"Passo {i+1}: Colocar {num} em ({r},{c}) - Técnica: {technique}")
            print(explanations[i])  # Mostrar explicação detalhada

            if current_step_grid[r][c] == 0:
                current_step_grid[r][c] = num
            else:
                print(f"  Advertência: A célula ({r},{c}) já estava preenchida antes do passo {i+1}")

            print_grid_with_borders(current_step_grid, chosen_regions)
            print("-" * (2*consts.N+1))

    if solved_by_basic:
        print("Sudoku resolvido completamente usando técnicas básicas!")
    elif utils.find_empty(final_grid) is not None:
        print("O Sudoku não pôde ser resolvido completamente apenas com Singles (Naked/Hidden).")
        print("Técnicas mais avançadas ou backtracking são necessárias.")
        print("\nEstado final alcançado com técnicas básicas:")
        print_grid_with_borders(final_grid, chosen_regions)
    else:
        print("O solver parou, mas a grade final parece estar completa.")
        print_grid_with_borders(final_grid, chosen_regions)


if __name__ == "__main__":
    main()