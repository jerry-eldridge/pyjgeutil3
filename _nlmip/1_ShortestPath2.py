from math import floor
from copy import deepcopy

class Heap:
    def Parent(self,i):
        return int(floor(i/2))
    
    def Left(self,i):
        return 2*i + 1
    
    def Right(self,i):
        return 2*i + 2
    
    def __init__(self,A,compare):
        self.A = deepcopy(A)
        self.heapsize = 0
        self.compare = compare
        self.BuildHeap()
        return
    def Empty(self):
        return self.heapsize == 0
    def Heapify(self,i):
        l = self.Left(i)
        r = self.Right(i)
        if (l < self.heapsize) and (self.compare(self.A[l],self.A[i])):
            largest = l
        else:
            largest = i
        if (r < self.heapsize) and (self.compare(self.A[r],self.A[largest])):
            largest = r
        if not (largest == i):
            tmp = self.A[i]
            self.A[i] = self.A[largest]
            self.A[largest] = tmp
            self.A = self.Heapify(largest)
        return self.A

    def BuildHeap(self):
        self.heapsize = len(self.A)
        for i in range(int(floor(len(self.A)/2))-1,-1,-1):
            self.A = self.Heapify(i)
        return

    def HeapSort(self):
        self.BuildHeap()
        self.heapsize = len(self.A)
        for i in range(len(self.A)-1,0,-1):
            tmp = self.A[0]
            self.A[0] = self.A[i]
            self.A[i] = tmp
            self.heapsize = self.heapsize - 1
            self.A = self.Heapify(0)
        return self.A

    def HeapExtract(self):
        if self.heapsize < 0:
            print("Error: heap underflow")
            return
        val = self.A[0]
        self.A[0] = self.A[self.heapsize-1]
        self.heapsize = self.heapsize - 1
        self.A = self.Heapify(0)
        return val

    def HeapInsert(self,key):
        self.heapsize = self.heapsize + 1
        i = self.heapsize-1
        self.A = self.A+[key]
        while (i > 0) and (not self.compare(self.A[self.Parent(i)],key)):
            self.A[i] = self.A[self.Parent(i)]
            i = self.Parent(i)
        self.A[i] = key
        return

class Queue:
    def __init__(self):
        self.L = []
        self.undef = None
        return
    def Initialize(self):
        self.__init__()
        return
    def Push(self,item):
        self.L = [item] + self.L 
        return
    def Pop(self):
        if self.Empty():
            return self.undef
        item = self.L[-1] # car
        self.L = self.L[:-1] # cdr
        return item
    def Empty(self):
        return self.L == []

class Stack:
    def __init__(self):
        self.L = []
        self.undef = None
        return
    def Initialize(self):
        self.__init__()
        return
    def Push(self,item):
        self.L = [item]+self.L
        return
    def Pop(self):
        if self.Empty():
            return self.undef
        item = self.L[0] # car
        self.L = self.L[1:] # cdr
        return item
    def Empty(self):
        return self.L == []

def InAdj2(doc,i):
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for k in range(len(E)):
        e = E[k]
        v,w = e
        if (u == w):
            adj.append((v,k))
    return adj

def OutAdj2(doc,i):
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for k in range(len(E)):
        e = E[k]
        v,w = e
        if (u == v):
            adj.append((w,k))
    return adj


import random

random.seed(0)
rnd = lambda x: int(random.uniform(0,100))
L = list(map(rnd,range(50)))

Q = Queue()
S = Stack()

order = lambda x,y: x < y
H = Heap(L,order)

def Path(t,dist,pred):
    L = [(t,dist[t])]
    try:
        v = pred[t]
        while v != s:
            L.append((v,dist[v]))
            v = pred[v]
    except:
        i = 0
    L.append((s,dist[s]))
    L.reverse()
    return L

def LabelPath(p):
    L = list(map(lambda tup: {"idx":tup[0],"name":G['L'][tup[0]],"cost":tup[1]}, p))
    return L

# [1] https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
# Bellman-Ford algorithm, wikipedia
# [2] https://en.wikipedia.org/wiki/Shortest_path_problem
def BellmanFord(G, s, t):
    V = G['V']
    E = G['E']
    W = G['W'] # edge weights
    dist = {}
    pred = {}
    oo = 1e8
    null = None
    for v in V:
        dist[v] = oo
        pred[v] = null

    dist[s] = 0

    pa = str(s)
    for i in range(1,len(V)):
        for j in range(len(E)):
            e = E[j]
            u,v = e
            w = W[j] # weight w of edge e
            if dist[u] + w < dist[v]:
                pa = pa + ","+str(v)
                dist[v] = dist[u] + w
                pred[v] = u

    for i in range(len(E)):
        e = E[i]
        u,v = e
        w = W[i] # weight w of edge e
        if dist[u] + w < dist[v]:
            print("Error: graph contains a negative weight cycle")
            dist = {}
            pred = {}
            return dist,pred
    print(pa)
    return dist, pred

