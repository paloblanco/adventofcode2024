SAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def main_1(text_input: str) -> int:
    map_obstacles = text_input.strip().split()
    obstacles = set()

    for y,row in enumerate(map_obstacles):
        for x,letter in enumerate(row):
            if letter == "#":
                obstacles.add((x,y))
            if letter == "^":
                guard_x = x
                guard_y = y

    dx = 0
    dy = -1

    next_directions = {
        (0,-1):(1,0),
        (1,0):(0,1),
        (0,1):(-1,0),
        (-1,0):(0,-1)
    }

    visited_set = set()
    
    while (0 <= guard_x < len(map_obstacles[0])) and (0 <= guard_y < len(map_obstacles)):
        visited_set.add((guard_x,guard_y))
        
        while (guard_x+dx,guard_y+dy) in obstacles:
            dx,dy = next_directions[(dx,dy)]

        guard_x += dx
        guard_y += dy

    return len(visited_set)

def main_2(text_input: str) -> int:
    map_obstacles = text_input.strip().split()
    obstacles = set()

    for y,row in enumerate(map_obstacles):
        for x,letter in enumerate(row):
            if letter == "#":
                obstacles.add((x,y))
            if letter == "^":
                guard_x = x
                guard_y = y

    dx = 0
    dy = -1
    guard_x0 = guard_x
    guard_y0 = guard_y

    next_directions = {
        (0,-1):(1,0),
        (1,0):(0,1),
        (0,1):(-1,0),
        (-1,0):(0,-1)
    }

    visited_set = set()
    
    next_steps = []
    while (0 <= guard_x < len(map_obstacles[0])) and (0 <= guard_y < len(map_obstacles)):
        visited_set.add((guard_x,guard_y))
        
        while (guard_x+dx,guard_y+dy) in obstacles:
            dx,dy = next_directions[(dx,dy)]

        guard_x += dx
        guard_y += dy

        next_steps.append((guard_x,guard_y))

    # go through visited set and put down new obstacles. see if they result in a loop.
    loop_locations = set()
    # print(visited_set)
    visited_set.remove((guard_x0,guard_y0))
    next_steps = [e if e != (guard_x0,guard_y0) else (-2,-2) for e in next_steps]
    
    for ix,block in enumerate(next_steps):
        visited_lookup = {}
        guard_x = guard_x0
        guard_y = guard_y0
        dx = 0
        dy = -1
        current_step = 0
        obstacles.add(block)
        while (0 <= guard_x < len(map_obstacles[0])) and (0 <= guard_y < len(map_obstacles)):
            # if current_step == ix: obstacles.add(block)
            
            if visited_lookup.get((guard_x,guard_y),(0,0)) == (dx,dy):
                loop_locations.add(block)
                # print(f"     BLOCKED: {block}")
                break

            visited_lookup[(guard_x,guard_y)] = (dx,dy)
            
            while (guard_x+dx,guard_y+dy) in obstacles:
                dx,dy = next_directions[(dx,dy)]

            guard_x += dx
            guard_y += dy
            current_step += 1
        # print((guard_x,guard_y))
        obstacles.remove(block)

    return len(loop_locations)
    

if __name__ == "__main__":
    print(f"{main_1(SAMPLE) = }")

    with open("input6.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }")

    print(f"{main_2(SAMPLE) = }")
    print(f"{main_2(real_input) = }") # 1893 is too low, 2149 too high

    """
    7, 7)
(3, 6)
(1, 8)
(7, 9)
(6, 7)
(3, 8)
"""