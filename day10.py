from collections import deque

class Queue:
    def __init__(self):
        self._container = deque([])

    def push(self,val):
        self._container.append(val)

    def pop(self):
        return self._container.popleft()
    
    def __len__(self):
        return len(self._container)
    
    def is_empty(self):
        return len(self._container)==0

SAMPLE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def count_trailheads(r: int, c: int, hike_map: list[list[int]]) -> int:
    if hike_map[r][c] != 0: return 0
    frontier = Queue()
    seen = {} # dict r,c tuples keys are height
    found_peaks = set() #set of r,c tuples
    frontier.push((r,c))
    seen[(r,c)] = hike_map[r][c]
    while not frontier.is_empty():
        r0,c0 = frontier.pop()
        height0 = hike_map[r0][c0]
        for (dr,dc) in [(-1,0),(1,0),(0,-1),(0,1)]:
            r1 = r0+dr
            c1 = c0+dc
            if (r1,c1) in seen: continue
            if r1<0 or r1 >= len(hike_map) or c1 < 0 or c1 >= len(hike_map[0]): continue
            height1 = hike_map[r1][c1]
            if height1 != height0 + 1: continue
            if height1 == 9:
                found_peaks.add((r1,c1))
                continue
            frontier.push((r1,c1))
            seen[(r1,c1)] = height1
    return len(found_peaks)

def count_trailheads_rating(r: int, c: int, hike_map: list[list[int]]) -> int:
    if hike_map[r][c] != 0: return 0
    frontier = Queue()
    found_peaks = list() #set of r,c tuples
    frontier.push((r,c))
    while not frontier.is_empty():
        r0,c0 = frontier.pop()
        height0 = hike_map[r0][c0]
        for (dr,dc) in [(-1,0),(1,0),(0,-1),(0,1)]:
            r1 = r0+dr
            c1 = c0+dc
            if r1<0 or r1 >= len(hike_map) or c1 < 0 or c1 >= len(hike_map[0]): continue
            height1 = hike_map[r1][c1]
            if height1 != height0 + 1: continue
            if height1 == 9:
                found_peaks.append((r1,c1))
                continue
            frontier.push((r1,c1))
    return len(found_peaks)


def main_1(text_input: str) -> int:
    hike_map = [[int(ee) for ee in e] for e in text_input.strip().split()]
    # print(hike_map)
    trailheads = []
    for ix_row,row in enumerate(hike_map):
        for ix_col,letter in enumerate(row):
            if letter != 0: continue
            trailheads.append(count_trailheads(ix_row,ix_col,hike_map))
    return sum(trailheads)

def main_2(text_input: str) -> int:
    hike_map = [[int(ee) for ee in e] for e in text_input.strip().split()]
    # print(hike_map)
    trailheads = []
    for ix_row,row in enumerate(hike_map):
        for ix_col,letter in enumerate(row):
            if letter != 0: continue
            trailheads.append(count_trailheads_rating(ix_row,ix_col,hike_map))
    return sum(trailheads)

if __name__ == "__main__":
    print(f"{main_1(SAMPLE) = }")

    with open("input10.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }") # 852 too high

    print(f"{main_2(SAMPLE) = }")
    print(f"{main_2(real_input) = }") 