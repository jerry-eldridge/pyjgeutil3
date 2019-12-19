from copy import deepcopy
import itertools
from math import pi,cos,sin
import mapto

import time # cartesian product
import datetime
import sys # cartesian product
import random

def Time():
    now = datetime.datetime.now()
    sec_now = time.mktime(now.timetuple())
    return sec_now

def factorial(n):
    if n <= 1:
        return 1
    else:
        return n*factorial(n-1)

def Degree(doc,v):
    return len(Adj(doc,v))

def Adj(doc,i):
    """
    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V. root is a vertex
    in V. Eg,

    doc = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}

    This creates a list of all vertices adjacent to vertex
    i, incoming or outgoing together in a list.
    """
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for e in E:
        v = e[0]
        w = e[1]
        if (u == v) and (w not in adj):
            adj.append(w)
        if (u == w) and (v not in adj):
            adj.append(v)
    return adj

def permute_in_place(a):
    """
http://stackoverflow.com/questions/104420/
how-to-generate-all-permutations-of-a-list-in-python

This calculates permutations without a memory error, but
still takes a while when computing n! > threshold amount
of permutations. The alternate method is:

    import itertools
    L = list(itertools.permutations(range(n1),n1))

which will run out of memory for n1! large.
    """
    a.sort()
    yield list(a)
    if len(a) <= 1:
        return

    first = 0
    last = len(a)
    while 1:
        i = last - 1
        while 1:
            i = i - 1
            if a[i] < a[i+1]:
                j = last - 1
                while not (a[i] < a[j]):
                    j = j - 1
                a[i], a[j] = a[j], a[i] # swap the values
                r = a[i+1:last]
                r.reverse()
                a[i+1:last] = r
                yield list(a)
                break
            if i == first:
                a.reverse()
                return

def Isomorphic(doc1,doc2):
    n1 = len(doc1["V"])
    n2 = len(doc2["V"])
    if n1 != n2:
        print "vertex sets sizes unequal"
        return False, []
    if len(doc1["E"]) != len(doc2["E"]):
        print "edge sets sizes unequal"
        return False, []
    V1 = doc1["V"]
    E1 = doc1["E"]
    V2 = doc2["V"]
    E2 = doc2["E"]
    if (V1 == V2) and (E1 == E2):
        return True, range(n1)
    
    deg1 = map(lambda v: Degree(doc1,v), doc1["V"])
    deg2 = map(lambda v: Degree(doc2,v), doc2["V"])
    deg1.sort()
    deg2.sort()
    print deg1
    print deg2

    if not (deg1 == deg2):
        print "degrees of vertices unequal"
        return False, []
    
    maxsize = 10e9
    sz = factorial(n1)
    if sz > maxsize:
        print "Error: n! > maxsize =",maxsize
        print "returning False though still may be isomorphic"
        return False, []
    #import itertools
    #L = list(itertools.permutations(range(n1),n1))
    print "Checking all ",sz,"permutations until a match is found"
    #for tup in L:
    i = 0
    for tup in permute_in_place(range(n1)):
        if tup == None:
            "tup is none"
            break
        flag = True
        for e in E1:
            u,v = e 
            f = [V2[tup[u]],V2[tup[v]]]
            flag =  flag and (f in E2)
            if not flag:
                break
        if flag:
            return True, list(tup)
        i += 1
    print "Checked exactly ",i,"permutations"
    return False, []


def AdjMatrix(doc):
    """
    AdjMatrix(doc) - returns the adjacency matrix
    of a graph document doc. Uses the Numpy library for
    array,zeros. If [u,v] in E, then A[u,v] for
    A = AdjMatrix(doc) where E = doc["E"] and V = doc["V"].
    """
    from numpy import array,zeros
    V = doc["V"]
    E = doc["E"]
    n = len(V)
    A = zeros((n,n))
    for e in E:
        u,v = e
        A[u,v] = 1
    return A

def GraphFromAdj(A):
    n = A.shape[0]
    doc = {}
    doc["_id"] = 1
    doc["V"] = range(n)
    doc["E"] = []
    doc["weights"] = []
    for u in range(n):
        for v in range(n):
            if A[u,v] != 0:
                doc["E"].append([u,v])
                doc["weights"].append(A[u,v])
    return doc

def GraphPow(doc,k):
    """
    The graph power G**n for the graph G in graph document doc
    """
    from numpy import array,identity,zeros
    A = AdjMatrix(doc)
    N = A.shape[0]
    def Pow(A,n):
        if n <= 0:
            return identity(N)
        elif n == 1:
            return A
        else:
            return A.dot(Pow(A,n-1))
    doc0 = deepcopy(doc)
    doc0["E"] = GraphFromAdj(Pow(A,k))["E"]
    return doc0
                    
def PathEdges(path):
    path0 = deepcopy(path)
    L = []
    i = 0
    for i in range(len(path)-1):
        e = [path0[i],path0[i+1]]
        L.append(e)
    return L

