SAMPLE = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

def return_neighbors(node: str, edges: list[set[str]]) -> list[str]:
    # print(node)
    # print(edges)
    neighbors = []
    for edge in edges:
        if node in edge: 
            n = (edge - set([node,])).pop()
            neighbors.append(n)
    return neighbors

def main_1(text_input: str) -> int:
    pairs = text_input.strip().split()
    pairs = [set(e.split("-")) for e in pairs]
    list_nodes = pairs[0]
    for pair in pairs[1:]:
        list_nodes = list_nodes | pair
    list_nodes = list(list_nodes)
    triples = set()
    for node in list_nodes:
        if not node.startswith("t"): continue
        neighbors = return_neighbors(node,pairs)
        for i,n0 in enumerate(neighbors[:-1]):
            for n1 in neighbors[i+1:]:
                if {n0,n1} in pairs:
                    new = [node,n0,n1]
                    new.sort()
                    new = tuple(new)
                    triples.add(new)
    # print(triples)
    return len(triples)

def return_neighbor_number(node: str, edges: list[set[str]]) -> int:
    count = 0
    for e in edges:
        if node in e: count+=1
    return count

def main_2(text_input: str) -> int:
    pairs = text_input.strip().split()
    pairs = [set(e.split("-")) for e in pairs]
    list_nodes = pairs[0]
    for pair in pairs[1:]:
        list_nodes = list_nodes | pair
    list_nodes = list(list_nodes)
    # maybe return triples, then attempt to add to each one?
    triples = set()
    neighbor_lookup = {}
    for node in list_nodes:
        neighbors = return_neighbors(node,pairs)
        neighbor_lookup[node] = set(neighbors)
        for i,n0 in enumerate(neighbors[:-1]):
            for n1 in neighbors[i+1:]:
                if {n0,n1} in pairs:
                    new = [node,n0,n1]
                    new.sort()
                    new = tuple(new)
                    triples.add(new)
    print(f"{len(list_nodes) = }")
    changed = True
    while changed:
        changed=False
        for node in list_nodes:
            subchange = True
            while subchange:
                subchange=False
                for t in triples:
                    if node in t: continue
                    neighbors = neighbor_lookup[node]
                    if neighbors & set(t) == set(t):
                        triples.remove(t)
                        new_t = tuple(sorted(t + (node,)))
                        triples.add(new_t)
                        changed=True
                        subchange = True
                        # print(new_t)
                        break
            list_nodes.remove(node)
            print(f"    killed {node}")
    for t in triples:
        print(t)
    triples = list(triples)
    triples.sort(key=lambda x: len(x),reverse=True)
    return ",".join(triples[0])


if __name__ == "__main__":
    with open("input23.txt","r") as f: real_input = f.read()

    print(f"{main_1(SAMPLE) = }") 
    print(f"{main_1(real_input) = }") #2264 too high

    print(f"{main_2(SAMPLE) = }") 
    print(f"{main_2(real_input) = }")