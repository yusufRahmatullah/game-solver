import sys
from copy import deepcopy


class State:
  def __init__(self, cells: list, finished_colors: list=None):
    self.cells = cells
    self._h = len(cells)
    self._w = len(cells[0])
    self._init_flags()
    self._init_colors_start_pos()
    if finished_colors is None:
      self.finished_colors = []
    else:
      self.finished_colors = finished_colors

  @property
  def available_colors(self) -> list:
    res = []
    for color in self.colors_start_pos:
      if color not in self.finished_colors:
        res.append(color)
    return res

  def available_neighbors(self, pos: tuple) -> list:
    res = []
    for i, j in self._neighbors(pos):
      if self.cells[i][j] == '_':
        res.append((i, j))
    return res
  
  @property
  def is_dead(self) -> bool:
    for color in self.available_colors:
      if len(self.possible_paths(color)) == 0:
        return True
    return False
  
  @property
  def is_finish(self) -> bool:
    for color in self.colors_start_pos:
      if color not in self.finished_colors:
        return False
    return True
  
  def possible_paths(self, color: str) -> list:
    res = []
    start_pos = self.colors_start_pos[color]
    neighbors = self._neighbors(start_pos)
    q = list(map(lambda x: (x, [start_pos]), neighbors))
    while q:
      pos, path = q.pop(0)
      # cutoff path
      if len(path) > self._h + self._w:
        continue
      i, j = pos
      cur = self.cells[i][j]
      if cur == '_':
        for nbor in self._neighbors(pos):
          if nbor not in path:
            q.append((nbor, path + [pos]))
      elif cur == color:
        res.append(path+[pos])
    return res
  
  def print(self):
    ctn = []
    for row in self.cells:
      rctn = ''
      for c in row:
        rctn += c
      ctn.append(rctn)
    print('\n'.join(ctn))
  
  def step(self, path: list) -> 'State':
    ncells = deepcopy(self.cells)
    # assume first and last path are the color
    i, j = path[0]
    color = ncells[i][j]
    for i, j in path[1:-1]:
      ncells[i][j] = color.lower()
    return State(ncells, self.finished_colors + [color])

  def step_all(self) -> list:
    res = []
    for color in self.available_colors:
      for path in self.possible_paths(color):
        res.append(self.step(path))
    return res
  
  def _init_colors_start_pos(self):
    self.colors_start_pos = {}
    for i in range(self._h):
      for j in range(self._w):
        cur = self.cells[i][j]
        if cur != '_' and cur not in self.colors_start_pos:
          self.colors_start_pos[cur] = (i, j)

  def _init_flags(self):
    self.flags = []
    for i in range(self._h):
      for j in range(self._w):
        frow = []
        if self.cells[i][j] == '_':
          frow.append(False)
        else:
          frow.append(True)
        self.flags.append(frow)
  
  def _neighbors(self, pos: tuple) -> list:
    res = []
    i, j = pos
    for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
      dpos = (i + di, j + dj)
      if self._valid_pos(dpos):
        res.append(dpos)
    return res

  def _valid_pos(self, pos: tuple) -> bool:
    i, j = pos
    if i < 0 or i >= self._h or j < 0 or j >= self._w:
      return False
    return True


def main():
  if len(sys.argv) != 2:
    print(f'Usage: python {sys.argv[0]} <input_file_path')
    quit()
  start_state = read_from_file(sys.argv[1])
  sol = solve_bt(start_state)
  print('Solution:')
  sol.print()


def read_from_file(path: str) -> State:
  ctn = open(path).read()
  lines = ctn.strip().split('\n')
  cells = []
  for line in lines:
    rcell = []
    for c in line:
      rcell.append(c)
    cells.append(rcell)
  return State(cells)


def solve(start_state: State) -> State:
  stack = [start_state]
  nod = 0
  nos = 0
  while stack:
    print('nod:', nod, 'nos:', nos)
    cur = stack.pop()
    if cur.is_finish:
      return cur
    elif cur.is_dead:
      nod += 1
      continue
    else:
      ns = cur.step_all()
      nos += len(ns)
      stack.extend(ns)


def solve_bt(start_state: State) -> State:
  cells = deepcopy(start_state.cells)
  av_colors = list(map(str.lower, start_state.colors_start_pos.keys()))

  def incr(pos: tuple) -> tuple:
    i, j = pos
    j += 1
    if j >= len(cells[0]):
      i += 1
      j = 0
    return (i, j)

  def is_safe_up_to(pos: tuple):
    return True

  def util(pos: tuple):
    i, j = pos
    if i >= len(cells):
      return
    while cells[i][j].isupper():
      i, j = incr((i, j))

    for color in av_colors:
      cells[i][j] = color
      if is_safe_up_to(pos):
        if (i >= len(cells) - 1 and j >= len(cells[0]) - 1) or util(incr(pos)):
            return State(cells)
  
  return util((0,0))
  

if __name__ == '__main__':
  main()