def LookupEdge(doc,e):
    """
    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V.  Eg,

    doc = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}
    """
    V = doc['V']
    E = doc['E']
    i = 0
    alt = -1
    for f in E:
        if f == e:
            return i
        i += 1
    return alt

def Indices(L,val):
    idxs = []
    i = 0
    for x in L:
        if x == val:
            idxs.append(i)
        i += 1
    return idxs

def DeleteVertexPseudo(G,v):
    V = deepcopy(G['V'])
    E = deepcopy(G['E'])
    try:
        V.remove(v)
    except:
        i = 0
    E2 = deepcopy(E)
    for e in E:
        u1,u2 = e
        if (u1 == v) or (u2 == v):
            E2.remove(e)
    G2 = {}
    G2['V'] = V
    G2['E'] = E2
    return G2

def DeleteVerticesPseudo(G,S):
    G2 = {}
    G2['V'] = deepcopy(G['V'])
    G2['E'] = deepcopy(G['E'])
    for v in S:
        G2 = DeleteVertexPseudo(G2,v)
    return G2

def DeleteVertex(doc,x):
    doc2 = deepcopy(doc)
    V = doc2["V"]
    E = doc2["E"]
    try:
        V.remove(x)
    except:
        return doc2
    EP = []
    i = 0
    j = 0
    g = {}
    for e in E:
        u,v = e
        j += 1
        if u == x or v == x:
            continue
        EP.append(e)
        g[i] = j
        i += 1
    for i in range(len(EP)):
        u,v = EP[i]
        u2 = Indices(V,u)
        if len(u2) == 0:
            print "Error:",u,"not in",V
            continue
        else:
            u2 = u2[0]
        v2 = Indices(V,v)
        if len(v2) == 0:
            print "Error:",v,"not in",V
            continue
        else:
            v2 = v2[0]
        e = [u2,v2]
        EP[i] = e
    h = {}
    i = 0
    for v in V:
        h[i] = v
        i += 1
    doc2["V"] = range(len(V))
    doc2["E"] = EP

    def geth(i):
        try:
            return h[i]
        except:
            return None
    def getg(i):
        try:
            return g[i]
        except:
            return None

    sub_V = map(geth,doc['V'])
    try:
        sub_V.remove(None)
    except:
        i = 0
    sub_E = map(getg, range(len(doc['E'])))
    try:
        sub_E.remove(None)
    except:
        i = 0
    doc2['subgraph_to_graph_V'] = sub_V
    doc2['subgraph_to_graph_E'] = sub_E
    return doc2

def SubgraphVPseudo(G,S):
    T = list(set(G['V'])-set(S))
    G2 = DeleteVerticesPseudo(G,T)
    return G2

def SubgraphV(doc,S):
    """
    Subgraph of doc induced by list S of vertices subset of V.

    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V.  Eg,

    doc = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}
    """
    doc2 = deepcopy(doc)
    V = doc2['V']
    E = doc2['E']
    D = list(set(V)-set(S))

    for x in D:
        try:
            V.remove(x)
        except:
            i = 0

    EP = []
    i = 0
    j = 0
    g = {}
    for e in E:
        u,v = e
        j += 1
        if u in D or v in D:
            continue
        EP.append(e)
        g[i] = j
        i += 1
    for i in range(len(EP)):
        u,v = EP[i]
        u2 = Indices(V,u)[0]
        v2 = Indices(V,v)[0]
        e = [u2,v2]
        EP[i] = e
        
    h = {}
    i = 0
    for v in V:
        h[i] = v
        i += 1
    doc2["V"] = range(len(V))
    doc2["E"] = EP

    def geth(i):
        try:
            return h[i]
        except:
            return None
    def getg(i):
        try:
            return g[i]
        except:
            return None

    sub_V = map(geth,doc['V'])
    try:
        sub_V.remove(None)
    except:
        i = 0
    sub_E = map(getg, range(len(doc['E'])))
    try:
        sub_E.remove(None)
    except:
        i = 0
    doc2['subgraph_to_graph_V'] = sub_V
    doc2['subgraph_to_graph_E'] = sub_E
    return doc2

def DeleteVertices(doc,S):
    G = deepcopy(doc)
    T = list(set(G["V"])-set(S))
    G = SubgraphV(G,T)
    return G

