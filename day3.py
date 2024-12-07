import re

def get_sample_input() -> str:
    return """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    
def get_real_input() -> str:
    with open("input3.txt","r") as f: 
        return f.read()
    
def main_1(text_input: str) -> int:
    pattern = r"mul\((\d+),(\d+)\)"
    pairs = re.findall(pattern,text_input)
    return sum([int(i)*int(j) for (i,j) in pairs])

def main_2(text_input: str) -> int:
    pattern = r"(?>(don't)\(\))|(?>(do)\(\))|(?>mul\((\d+),(\d+)\))"
    commands = re.findall(pattern,text_input)
    running_total = 0
    multiply_on = True
    for command in commands:
        if command[1] == "do": 
            multiply_on = True
            continue
        if command[0] == "don't": 
            multiply_on = False
            continue
        if not multiply_on: 
            continue
        running_total += int(command[2]) * int(command[3])
    return running_total


if __name__ == "__main__":
    sample = get_sample_input()
    print(f"{main_1(sample) = }")

    real_input = get_real_input()
    print(f"{main_1(real_input) = }")

    sample2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    print(f"{main_2(sample2) = }")

    real_input = get_real_input()
    print(f"{main_2(real_input) = }")