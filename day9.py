SAMPLE = """2333133121414131402"""

def main_1(text_input: str) -> int:
    list_input = [int(e) for e in text_input.strip()]
    indices_blanks = []
    decompressed = []
    for ix, num in enumerate(list_input):
        even = ix%2==0
        if even:
            ix_data = ix//2
            decompressed += [ix_data,]*num
        else:
            index_current = len(decompressed)
            blanks = [".",] * num
            indices_blanks += list(range(index_current,index_current+len(blanks)))
            decompressed += blanks
    
    indices_blanks = indices_blanks[::-1]
    while indices_blanks:
        next_blank = indices_blanks.pop()
        if next_blank>=len(decompressed): break
        next_digit = "."
        while next_digit == ".":
            next_digit = decompressed.pop()
        decompressed[next_blank] = next_digit
    
    muls = [ix*num for ix,num in enumerate(decompressed) if num != "."]

    return sum(muls)

class Chunk:
    def __init__(self, data: list[int], blank: bool =False):
        self.data = data
        self.blank = blank
        self.prev = None
        self.next = None
        self.moved = False

    def __len__(self):
        return len(self.data)
    
    def assign_next(self, other):
        self.next = other
        if other: other.prev = self

    def assign_prev(self,other):
        self.prev = other
        if other: other.next = self

    def replace(self,other):
        self.assign_next(other.next)
        self.assign_prev(other.prev)

    def insert_self_after(self,other):
        next_one = other.next
        self.assign_prev(other)
        self.assign_next(next_one)

    def yoink(self):
        replacement = Chunk([".",]*len(self),True)
        replacement.replace(self)
        self.moved=True

def main_2(text_input: str) -> int:
    list_input = [int(e) for e in text_input.strip()]
    print(list_input)
    prev_chunk = None
    chunks_to_move = []
    for ix, num in enumerate(list_input):
        even = ix%2==0
        if even:
            ix_data = ix//2
            data = [ix_data,]*num
            chunk = Chunk(data)
            chunks_to_move.append(chunk)
        else:
            blanks = [".",] * num
            if num <= 0: continue
            chunk = Chunk(blanks,True)
        if prev_chunk:
            prev_chunk.next = chunk
            chunk.prev = prev_chunk
        else:
            root = chunk
        prev_chunk = chunk

    chunks_to_move = chunks_to_move[::-1]
    print([c.data for c in chunks_to_move])

    # while chunk:
    for chunk in chunks_to_move:
        # chunk_check_next = chunk.prev
        # if chunk.moved:
        #     chunk = chunk_check_next
        #     continue
        check_chunk = root
        while check_chunk != chunk:
            if (not check_chunk.blank):
                check_chunk = check_chunk.next
                continue
            if len(check_chunk) < len(chunk):
                check_chunk = check_chunk.next
                continue
            new_len = len(check_chunk) - len(chunk)
            if new_len == 0:
                chunk.yoink()
                chunk.replace(check_chunk)
                break
            else:
                chunk.yoink()
                chunk.replace(check_chunk)
                blank_chunk = Chunk(["."]*new_len,True)
                blank_chunk.insert_self_after(chunk)
                break
        # chunk = chunk_check_next
    
    c = root
    decompressed = []
    while c:
        decompressed += c.data
        c = c.next   
    # print(decompressed)
    muls = [ix*num for ix,num in enumerate(decompressed) if num != "."]

    return sum(muls)

if __name__ == "__main__":
    print(f"{main_1(SAMPLE) = }")

    with open("input9.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }") # 6421128769094

    print(f"{main_2(SAMPLE) = }")
    print(f"{main_2(real_input) = }") # 6451140796324 too high