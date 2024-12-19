SAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def crawl_plot(gardens: list[list[str]], r: int, c: int, visited: set|None = None ) -> tuple[int,int]:
    val = gardens[r][c]
    if not visited: visited = set()
    area = 1
    borders = 0
    visited.add((r,c))
    for dr,dc in [(-1,0),(0,-1),(0,1),(1,0)]:
        rnew,cnew = r+dr,c+dc
        if (rnew,cnew) in visited: continue
        if (rnew<0 or rnew >= len(gardens) or 
            cnew<0 or cnew >= len(gardens[0]) or 
            gardens[rnew][cnew] != val):
            borders += 1
        else:
            area_extra, borders_extra = crawl_plot(gardens,rnew,cnew,visited)
            area += area_extra
            borders += borders_extra
    gardens[r][c] = "."
    return area, borders

def main_1(text_input: str) -> int:
    gardens = [[e for e in line] for line in text_input.strip().split()]
    cols = len(gardens[0])
    rows = len(gardens)
    score = 0
    for r in range(rows):
        for c in range(cols):
            if gardens[r][c] == ".": continue
            area, borders = crawl_plot(gardens,r,c)
            # print(f"{area = }   {borders = }")
            # for line in gardens:
            #     print(''.join(line))
            # input()
            score += area*borders
    return score

def crawl_plot2(gardens: list[list[str]], r: int, c: int, visited: set|None = None, borders = None ) -> tuple[int,int]:
    val = gardens[r][c]
    if not visited: visited = set()
    area = 1
    if not borders:
        borders = {
            (-1,0): list(),
            (0,-1): list(),
            (0,1): list(),
            (1,0): list()
        }
    visited.add((r,c))
    for dr,dc in [(-1,0),(0,-1),(0,1),(1,0)]:
        rnew,cnew = r+dr,c+dc
        if (rnew,cnew) in visited: continue
        if (rnew<0 or rnew >= len(gardens) or 
            cnew<0 or cnew >= len(gardens[0]) or 
            gardens[rnew][cnew] != val):
            borders[(dr,dc)].append((rnew,cnew))
        else:
            area_extra, borders_extra = crawl_plot2(gardens,rnew,cnew,visited,borders)
            area += area_extra
            # borders += borders_extra
    gardens[r][c] = "."
    return area, borders

def calc_sides(borders) -> int:
    sides = 0
    
    nodes = borders[(-1,0)] # upper boundary, needs c neighbors
    rows_distinct = {r for r,c in nodes}
    for row in rows_distinct:
        vals = [c for r,c in nodes if r==row]
        vals.sort()
        gaps=0
        for ix,val in enumerate(vals[:-1]):
            if vals[ix+1]-val>1: gaps+=1
        sides += 1 + gaps

    nodes = borders[(1,0)] # lower boundary, needs c neighbors
    rows_distinct = {r for r,c in nodes}
    for row in rows_distinct:
        vals = [c for r,c in nodes if r==row]
        vals.sort()
        gaps=0
        for ix,val in enumerate(vals[:-1]):
            if vals[ix+1]-val>1: gaps+=1
        sides += 1 + gaps

    nodes = borders[(0,-1)] # left boundary, needs r neighbors
    cols_distinct = {c for r,c in nodes}
    for col in cols_distinct:
        vals = [r for r,c in nodes if c==col]
        vals.sort()
        gaps=0
        for ix,val in enumerate(vals[:-1]):
            if vals[ix+1]-val>1: gaps+=1
        sides += 1 + gaps

    nodes = borders[(0,1)] # right boundary, needs r neighbors
    cols_distinct = {c for r,c in nodes}
    for col in cols_distinct:
        vals = [r for r,c in nodes if c==col]
        vals.sort()
        gaps=0
        for ix,val in enumerate(vals[:-1]):
            if vals[ix+1]-val>1: gaps+=1
        sides += 1 + gaps

    return sides

def main_2(text_input: str) -> int:
    gardens = [[e for e in line] for line in text_input.strip().split()]
    cols = len(gardens[0])
    rows = len(gardens)
    score = 0
    for r in range(rows):
        for c in range(cols):
            if gardens[r][c] == ".": continue
            area, borders = crawl_plot2(gardens,r,c)
            # print(borders)
            sides = calc_sides(borders)
            # print(f"{area = }   {sides = }")
            # for line in gardens:
            #     print(''.join(line))
            # input()
            score += area*sides
    return score

if __name__ == "__main__":

    print(f"{main_1(SAMPLE) = }")

    with open("input12.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }")

    print(f"{main_2(SAMPLE) = }")
    print(f"{main_2(real_input) = }")