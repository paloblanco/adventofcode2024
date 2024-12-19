SAMPLE = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

class Layout:

    def __init__(self,layout_str: str):
        self._container = [[e for e in row] for row in layout_str.split()]
        for irow, row in enumerate(self._container):
            for icol,letter in enumerate(row):
                if letter=="@":
                    self._container[irow][icol] = "."
                    self.rx, self.ry = icol,irow

    def expand(self):
        new_container = []
        for row in self._container:
            new_row = []
            for letter in row:
                if letter == BOX:
                    new_row += [BOXL, BOXR]
                else:
                    new_row += [letter,letter]
            new_container.append(new_row)
        self._container = new_container
        self.rx *= 2
    
    @property
    def rstart(self):
        return self.rx,self.ry

    @property                
    def shape(self):
        return len(self._container[0]),len(self._container)
                
    def get(self, x:int, y:int):
        return self._container[y][x]
    
    def set(self, x:int, y:int, val: str):
        self._container[y][x] = val

    @property
    def score(self) -> int:
        score = 0
        sx, sy = self.shape
        for xx in range(sx):
            for yy in range(sy):
                if self.get(xx,yy) == BOX or self.get(xx,yy) == BOXL:
                    score += 100*yy + xx
        return score
    
    def __str__(self):
        string = ""
        for row in self._container:
            string += ''.join(row) + "\n"
        return string
    
    def __repr__(self):
        return self.__str__()

WALL = "#"
BOX = "O"
FREE = "."

BOXL = "["
BOXR = "]"
BOXES = {BOXL,BOXR}

def main_1(text_input: str) -> int:
    layout_str, instructions_str = text_input.strip().split("\n\n")
    layout = Layout(layout_str)
    rx, ry = layout.rstart
    instructions = "".join(instructions_str.split())
    directions = {
        "^":(0,-1),
        "<":(-1,0),
        ">":(1,0),
        "v":(0,1)
    }
    instructions = [directions[i] for i in instructions]
    for dx,dy in instructions:
        xcheck,ycheck = rx+dx, ry+dy
        tile = layout.get(xcheck,ycheck)
        
        if tile == WALL: continue
        
        if tile == FREE:
            rx += dx
            ry += dy
            continue

        box_list = []
        while tile == BOX:
            box_list.append((xcheck,ycheck))
            xcheck += dx
            ycheck += dy
            tile = layout.get(xcheck,ycheck)

        if tile == WALL:
            continue

        if tile == FREE:
            for bx,by in box_list[::-1]:
                layout.set(bx,by,FREE) # should move last first so this is OK
                layout.set(bx+dx,by+dy,BOX)
            rx += dx
            ry += dy
            continue
    return layout.score

def main_2(text_input: str) -> int:
    layout_str, instructions_str = text_input.strip().split("\n\n")
    layout = Layout(layout_str)
    layout.expand()
    # print(layout)
    rx, ry = layout.rstart
    instructions = "".join(instructions_str.split())
    directions = {
        "^":(0,-1),
        "<":(-1,0),
        ">":(1,0),
        "v":(0,1)
    }
    instructions = [directions[i] for i in instructions]

    for dx,dy in instructions:
        xcheck,ycheck = rx+dx, ry+dy
        tile = layout.get(xcheck,ycheck)
        
        if tile == WALL: continue
        
        if tile == FREE:
            rx += dx
            ry += dy
            continue

        if dy == 0: # the same for left right movement
            box_list = []
            while tile in BOXES:
                box_list.append((xcheck,ycheck))
                xcheck += dx
                ycheck += dy
                tile = layout.get(xcheck,ycheck)

            if tile == WALL:
                continue

            if tile == FREE:
                for bx,by in box_list[::-1]:
                    character = layout.get(bx,by)
                    layout.set(bx,by,FREE) # should move last first so this is OK
                    layout.set(bx+dx,by+dy,character)
                rx += dx
                ry += dy
                continue
        
        else:
            check_set = {(xcheck,ycheck)}
            box_to_move_set = set()
            move_succeed = True
            while check_set:
                xcheck,ycheck = check_set.pop()
                tile = layout.get(xcheck,ycheck)
                if tile==FREE: continue
                if tile == WALL:
                    move_succeed = False
                    break
                if tile == BOXL:
                    box_to_move_set.add((xcheck,ycheck))
                    check_set.add((xcheck,ycheck+dy))
                    check_set.add((xcheck+1,ycheck+dy))
                if tile == BOXR:
                    box_to_move_set.add((xcheck-1,ycheck))
                    check_set.add((xcheck,ycheck+dy))
                    check_set.add((xcheck-1,ycheck+dy))
            if not move_succeed: continue
            rx += dx
            ry += dy
            for xx,yy in box_to_move_set:
                layout.set(xx,yy,FREE)
                layout.set(xx+1,yy,FREE)
            for xx,yy in box_to_move_set:
                layout.set(xx+dx,yy+dy,BOXL)
                layout.set(xx+1+dx,yy+dy,BOXR)
    
    print(layout)
    return layout.score


if __name__ == "__main__":
    
    with open("input15.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }")
    print(f"{main_1(real_input) = }")

    print(f"{main_2(SAMPLE) = }")
    print(f"{main_2(real_input) = }")