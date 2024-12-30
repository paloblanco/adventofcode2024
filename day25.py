SAMPLE = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

def main_1(text_input: str) -> str:
    items = text_input.strip().split("\n\n")
    items = [e.split() for e in items]
    # print(f"{items = }")
    locks=[]
    keys=[]
    for each in items:
        if each[0][0]=="#": #lock
            lock=[]
            for col in range(5):
                for h in range(1,7):
                    if each[h][col]==".":
                        lock.append(h-1)
                        break
            locks.append(lock)
        if each[0][0]==".": #key
            key=[]
            for col in range(5):
                for h in range(0,7):
                    if each[h][col]=="#":
                        key.append(6-h)
                        break
            keys.append(key)
    fits = 0
    for lock in locks:
        for key in keys:
            ok=True
            for i in range(5):
                if lock[i]+key[i] > 5: 
                    ok=False
                    break
            if ok:
                fits += 1
    return fits


if __name__ == "__main__":
    with open("input25.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }") 
    print(f"{main_1(real_input) = }") 