def SubgraphE(doc,S):
    """
    Subgraph of doc induced by list E of edges subset of E.

    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V.

    Eg,

    from graph import SubgraphV, SubgraphE, PathEdges
    from a_star_doc import A_star

    doc2 = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}

    SV = [0,1,3]
    start = 0
    goal = 2
    SE = PathEdges(A_star(doc2,start,goal))
    # the subgraph relabels the vertex indices
    # but keeps a subgraph to graph function for V and E
    subgraph = SubgraphV(doc2,SV)

    # The list L defines a function i -> L[i] where i
    # is an index in subgraph and L[i] is an index in graph
    print subgraph['subgraph_to_graph_V']
    print subgraph['subgraph_to_graph_E']

    L = subgraph['subgraph_to_graph_V']
    subgraph['labels'] = [0]*len(L)
    for i in range(len(L)):
        subgraph['labels'][i] = str(i)+","+str(L[i])
    L = subgraph['subgraph_to_graph_E']
    subgraph['Enames'] = ['']*len(L)
    for i in range(len(L)):
        w = int(round(doc2['weights'][L[i]]))
        subgraph['Enames'][i] = str(w)

`   from plot_graph import Show,Plot,End
    h = w = 800
    im1 = ones((h,w,3),dtype='uint8')*255
    im1 = Plot(im1,subgraph)
    ch = Show("result",im1,-1)
    End()
    """
    V = doc['V']
    E = doc['E']
    pts = doc['pts']

    B = [0]*len(V)
    for e in S:
        if e not in E:
            continue
        u,v = e
        B[u] = 1
        B[v] = 1
    VS = []
    f = {}
    g = {}
    h = {}
    ptsS = []
    k = 0
    for i in range(len(B)):
        if B[i] == 1:
            VS.append(k)
            ptsS.append(pts[i])
            f[V[i]] = k
            h[k] = V[i]
            k += 1
    ES = []
    k = 0
    K = 0
    for e in E:
        if e not in S:
            k += 1
            continue
        u,v = e
        u = f[u]
        v = f[v]
        e = [u,v]
        g[K] = k
        ES.append(e)
        k += 1
        K += 1
        
    doc2 = deepcopy(doc)
    doc2['V'] = VS
    doc2['E'] = ES
    doc2['pts'] = ptsS

    def geth(i):
        try:
            return h[i]
        except:
            return None
    def getg(i):
        try:
            return g[i]
        except:
            return None

    sub_V = map(geth,doc['V'])
    try:
        sub_V.remove(None)
    except:
        i = 0
    sub_E = map(getg, range(len(doc['E'])))
    try:
        sub_E.remove(None)
    except:
        i = 0
    doc2['subgraph_to_graph_V'] = sub_V
    doc2['subgraph_to_graph_E'] = sub_E
    return doc2

def AddVertex(doc):
    """
    Add a vertex to graph document. We assume
    that doc["V"] is just range(n) for n = |V|.
    If you want to store non-indices as vertices,
    create a doc["objects"][i] to store the i-th
    object.

    doc2,n = AddVertex(doc)

    where n is the new vertex index
    """
    doc2 = deepcopy(doc)
    V = doc2["V"]
    n = len(V)
    doc2["V"] = range(n+1)
    return doc2,n

def AddEdge(doc,e):
    """
    Adds an undirected edge [u,v] to graph document
    """
    doc2 = deepcopy(doc)
    E = doc2["E"]
    E.append(e)
    doc2["E"] = E
    return doc2

def DeleteEdge(doc,e):
    doc2 = deepcopy(doc)
    E = doc2['E']
    try:
        E.remove(e)
    except:
        return doc2
    doc2 = SubgraphE(doc,E)
    return doc2

def DeleteEdges(doc,ES):
    doc2 = deepcopy(doc)
    E = doc2['E']
    for e in ES:
        try:
            E.remove(e)
        except:
            continue
    doc2 = SubgraphE(doc,E)
    return doc2

def ContractEdge(doc,e):
    doc2 = deepcopy(doc)
    E = doc2['E']
    V = doc2['V']
    u,v = e
    try:
        E.remove([u,v])
    except:
        i = 0
    try:
        E.remove([v,u])
    except:
        i = 0
    def equate(e,u,v):
        uu,vv = e
        if uu == v:
            uu = u
        if vv == v:
            vv = u
        return [uu,vv]
    up = min(u,v)
    vp = max(u,v)
    u = up
    v = vp
    E = map(lambda e: equate(e,u,v), E)
    # make E a set but will lose the order of edges and weights
    doc2["E"] = map(eval,list(set(map(lambda e: str(e),E))))
    doc2["weights"] = [0]*len(doc2["E"])
    doc2["V"] = V
    doc3 = DeleteVertex(doc2,v)
    return doc3

def GraphProduct(doc1,doc2):
    """
    [Bondy,Murty] Graph Theory with Applications,
    North-Holland, 1976

    The product of simple graphs G and H is the simple
    graph G x H with vertex set V(G) x V(H) ('x' cartesian
    product) in which (u,v) is adjacent to (u',v') if and only
    if u = u' and [v,v'] in E(H), or v = v' and [u,u']
    in E(G).

    A simple graph is a graph with no loops [u,u] or
    two parallel edges [u,v] and [u,v] both in E.
    """
    Obj = []
    for el in itertools.product(doc1["V"],doc2["V"]):
        Obj.append(el)
    V = range(len(Obj))
    def LookupObj(Obj,v):
        i = 0
        for obj in Obj:
            if v == obj:
                return i
            i += 1
        return -1
    E = []
    for i in V:
        u,v = Obj[i]
        for j in V:
            up,vp = Obj[j]
            if (u == up and ([v,vp]in doc2["E"])) or \
               (v == vp and ([u,up] in doc1["E"])):
                E.append([i,j])
    doc = {}
    doc["V"] = V
    doc["E"] = E
    doc["object"]=Obj
    return doc

