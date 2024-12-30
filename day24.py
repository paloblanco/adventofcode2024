import operator
from dataclasses import dataclass,field
from collections import defaultdict
import re
from functools import cache

import matplotlib.pyplot as plt

import networkx as nx
import random

SAMPLE = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

band = operator.and_
bor  = operator.or_
bxor = operator.xor

OP_LOOKUP = {
    "AND": band,
    "OR":  bor,
    "XOR": bxor
}

op_lookup = r"([\w\d]{3}) (\w{2,3}) ([\w\d]{3}) -> ([\w\d]{3})"

def main_1(text_input: str) -> int:
    ivalues, operations = text_input.strip().split("\n\n")
    values = {}
    
    for row in ivalues.split("\n"):
        k = row.split(":")
        values[k[0]] = int(k[1])

    # @cache
    # def get_value(n: str) -> int:
    #     if n in values:
    #         return values[n]
    
    ops = re.findall(op_lookup,operations)
    links = {}
    for n0,op,n1,n in ops:
        links[n] = (n0,n1,OP_LOOKUP[op])
    
    zs = [n for n in links.keys() if n.startswith("z")]
    nodes = [n for n in links.keys()]

    def get_value(n: str) -> int:
        if n in values: return values[n]
        n0,n1,op = links[n]
        v0 = get_value(n0)
        v1 = get_value(n1)
        myval = op(v0,v1)
        values[n]=myval
        return myval

    for n in nodes:
        values[n] = get_value(n)

    zs.sort(reverse=True)
    zval = "".join([str(values[z]) for z in zs])
    return int(zval,2)

def main_2(text_input: str) -> str:
    ivalues, operations = text_input.strip().split("\n\n")
    values = {}
    
    for row in ivalues.split("\n"):
        k = row.split(":")
        values[k[0]] = int(k[1])

    # @cache
    # def get_value(n: str) -> int:
    #     if n in values:
    #         return values[n]
    
    ops = re.findall(op_lookup,operations)
    links = {}
    for n0,op,n1,n in ops:
        links[n] = (n0,op,n1)
    
    edges = [(e[0],e[3]) for e in ops] + [(e[2],e[3]) for e in ops]

    DX = nx.DiGraph()
    DX.add_edges_from(edges)
    pos = nx.spring_layout(DX)
    print(pos)    
    
    @cache
    def return_deepest_ancestor_depth(n):
        depth = 0
        id = 0
        ancestors = nx.ancestors(DX,n)
        # print(ancestors)
        # input()
        if not ancestors:
            return 0, int(n[1:])
        for a in ancestors:
            d,i = return_deepest_ancestor_depth(a)
            d += 1
            depth = max(d,depth)
            id = max(i,id)
        return depth, id

    lmax = 10
    for node in DX.nodes:
        if not re.match(r"\D\D\D",node): continue
        op = links[node][1]
        if op == "AND": adder = -.5
        if op == "OR": adder = 0.5
        if op == "XOR": adder = 0
        level, height = return_deepest_ancestor_depth(node)
        level = 3 + 0.05 * level + adder
        inputs = links[node]
        if "XOR" in inputs:
            if ((re.match(r"x\d\d",inputs[0]) or re.match(r"x\d\d",inputs[2])) and
            (re.match(r"y\d\d",inputs[0]) or re.match(r"y\d\d",inputs[2]))):
                level=1.5
                height += 1
            else:
                level = 6
                height += 2
        if "OR" in inputs:
            level = 4.5
            height += 3
        if "AND" in inputs:
            if ((re.match(r"x\d\d",inputs[0]) or re.match(r"x\d\d",inputs[2])) and
            (re.match(r"y\d\d",inputs[0]) or re.match(r"y\d\d",inputs[2]))):
                level=3
                height += 4
            else:
                level = 8
                height += 5
        DX.nodes[node]["level"] = level
        DX.nodes[node]["height"] = height
        DX.nodes[node]["number"] = int(height)
        DX.nodes[node]["op"] = op
        pos[node] = (level,height)
        # lmax = max(lmax,level)

    props = {}
    for node in DX.nodes:
        if re.match(r"\D\D\D",node): continue
        op="SIG"
        if re.match(r"x\d\d",node): 
            level = 0
            height = int(str(node)[1:])
        if re.match(r"y\d\d",node): 
            level = 0.15
            height = int(str(node)[1:]) + 0.15
        if re.match(r"z\d\d",node): 
            level = lmax
            height = int(str(node)[1:]) + 0.15
            op = links[node][1]
        DX.nodes[node]["level"] = level
        DX.nodes[node]["height"] = height+3
        DX.nodes[node]["number"] = int(height)
        
        DX.nodes[node]["op"] = op
        pos[node] = (level,height+3)

    print(DX.nodes["x00"])

    # nx.draw(DX,pos=pos,with_labels=True)


    siglist,orlist,xorlist,andlist = [],[],[],[]
    
    for node in DX.nodes:
        if DX.nodes[node]["op"] == "SIG": siglist.append(node)
        if DX.nodes[node]["op"] == "AND": andlist.append(node)
        if DX.nodes[node]["op"] == "OR": orlist.append(node)
        if DX.nodes[node]["op"] == "XOR": xorlist.append(node)

    nx.draw_networkx_nodes(DX,pos,nodelist=siglist,node_color="blue",alpha=0.5)
    nx.draw_networkx_nodes(DX,pos,nodelist=xorlist,node_color="red",alpha=0.5)
    nx.draw_networkx_nodes(DX,pos,nodelist=andlist,node_color="yellow",alpha=0.5)
    nx.draw_networkx_nodes(DX,pos,nodelist=orlist,node_color="orange",alpha=0.5)
    nx.draw_networkx_labels(DX,pos)

    nx.draw_networkx_edges(DX,pos=pos)

    # plt.show()
    # ops2.sort(key=lambda x: x[3])
    # ops2.sort(key=lambda x: x[1])

    # for e in ops2:
    #     print(e)
    # bad ones: z38,nbf,bhd,dhg,z23,z06,krq,cgn

    # shamelessly copied from reddit.
    
    wrong = set()
    for op1, op, op2, res in ops:
        if res[0] == "z" and op != "XOR" and res != "z45":
            wrong.add(res)
        if (
            op == "XOR"
            and res[0] not in ["x", "y", "z"]
            and op1[0] not in ["x", "y", "z"]
            and op2[0] not in ["x", "y", "z"]
        ):
            wrong.add(res)
        if op == "AND" and "x00" not in [op1, op2]:
            for subop1, subop, subop2, subres in ops:
                if (res == subop1 or res == subop2) and subop != "OR":
                    wrong.add(res)
        if op == "XOR":
            for subop1, subop, subop2, subres in ops:
                if (res == subop1 or res == subop2) and subop == "OR":
                    wrong.add(res)
    wrong = list(wrong)
    wrong.sort()
    print(",".join(wrong))




    

if __name__ == "__main__":
    with open("input24.txt","r") as f: real_input = f.read()

    # print(f"{main_1(SAMPLE) = }") 
    # print(f"{main_1(real_input) = }") 

    # print(f"{main_2(SAMPLE) = }") 
    print(f"{main_2(real_input) = }")