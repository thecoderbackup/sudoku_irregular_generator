# Sudoku Irregular 5x5 com Bordas

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
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║X 3║X║
║ ╔═╬═╗ ║ ║
║4║X║X║X║X║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║X X║1 X║2║
╚═══╩═══╩═╝
```

### Mapa das Regiões:

```
3 3 4 4 2
3 3 4 4 2
3 1 0 4 2
1 1 0 0 2
1 1 0 0 2
```

### Solução Passo a Passo:

Passo 1: Colocar 4 em (4,3) - Técnica: Naked Single
Naked Single 4 na célula (4,3) porque:
  - Número 1 é bloqueado por: linha nas células (4,2); região nas células (4,2)
  - Número 2 é bloqueado por: linha nas células (4,4)
  - Número 3 é bloqueado por: coluna nas células (1,3)
  - Número 5 é bloqueado por: coluna nas células (3,3); região nas células (3,3)
Portanto, o único número possível é 4.
```
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║X 3║X║
║ ╔═╬═╗ ║ ║
║4║X║X║X║X║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║X X║1 4║2║
╚═══╩═══╩═╝
```

Passo 2: Colocar 3 em (4,1) - Técnica: Naked Single
Naked Single 3 na célula (4,1) porque:
  - Número 1 é bloqueado por: linha nas células (4,2)
  - Número 2 é bloqueado por: linha nas células (4,4)
  - Número 4 é bloqueado por: linha nas células (4,3)
  - Número 5 é bloqueado por: coluna nas células (0,1)
Portanto, o único número possível é 3.
```
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║X 3║X║
║ ╔═╬═╗ ║ ║
║4║X║X║X║X║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║X 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 3: Colocar 5 em (4,0) - Técnica: Naked Single
Naked Single 5 na célula (4,0) porque:
  - Número 1 é bloqueado por: linha nas células (4,2)
  - Número 2 é bloqueado por: linha nas células (4,4)
  - Número 3 é bloqueado por: linha nas células (4,1); região nas células (4,1)
  - Número 4 é bloqueado por: linha nas células (4,3); coluna nas células (2,0)
Portanto, o único número possível é 5.
```
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║X 3║X║
║ ╔═╬═╗ ║ ║
║4║X║X║X║X║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 4: Colocar 5 em (2,4) - Técnica: Hidden Single (Row 2)
Hidden Single 5 na célula (2,4) porque é o único lugar na Row 2 onde esse número pode estar.
```
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║X 3║X║
║ ╔═╬═╗ ║ ║
║4║X║X║X║5║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 5: Colocar 5 em (1,2) - Técnica: Hidden Single (Row 1)
Hidden Single 5 na célula (1,2) porque é o único lugar na Row 1 onde esse número pode estar.
```
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║5 3║X║
║ ╔═╬═╗ ║ ║
║4║X║X║X║5║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 6: Colocar 4 em (1,4) - Técnica: Hidden Single (Row 1)
Hidden Single 4 na célula (1,4) porque é o único lugar na Row 1 onde esse número pode estar.
```
╔═══╦═══╦═╗
║X 5║X X║X║
║   ║   ║ ║
║X X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║X║X║5║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 7: Colocar 4 em (0,2) - Técnica: Hidden Single (Row 0)
Hidden Single 4 na célula (0,2) porque é o único lugar na Row 0 onde esse número pode estar.
```
╔═══╦═══╦═╗
║X 5║4 X║X║
║   ║   ║ ║
║X X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║X║X║5║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 8: Colocar 3 em (2,2) - Técnica: Hidden Single (Row 2)
Hidden Single 3 na célula (2,2) porque é o único lugar na Row 2 onde esse número pode estar.
```
╔═══╦═══╦═╗
║X 5║4 X║X║
║   ║   ║ ║
║X X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║X X║X 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 9: Colocar 2 em (3,2) - Técnica: Naked Single
Naked Single 2 na célula (3,2) porque:
  - Número 1 é bloqueado por: coluna nas células (4,2); região nas células (4,2)
  - Número 3 é bloqueado por: coluna nas células (2,2); região nas células (2,2)
  - Número 4 é bloqueado por: coluna nas células (0,2); região nas células (4,3)
  - Número 5 é bloqueado por: linha nas células (3,3); coluna nas células (1,2); região nas células (3,3)