def ExtrudeGraph(doc):
    """
    Extrude Graph by Multiplying a single edge with the
    doc: doc2 = edge x doc, with doc2["object"] and vertices
    ordered so that (0,doc) and (1,doc) are copies of doc
    and corresponding vertices are edges from (0,doc) and (1,doc).
    """
    doc1 = {"V":range(2),"E":PathEdges(range(2))}
    doc2 = GraphProduct(doc1,doc)
    return doc2

def ExtrudeVertices(doc,S):
    """
    Extrude Vertices using ExtrudeGraph, we assume that
    ExtrudeGraph has doc2 = edge x doc producing (0,doc) and
    (1,doc) and edges between corresponding vertices. We
    obtain the subgraph for vertex set T for u,v in doc2["object"]
    such that (u == 1 and (v in S)) or (u==0) and lookup vertex
    index for obj = (u,v). In other words, we remove all vertices
    of (1,doc) that aren't in S. We use
    doc2 = graph.SubgraphV(doc1,T) for doc1 = ExtrudeGraph(doc)
    and T defined above.
    """
    def LookupObj(Obj,v):
        i = 0
        for obj in Obj:
            if v == obj:
                return i
            i += 1
        return -1
    doc1 = ExtrudeGraph(doc)
    T = []
    for obj in doc1["object"]:
        u,v = obj
        if (u == 1 and (v in S)) or (u==0):
            i = LookupObj(doc1["object"],obj)
            if i != -1:
                T.append(i)
    doc2 = SubgraphV(doc1,T)
    return doc2

def CreateCircleGeometry(doc,cx,cy,cz,r):
    doc2 = deepcopy(doc)
    doc2["pts"] = []
    n = len(doc2["V"])
    for i in range(n):
        theta = mapto.MapTo(0,0,n,2*pi,i)
        x = cx + r*cos(theta)
        y = cy + r*sin(theta)
        z = 0
        pt = [x,y,z]
        pt = map(int,map(round,pt))
        doc2["pts"].append(pt)
    return doc2

def Cn(N=3):
    """
    https://en.wikipedia.org/wiki/Cycle_graph
    """
    if N < 3:
        print "Error: Cycle must have at least 3 vertices"
        return {}
    doc = {"V":range(N),"E":PathEdges(range(N))+[[N-1,0]]}
    return doc

def Pn(N):
    """
    https://en.wikipedia.org/wiki/Path_graph
    """
    doc = {}
    doc["V"] = range(N)
    doc["E"] = PathEdges(range(N))
    return doc

def KProduct(doc1,doc2):
    """
    KProduct - this is a stub function. For two graph documents,
    it is create a graph document from V = doc1["V"] \/ doc2["V"]
    and add edges [u,v] for u in doc1["V"] and for v in doc2["V"]
    """
    doc = {}
    return doc

def MergeTwoVertices(doc,u,v):
    """
    MergeTwoVertices(doc,u,v) - will glue two vertices u and
    v together.

    Creates a graph document doc where vertices u and v
    in doc["V"] are merged.

    It creates an edge [u,v] if not already in document
    and then contracts it.
    """
    doc1 = deepcopy(doc)
    V = doc1["V"]
    E = doc1["E"]
    if (u in V) and (v in V):
        if not [u,v] in E:
             doc1["E"].append([u,v])
    return ContractEdge(doc1,[u,v])

def MergeEdge(doc,e1,e2):
    """
    MergeEdge(doc,e1,e2) - will glue two edges e1 and e2
    together.

    For e1 and e2 in doc["E"], and u1,v1 = e1 and
    u2,v2 = e2, then do

    doc1 = MergeTwoVertices(doc,u1,u2)
    doc2 = MergeTwoVertices(doc1,v1,v2)

    and return doc2
    """
    u1,v1 = e1
    u2,v2 = e2
    doc1 = MergeTwoVertices(doc,u1,u2)
    doc2 = MergeTwoVertices(doc1,v1,v2)
    return doc2

def MergeVertices(doc,S):
    """
    MergeVertices(doc,S) - will glue all vertices from
    S together.

    For a graph document doc and vertex set S,
    merge all the vertices in S to one vertex.

    Edited 6/30/2015 to sort S so that when merging,
    highest labels are merged first.
    """
    doc1 = deepcopy(doc)
    if len(S) < 2:
        return doc1
    S0 = deepcopy(S)
    S0.sort()
    u = S0[0]
    S1 = S0[1:]
    S1.reverse()
    for v in S1:
        doc1 = MergeTwoVertices(doc1,u,v)
    return doc1

