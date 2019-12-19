##import sys
##sys.path.insert(0,r"C:\_PythonJGE\Utility")
import graph as g
import a_star_doc_nd as asdn
import set_bits
#import connected_components as cc
import connected_components_quick as cc

from copy import deepcopy
import time

def GraphCycles(G):
    G = g.LexOrder(G)
    print "This function will iterate through all matroid elements!"
    print "There is at most |E| = C(|V|,2) edges and 2**|E| matroid elements."
    print "For G, |E| = ", len(G['E'])
    print "For G, 2**|E| = ", 2**len(G['E'])
    G["pts"] = [0]*len(G["V"])
    for i in range(len(G["V"])):
        G["pts"][i] = [0,0,0]
    print "Estimated Time: ", 0.001349609375*2**(len(G['E']))
    start_time = time.time()

    base = 2
    bits = len(G["E"])
    I = []
    D = []
    verbose = True
    meet = lambda S1,S2: S1.intersection(S2)
    join = lambda S1,S2: S1.union(S2)
    diff = lambda S1,S2: S1.difference(S2)
    less = lambda S1,S2: meet(S1,S2)==S1
    for i in range(base**bits):
        v = set_bits.Base(i,base,bits)
        X = set_bits.Indices(v,1)
        ES = map(lambda i: G["E"][i], X)
        Gi = g.MakeUndirected(g.SubgraphE(G,ES))
        independent = cc.IsAForest(Gi)
        dependent = not independent
        if independent:
            I.append(i)
        else:
            D.append(i)
    C = deepcopy(D)
    for i in C:
        v = set_bits.Base(i,base,bits)
        X = set_bits.Indices(v,1)
        S = set(X)
        for j in D:
            w = set_bits.Base(j,base,bits)
            Y = set_bits.Indices(w,1)
            T = set(Y)
            if i == j:
                continue
            if less(S,T):
                try:
                    C.remove(j)
                except:
                    tmp = 0

    CC = []
    for i in C:
        v = set_bits.Base(i,base,bits)
        X = set_bits.Indices(v,1)
        ES = map(lambda i: G["E"][i], X)
        CC.append(ES)
    elapsed_time = time.time() - start_time
    s = "elapsed time: %.4f\n" % elapsed_time
    print s
    return CC
