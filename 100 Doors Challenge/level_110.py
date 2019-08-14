"""
Level 110 is key-pass with 8 sliding numbers
The first state is 78569354
and the final state is 89346575

Each two-consecutive-numbers can be moved
78 569354 can be moved to 5 78 69354, 56 78 9354, etc...
"""
import time
from collections import deque
from copy import copy

steps = []
for i in range(0, 6):
    for j in range(i+2, 7):
        steps.append((i, j))
for step in steps:
    print(step)


class State:
    def __init__(self, text: str, steps: list=None):
        self.text = text
        if steps is None:
            self.steps = []
        else:
            self.steps = steps
    
    def is_finish(self) -> bool:
        return self.text == '89346575'

    def is_nothing(self) -> bool:
        return self.text == '78569354'

    def _is_repeated(self, step: tuple) -> bool:
        return self.steps[-1] == step

    def move(self, step: tuple) -> 'State':
        sp, ep = step
        text = list(self.text)
        tsp, tep = text[sp:sp+2]
        text[sp] = text[ep]
        text[sp+1] = text[ep+1]
        text[ep] = tsp
        text[ep+1] = tep
        nsteps = self.steps + [step]
        return State(''.join(text), steps=nsteps)

    def steps_string(self) -> str:
        text = []
        for step in self.steps:
            text.append(f'({step[0]},{step[1]})')
        return '(' + ', '.join(text) + ')'


def main():
    q = deque([State('78569354')])
    sol = solve(q)
    print('Solution:', sol.steps_string())
    print('text:', sol.text)

def solve(q: deque) -> State:
    start_time = time.time()
    longest_steps = 0
    cur: State
    while q:
        cur = q.popleft()
        if longest_steps < len(cur.steps):
            longest_steps = len(cur.steps)
            print('==============================')
            print('longest steps:', longest_steps)
            print('current queues:', len(q))
            print('elapsed time:', time.time() - start_time, 'seconds')
            print('==============================')
        if cur.is_finish():
            return cur
        for step in steps:
            nstate = cur.move(step)
            if not nstate.is_nothing():
                q.append(nstate)
    return State('78569354')


if __name__ == '__main__':
    main()