def MergeEdges(doc,ES):
    """
    MergeEdges(doc,ES) - will glue all edges in ES,
    keeping ordering, together.

    For a set of edges ES named [ui,vi], two
    lists S1 = [ui] and S2 = [vi] for i in
    range(len(ES)). Then do

    doc1 = deepcopy(doc)
    doc1 = MergeVertices(doc1,S1)
    doc1 = MergeVertices(doc1,S2)

    and return doc1
    """
    doc1 = deepcopy(doc)
    S1 = []
    S2 = []
    for e in ES:
        u,v = e
        S1.append(u)
        S2.append(v)
    doc1 = MergeVertices(doc1,S1)
    doc1 = MergeVertices(doc1,S2)
    return doc1


def InAdj(doc,i):
    """
    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V. root is a vertex
    in V. Eg,

    doc = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}

    add incoming-vertices to vertex i to list adj
    """
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for e in E:
        v,w = e
        if (u == w):
            adj.append(v)
    return adj

def OutAdj(doc,i):
    """
    doc is an associative array with keys 'V' and 'E'
    containing a graph's vertices and edges. Vertices
    have values from 0 to len(V)-1 and edges are a list of
    list pairs [u,v] where u,v are in V. root is a vertex
    in V. Eg,

    doc = {'V':[0,1,2,3],'E':[[2,1],[0,3],[2,3],[3,1]]}

    add outgoing-vertices to vertex i to list adj
    """
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for e in E:
        v,w = e
        if (u == v):
            adj.append(w)
    return adj

def SplitVertex(doc,u):
    """
    SplitVertex(doc,u) - this tries to be the inverse
    of edge contraction for [u,u'] though isn't.

    For vertex u, add a new vertex u' not in graph doc
    and for v in InAdj(doc,u) add edges [v,u'] and
    for v in OutAdj(doc,u) add edges [u',v'] to a new
    graph document doc1.

    It adds u' =  len(doc["V"]) as the vertex.

    doc1,u' = SplitVertex(doc,u)
    """
    doc1 = deepcopy(doc)
    n = len(doc1["V"])
    in_neigh = InAdj(doc, u)
    out_neigh = OutAdj(doc, u)

    u2 = n
    V1 = [u2]
    E1 = []
    for w in in_neigh:
        E1.append([w,u2])
    for w in out_neigh:
        E1.append([u2,w])
    doc1["V"] = doc1["V"] + V1
    doc1["E"] = doc1["E"] + E1
    return doc1,u2

def SplitEdge(doc,e):
    """
    For an edge e = u,v in doc["E"], do
    doc1 = deepcopy(doc)
    doc1,u' = SplitVertex(doc1,u) and
    doc1,v' = SplitVertex(doc1,v)
    returning doc1,e' for e' = [u',v'].
    """
    u,v = e
    doc1 = deepcopy(doc)
    doc1,up = SplitVertex(doc1,u)
    doc1,vp = SplitVertex(doc1,v)
    ep = [up,vp]
    return doc1,ep

def MakeUndirected(doc):
    doc1 = deepcopy(doc)
    V = doc["V"]
    E = doc["E"]
    E1 = []
    for u in V:
        for v in V:
            e = [u,v]
            f = [v,u]
            if (e in E) or (f in E):
                if e not in E1:
                    E1.append(e)
                if f not in E1:
                    E1.append(f)
    doc1["E"] = E1
    return doc1

def Complement(doc):
    doc1 = deepcopy(doc)
    E1 = []
    for u in doc["V"]:
        for v in doc["V"]:
            if u == v:
                continue
            e = [u,v]
            if (e not in doc["E"]):
                E1.append(e)                
    doc1["E"] = E1
    return doc1

def LexOrder(doc):
    """
    We assume that V is just range(n)
    for n = |V|. If you want to have
    different numbers for V, then use
    a doc["V_elem"] or other name to denote
    the elements of V.
    """
    doc1 = deepcopy(doc)
    V = range(len(doc["V"]))
    E = doc["E"]
    E1 = []
    for u in V:
        for v in V:
            if [u,v] in E:
                E1.append([u,v])
    doc1["E"] = E1
    return doc1

def Kn(n):
    """
    Complete graph Kn on n vertices.
    https://en.wikipedia.org/wiki/Complete_graph
    """
    doc = {}
    doc["V"] = range(n)
    E = []
    for u in doc["V"]:
        for v in doc["V"]:
            if u == v:
                continue
            E.append([u,v])
    doc["E"] = E
    return doc

def Sk(n):
    """
    Star Graph Sk
    https://en.wikipedia.org/wiki/Star_(graph_theory)
    """
    doc = {}
    V = range(n)
    E = []
    for i in range(1,n):
        e = [0,i]
        f = [i,0]
        E.append(e)
        E.append(f)
    doc["V"] = V
    doc["E"] = E
    return doc

def Bp(p):
    """
    https://en.wikipedia.org/wiki/Book_(graph_theory)
    There are p pages of the book with only
    the corners of a page as vertices and the book
    being sewn together at a seam.

    Quadrilateral book = Sk(p) x Kn(2)
    """
    return GraphProduct(Sk(p),Kn(2))

