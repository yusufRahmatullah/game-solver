"""
Level 074 is a hexagonal game
Here is the initial state of the game

     O O X X X
    O X O O O O
   O O O O O O O
  O O O O O O X O
 O O O O V O O O O
  O O O O O O O O
   O O O O O O O
    O O O O X X
     O O O O O

O is the playable cell
X is the red block
V is the agent

Since it's hexagonal, agent can move on 6 direction, there are
Left-Up (LU), Right-Up (RU), Right (R), Right-Down (RD),
Left-Down (LD), and Left (L) which numbered 0-5. Agent move in
straight line. Thus, agent will move toward cells in same direction
until meet a block. Agent will change the playable cell into block cell.
Game is finish if all playable cells become blocks. Game is dead
if agent cannot move anymore on current cell

Hexagonal board can be stored as an 2-D array which each
even-index row (index start from 0) has least columns than
odd-index row. Since the first row of the game has 5 (odd) columns,
then the first row is stored in index-1. We use index-0 for
the invisible block (symbolize as B). First row has 5 columns but
fifth row has 9 columns. We set all rows to has 9 columns thus
the size of the board is 10x9. Each even row has additional invisible
block on the last column.
This level's board can be defined as:

B B B B B B B B B
B B O O X X X B B
B O X O O O O B B
B O O O O O O O B
O O O O O O X O B
O O O O V O O O O
O O O O O O O O B
B O O O O O O O B
B O O O O X X B B
B B O O X O O B B

If agent on even-row cell, go Left-Up and Left-Down only
changes the row and go Right-Up and Right-Down will
changes the row and increase the column's index.
If agent on odd-row cell, go Left-Up and Left-Down changes
the row and decrease the column's index  and go Right-Up and Right-Down
will changes the row only.
"""

from copy import deepcopy

directions = ['LU', 'RU', 'R', 'RD', 'LD', 'L']
even_steps = {
    'LU': (-1, 0),
    'RU': (-1, 1),
    'R': (0, 1),
    'RD': (1, 1),
    'LD': (1, 0),
    'L': (0, -1)
}
odd_steps = {
    'LU': (-1, -1),
    'RU': (-1, 0),
    'R': (0, 1),
    'RD': (1, 0),
    'LD': (1, -1),
    'L': (0, -1)
}
initial_board = [
    'B B B B B B B B B',
    'B B O O X X X B B',
    'B O X O O O O B B',
    'B O O O O O O O B',
    'O O O O O O X O B',
    'O O O O V O O O O',
    'O O O O O O O O B',
    'B O O O O O O O B',
    'B O O O O X X B B',
    'B B O O X O O B B'
]


class Board:
    def __init__(self, cells: list=None, steps: list=None, ):
        if cells is None:
            self.cells = []
            for row in initial_board:
                self.cells.append(row.split())
        else:
            self.cells = cells
        self._init_agent_pos()
        self.last_direction_idx = -1
        self.find_possible_direction_index()
        if steps is None:
            self.steps = []
        else:
            self.steps = steps

    def do_possible_move(self) -> 'Board':
        ncells = deepcopy(self.cells)
        curpos = deepcopy(self.agent_pos)
        step = self._next_step(curpos[0] %2 == 0, self.last_direction_idx)
        napos = (curpos[0] + step[0], curpos[1] + step[1])
        while self._valid_pos(napos) and ncells[napos[0]][napos[1]] == 'O':
            ncells[curpos[0]][curpos[1]] = 'X'
            ncells[napos[0]][napos[1]] = 'V'
            curpos = napos
            step = self._next_step(curpos[0] %2 == 0, self.last_direction_idx)
            napos = (curpos[0] + step[0], curpos[1] + step[1])
        nsteps = self.steps + [directions[self.last_direction_idx]]
        self.last_direction_idx += 1
        return Board(cells=ncells, steps=nsteps)

    def find_possible_direction_index(self):
        r, c = self.agent_pos
        even = r % 2 == 0
        for i in range(self.last_direction_idx+1, len(directions)):
            dr, dc = self._next_step(even, i)
            if self._valid_pos((r + dr, c + dc)) and self.cells[r + dr][c + dc] == 'O':
                self.last_direction_idx = i
                break
    
    def is_finish(self) -> bool:
        for row in self.cells:
            for cell in row:
                if cell == 'O':
                    return False
        return True

    def is_dead(self) -> bool:
        return len(self.possible_neighbors()) == 0

    def possible_neighbors(self) -> list:
        res = []
        for i in range(self.last_direction_idx, len(directions)):
            step = self._next_step(self.agent_pos[0] % 2 == 0, i)
            apos = self.agent_pos
            next_pos = (apos[0] + step[0], apos[1] + step[1])
            r, c = next_pos
            if self._valid_pos(next_pos) and self.cells[r][c] == 'O':
                res.append(next_pos)
        return res

    def print_cells(self):
        self._print_cells(self.cells)

    def _init_agent_pos(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell == 'V':
                    self.agent_pos = (i, j)

    def _next_step(self, even: bool, direction_idx: int) -> tuple:
        drc = directions[direction_idx]
        if even:
            return even_steps[drc]
        else:
            return odd_steps[drc]
    
    @staticmethod
    def _print_cells(cells):
        for r, row in enumerate(cells):
            row_ctn = []
            for cell in row:
                if cell == 'B':
                    row_ctn.append(' ')
                else:
                    row_ctn.append(cell)
            prefix = ' ' if r % 2 == 0 else ''
            print(prefix, ' '.join(row_ctn), sep='', end='\n')
    
    def _valid_pos(self, pos: tuple) -> bool:
        r, c = pos
        return 0 <= r < len(self.cells) and 0 <= c < len(self.cells[0])

def main():
    board = Board()
    stack = [board]
    solution = solve(stack)
    solution.print_cells()
    print('Steps:', solution.steps)


def solve(stack: list):
    while stack:
        cur_board = stack[-1]
        if cur_board.is_finish():
            return cur_board
        elif cur_board.is_dead():
            _p = stack.pop()
            if stack:
                stack[-1].find_possible_direction_index()
        else:
            stack.append(cur_board.do_possible_move())

if __name__ == '__main__':
    main()
