from functools import lru_cache

SAMPLE = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def main_1(text_input: str) -> int:
    towels,patterns = text_input.strip().split("\n\n")
    towels = set(towels.split(", "))
    max_towel_len = max([len(e) for e in towels])

    patterns = patterns.split()
    patterns_good = []
    for pattern in patterns:
        # print(f"   =   {pattern}")
        frontier = []
        pattern_ok = False
        explored = set()
        frontier.append(pattern)
        while frontier:
            pat = frontier.pop()
            if pat in explored: continue
            explored.add(pat)
            for i in range(1,max_towel_len+1):
                p = pat[:i]
                if p not in towels: continue
                new_p = pat[i:]
                if len(new_p) == 0: 
                    patterns_good.append(pattern)
                    pattern_ok = True
                    break
                frontier.append(new_p)
            if pattern_ok: break
    return len(patterns_good)

@lru_cache
def solve_pattern(pattern: str, towels: set[str], max_len):
    if pattern in towels: return 1
    running_amount = 0
    for i in range(1,max_len+1):
        p = pattern[:i]
        if p not in towels: continue
        running_amount += solve_pattern(pattern)
    return running_amount

def main_2(text_input: str) -> int:
    towels,patterns = text_input.strip().split("\n\n")
    towels = set(towels.split(", "))
    max_towel_len = max([len(e) for e in towels])

    patterns = patterns.split()
    patterns_good = []

    @lru_cache
    def solve_pattern(pattern: str):
        running_amount = 0
        if pattern in towels: running_amount += 1
        for i in range(1,max_towel_len+1):
            p = pattern[:i]
            if p not in towels: continue
            running_amount += solve_pattern(pattern[i:])
        return running_amount

    for pattern in patterns:
        # print(f"== {pattern}")
        solutions = solve_pattern(pattern)
        if solutions: patterns_good.append(solutions)

    # print(patterns_good)
    return sum(patterns_good)

if __name__ == "__main__":
    with open("input19.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }") 
    print(f"{main_1(real_input) = }") 

    print(f"{main_2(SAMPLE) = }") 
    print(f"{main_2(real_input) = }") 