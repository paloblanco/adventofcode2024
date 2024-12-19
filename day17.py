import re

SAMPLE = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

SAMPLE2 = """Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

SAMPLE3 = """Register A: 192
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

TEST_ANSWER = """4,6,3,5,6,3,5,2,1,0"""

################
# REGISTER
###############

A = 0
B = 0
C = 0
P = 0 # pointer


def initialize_computer(a: int, b: int, c: int) -> None:
    global A,B,C,P
    A = a
    B = b
    C = c
    P = 0

REG = r"""Register A: (\d+)
Register B: (\d+)
Register C: (\d+)

Program: ([\d,]+)"""

def adv(op):
    global A,B,C,P
    if op > 3:
        match op:
            case 4: op=A
            case 5: op=B
            case 6: op=C
    A = A // (2**op)

def bxl(op):
    global A,B,C,P
    B = B ^ op

def bst(op):
    global A,B,C,P
    if op > 3:
        match op:
            case 4: op=A
            case 5: op=B
            case 6: op=C
    B = op % 8

def jnz(op):
    global A,B,C,P
    if A == 0: return
    P = op - 2

def bxc(op):
    global A,B,C,P
    B = B ^ C

def out(op):
    global A,B,C,P
    if op > 3:
        match op:
            case 4: op=A
            case 5: op=B
            case 6: op=C
    return op % 8

def bdv(op):
    global A,B,C,P
    if op > 3:
        match op:
            case 4: op=A
            case 5: op=B
            case 6: op=C
    B = A // (2**op)

def cdv(op):
    global A,B,C,P
    if op > 3:
        match op:
            case 4: op=A
            case 5: op=B
            case 6: op=C
    C = A // (2**op)

OPS = [adv,bxl, bst, jnz, bxc, out, bdv, cdv]

def main_1(text_input: str) -> int:
    global A,B,C,P,OPS
    a,b,c,p = re.findall(REG,text_input)[0]
    a = 67451919
    initialize_computer(int(a),int(b),int(c))
    program = [int(e) for e in p.split(",")]
    results = []
    while P < len(program):
        print(f"{A = }")
        print(f"{bin(A) = }")
        instruction = program[P]
        operand = program[P+1]
        operator = OPS[instruction]
        result = operator(operand)
        if result is not None: 
            results.append(result)
            print(f"{A,B,C,P = }   {results = }")
            input()
        P += 2
    return ",".join([str(r) for r in results])

from collections import deque
from dataclasses import dataclass, field
from heapq import heappush,heappop

class Queue:
    def __init__(self, starter: None|list = None):
        if not starter:
            self._container = deque([])
        else:
            self._container = deque(starter)

    def push(self,val):
        self._container.append(val)

    def pop(self):
        return self._container.popleft()
    
    def __len__(self):
        return len(self._container)
    
    def is_empty(self):
        return len(self._container)==0


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

@dataclass    
class Tup:
    val: tuple

    def __lt__(self,other):
        if len(self.val) < len(other.val):
            return True
        elif len(self.val) > len(other.val):
            return False
        else:
            return self.get_a() < other.get_a()
    
    def get_a(self):
        aa = 0
        for i,n in enumerate(self.val):
            aa += n * (2**i)
        return aa
    
    def __len__(self):
        return len(self.val)
    
    def __str__(self):
        return str(self.val)
    
    def __repr__(self):
        return str(self.val)
    
    def __add__(self,other):
        return Tup(self.val + other.val)
    

def main_2(text_input: str) -> int:
    global A,B,C,P,OPS
    a,b,c,p = re.findall(REG,text_input)[0]
    initialize_computer(int(a),int(b),int(c))
    new_tuples = (
        (0,0,0),
        (1,0,0),
        (0,1,0),
        (1,1,0),
        (0,0,1),
        (1,0,1),
        (0,1,1),
        (1,1,1)
    )
    new_tuples = [Tup(t) for t in new_tuples]
    program = tuple(int(e) for e in p.split(","))
    frontier = PQueue([t for t in new_tuples]) # will push 8 bits at a time
    closest_len = 0
    def a_from_tuple(t) -> int:
        aa = 0
        for i,n in enumerate(t):
            aa += n * (2**i)
        return aa

    while frontier:
        a_tup: Tup = frontier.pop()
        loops = len(a_tup)//3
        a_trial = a_tup.get_a()
        # print(f"{a_trial = }")
        # print(f"{a_tup = }")
        initialize_computer(a_trial,0,0)
        # print(f"{A,B,C,P = }")
        results = []
        while P < len(program):
            instruction = program[P]
            operand = program[P+1]
            operator = OPS[instruction]
            result = operator(operand)
            # print(f"{A,B,C,P = }  {instruction = }  {operator.__name__}  {operand = }")
            if result is not None: 
                results.append(result)
                # print(f"{a_trial=}     {A,B,C,P = }   {results = }")
                if len(results) > 2 and (tuple(results)[:-2] != program[:len(results)-2]):
                    break # early kill
                if (len(results) >= loops) or A==0: #program will terminate next, add children to frontier
                    
                    new_tups = [a_tup + b for b in new_tuples]
                    for n in new_tups: frontier.push(n)
                    if len(results) >= closest_len:
                        closest_len = len(results)
                        print("BEST SO FAR")
                        print(f"{a_trial = }")
                        print(f"{a_tup = }")
                        print(f"{len(frontier)}")
                    # print(f"======MATCH========")
                    # print(f"{a_trial=}     {A,B,C,P = }   {results = }")
                    # print(f"{bin(a_trial) = }")
                    # print(f"{a_tup = }")
                    # print(frontier)
                    # input()
            P += 2
        if tuple(results) == program:
            return a_trial
        

if __name__ == "__main__":
    with open("input17.txt","r") as f: real_input = f.read()

    # print(f"{main_1(SAMPLE2) = }") #4,6,3,5,6,3,5,2,1,0
    # print(f"{main_1(SAMPLE3) = }") #4,6,3,5,6,3,5,2,1,0
    # print(f"{main_1(real_input) = }") 

    # print(f"{main_2(SAMPLE2) = }") #117_440, 0b11100101011000000
    print(f"{main_2(real_input) = }") # 441_000_000 too low