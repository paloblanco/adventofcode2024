from collections import defaultdict

SAMPLE = """1
10
100
2024"""

SAMPLE2 = """1
2
3
2024"""

def main_1(text_input: str) -> int:
    secrets = text_input.strip().split()
    solutions = []
    for s in secrets:
        s = int(s)
        for i in range(2000):
            s = ((s*64) ^ s) % 16777216
            s = ((s//32) ^ s) % 16777216
            s = ((s*2048) ^ s) % 16777216
        solutions.append(s)
    # print(solutions)
    return sum(solutions)


def main_2(text_input: str) -> int:
    secrets = text_input.strip().split()
    solutions = []
    trends = defaultdict(int)
    for s in secrets:
        s = int(s)
        running_tuple = ()
        this_monkey_see = set()
        prev = s%10
        for i in range(2000):
            s = ((s*64) ^ s) % 16777216
            s = ((s//32) ^ s) % 16777216
            s = ((s*2048) ^ s) % 16777216
            price = s%10
            if len(running_tuple) < 4:
                running_tuple = running_tuple + (price-prev,)
                if len(running_tuple) == 4:
                    if running_tuple not in this_monkey_see:
                        trends[running_tuple] += price
                        this_monkey_see.add(running_tuple)
                prev = price
                continue
            # only reach this if you are valid so far
            running_tuple = running_tuple[1:] + (price-prev,)
            if running_tuple not in this_monkey_see:
                trends[running_tuple] += price
                this_monkey_see.add(running_tuple)
            prev = price
        # solutions.append(s)
    # print(solutions)
    trend_pairs = [(k,v) for k,v in trends.items()]
    trend_pairs.sort(key = lambda x: x[1], reverse=True)
    # return trend_pairs[0][1]
    return trend_pairs[:5]


if __name__ == "__main__":
    with open("input22.txt","r") as f: real_input = f.read()

    # print(f"{main_1(SAMPLE) = }") 
    # print(f"{main_1(real_input) = }") 

    print(f"{main_2("123") = }") 
    print(f"{main_2(SAMPLE2) = }") 
    print(f"{main_2(real_input) = }") # 1974 too high