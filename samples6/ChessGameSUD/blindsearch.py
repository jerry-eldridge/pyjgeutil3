from copy import deepcopy

# [1] @book{Ginsberg93,
# author = "Ginsberg, Matt",
# title = "Essentials of Artificial Intelligence",
# publisher = "Morgan Kaufmann, San Mateo, CA",
# year = "1993"
# }
# (Algorithm for DFS Depth-first Search and
# BFS Breadth-first Search as a way to search a Game
# Tree).

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

def DFS(G,v):
    S = Stack()
    S.Push(v)
    V = deepcopy(G['V'])
    labeled = ["" for v in V]
    path = []
    while not S.Empty():
        v = S.Pop()
        path.append(v)
        idx = V.index(v)
        if labeled[idx] != "discovered":
            labeled[idx] = "discovered"
            N = OutAdj(G,v)
            for ww in N:
                S.Push(ww)
    return path

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

def BFS(G,v):
    Q = Queue()
    Q.Push(v)
    V = deepcopy(G['V'])
    labeled = ["" for v in V]
    path = []
    while not Q.Empty():
        v = Q.Pop()
        path.append(v)
        idx = V.index(v)
        if labeled[idx] != "discovered":
            labeled[idx] = "discovered"
            N = OutAdj(G,v)
            for ww in N:
                Q.Push(ww)
    return path