# [3] "Dynamic Programming and Optimal Control",
#  4th ed, 2017, Dimitri P. Bertsekas, Athena
#  Scientific. (Label Correcting Algorithms)
def BreadthFirst(G,s,t):
    dist = {}
    pred = {}
    oo = 1e8
    null = None
    upper = oo
    V = G['V']
    E = G['E']
    W = G['W']
    for v in V:
        dist[v] = oo
        pred[v] = null
    dist[s] = 0
    O = Queue()
    O.Push(s)
    pa = ""
    while not O.Empty():
        i = O.Pop()
        pa = pa + "," + str(i)
        for tup in OutAdj2(G,i):
            j,k = tup
            if dist[i]+W[k] < min(dist[j],upper):
                dist[j] = dist[i] + W[k]
                pred[j] = i
                if j != t:
                    if j not in O.L:
                        O.Push(j)
                else:
                    upper = dist[i] + W[k]
    print(pa)
    return dist,pred

# [3] see above
def DepthFirst(G,s,t):
    dist = {}
    pred = {}
    oo = 1e8
    null = None
    upper = oo
    V = G['V']
    E = G['E']
    W = G['W']
    for v in V:
        dist[v] = oo
        pred[v] = null
    dist[s] = 0
    S = Stack()
    S.Push(s)
    pa = ""
    while not S.Empty():
        i = S.Pop()
        pa = pa + "," + str(i)
        for tup in OutAdj2(G,i):
            j,k = tup
            if dist[i]+W[k] < min(dist[j],upper):
                dist[j] = dist[i] + W[k]
                pred[j] = i
                if j != t:
                    if j not in S.L:
                        S.Push(j)
                else:
                    upper = dist[i] + W[k]
    print(pa)
    return dist,pred

# [3] see above
def BestFirst(G,s,t):
    dist = {}
    pred = {}
    oo = 1e8
    null = None
    upper = oo
    V = G['V']
    E = G['E']
    W = G['W']
    for v in V:
        dist[v] = oo
        pred[v] = null
    dist[s] = 0
    LT = lambda x,y: x < y
    H = Heap([],LT) # priority queue using a Heap
    H.HeapInsert(s)
    pa = ""
    while not H.Empty():
        i = H.HeapExtract()
        pa = pa + "," + str(i)
        for tup in OutAdj2(G,i):
            j,k = tup
            if dist[i]+W[k] < min(dist[j],upper):
                dist[j] = dist[i] + W[k]
                pred[j] = i
                if j != t:
                    H.HeapInsert(j)
                else:
                    upper = dist[i] + W[k]
    print(pa)
    return dist,pred

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
    print("A=\n",A)
    b[s] = 1
    b[t] = -1
    print("b=",b)
    c = deepcopy(G['W'])
    print("c=",c)
    res = list(so.linprog(c,A_ub=A,b_ub=b,bounds=[(0,1)]*len(G['E']),
                          method='simplex').x)
    print("res = ",res)
    pred = {}
    for i in range(len(res)):
        if res[i] == 1:
            e = G['E'][i]
            u,v = e
            pred[v] = u
    path = []
    u = t
    while u != s:
        path.append(u)
        u = pred[u]
    path.append(u)
    path.reverse()
    if len(path) > 2:
        u = path[0]
        for v in path[1:]:
            e = [u,v]
            print(e)
            i = G['E'].index(e)
            dist[v] = dist[u] + G['W'][i]
            u = v
    return dist,pred
def Display(G,s,t, c):
    import time
    assert(len(G['W'])==len(G['E']))
    print("s,t =",s,t)
    print("G = ",G)
    if c == 0:
        print("BellmanFord")
        start = time.time()
        dist,pred = BellmanFord(G,s,t)
        end = time.time()
        print("Time elapsed: ", end-start)
    elif c == 1:
        print("BreadthFirst")
        start = time.time()
        dist,pred = BreadthFirst(G,s,t)
        end = time.time()
        print("Time elapsed: ", end-start)
    elif c == 2:
        print("DepthFirst")
        start = time.time()
        dist,pred = DepthFirst(G,s,t)
        end = time.time()
        print("Time elapsed: ", end-start)
    elif c == 3:
        print("BestFirst")
        start = time.time()
        dist,pred = BestFirst(G,s,t)
        end = time.time()
        print("Time elapsed: ", end-start)
    elif c == 4:
        print("LinearProg")
        start = time.time()
        dist,pred = LinearProgramming(G,s,t)
        end = time.time()
        print("Time elapsed: ", end-start)
    else:
        print("Error: choices can be 0,1,2")
        return
    p = Path(t,dist,pred)
    p2 = LabelPath(p)
    print("path: ",p2)
    print("="*30)
    return


# assume positive weights G['W'] except when
# using BellmanFord algorithm.
G = {}
G['V'] = list(range(12)) # [0 to 11]
# edges, edge weight (e, w_e) with e = [u,v] for
# u,v in V
T = [
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
for tup in T:
    x,y = tup
    G['E'].append(x)
    G['W'].append(y)

# could use any labels or use str(i) as the label.
# use labels G['L'][k] 'a' through 'l' for G['V'][k]
G['L'] = list(map(lambda i: chr(+ord('a')+i), range(12)))

s = 0
t = 11
Display(G,s,t, c=0)   
Display(G,s,t, c=1) 
Display(G,s,t, c=2)
Display(G,s,t, c=3)
Display(G,s,t, c=4)
