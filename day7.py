SAMPLE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def valid(test_value: int, numbers: list[int]) -> bool:
    frontier = [numbers[0]]
    for n in numbers[1:]:
        new_frontier = []
        for f in frontier:
            f_next = f+n
            if f_next <= test_value: 
                new_frontier.append(f_next)
            
            f_next = f*n
            if f_next <= test_value:
                new_frontier.append(f_next)

            f_next = int(f"{f}{n}")
            if f_next <= test_value:
                new_frontier.append(f_next)
            
        frontier = new_frontier
    # print(frontier)
    return test_value in frontier

def main_1(text_input: str) -> int:
    rows = text_input.strip().split("\n")
    test_values = [int(e.split(":")[0]) for e in rows]
    numbers = [[int(ee) for ee in e.split(":")[1].split()] for e in rows]
    valid_tests = []
    for t,n in zip(test_values,numbers):
        if valid(t,n): valid_tests.append(t)
    return sum(valid_tests)


if __name__ == "__main__":
    print(f"{main_1(SAMPLE) = }")

    with open("input7.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }")