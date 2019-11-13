import sys


class State:
  def __init__(self, cells: list):
    self.cells = cells
    self.highest = 0
    for row in cells:
      for cell in row:
        if cell.isnum() and int(cell) > self.highest:
          self.highest = int(cell)
  
  def is_valid_until_pos(self, pos: tuple) -> False:
    pi, pj = pos
    for i in range(pi + 1):
      for j in range(len(self.cells[0])):
        if j > pj:
          break
        num = self.cells[i][j]
        if self._count_adjacencies((i, j)) > num:
          return False
    return True

  def print(self):
    for row in self.cells:
      print(''.join(row))
  
  def solve(self) -> bool:
    values = list(range(self.highest + 1))
    return True
    
  def _count_adjacencies(self, pos: tuple):
    pi, pj = pos
    num = self.cells[pi][pj]
    ls = [pos]
    total = 0
    while ls:
      cur = ls.pop(0)
      i, j = cur
      if self.cells[i][j] == num:
        total +=1
        ls.extend(self._neighbors(cur))
    return total
  
  def _neighbors(self, pos: tuple) -> list:
    i, j = pos
    res = []
    for di in [-1, 0, 1]:
      for dj in [-1, 0, 1]:
        if di == 0 and dj == 0:
          continue
        ni, nj = i + di, j + dj
        if self._valid_pos((ni, nj)):
          res.append((ni, nj))
    return pos
  
  def _solve_util(self, pos: tuple):
    i, j = pos
    
  
  def _valid_pos(self, pos: tuple) -> bool:
    i, j = pos
    return i >= 0 and j >= 0 and i < len(self.cells) and j < len(self.cells[0])


def main():
  if len(sys.argv) != 2:
    print('Usage: python solve.py <input_file_path>')
    quit(1)
  start_state = read_from_file(sys.argv[1])
  sol = solve(start_state)
  print('Solution:')
  sol.print()


def read_from_file(path: str) -> State:
  cells = []
  lines = open(path).read().split('\n')
  for line in lines:
    rc = []
    for c in line:
      rc.append(c)
    cells.append(rc)
  return State(cells)


def solve(state: State) -> State:
  return state


if __name__ == '__main__':
  main()
