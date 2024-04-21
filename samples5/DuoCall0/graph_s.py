from copy import deepcopy

import random

def Degree(doc,v):
    return len(Adj(doc,v))

def Adj(doc,i):
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

def AdjMatrix(doc):
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
    doc["V"] = list(range(n))
    doc["E"] = []
    doc["weights"] = []
    for u in range(n):
        for v in range(n):
            if A[u,v] != 0:
                doc["E"].append([u,v])
                doc["weights"].append(A[u,v])
    return doc
      
def PathEdges(path):
    path0 = deepcopy(path)
    L = []
    i = 0
    for i in range(len(path)-1):
        e = [path0[i],path0[i+1]]
        L.append(e)
    return L

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

def AddVertex(doc):
    doc2 = deepcopy(doc)
    V = doc2["V"]
    n = len(V)
    doc2["V"] = list(range(n+1))
    return doc2,n

def AddEdge(doc,e):
    doc2 = deepcopy(doc)
    E = doc2["E"]
    E.append(e)
    doc2["E"] = E
    return doc2

def Cn(N=3):
    if N < 3:
        print("Error: Cycle must have at least 3 vertices")
        return {}
    doc = {"V":list(range(N)),"E":PathEdges(list(range(N)))+[[N-1,0]]}
    return doc

def Pn(N):
    doc = {}
    doc["V"] = list(range(N))
    doc["E"] = PathEdges(list(range(N)))
    return doc

def InAdj(doc,i):
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
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for e in E:
        v,w = e
        if (u == v):
            adj.append(w)
    return adj

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

def IncidenceMatrix(doc):
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

def Knm(n,m):
    V = list(range(n+m))
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

def PseudoToGraph(G):
    V = list(range(len(G['V'])))
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
    G2['names'] = deepcopy(G['V'])
    return G2
