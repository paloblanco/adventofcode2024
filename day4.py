sample1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip()

def main_1(text_input: str) -> int:

    left_right = text_input.split()

    up_down = []
    for i,_ in enumerate(left_right[0]):
        ud_str = ''.join([row[i] for row in left_right])
        up_down.append(ud_str)

    diagonal_down_right_from_top = []
    for i_letter0, _ in enumerate(left_right[0]):
        diag = []
        for i_row,row in enumerate(left_right):
            ix_here = i_letter0 + i_row
            if ix_here >= len(row): continue
            diag.append(row[ix_here])
        diag_str = ''.join(diag)
        diagonal_down_right_from_top.append(diag_str)

    diagonal_down_right_from_left = []
    for i_letter0, _ in enumerate(left_right[0]):
        diag = []
        if i_letter0 == 0: continue
        for i_row,row in enumerate(left_right):
            ix_here = i_row - i_letter0
            if ix_here < 0: continue
            diag.append(row[ix_here])
        diag_str = ''.join(diag)
        diagonal_down_right_from_left.append(diag_str)

    diagonal_down_left_from_top = []
    right_left = [row[::-1] for row in left_right]
    for i_letter0, _ in enumerate(right_left[0]):
        diag = []
        for i_row,row in enumerate(right_left):
            ix_here = i_letter0 + i_row
            if ix_here >= len(row): continue
            diag.append(row[ix_here])
        diag_str = ''.join(diag)
        diagonal_down_left_from_top.append(diag_str)

    diagonal_down_left_from_right = []
    for i_letter0, _ in enumerate(right_left[0]):
        diag = []
        if i_letter0 == 0: continue
        for i_row,row in enumerate(right_left):
            ix_here = i_row - i_letter0
            if ix_here < 0: continue
            diag.append(row[ix_here])
        diag_str = ''.join(diag)
        diagonal_down_left_from_right.append(diag_str)

    big_string = " ".join(right_left + [row[::-1] for row in right_left] +
                            up_down + [row[::-1] for row in up_down] +
                            diagonal_down_right_from_top + [row[::-1] for row in diagonal_down_right_from_top] +
                            diagonal_down_right_from_left + [row[::-1] for row in diagonal_down_right_from_left] +
                            diagonal_down_left_from_top + [row[::-1] for row in diagonal_down_left_from_top] +
                            diagonal_down_left_from_right + [row[::-1] for row in diagonal_down_left_from_right])

    return big_string.count('XMAS')

def main_2(text_input: str) -> int:
    cw = text_input.split()
    x_count = 0
    winners = {"MMSS","SMMS","SSMM","MSSM"}
    for row_ix,row in enumerate(cw[:-1]):
        if row_ix == 0: continue
        for col_ix,letter in enumerate(row[:-1]):
            if col_ix==0: continue
            if letter != "A": continue
            corners = cw[row_ix-1][col_ix-1] + cw[row_ix-1][col_ix+1] + cw[row_ix+1][col_ix+1] + cw[row_ix+1][col_ix-1]
            if corners in winners: x_count+=1
    return x_count

if __name__ == "__main__":
    print(f"{main_1(sample1) = }")

    with open("input4.txt","r") as f: real_input = f.read()
    print(f"{main_1(real_input) = }")

    print(f"{main_2(sample1) = }")
    print(f"{main_2(real_input) = }")