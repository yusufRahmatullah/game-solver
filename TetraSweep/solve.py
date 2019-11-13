import sys
from copy import deepcopy
from itertools import product

LOWEST = -1_000_000

piece_rotations = {
  'O': [
    [[True, True], [True, True]]
  ],
  'I': [
    [[True, True, True, True]],
    [[True], [True], [True], [True]]
  ],
  'S': [
    [[False, True, True], [True, True, False]],
    [[True, False], [True, True], [False, True]]
  ],
  'Z': [
    [[True, True, False], [False, True, True]],
    [[False, True], [True, True], [True, False]]
  ],
  'L': [
    [[True, False], [True, False], [True, True]],
    [[False, False, True], [True, True, True]],
    [[True, True], [False, True], [False, True]],
    [[True, True, True], [True, False, False]]
  ],
  'J': [
    [[False, True], [False, True], [True, True]],
    [[True, False, False], [True, True, True]],
    [[True, True], [True, False], [True, False]],
    [[True, True, True], [False, False, True]]
  ],
  'T': [
    [[True, True, True], [False, True, False]],
    [[False, True], [True, True], [False, True]],
    [[False, True, False], [True, True, True]],
    [[True, False], [True, True], [True, False]]
  ]
}

class Board:
  def __init__(self, cells: list, flags: list=None):
    self.cells = cells
    if flags is None:
      self._init_flags()
    else:
      self.flags = flags

  def available_piece_positions(self, piece) -> list:
    res = []
    for i in range(len(self.cells)):
      for j in range(len(self.cells[0])):
        if self._can_place(piece, (i, j)):
          res.append((i, j))
    return res
  
  def clone(self) -> 'Board':
    return Board(self.cells, flags=self.flags)

  def place(self, piece: list, pos:tuple) -> 'Board':
    i, j = pos
    nflags = deepcopy(self.flags)
    for pi in range(len(piece)):
      for pj in range(len(piece[0])):
        if piece[pi][pj]:
          nflags[i+pi][j+pj] = False
    return Board(self.cells, nflags)
  
  def print(self):
    ctn = []
    for i, row in enumerate(self.flags):
      rctn = []
      for j, flag in enumerate(row):
        p = self.cells[i][j]
        if flag:
          if p < 0:
            s = ''
          else:
            s = ' '
          rctn.append(f'{s} {p}')
        else:
          if p == LOWEST:
            c = 'X'
          else:
            c = 'O'
          rctn.append(f'  {c}')
      ctn.append(''.join(rctn))
    print('\n'.join(ctn))

  def score(self) -> int:
    res = 0
    for i, row in enumerate(self.flags):
      for j, flag in enumerate(row):
        if not flag and self.cells[i][j] > LOWEST:
          res += self.cells[i][j]
    return res

  def _can_place(self, piece: list, pos: tuple) -> bool:
    i, j = pos
    if len(self.flags) - i < len(piece):
      return False
    if len(self.flags[0]) - j < len(piece[0]):
      return False
    for pi in range(len(piece)):
      for pj in range(len(piece[0])):
        if piece[pi][pj] and not self.flags[i+pi][j+pj]:
          return False
    return True
    
  def _init_flags(self):
    self.flags = []
    for row in self.cells:
      rctn = []
      for cell in row:
        rctn.append(cell > LOWEST)
      self.flags.append(rctn)


class State:
  def __init__(self, target: int, board: Board, pletters: list, steps: list=None):
    self.target = target
    self.board = board
    self.pletters = pletters
    if steps is None:
      self.steps = []
    else:
      self.steps = steps

  def is_finish(self):
    return len(self.pletters) == 0 and self.board.score() >= self.target
  
  def is_dead(self):
    return len(self.pletters) == 0 and self.board.score() < self.target
  
  def is_dead_wannabe(self):
    return self.board.score() < 0
  
  def print(self):
    print('Board:')
    self.board.print()
    print('Steps:')
    for i, step in enumerate(self.steps):
      pr, pos = step
      print(f'Step {i+1} on pos ({pos[0]}, {pos[1]}) using piece:')
      pctn = []
      for row in pr:
        rctn = ''.join(list(map(lambda x: 'O' if x else 'X', row)))
        pctn.append(rctn)
      print('\n'.join(pctn))
      print('========')
    print('================')
  
  def step(self) -> list:
    pl = self.pletters.pop(0)
    prs = piece_rotations[pl]
    res = []
    for pr in prs:
      av_pos = self.board.available_piece_positions(pr)
      for pos in av_pos:
        nboard = self.board.place(pr, pos)
        nsteps = self.steps + [(pr, pos)]
        npletters = deepcopy(self.pletters)
        res.append(State(self.target, nboard, npletters, steps=nsteps))
    return res


def main():
  if len(sys.argv) != 2:
    print(f'Usage: python {sys.argv[0]} <input_file_path')
    quit()
  state = read_from_file(sys.argv[1])
  print('Target:', state.target)
  sol = solve([state])
  print(f'Solution (score: {sol.board.score()})')
  sol.print()


def read_from_file(path: str) -> State:
  ctn = open(path).read()
  lines = ctn.split('\n')
  # first line is target
  target = int(lines[0])
  # second line is pieces
  pieces = lines[1].split(' ')
  cells = []
  for line in lines[2:]:
    row = []
    for cell in line.split(' '):
      if cell == 'X':
        row.append(LOWEST)
      else:
        row.append(int(cell))
    cells.append(row)
  board = Board(cells)
  return State(target, board, pieces)


def solve(q: list) -> State:
  lsteps = 0
  processed = 0
  while q:
    cur = q.pop()
    if len(cur.steps) > lsteps:
      print('longest steps:', len(cur.steps))
      print('current queue:', len(q))
      lsteps = len(cur.steps)
    if processed % 100 == 0:
      print('Has process', processed, 'states')
    if cur.is_finish():
      return cur
    if cur.is_dead() or cur.is_dead_wannabe():
      processed += 1
      continue
    s = cur.step()
    q.extend(s)


if __name__ == '__main__':
  main()
