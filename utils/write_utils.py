def create_readme_steps(featured_puzzle):
    return "".join(f"```\n{step}\n" if step.startswith(("╔", "═")) else f"{step}\n```\n\n" if step.endswith(("╝", "═")) else f"{step}\n" for step in featured_puzzle["steps_output"])

def create_readme_content(featured_puzzle):
    """Cria o conteúdo do README com base no puzzle em destaque"""
    
    readme_content = """# Sudoku Irregular 5x5 com Bordas

Este projeto gera e resolve sudokus irregulares 5x5. O sudoku irregular é uma variante onde as regiões não são quadradas regulares, mas grupos irregulares de células conectadas.

## Como Executar

Para gerar 10 puzzles diferentes e salvá-los na pasta 'solucoes':

```
python irregular_sudoku.py -m 10
```

Outras opções:
- `-s` ou `--ShowSteps`: Mostra os passos para resolver o puzzle
- `-c` ou `--CreatePuzzle`: Cria um puzzle a partir da solução completa
- `-m N` ou `--MultiPuzzle N`: Gera N puzzles diferentes e salva na pasta 'solucoes'
- `-f` ou `--Featured`: Seleciona um puzzle para ser destacado no README

## Técnicas Implementadas

- Naked Singles: Quando apenas um número é possível em uma célula
- Hidden Singles: Quando um número só pode estar em uma posição dentro de uma região/linha/coluna


## Puzzle em Destaque

Abaixo está um exemplo de puzzle gerado pelo programa, junto com sua solução passo a passo:

### Sudoku Puzzle Initial:

```
"""
    for line in featured_puzzle["puzzle_output"]:
        readme_content += line + "\n"
    
    readme_content += "```\n\n### Mapa das Regiões:\n\n```\n"
    
    for row in featured_puzzle["regions"]:
        readme_content += " ".join(map(str, row)) + "\n"
    
    readme_content += "```\n\n### Solução Passo a Passo:\n\n"
    
    readme_content += create_readme_steps(featured_puzzle)
    
    if featured_puzzle["solved_completely"]:
        readme_content += "\n### Resultado: Sudoku resolvido completamente usando técnicas básicas!"
    else:
        readme_content += "\n### Resultado: O Sudoku não pôde ser resolvido completamente apenas com técnicas básicas."
    
    
    return readme_content