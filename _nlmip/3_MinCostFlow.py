from copy import deepcopy
from collections import namedtuple

Edge = namedtuple("Edge",["u","v","wt"])
Weight = namedtuple("Weight",["ecost"])

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

def LinearProgramming(G,s,t):
    import numpy as np
    import scipy.optimize as so
    print("G=",G)
    print("s=",s)
    print("t=",t)
    A = np.zeros((len(G['V']),len(G['E'])))
    oo = 100
    dist = {}
    for v in G['V']:
        dist[v] = 0
    for v in G['V']:
        S1 = InAdj(G,v)
        S2 = OutAdj(G,v)
        for e in G['E']:
            u1,u2 = e
            if u2 == v and u1 in S1:
                i = G['V'].index(v)
                j = G['E'].index(e)
                A[i,j] = A[i,j] - 1
            u1,u2 = e
            if u1 == v and u2 in S2:
                i = G['V'].index(v)
                j = G['E'].index(e)
                A[i,j] = A[i,j] + 1
    b = [0]*len(G['V'])
    #print("A=\n",A)
    for si in s:
        ii,cc = si
        b[ii] = cc
    for ti in t:
        ii,cc = ti
        b[ii] = cc
    #print("b=",b)
    c = deepcopy(G['W'])
    #print("c=",c)
    res = list(so.linprog(c,A_ub=A,b_ub=b,bounds=[(0,None)]*len(G['E']),
                          method='simplex').x)
    return list(zip(G['E'],res))

# assume positive weights G['W'] except when
# using BellmanFord algorithm.
G = {}
G['V'] = list(range(12)) # [0 to 11]
T1 = [
    (0,"a"),
    (1,"b"),
    (2,"c"),
    (3,"d"),
    (4,"e"),
    (5,"f"),
    (6,"g"),
    (7,"h"),
    (8,"i"),
    (9,"j"),
    (10,"k"),
    (11,"l")]
# edges, edge weight (e, w_e) with e = [u,v] for
# u,v in V
T2 = [
    ([0,1],3),
    ([1,4],1),
    ([1,5],2),
    ([4,10],1),
    ([5,10],2),
    ([10,11],3),
    ([0,2],4),
    ([0,3],3),
    ([2,6],1),
    ([2,7],2),
    ([6,9],4),
    ([7,9],2),
    ([9,11],1),
    ([3,8],2),
    ([8,9],1)]

G['E'] = []
G['W'] = []
G['L'] = [None]*len(G['V'])
for tup in T2:
    x,y = tup
    G['E'].append(x)
    G['W'].append(y)
for tup in T1:
    v,l = tup
    if v in G['V']:
        G['L'][v] = l
    else:
        print("Error: ",tup," -- vertex not in G['V']")
          

s = [(0, 3),(3, 6)] # [(source,flow)]
t = [(9, -5),(10, -4)] # [(target,flow)]
oo = 1e16

def Find(G,s,t):
    Ws = LinearProgramming(G,s,t)
    for tup in Ws:
        print(tup)
Find(G,s,t)

