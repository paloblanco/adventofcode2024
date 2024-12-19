from dataclasses import dataclass, field
from heapq import heappush,heappop


SAMPLE = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

@dataclass
class PQueue:
    _container: list = field(default_factory=list)

    def push(self, node):
        heappush(self._container, node)

    def pop(self):
        return heappop(self._container)

    @property
    def empty(self) -> bool:
        return len(self._container) <= 0


class Layout:
    def __init__(self,layout_str: str):
        self._container = [[e for e in row] for row in layout_str.strip().split()]
        for irow, row in enumerate(self._container):
            for icol,letter in enumerate(row):
                if letter=="S":
                    self._container[irow][icol] = "."
                    self.sx, self.sy = icol,irow
                if letter=="E":
                    self._container[irow][icol] = "."
                    self.ex, self.ey = icol,irow
    
    @property
    def start(self):
        return self.sx,self.sy
    
    @property
    def end(self):
        return self.ex,self.ey

    @property                
    def shape(self):
        return len(self._container[0]),len(self._container)
                
    def get(self, x:int, y:int):
        return self._container[y][x]
    
    def set(self, x:int, y:int, val: str):
        self._container[y][x] = val

    def __str__(self):
        string = ""
        for row in self._container:
            string += ''.join(row) + "\n"
        return string
    
    def __repr__(self):
        return self.__str__()


@dataclass
class State:
    x: int
    y: int
    direction: tuple[int,int]
    score: int
    parent: 'State' = None

    def __lt__(self, other):
        return self.score < other.score
    
    @property
    def location(self):
        return self.x,self.y
    
TURNS = {
    (1,0): [(0,-1),(0,1)],
    (-1,0): [(0,-1),(0,1)],
    (0,1): [(1,0),(-1,0)],
    (0,-1): [(1,0),(-1,0)],
}

EMPTY = "."
WALL  = "#"

def main_1(text_input: str) -> int:
    layout = Layout(text_input)
    explored = dict() # x,y,dx,dy tuples, score values
    frontier = PQueue()

    start = State(layout.sx, layout.sy, (1,0),0)
    end = layout.end

    frontier.push(start)
    # explored.add(layout.start)
    space = start
    explored[(space.x,space.y,space.direction[0],space.direction[1])] = space.score

    # winner = None

    first_win = False # found a value yet?
    winning_score = None
    winners = list()
    while not frontier.empty:
        space: State = frontier.pop()
        if (space.x,space.y,space.direction[0],space.direction[1]) in explored:
            if explored[(space.x,space.y,space.direction[0],space.direction[1])] < space.score:
                continue
        else:
            explored[(space.x,space.y,space.direction[0],space.direction[1])] = space.score
        # layout.set(space.x,space.y,"X")
        # print(layout)
        # print(f"{space.direction = }")
        # input()
        
        if space.location == end:
            if not first_win:
                winners.append(space)
                winning_score = space.score
                first_win = True
            else:
                if space.score > winning_score:
                    break
                else:
                    winners.append(space)
            # break

        x,y = space.location
        dx, dy = space.direction
        tile = layout.get(x+dx,y+dy)
        if tile == EMPTY and (x+dx,y+dy) not in explored:
            new_state = State(x+dx,y+dy,(dx,dy),space.score+1, space)
            frontier.push(new_state)

        for dx,dy in TURNS[space.direction]:
            new_state = State(x,y,(dx,dy),space.score+1000, space)
            frontier.push(new_state)
        
        # layout.set(space.x,space.y,"0")

    if winners:
        spots = set()

        for winner in winners:
            while winner:
                layout.set(winner.x,winner.y,"0")
                spots.add(winner.location)
                winner = winner.parent
        print(layout)
        return len(spots)


if __name__ == "__main__":
    
    with open("input16.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }")
    print(f"{main_1(real_input) = }") # 470 too low