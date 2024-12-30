from collections import defaultdict

SAMPLE = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

class Layout:

    def __init__(self,layout_str: str):
        self._container = [[e for e in row] for row in layout_str.strip().split()]
        for irow, row in enumerate(self._container):
            for icol,letter in enumerate(row):
                if letter=="S":
                    # self._container[irow][icol] = "."
                    self.sx, self.sy = icol,irow
                if letter=="E":
                    # self._container[irow][icol] = "."
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
        if x<0 or x>=self.shape[0] or y < 0 or y >= self.shape[1]:
            return "#"
        return self._container[y][x]
    
    def set(self, x:int, y:int, val: str):
        self._container[y][x] = val

    def __str__(self):
        string = ""
        for row in self._container:
            string += ''.join([str(e) for e in row]) + "\n"
        return string
    
    def __repr__(self):
        return self.__str__()
    
    def crawl_end_to_start(self): # only works on day20
        steps = 0
        x,y = self.end
        directions = [(1,0),(-1,0),(0,-1),(0,1)]
        while True:
            self.set(x,y,steps)
            for dx,dy in directions:
                if self.get(x+dx,y+dy) in {".","S"}:
                    x+=dx
                    y+=dy
                    steps+=1
                    break
            if (x,y) == self.start:
                self.set(x,y,steps)
                break


def main_1(text_input: str, cutoff: int = 100) -> int:
    layout = Layout(text_input)
    layout.crawl_end_to_start()
    x,y = layout.start
    directions = [(1,0),(-1,0),(0,-1),(0,1)]
    shortcuts = defaultdict(int)
    check_spots = set()
    
    for dx0,dy0 in directions:
        for dx1,dy1 in directions:
            check_spots.add((dx0+dx1,dy0+dy1))
            # for dx2,dy2 in directions:
            #     check_spots.add((dx0+dx1+dx2,dy0+dy1+dy2))
    
    while (x,y) != layout.end:
        num_here = layout.get(x,y)
        for dx,dy in check_spots:
            num_there = layout.get(x+dx,y+dy)
            if num_there != "#" and num_here - num_there > 2:
                shortcuts[num_here-num_there - 2] += 1
        for dx,dy in directions:
            nx = dx+x
            ny = dy+y
            if layout.get(nx,ny) == num_here-1:
                x=nx
                y=ny
                break

    return sum([v for k,v in shortcuts.items() if k >= 100])

def main_2(text_input: str, cutoff: int = 100) -> int:
    layout = Layout(text_input)
    layout.crawl_end_to_start()
    x,y = layout.start
    directions = [(1,0),(-1,0),(0,-1),(0,1)]
    shortcuts = defaultdict(int)
    check_spots = set()
    
    for dx in range(21):
        for dy in range(21-dx):
            check_spots.add((dx,dy))
            check_spots.add((-dx,dy))
            check_spots.add((dx,-dy))
            check_spots.add((-dx,-dy))
    
    while (x,y) != layout.end:
        num_here = layout.get(x,y)
        for dx,dy in check_spots:
            dist = abs(dx) + abs(dy)
            num_there = layout.get(x+dx,y+dy)
            if num_there != "#" and num_here - num_there > dist:
                shortcuts[num_here-num_there - dist] += 1
        for dx,dy in directions:
            nx = dx+x
            ny = dy+y
            if layout.get(nx,ny) == num_here-1:
                x=nx
                y=ny
                break
    
    # return {k:v for k,v in shortcuts.items() if k >=50 }
    return sum([v for k,v in shortcuts.items() if k >= 100])

if __name__ == "__main__":
    with open("input20.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }") 
    print(f"{main_1(real_input) = }") 

    print(f"{main_2(SAMPLE) = }") 
    print(f"{main_2(real_input) = }")