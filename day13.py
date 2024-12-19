import re

SAMPLE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

REG = r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)"""

def main_1(text_input: str) -> int:
    data = re.findall(REG, text_input)
    coins = []
    for entry in data:
        a = (int(entry[0]),int(entry[1]))
        b = (int(entry[2]),int(entry[3]))
        p = (int(entry[4]),int(entry[5]))
        solutions = []
        for bb in range(101):
            for aa in range(101):
                x = aa*a[0] + bb*b[0]
                y = aa*a[1] + bb*b[1]
                if x==p[0] and y==p[1]:
                    # solutions.append(aa*3 + bb)
                    solutions.append((aa,bb))
        aaa = (p[0] - ((b[0]*p[1])/b[1])) / (a[0] + ((-b[0]*a[1]/b[1])))
        bbb = (p[1] - a[1]*aaa) / b[1]
        if solutions:
            print(solutions)
            print(f"{aaa = }   {bbb = }")
            coins.append(min([i*3+j for i,j in solutions]))
        else:
            coins.append(0)
    return sum(coins)

def main_2(text_input: str) -> int:
    data = re.findall(REG, text_input)
    coins = []
    for entry in data:
        a = (int(entry[0]),int(entry[1]))
        b = (int(entry[2]),int(entry[3]))
        p = (10000000000000 + int(entry[4]), 10000000000000 + int(entry[5]))
        # p = (int(entry[4]),int(entry[5]))
        
        # p[0] = a[0]*aa + b[0]*bb
        # p[1] = a[1]*aa + b[1]*bb

        # aa = (p[0] - b[0]*bb) / a[0]
        # bb = (p[1] - a[1]*aa) / b[1]

        # p[0] = a[0]*aa + b[0]*((p[1] - a[1]*aa) / b[1])
        # p[0] = a[0]*aa + ((b[0]*p[1])/b[1]) + aa * ((-b[0]*a[1]/b[1]))

        # p[0] - ((b[0]*p[1])/b[1]) = aa * (a[0] + ((-b[0]*a[1]/b[1])))

        aa = (p[0] - ((b[0]*p[1])/b[1])) / (a[0] + ((-b[0]*a[1]/b[1])))
        bb = (p[1] - a[1]*aa) / b[1]

        aa = round(aa)
        bb = round(bb)

        if (p[0] == a[0]*int(aa) + b[0]*int(bb)) and (p[1] == a[1]*int(aa) + b[1]*int(bb)) and (aa>=0) and (bb>=0):
            coins.append(aa*3 + bb)
    
    return sum(coins)


# 201 - 352 - 0178

                

if __name__ == "__main__":
    with open("input13.txt","r") as f: real_input = f.read()
    print(f"{main_1(SAMPLE) = }")
    print(f"{main_2(real_input) = }")

    # print(f"{main_2(SAMPLE) = }")