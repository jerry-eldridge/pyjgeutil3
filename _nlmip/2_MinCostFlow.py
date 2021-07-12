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
    res = list(so.linprog(c,A_ub=A,b_ub=b,bounds=[(0,1)]*len(G['E']),
                          method='simplex').x)
    #print("res = ",res)
    Es = []
    for i in range(len(res)):
        if res[i] == 1.0:
            e = G['E'][i]
            u,v = e
            up = (u,G['L'][u])
            vp = (v,G['L'][v])
            tup = [up,vp,G['W'][i]]
            #print(tup,end=', ')
            Es.append(Edge._make(tup))
    #print(end='\n')
    #print("="*3)
    return Es

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
    Es = LinearProgramming(G,s,t)
    pred = {}
    for v in G['V']:
        vp = (v,G['L'][v])
        pred[vp] = None
    for tup in Es:
        u,v,cc = tup
        pred[v] = u
    #print("Es = ",Es)
    #print("pred = ",pred)
    return pred,Es
pred,Es = Find(G,s,t)

def DisplayPath(G,T2,Es,ii,jj):
    start = T1[ii] # select start
    goal = T1[jj] # select target
    u = goal
    path = []
    cost = 0
    while u != start:
        path.append(u)
        if u == None:
            break
        v = pred[u]
        if v is not None:
            e = [v[0],u[0]]
            k = G['E'].index(e)
            wt = G['W'][k]
            path.append(Weight._make([wt]))
            cost = cost + wt
        else:
            cost = oo
        u = v
    path.append(u)
    path.reverse()
    total_cost = 0
    for e in Es:
        u,v,cc = e
        total_cost = total_cost + cc
    return path,cost,total_cost
for si in s:
    u,cc = si
    for ti in t:
        v,cc2 = ti
        path,cost,net_cost = DisplayPath(G,T2,Es,u,v)
        if cost < oo:
            print("path = ",path)
            print("path_cost = ",cost)
            print("="*3)
print("Decisions net_cost = ",net_cost)
print("Decisions: Es=",Es)
print("Predecessor: pred=",pred)
