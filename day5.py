from collections import Counter

sample = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def main_1(text_input: str) -> int:
    rules = {tuple(int(e) for e in line.split("|")) for line in text_input.strip().split() if "|" in line}
    pages = [[int(e) for e in line.split(",")] for line in text_input.strip().split() if "," in line]

    middle_sum = 0
    for book in pages:
        check_set = set()
        for i,p in enumerate(book[:-1]):
            for p2 in book[i+1:]:
                check_set.add((p2,p))
        if check_set & rules: continue # this needs to be empty to be ok
        middle_sum += book[(len(book)//2)]
    
    return middle_sum

def main_2(text_input: str) -> int:
    rules = {tuple(int(e) for e in line.split("|")) for line in text_input.strip().split() if "|" in line}
    pages = [[int(e) for e in line.split(",")] for line in text_input.strip().split() if "," in line]

    middle_sum = 0
    for book in pages:
        
        check_set = set()
        for i,p in enumerate(book[:-1]):
            for p2 in book[i+1:]:
                check_set.add((p2,p))
        if not check_set & rules: continue # if empty, no need to fix
        
        all_possible = set()
        for p1 in book:
            for p2 in book:
                all_possible.add((p1,p2))
        all_possible = all_possible & rules # all possible now holds all applicable rules to this set

        counter = Counter([e[0] for e in all_possible]) # how many times each entry STARTS a rule
        book.sort(key = lambda x: counter[x], reverse=True) # order them by the times they start a rule
        middle_sum += book[len(book)//2]
    
    return middle_sum

if __name__ == "__main__":
    print(f"{main_1(sample) = }")

    with open("input5.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }")

    print(f"{main_2(sample) = }")
    print(f"{main_2(real_input) = }")

