def get_sample_input() -> str:
    return """3   4
4   3
2   5
1   3
3   9
3   3"""
    
def get_real_input() -> str:
    with open("input1.txt","r") as f: 
        return f.read()

def main_1(text_input: str) -> int:
    numbers = [int(e) for e in text_input.split()]
    l1 = numbers[::2]
    l2 = numbers[1::2]
    l1.sort()
    l2.sort()
    return sum([abs(first-second) for first,second in zip(l1,l2)])

def main_2(text_input: str) -> int:
    numbers = [int(e) for e in text_input.split()]
    l1 = numbers[::2]
    l2 = numbers[1::2]
    l3 = [i*l2.count(i) for i in l1]
    return sum(l3)


if __name__ == "__main__":
    sample = get_sample_input()
    print(f"{main_2(sample) = }")

    real_1 = get_real_input()
    print(f"{main_2(real_1) = }")