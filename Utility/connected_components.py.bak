import graph as g
import a_star_doc_nd as asdn
from copy import deepcopy


def ConnectedComponentsBrute(doc):
    doc1 = deepcopy(doc)
    V = doc1["V"]
    E = doc1["E"]
    if len(V) == 0:
        return []
    u = V[0]
    C = [[u]] # connected components
    def cost(pts,u,v):
        if ([u,v] in E) or ([v,u] in E):
            return 1
        else:
            return 0
    asdn.heurist_cost_estimate = cost
    doc1["pts"] = []
    def LookupClass(C,i):
        k = 0
        for c in C:
            for u in c:
                if u == i:
                    return k
            k += 1
        return -1
    for v in V:
        k = LookupClass(C,v)
        if k <> -1:
            continue
        flag = True
        for i in range(len(C)):
            c = C[i]
            u = c[0]
            path = asdn.A_star(doc1,u,v)
            if len(path) > 0:
                C[i].append(v)
                flag = False
        if flag:
            C.append([v])
    return C

def IsAForest(doc):
    C = ConnectedComponentsBrute(doc)
    V = doc["V"]
    E = doc["E"]
    e = len(E)/2 # we assume undirected edges
    v = len(V)
    c = len(C)
    residue = e - (v - c)
    return residue == 0
def IsATree(doc):
    C = ConnectedComponentsBrute(doc)
    V = doc["V"]
    E = doc["E"]
    e = len(E)/2 # we assume undirected edges
    v = len(V)
    c = len(C)
    residue = e - (v - 1)
    return residue == 0

# also there is connected_components_quick
def NumberOfComponents(G):
    C = ConnectedComponentsBrute(G)
    return len(C)
