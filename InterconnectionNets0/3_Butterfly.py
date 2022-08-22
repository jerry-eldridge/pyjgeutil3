from math import log
from copy import deepcopy

###############################################
# a_star_digraph.py
#
"""
http:#en.wikipedia.org/wiki/A*_search_algorithm
"""
from math import sqrt

def neighbor_nodes(G,current):
    V = G[0]
    E = G[1]
    S = set([])
    for e in E:
        S.add(str(e))
    L = []
    for v in V:
        if (str([current,v]) in S):
            L.append(v)
    return L

def A_star_digraph(G,start,goal, cost):
    emptyset = set([])
    closedset = emptyset    # The set of nodes already evaluated.
    openset = set([start])    # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = {}    # The map of navigated nodes.
    g_score = {}
    f_score = {}
    g_score[start] = 0    # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + cost(start, goal)

    while len(list(openset)) != 0:
        L = list(openset)
        L = sorted(L, key=lambda node: f_score[node])
        current = L[0]
        if current == goal:
            path = reconstruct_path(came_from, goal)
            path.reverse()
            return path
        openset.remove(current)
        closedset.add(current)
        for neighbor in neighbor_nodes(G,current):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + cost(current,neighbor)

            if (neighbor not in openset) or (tentative_g_score < g_score[neighbor]):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + cost(neighbor, goal)
                if neighbor not in openset:
                    openset.add(neighbor)
 
    return []
 
def reconstruct_path(came_from,current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path
#
############################################

#################################################
# butterfly.py
#
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
    G2['O'] = deepcopy(G['V'])
    return G2

def InAdj(doc,i):
    ii = doc['V'].index(i)
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[ii]
    for e in E:
        v,w = e
        if (u == w):
            adj.append(v)
    return adj

def OutAdj(doc,i):
    ii = doc['V'].index(i)
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[ii]
    for e in E:
        v,w = e
        if (u == v):
            adj.append(w)
    return adj

def Base(i,base, bits):
    L = []
    j = 0
    n = 0
    ii = i
    for j in range(bits):
        a = ii%base
        ii = int(ii/base)
        n = n + a*base**j
        L.append(a)
    L.reverse()
    return L

def Number(L,base):
    n = 0
    k = len(L)-1
    for i in range(len(L)):
        n = n + L[k-i]*base**i
    return n

def S(i,j,p,base):
    x = Base(j,base,int(round(log(p)/log(base))))
    x[i] = x[i]^1
    v = Number(x,base)
    return v,x

# [1] https://en.wikipedia.org/wiki/Butterfly_network
def Butterfly(p,base=2):
    N2 = p
    N1 = int(log(p)/log(base))
    n = (N1+1)*N2
    G = {}

    G['V'] = []
    for i in range(N1+1):
        for j in range(N2):
            u = (i,j)
            G['V'].append(u)

    G['E'] = []
    for i in range(N1):
        for j in range(N2):
            u = (i,j)
            v = ((i+1)%(N1+1),j)
            m,x = S(i,j,p,base)
            w = ((i+1)%(N1+1),m)
            e1 = [u,v]
            e2 = [u,w]
            G['E'].append(e1)
            G['E'].append(e2)
    return G
#
############################################

G1 = Butterfly(p=8,base=2)
G1b = PseudoToGraph(G1)
print("G1 = ", G1)
print("G1b = ", G1b)
def cost(u,v):
    oo = 1e8
    if [u,v] in G1['E']:
        return 1
    else:
        return oo

# 
start = (0,5)
goal = (3,2)
path = A_star_digraph((G1['V'],G1['E']),
                start,goal, cost)
print("path = ", path)
