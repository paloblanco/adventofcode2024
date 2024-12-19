from collections import defaultdict, deque

SAMPLE = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

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
    
    def __str__(self):
        return str(self._container)
    
    def __repr__(self):
        return self.__str__()
    
def print_walls(walls,s):
    layout = ""
    for y in range(-1,s+2):
        for x in range(-1,s+2):
            if (x,y) in walls:
                layout +="#"
            else:
                layout += "."
        layout += "\n"
    print(layout)
   

def main_1(text_input: str, wall_count: int = 12, size: int = 6) -> int:
    walls = [tuple(int(ee) for ee in e.split(",")) for e in text_input.strip().split("\n")]
    walls = set(walls[:wall_count])
    for bound in range(0,size+2):
        walls.add((-1,bound))
        walls.add((size+1,bound))
        walls.add((bound,-1))
        walls.add((bound,size+1))
    print_walls(walls,size)
    frontier = Queue()
    start = (0,0)
    frontier.push(start)
    explored = {start:0} #values are steps
    directions = [
        (1,0),
        (-1,0),
        (0,1),
        (0,-1)
    ]
    while frontier:
        # print(frontier)
        # input()
        location = frontier.pop()
        steps = explored[location]
        if location == (size,size):
            return steps
        for dx,dy in directions:
            nx,ny = location[0]+dx,location[1]+dy
            new_loc = (nx,ny)
            if new_loc in explored or new_loc in walls:
                continue
            frontier.push(new_loc)
            explored[new_loc] = steps+1

def main_2(text_input: str, wall_count: int = 12, size: int = 6) -> int:
    walls_original = [tuple(int(ee) for ee in e.split(",")) for e in text_input.strip().split("\n")]
    walls = set(walls_original)
    wall_removed = None
    for bound in range(0,size+2):
        walls.add((-1,bound))
        walls.add((size+1,bound))
        walls.add((bound,-1))
        walls.add((bound,size+1))

    print_walls(walls,size)

    while True:
        solved = False
        frontier = Queue()
        start = (0,0)
        frontier.push(start)
        explored = {start:0} #values are steps
        directions = [
            (1,0),
            (-1,0),
            (0,1),
            (0,-1)
        ]
        while frontier:
            # print(frontier)
            # input()
            location = frontier.pop()
            steps = explored[location]
            if location == (size,size):
                solved = steps
                break
            for dx,dy in directions:
                nx,ny = location[0]+dx,location[1]+dy
                new_loc = (nx,ny)
                if new_loc in explored or new_loc in walls:
                    continue
                frontier.push(new_loc)
                explored[new_loc] = steps+1
        if solved:
            return wall_removed
        else:
            wall_removed = walls_original.pop()
            walls.remove(wall_removed)

if __name__ == "__main__":
    with open("input18.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }") 
    print(f"{main_1(real_input, wall_count=1024, size=70) = }") 

    print(f"{main_2(SAMPLE) = }") 
    print(f"{main_2(real_input, wall_count=1024, size=70) = }") 