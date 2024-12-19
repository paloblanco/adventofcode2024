SAMPLE = """125 17"""
from collections import defaultdict

"""If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone."""

class Stone:

    def __init__(self, number: int):
        self.number = number
        self.prev = None
        self.next = None

    def assign_prev(self, other: "Stone"):
        self.prev = other
        if other: other.next = self

    def assign_next(self, other: "Stone"):
        self.next = other
        if other: other.prev = self

    def split(self) -> "Stone":
        half_len = len(self) // 2
        num_left = int(str(self.number)[:half_len])
        num_right = int(str(self.number)[half_len:])
        # stone_left = Stone(num_left)
        self.number = num_left
        stone_right = Stone(num_right)
        # stone_left.assign_prev(self.prev)
        stone_right.assign_next(self.next)
        self.assign_next(stone_right)
        return stone_right.next
    
    def __len__(self) -> int:
        return len(str(self.number))
    
    def __str__(self) -> str:
        return str(self.number)
    
    def __repr__(self) -> str:
        return str(self.number)
    

def main_1(text_input: str, loops: int = 25) -> int:
    stone_list = [int(e) for e in text_input.strip().split()]
    stone_list = [Stone(e) for e in stone_list]
    for ix,stone in enumerate(stone_list[:-1]):
        stone.assign_next(stone_list[ix+1])
    root = stone_list[0]
    print(stone_list)
    for loop in range(loops):
        # print(loop)
        stone = root
        while stone:
            if stone.number == 0:
                stone.number = 1
                stone = stone.next
            elif len(stone) % 2 == 0:
                stone = stone.split()
            else:
                stone.number *= 2024
                stone = stone.next
    # count
    stone = root
    stone_count = 0
    while stone:
        stone_count += 1
        stone = stone.next
    
    return stone_count

def main_2(text_input: str, loops: int = 25) -> int:
    
    counter = defaultdict(int,{int(e):1 for e in text_input.strip().split()})

    for loop in range(loops):
        new_counter = defaultdict(int)
        for k,v in counter.items():
            if k==0:
                new_counter[1] += v
            elif len(str(k))%2==0:
                half = len(str(k))//2
                left = int(str(k)[:half])
                right = int(str(k)[half:])
                new_counter[left] += v
                new_counter[right] += v
            else:
                new_counter[k*2024] += v
        counter = new_counter

    return sum(counter.values())


if __name__ == "__main__":
    print(f"{main_1(SAMPLE, 25) = }")

    with open("input11.txt","r") as f: real_input = f.read()
    # print(f"{main_1(real_input) = }")

    print(f"{main_2(real_input, 75) = }")