Portanto, o único número possível é 2.
```
╔═══╦═══╦═╗
║X 5║4 X║X║
║   ║   ║ ║
║X X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║X X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 10: Colocar 1 em (3,0) - Técnica: Naked Single
Naked Single 1 na célula (3,0) porque:
  - Número 2 é bloqueado por: linha nas células (3,2)
  - Número 3 é bloqueado por: região nas células (4,1)
  - Número 4 é bloqueado por: coluna nas células (2,0)
  - Número 5 é bloqueado por: linha nas células (3,3); coluna nas células (4,0); região nas células (4,0)
Portanto, o único número possível é 1.
```
╔═══╦═══╦═╗
║X 5║4 X║X║
║   ║   ║ ║
║X X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 11: Colocar 2 em (1,0) - Técnica: Naked Single
Naked Single 2 na célula (1,0) porque:
  - Número 1 é bloqueado por: coluna nas células (3,0)
  - Número 3 é bloqueado por: linha nas células (1,3)
  - Número 4 é bloqueado por: linha nas células (1,4); coluna nas células (2,0); região nas células (2,0)
  - Número 5 é bloqueado por: linha nas células (1,2); coluna nas células (4,0); região nas células (0,1)
Portanto, o único número possível é 2.
```
╔═══╦═══╦═╗
║X 5║4 X║X║
║   ║   ║ ║
║2 X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 12: Colocar 3 em (0,0) - Técnica: Naked Single
Naked Single 3 na célula (0,0) porque:
  - Número 1 é bloqueado por: coluna nas células (3,0)
  - Número 2 é bloqueado por: coluna nas células (1,0); região nas células (1,0)
  - Número 4 é bloqueado por: linha nas células (0,2); coluna nas células (2,0); região nas células (2,0)
  - Número 5 é bloqueado por: linha nas células (0,1); coluna nas células (4,0); região nas células (0,1)
Portanto, o único número possível é 3.
```
╔═══╦═══╦═╗
║3 5║4 X║X║
║   ║   ║ ║
║2 X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 13: Colocar 1 em (0,4) - Técnica: Naked Single
Naked Single 1 na célula (0,4) porque:
  - Número 2 é bloqueado por: coluna nas células (4,4); região nas células (4,4)
  - Número 3 é bloqueado por: linha nas células (0,0)
  - Número 4 é bloqueado por: linha nas células (0,2); coluna nas células (1,4); região nas células (1,4)
  - Número 5 é bloqueado por: linha nas células (0,1); coluna nas células (2,4); região nas células (2,4)
Portanto, o único número possível é 1.
```
╔═══╦═══╦═╗
║3 5║4 X║1║
║   ║   ║ ║
║2 X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 14: Colocar 2 em (0,3) - Técnica: Naked Single
Naked Single 2 na célula (0,3) porque:
  - Número 1 é bloqueado por: linha nas células (0,4)
  - Número 3 é bloqueado por: linha nas células (0,0); coluna nas células (1,3); região nas células (1,3)
  - Número 4 é bloqueado por: linha nas células (0,2); coluna nas células (4,3); região nas células (0,2)
  - Número 5 é bloqueado por: linha nas células (0,1); coluna nas células (3,3); região nas células (1,2)
Portanto, o único número possível é 2.
```
╔═══╦═══╦═╗
║3 5║4 2║1║
║   ║   ║ ║
║2 X║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 15: Colocar 1 em (1,1) - Técnica: Naked Single
Naked Single 1 na célula (1,1) porque:
  - Número 2 é bloqueado por: linha nas células (1,0); região nas células (1,0)
  - Número 3 é bloqueado por: linha nas células (1,3); coluna nas células (4,1); região nas células (0,0)
  - Número 4 é bloqueado por: linha nas células (1,4); região nas células (2,0)
  - Número 5 é bloqueado por: linha nas células (1,2); coluna nas células (0,1); região nas células (0,1)
