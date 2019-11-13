"""
level 045 is door with lamp
there are 9 lamps on the door like this
    4 5 6
    O O O
3 O       X 7
2 X       O 8
1 X       X 9

O means the lamp is off and
X means the lamp is on
the lamp is identify by number 1-9 from left-bottom to right bottom
in order like on the above

The initial state has 4 lamps which have been on that is
lamp number 1, 2, 7, and 9 (defined in start_lamps)
Each lamp has own configuration which stored in lamps_step
if lamp number 1 has been clicked, then lamps number 1, 6, and 8
will be toggled on/off.

The game is finish if all lamps are on. The solving algorithm
is using BFS (with deque).
"""

import time
from collections import deque

lamps_step = {
  1: [1, 6, 8],
  2: [2, 6, 7, 9],
  3: [3, 5, 9],
  4: [1, 4, 7],
  5: [1, 2, 3, 5],
  6: [4, 6, 9],
  7: [1, 3, 7],
  8: [4, 5, 8],
  9: [2, 8, 9]
}
start_lamps = [1, 2, 7, 9]


class State:
  def __init__(self, lamps: list=None, steps: list=None):
    if lamps is None:
      self.lamps = [False] * 10
    else:
      self.lamps = lamps
    if steps is None:
      self.steps = []
    else:
      self.steps = steps

  def finish(self) -> bool:
    for lamp in self.lamps[1:]:
      if not lamp:
        return False
    return True

  def print_lamps(self):
    s = ''
    for lamp in self.lamps[1:]:
      s += '1' if lamp else '0'
    print(s)

  def print_steps(self):
    print(' -> '.join(map(str, self.steps)))

  def step(self, step: int) -> 'State':
    if step < 1 or step > 9:
      return
    lamps = lamps_step[step]
    new_lamps = list(self.lamps)
    new_steps = list(self.steps)
    for lamp in lamps:
      new_lamps[lamp] = not new_lamps[lamp]
    new_steps.append(step)
    return State(new_lamps, new_steps)


def init_start_state() -> State:
  lamps = [False] * 10
  for lamp in start_lamps:
    lamps[lamp] = True
  return State(lamps=lamps)


def main():
  start_state = init_start_state()
  q = deque([start_state])
  solution = solve(q)
  solution.print_steps()


def solve(q: deque) -> State:
  start_time = time.time()
  last_steps_num = -1
  while q:
    s: State
    s = q.popleft()
    if len(s.steps) > last_steps_num:
      print(f'Elasped time: {time.time() - start_time} seconds')
      print('Longest steps:', len(s.steps))
      print('Current queue:', len(q))
      last_steps_num += 1
    if s.finish():
      return s
    for step in range(1, 10):
      if s.steps and s.steps[-1] == step:
        continue
      q.append(s.step(step))
  return init_start_state()


if __name__ == '__main__':
  main()
