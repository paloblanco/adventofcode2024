SAMPLE = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

def main_1(text_input: str) -> int:
    lines = text_input.strip().split()

    antennas = {}
    for row_num, row in enumerate(lines):
        for col_num, letter in enumerate(row):
            if letter == ".": continue
            if letter not in antennas: antennas[letter] = []
            antennas[letter].append((row_num,col_num))

    # print(antennas)

    row_max = len(lines)
    col_max = len(lines[0])

    antinode_set = set()

    for aname, antenna_list in antennas.items():
        # print(antenna_list)
        for i, a0 in enumerate(antenna_list[:-1]):
            for j, a1 in enumerate(antenna_list[i+1:]):
                drow = a1[0] - a0[0]
                dcol = a1[1] - a0[1]
                
                row0 = a0[0] - drow
                col0 = a0[1] - dcol
                if (0 <= row0 < row_max) and (0 <= col0 < col_max):
                    antinode_set.add((row0,col0))

                row0 = a1[0] + drow
                col0 = a1[1] + dcol
                if (0 <= row0 < row_max) and (0 <= col0 < col_max):
                    antinode_set.add((row0,col0))

    return len(antinode_set)

def main_2(text_input: str) -> int:
    lines = text_input.strip().split()

    antennas = {}
    for row_num, row in enumerate(lines):
        for col_num, letter in enumerate(row):
            if letter == ".": continue
            if letter not in antennas: antennas[letter] = []
            antennas[letter].append((row_num,col_num))

    # print(antennas)

    row_max = len(lines)
    col_max = len(lines[0])

    antinode_set = set()

    for aname, antenna_list in antennas.items():
        # print(antenna_list)
        for i, a0 in enumerate(antenna_list[:-1]):
            for j, a1 in enumerate(antenna_list[i+1:]):
                drow = a1[0] - a0[0]
                dcol = a1[1] - a0[1]
                
                row_new, col_new = a0
                while (0 <= row_new < row_max) and (0 <= col_new < col_max):
                    antinode_set.add((row_new,col_new))
                    row_new -= drow
                    col_new -= dcol

                row_new, col_new = a1
                while (0 <= row_new < row_max) and (0 <= col_new < col_max):
                    antinode_set.add((row_new,col_new))
                    row_new += drow
                    col_new += dcol

    return len(antinode_set)


if __name__ == "__main__":
    print(f"{main_1(SAMPLE) = }")

    with open("input8.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }")

    print(f"{main_2(SAMPLE) = }")
    print(f"{main_2(real_input) = }")