Portanto, o único número possível é 1.
```
╔═══╦═══╦═╗
║3 5║4 2║1║
║   ║   ║ ║
║2 1║5 3║4║
║ ╔═╬═╗ ║ ║
║4║X║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 16: Colocar 2 em (2,1) - Técnica: Naked Single
Naked Single 2 na célula (2,1) porque:
  - Número 1 é bloqueado por: coluna nas células (1,1); região nas células (3,0)
  - Número 3 é bloqueado por: linha nas células (2,2); coluna nas células (4,1); região nas células (4,1)
  - Número 4 é bloqueado por: linha nas células (2,0)
  - Número 5 é bloqueado por: linha nas células (2,4); coluna nas células (0,1); região nas células (4,0)
Portanto, o único número possível é 2.
```
╔═══╦═══╦═╗
║3 5║4 2║1║
║   ║   ║ ║
║2 1║5 3║4║
║ ╔═╬═╗ ║ ║
║4║2║3║X║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 17: Colocar 1 em (2,3) - Técnica: Naked Single
Naked Single 1 na célula (2,3) porque:
  - Número 2 é bloqueado por: linha nas células (2,1); coluna nas células (0,3); região nas células (0,3)
  - Número 3 é bloqueado por: linha nas células (2,2); coluna nas células (1,3); região nas células (1,3)
  - Número 4 é bloqueado por: linha nas células (2,0); coluna nas células (4,3); região nas células (0,2)
  - Número 5 é bloqueado por: linha nas células (2,4); coluna nas células (3,3); região nas células (1,2)
Portanto, o único número possível é 1.
```
╔═══╦═══╦═╗
║3 5║4 2║1║
║   ║   ║ ║
║2 1║5 3║4║
║ ╔═╬═╗ ║ ║
║4║2║3║1║5║
╠═╝ ║ ╚═╣ ║
║1 X║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 18: Colocar 4 em (3,1) - Técnica: Naked Single
Naked Single 4 na célula (3,1) porque:
  - Número 1 é bloqueado por: linha nas células (3,0); coluna nas células (1,1); região nas células (3,0)
  - Número 2 é bloqueado por: linha nas células (3,2); coluna nas células (2,1); região nas células (2,1)
  - Número 3 é bloqueado por: coluna nas células (4,1); região nas células (4,1)
  - Número 5 é bloqueado por: linha nas células (3,3); coluna nas células (0,1); região nas células (4,0)
Portanto, o único número possível é 4.
```
╔═══╦═══╦═╗
║3 5║4 2║1║
║   ║   ║ ║
║2 1║5 3║4║
║ ╔═╬═╗ ║ ║
║4║2║3║1║5║
╠═╝ ║ ╚═╣ ║
║1 4║2 5║X║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```

Passo 19: Colocar 3 em (3,4) - Técnica: Naked Single
Naked Single 3 na célula (3,4) porque:
  - Número 1 é bloqueado por: linha nas células (3,0); coluna nas células (0,4); região nas células (0,4)
  - Número 2 é bloqueado por: linha nas células (3,2); coluna nas células (4,4); região nas células (4,4)
  - Número 4 é bloqueado por: linha nas células (3,1); coluna nas células (1,4); região nas células (1,4)
  - Número 5 é bloqueado por: linha nas células (3,3); coluna nas células (2,4); região nas células (2,4)
Portanto, o único número possível é 3.
```
╔═══╦═══╦═╗
║3 5║4 2║1║
║   ║   ║ ║
║2 1║5 3║4║
║ ╔═╬═╗ ║ ║
║4║2║3║1║5║
╠═╝ ║ ╚═╣ ║
║1 4║2 5║3║
║   ║   ║ ║
║5 3║1 4║2║
╚═══╩═══╩═╝
```


### Resultado: Sudoku resolvido completamente usando técnicas básicas!