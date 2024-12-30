from functools import cache
from dataclasses import dataclass, field
from heapq import heappush,heappop

"""
I think I can hard-code this somwehat. 
Need a function that has a start key for the final (0) robot and an end key.
Robot (1) will always start and end on A, so it is "stateless". All 
subsequent robots are also stateless.

first example 029a would be like sum(A-0, 0-2, 2-9, 9-A). 

Might also be able to solve a-priori. EG, 9-A happens three times in the example.
"""



SAMPLE = """029A
980A
179A
456A
379A"""

KEYPAD = """789
456
123
_0A""".split()

KEY_LOCS = {v:(x,y) for y,row in enumerate(KEYPAD) for x,v in enumerate(list(row)) }
LOCS_KEY = {v:k for k,v in KEY_LOCS.items()}

def return_num_from_loc(x:int, y: int) -> str:
    return LOCS_KEY[(x,y)]

def return_loc_from_num(num: str) -> tuple[str,str]:
    return KEY_LOCS[num]

ARROWPAD = """_^A
<v>""".split()

DIR_LOCS = {v:(x,y) for y,row in enumerate(ARROWPAD) for x,v in enumerate(list(row)) }
LOCS_DIR = {v:k for k,v in DIR_LOCS.items()}

def return_loc_from_delta(dx,dy):
    if (dx,dy) == (0,1): return (1,1)
    if (dx,dy) == (0,-1): return (1,0)
    if (dx,dy) == (1,0): return (2,1)
    if (dx,dy) == (-1,0): return (0,1)
    if (dx,dy) == (0,0): return (2,0)

def str_from_0_loc(dx,dy):
    if (dx,dy) == (0,0): return "X"
    if (dx,dy) == (1,0): return "^"
    if (dx,dy) == (2,0): return "A"
    if (dx,dy) == (0,1): return "<"
    if (dx,dy) == (1,1): return "v"
    if (dx,dy) == (2,1): return ">"

@dataclass
class State:
    x: int
    y: int
    steps: int
    # steps: str
    pre_child: tuple[int,int] = (2,0)
    solved: bool = False

    def __lt__(self,other):
        return self.steps < other.steps
        # return len(self.steps) < len(other.steps)
    
    @property
    def loc(self):
        return self.x,self.y
    
    def __str__(self):
        return str(f"{self.x,self.y}, {self.steps = }, {self.pre_child=}")
    
    def __repr__(self):
        return self.__str__()
    
@dataclass
class PQueue:
    _container: list = field(default_factory=list)

    def push(self, node):
        heappush(self._container, node)

    def pop(self):
        return heappop(self._container)

    def __len__(self):
        return len(self._container)
    
    def is_empty(self):
        return len(self._container)==0
    
    def __str__(self):
        return str(self._container)
    
    def __repr__(self):
        return self.__str__()

new_steps = [
    (-1,0),
    (0,-1),
    (0,1),
    (1,0),
    (0,0)
]

@cache
def steps_from_start_to_end(start,end,depth=0,keypad=False) -> int:
    # print(f"{depth = }   {start = }   {end = }")
    if depth==0:
        return 1
    s = State(start[0],start[1],0,(2,0))
    frontier = PQueue()
    frontier.push(s)
    explored = {}
    while frontier:
        s: State = frontier.pop()
        if s.loc == end and s.solved:
            return s.steps
        if s.solved: continue
        for dx,dy in new_steps:
            nx, ny = s.x+dx, s.y+dy
            if nx < 0 or nx > 2: continue
            if ny < 0: continue
            if ny > 1 and not keypad: continue
            if ny > 3: continue
            if keypad and (nx,ny) == (0,3): continue
            if not keypad and (nx,ny) == (0,0): continue
            new_child = return_loc_from_delta(dx,dy)
            steps_incremental = steps_from_start_to_end(s.pre_child,new_child,depth=depth-1, keypad=False)
            new_incremental = s.steps+steps_incremental
            solved = False
            if (dx,dy) == (0,0): solved = True
            new_state = State(nx,ny,new_incremental,pre_child=new_child, solved=solved)
            frontier.push(new_state)

def presses_to_solve(code: str):
    prev = "A"
    sequence = []
    for c in code:
        loc0 = KEY_LOCS[prev]
        loc1 = KEY_LOCS[c]
        sequence.append((loc0,loc1))
        prev=c
    
    # locations = [(1,0),(2,0),(0,1),(1,1),(2,1)]
    # for d in range(1,26):
    #     print(d)
    #     for start in locations:
    #         for end in locations:
    #             print(steps_from_start_to_end(start,end,depth=d))
    presses=0
    for start,end in sequence:
        # print(f"{start}  {end}")
        presses += steps_from_start_to_end(start,end,depth=26,keypad=True)
    return presses

def main_1(text_input: str) -> int:
    global solve_str
    codes = text_input.strip().split()
    solutions = []
    for code in codes:
        # print(code)
        value = int(code[:3])
        solution = presses_to_solve(code)
        solutions.append((value,solution))
    # print(solutions)
    # print([(i,len(ii)) for i,ii in solutions])
    return sum([v*s for v,s in solutions])
    # return sum([v*len(s) for v,s in solutions])

if __name__ == "__main__":
    with open("input21.txt","r") as f: real_input = f.read()

    # print(f"{main_1(SAMPLE) = }") 
    print(f"{main_1(real_input) = }") # 163840 too high

    # print(f"{main_2(SAMPLE) = }") 
    # print(f"{main_2(real_input) = }")