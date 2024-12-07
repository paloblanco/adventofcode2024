def get_sample_input() -> str:
    return """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    
def get_real_input() -> str:
    with open("input2.txt","r") as f: 
        return f.read()

def is_safe_simple(r: list[int]) -> bool:
    if len(r) < 2: return True
    direction = r[0] < r[1]
    for current,prev in zip(r[:-1],r[1:]):
        if current == prev: return False
        if (current < prev) != direction: return False
        if abs(current - prev) > 3 or abs(current - prev) < 1: return False
    return True

def is_safe_brute(r: list[int]) -> bool:
    if is_safe_simple(r): return True
    for ix in range(len(r)):
        if is_safe_simple(r[:ix] + r[ix+1:]): return True
    return False

def main_1(text_input: str) -> int:
    reports = [[int(ee) for ee in e.split()] for e in text_input.split("\n") if e]
    safe_count = 0
    for r in reports:
        safe = is_safe_simple(r)
        if safe: safe_count += 1
    return safe_count

def main_2(text_input: str) -> int:
    reports = [[int(ee) for ee in e.split()] for e in text_input.split("\n") if e]
    safe_count = 0
    for r in reports:
        safe = is_safe_brute(r)
        if safe: safe_count += 1
    return safe_count

if __name__ == "__main__":
    sample = get_sample_input()
    print(f"{main_1(sample) = }") 

    real_1 = get_real_input()
    print(f"{main_1(real_1) = }") # 513 is too low

    sample = get_sample_input()
    print(f"{main_2(sample) = }") 

    real_1 = get_real_input()
    print(f"{main_2(real_1) = }") # 513 is too low