def Ke2(p):
    """
    https://en.wikipedia.org/wiki/Book_(graph_theory)
    Triangular book, p triangles sharing
    a common edge.
    Let G,u = SplitVertex(Sk(p),0) and add [0,u] and [u,0]
    to G["E"] where 0 is the star vertex.
    """
    G,u = SplitVertex(Sk(p),0)
    G["E"].append([0,u])
    G["E"].append([u,0])
    return G

def IntersectionGraph(S,sort=True):
    """
    https://en.wikipedia.org/wiki/Intersection_graph
    https://en.wikipedia.org/wiki/Line_graph_of_a_hypergraph

    S is a set of sets, implemented as a list of lists.
    IntersectionGraph(S) first sorts each of the sublists
    with L.sort() if sort=True (the default) which puts
    it in standard form. For making a set from S,
    the sublists are converted to strings first, which makes
    the vertices unique. If two vertices (the sublists)
    intersect, create an edge between them.
    """
    doc = {}
    S2 = deepcopy(S)
    if sort:
        for i in range(len(S2)):
            S2[i].sort()
    T = set(map(str,S2))
    doc["V"] = range(len(T))
    doc["E"] = []
    #Obj = []
    V = doc["V"]
    TL = list(T)
    doc["object"] = map(eval,TL)
    for u in V:
        for v in V:
            if u == v:
                continue
            L1 = eval(TL[u])
            L2 = eval(TL[v])
            S1 = set(L1)
            S2 = set(L2)
            #Obj.append((L1,L2))
            S3 = S1 & S2
            if len(list(S3)) > 0:
                e = [u,v]
                doc["E"].append(e)
    # The objects, Obj, may be calculated but not returned
    # as they may be plentiful.
    return doc

def LineGraph(doc):
    """
    Line Graph of a graph G, L(G), obtained
    by the intersection graph of its edges.
    The edge u,v creates [u,v] which is sorted.
    The list of edges S = [e1...en] has Line Graph
    of IntersectionGraph(S).

    https://en.wikipedia.org/wiki/Line_graph
    """
    doc1 = deepcopy(doc)
    E = doc1["E"]
    S = []
    for e in E:
        u,v = e
        L = [u,v]
        L.sort()
        S = S + [L]
    doc1 = IntersectionGraph(S)
    return doc1

def IncidenceMatrix(doc):
    """
    https://en.wikipedia.org/wiki/Incidence_matrix

    B[i,j] = 1 if vertex i is incident with edge j, and
    is 0 otherwise.

    The vertices are doc["V"] and edges are doc["E"].
    A vertex is incident with an edge if it is contained
    in its set. Eg vertex 2 is incident with edges [3,2]
    and [2,4] in some graph containing those edges.
    """
    from numpy import array,zeros
    V = doc["V"]
    E = doc["E"]
    n = len(V)
    m = len(E)
    B = zeros((n,m),dtype='int')
    i = 0
    for w in V:
        j = 0
        for e in E:
            u,v = e
            if (w == u) or (w == v):
                B[i,j] = 1
            j += 1
        i += 1
    return B


def imm(A,chi,verbose=False):
    """
    https://en.wikipedia.org/wiki/Immanant_of_a_matrix
    """
    import itertools
    from numpy import array,zeros,ones,identity
    sh = A.shape
    print sh
    n = sh[0]
    print n
    L = list(itertools.permutations(range(n),n))
    S = 0
    for tup in L:
        if verbose:
            print tup
        Pi = 1
        for i in range(n):
            Pi *= chi(tup)*A[i,tup[i]]
        S += Pi
    return S

def perm(A):
    """
    https://en.wikipedia.org/wiki/Permanent
    https://en.wikipedia.org/wiki/Computing_the_permanent

    This method calculates the permanent of a matrix
    using the immanant of a matrix with chi = 1
    """
    from numpy import array,zeros,ones,identity
    def chi(tup):
        return 1
    return imm(A,chi)

def det(A):
    """
    https://en.wikipedia.org/wiki/Determinant

    This method calculates the determinant of a matrix
    use the immanant of a matrix with chi = LeviCivita

    The usual method is to though use
    numpy.linalg.det(A) with the Numpy python library.
    """
    from numpy import array,zeros,ones,identity
    import generalized_cross_product as gcp
    sh = A.shape
    n = sh[1]
    def chi(tup):
        return gcp.LeviCivita(list(tup),n)
    return imm(A,chi)

def SubdivideEdges(doc,S,midpt=False, undirected=True):
    """
    Subdivide edges in list S by adding a new vertex in
    each edge.

    It assumes undirected edges, with undirected=True,
    else you need to set to false.
    """
    import vectors
    doc1 = deepcopy(doc)
    for e in S:
        if e in doc1["E"]:
            n = len(doc1["V"])
            u,v = e
            if (v > u) and undirected:
                continue
            flag = False
            if midpt:
                try:
                    pt1 = doc1["pts"][u]
                    pt2 = doc1["pts"][v]
                    pt = map(int,vectors.lerp(pt1,pt2,0.4))
                    flag = True
                except:
                    print """doc["pts"] not defined"""
                    flag = False
            doc1["V"].append(n)
            if midpt and flag:
                doc1["pts"].append(pt)
            doc1["E"].remove(e)
            doc1["E"].append([u,n])
            doc1["E"].append([n,v])
    return doc1

