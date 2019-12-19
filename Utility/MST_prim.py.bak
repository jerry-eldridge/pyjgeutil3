#[1] Introduction to Algorithms, Thomas H. Cormen,
# Charles E. Leiserson, Ronald L. Rivest, 6ed, 1992, The MIT Press
#
# We implement MST (Minimum Spanning Trees) Prim Algorithm
# from [1].

from heap import Heap
from graph import Adj,LookupEdge

def MST_prim(doc,root):
    """
    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V. root is a vertex
    in V. Eg,

    doc = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}
    root = 3

    and w(u,v) is a weight function on the edges
    [u,v].
    """
    V = doc['V']
    E = doc['E']
    w = doc['weights']
    r = root
    key = {}
    pred = {}
    INFINITY = 1e8
    NIL = -1
    for u in V:
        key[u] = INFINITY
        pred[u] = NIL
    key[r] = 0
    A = []
    for u in V:
        tup = (u,key[u])
        A.append(tup)
    Q = Heap(A, lambda x,y: x[1] < y[1])
    while Q.heapsize > 0:
        u,k = Q.HeapExtract()
        L = []
        i = 0
        for tup in Q.A:
            if not (i < Q.heapsize):
                break
            L.append(tup[0])
            i += 1
        for v in Adj(doc,u):
            idx = LookupEdge(doc,[u,v])
            wuv = w[idx]
            if (v in L) and (wuv < key[v]):
                pred[v] = u
                key[v] = wuv

        for i in range(Q.heapsize,-1,-1):
            tup = Q.A[i]
            v,k = tup
            Q.A[i] = (v,key[v])

        Q = Heap(Q.A[:Q.heapsize],lambda x,y: x[1] < y[1]) 


    tree = {}
    tree['V'] = V
    ET = []
    for v in V:
        if pred[v] == NIL:
            continue
        ET.append([v,pred[v]])
    tree['E'] = ET
    return tree