def Subdivide(doc,midpt=False,undirected=True):
    """
    Subdivide the whole graph using
    doc1 = SubdivideEdges(doc,doc["E"])
    """
    return SubdivideEdges(doc,doc["E"],midpt)

def Gnm(n,m):
    """
    Grid graph

    Gnm(n,m) = Pn(n) x Pn(m)

    See also:
    https://en.wikipedia.org/wiki/Lattice_graph
    http://mathworld.wolfram.com/LatticeGraph.html
    for related
    """
    return GraphProduct(Pn(n),Pn(m))

def Lnm(n,m):
    """
    Lattice graph

    https://en.wikipedia.org/wiki/Lattice_graph
    http://mathworld.wolfram.com/LatticeGraph.html

    Lnm(n,m) = Kn(n) x Kn(m)
    """
    return GraphProduct(Kn(n),Kn(m))
    
def CreateGridGeometry(doc,w,h):
    """
    Create a grid geometry of pts size n x n

    It assumes a doc["object"] attribute containing
    (u,v) the u,v coordinate of a vertex.
    """
    doc2 = deepcopy(doc)
    doc2["pts"] = []
    umax,vmax = max(doc["object"])
    for obj in doc2["object"]:
        u,v = obj
        x = w/2.0 + mapto.MapTo(umax/2.0,w/2.0,umax,w,u)
        y = h/2.0 + mapto.MapTo(vmax/2.0,h/2.0,vmax,h,v)
        z = 0
        pt = [x,y,z]
        pt = map(int,map(round,pt))
        doc2["pts"].append(pt)
    return doc2

def TransitiveClosure(doc,K):
    """
    Obtains for G = doc, the graph
    E = (G**0)["E"] + (G**1)["E"] + (G**2)["E"]) + ... + (G**K)["E"]
    so the transitive closure is TransitiveClosure(doc,infinity)
    with infinity a large integer n > len(G["V"]),
    with (G**k) as GraphPow(G,k).
    """
    doc1 = deepcopy(doc)
    E = []
    for k in range(K):
        for e in GraphPow(doc,k)["E"]:
            if e not in E:
                E.append(e)
    doc1["E"] = E
    return doc1

def HasseGraph(doc,K):
    """
    Obtains the Hasse Graph of graph document G = doc,
    by subtracting doc - G**0 - G**2 - G**3 - ... -G**K
    for i != 1
    """
    doc1 = deepcopy(doc)
    for v in doc1["V"]:
        try:
            doc1["E"].remove([v,v])
        except:
            continue
    for k in range(K,1,-1): # K downto 2
        H = GraphPow(doc1,k)
        for e in H["E"]:
            try:
                doc1["E"].remove(e)
            except:
                continue
    return doc1

def CartesianProduct(S1,S2,maxtime=30):
    S = []
    start = Time()
    done = False
    for x in S1:
        if done:
            break
        for y in S2:
            z = []
            flag1 = (type(x) == type([]))
            flag2 = (type(y) == type([]))
            if not flag1:
                x = [x]
            if not flag2:
                y = [y]
            z = x + y
            S.append(z)
            stop = Time()
            if stop-start >= maxtime:
                done = True
                print "Exceeded Computation time, maxtime of ",maxtime,"seconds"
                print "CartesianProduct: Operation not complete"
                break
    print "CartesianProduct: S is size (bytes):",sys.getsizeof(S)
    stop = Time()
    print "Elapsed Time (seconds):",stop-start
    return S

def Domain(R):
    domain = list(set(map(lambda tup: tup[0], R)))
    return domain
def Range(R):
    range0 = list(set(map(lambda tup: tup[1], R)))
    return range0
def PreImage(R,y):
    Ry = filter(lambda tup: tup[1]==y, R)
    return Ry
def Image(R,x):
    Rx = filter(lambda tup: tup[0]==x, R)
    return Rx 

def Knm(n,m):
    """
    Creates a bipartite graph Knm from n vertices on
    left to m vertices on right where each vertex on left
    is connected to each vertex on right.
    https://en.wikipedia.org/wiki/Bipartite_graph
    """
    V = range(n+m)
    obj = []
    E = []
    for i in range(n):
        for j in range(m):
            obj.append([i,j])
            E.append([i,j+n])
    doc = {}
    doc["V"] = V
    doc["E"] = E
    doc["obj"] = obj
    return doc

def RelationGraph(R):
    """
    R is a relation, a list of pairs [r,s]
    with domain = Domain(R) and range0 = Range(R)
    then create graph for the relation with
    relation stored as G["obj"].
    """
    obj = deepcopy(R)
    domain = Domain(R)
    range0 = Range(R)
    V = range(len(domain)+len(range0))
    E = []
    n = len(domain)
    for i in range(len(domain)):
        for j in range(len(range0)):
            e = [domain[i],range0[j]]
            if e in R:
                f = [i,j+n]
                if f not in E:
                    E.append(f)                
    G = {}
    G["V"] = V
    G["E"] = E
    G["obj"] = obj
    return G

def RandomGraph(nvertices=10,nedges=10,maxedges=100,maxcount=100):
    G = {}
    V = range(nvertices)
    E = []
    count = 0
    while (len(E) < nedges) and (len(E) < maxedges) and (count < maxcount):
        u = random.choice(V)
        v = random.choice(V)
        e = [u,v]
        if e not in E:
            E.append(e)
        count += 1
    G['V'] = V
    G['E'] = E
    return G

def RandomFunction(ndomain=10,nrange=10):
    V1 = range(ndomain)
    V2 = range(nrange)
    R = []
    for u in V1:
        v = random.choice(V2)
        R.append([u,v])
    return R
def RandomFunctionGraph(ndomain=10,nrange=10):
    R = RandomFunction(ndomain,nrange)
    G = RelationGraph(R)
    return G
def RandomAutomorphismGraph(n=10):
    G = {}
    R = []
    try:
        import numpy.random as npr
        pi = list(npr.permutation(n))
        for i in range(n):
            R.append([i,pi[i]])
        G = RelationGraph(R)
        return G
    except:
        print "Error: You need numpy library (to generate random permutation)"
        G['V'] = range(10)
        G['E'] = []
        return G

def MergeVerticesPseudo(G,S):
    v = S[0]
    V = []
    for u in G['V']:
        if u == v:
            V.append(v)
        if u in S:
            continue
        else:
            V.append(u)
    E = []
    for e in G['E']:
        u0,v0 = e
        f = [u0,v0]
        if (u0 in S) and (v0 in S):
            f = [v,v]
        elif u0 in S:
            f = [v,v0]
        elif v0 in S:
            f = [u0,v]
        if f != [v,v] and f not in E:
            E.append(f)
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    return G2

def PseudoToGraph(G):
    V = range(len(G['V']))
    d = {}
    i = 0
    for i in V:
        v = G['V'][i]
        d[v] = i
    E = []
    for e in G['E']:
        u,v = e
        f = [d[u],d[v]]
        E.append(f)
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    return G2

def Snm(n,m):
    """
    Create a sphere graph from Gnm(n,m) by glueing
    together top vertices and bottom vertices and left
    side to right side
    """
    # grid graph
    G2 = Gnm(n,m)
    # top side
    V1 = filter(lambda v: G2['object'][v][1]==0,G2['V'])
    # bottom side
    V2 = filter(lambda v: G2['object'][v][1]==m-1,G2['V'])
    G1 = MergeVerticesPseudo(G2,V2)
    G = MergeVerticesPseudo(G1,V1)
    # left side
    V3 = filter(lambda v: G2['object'][v][0]==0,G2['V'])
    # right side
    V4 = filter(lambda v: G2['object'][v][0]==n-1,G2['V'])
    # for pairing (x,y) with x on left and y on right
    for tup in zip(V3,V4):
        u,v = tup
        G = MergeVerticesPseudo(G,[u,v])
    # now standardize the graph to use V = range(len(V))
    # relabeling edge's vertices
    G3 = PseudoToGraph(G)
    return G3

def Tnm(n,m):
    """
    Create torus graph G = GraphProduct(Cn(n),Cn(m)).
    """
    return GraphProduct(Cn(n),Cn(m))

def GraphUnionPseudo(G1,G2):
    G = {}
    G['V'] = zip(G1['V'],[0]*len(G1['V']))+\
             zip(G2['V'],[1]*len(G2['V']))
    G['E'] = map(lambda e: [(e[0],0),(e[1],0)],G1['E'])+\
             map(lambda e: [(e[0],1),(e[1],1)],G2['E'])
    return G

def GraphUnion(G1,G2):
    H = GraphUnionPseudo(G1,G2)
    G = PseudoToGraph(H)
    return G

def Tadpole_Tnm(n,m):
    """
    Create Tadpole graph Tadpole_Tnm(n,m)
    G = GraphUnionPseudo(Cn(n),Pn(n))
    with edge between vertex 0 in Cn(n) and
    vertex 0 in Pn(n).
    """
    G1 = Cn(n)
    G2 = Pn(m)
    H = GraphUnionPseudo(G1,G2)
    H['E'].append([(0,0),(0,1)])
    G = PseudoToGraph(H)
    return G

def TensorProduct(G1,G2):
    H1 = deepcopy(G1)
    H1 = PseudoToGraph(H1)
    H2 = deepcopy(G2)
    H2 = PseudoToGraph(H2)
    V = CartesianProduct(H1['V'],H2['V'])
    V = map(lambda v: tuple(v), V)
    E = []
    for u in V:
        for v in V:
            u1,u2 = u
            v1,v2 = v
            if [u2,v2] in H2['E'] and \
               [u1,v1] in H1['E']:
                E.append([tuple(u),tuple(v)])
    G = {}
    G['V'] = V
    G['E'] = E
    G = PseudoToGraph(G)
    return G

