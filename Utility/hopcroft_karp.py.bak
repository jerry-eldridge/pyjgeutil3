import graph
import queue

# https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
# finds a maximum matching in a bipartite graph (Dom,Ran) with edges Bi.
class HopcroftKarp:
    def __init__(self,Dom,Ran,Bi):
        self.Bi = Bi
        self.Dom = Dom
        self.Ran = Ran
        self.U = []
        self.V = []
        self.NIL = 0
        self.G = self.DefineGraph()
        self.Pair_U = {}
        self.Pair_V = {}
        self.oo = 1e8
        self.Dist = {}
        self.matching = -1
        return
    def doit(self):
        self.matching = self.HopcroftKarp()
        return self.matching, self.Pair_U, self.Pair_V
    def GetMap(self):
        m,d1,d2 = self.doit()
        d3 = {}
        for key in d1.keys():
            try:
                d3[self.Dom[key]] = self.Ran[d1[key]-len(self.Dom)]
            except:
                d3[self.Dom[key]] = "unmatched"
        return d3
    def DefineGraph(self):
        U0 = zip(self.Dom,[0]*len(self.Dom))
        V0 = zip(self.Ran,[1]*len(self.Ran))
        n1 = len(U0)
        n2 = len(V0)
        NIL = n1+n2
        Vdesc = U0 + V0 + [(NIL,2)]
        V = range(len(Vdesc))
        E = []
        for i in V:
            x1,y1 = Vdesc[i]
            if y1 != 0:
                continue
            for j in V:
                x2,y2 = Vdesc[j]
                if y2 != 1:
                    continue
                if [x1,x2] in self.Bi:
                    E.append([i,j])
        G = {}
        G['V'] = V
        G['Vdesc'] = Vdesc
        G['E'] = E
        self.U = range(n1)
        self.V = range(n1,n1+n2)
        self.NIL = NIL
        return G

    # https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
    def BFS(self):
        Q = queue.Queue()
        for u in self.U:
            if self.Pair_U[u] == self.NIL:
                self.Dist[u] = 0
                Q.Push(u)
            else:
                self.Dist[u] = self.oo
        self.Dist[self.NIL] = self.oo
        while Q.Empty() == False:
            u = Q.Pop()
            if self.Dist[u] < self.Dist[self.NIL]:
                for v in graph.Adj(self.G,u):
                    if self.Dist[self.Pair_V[v]] == self.oo:
                        self.Dist[self.Pair_V[v]] = self.Dist[u] + 1
                        Q.Push(self.Pair_V[v])
        return self.Dist[self.NIL] != self.oo     

    # https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
    def DFS(self,u):
        if u != self.NIL:
            for v in graph.Adj(self.G,u):
                if self.Dist[self.Pair_V[v]] == self.Dist[u] + 1:
                    if self.DFS(self.Pair_V[v]) == True:
                        self.Pair_V[v] = u
                        self.Pair_U[u] = v
                        return True
            self.Dist[u] = self.oo
            return False
        return True

    # https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
    def HopcroftKarp(self):
        for u in self.U:
            self.Pair_U[u] = self.NIL
        for v in self.V:
            self.Pair_V[v] = self.NIL
        matching = 0
        while self.BFS() == True:
            for u in self.U:
                if self.Pair_U[u] == self.NIL:
                    if self.DFS(u) == True:
                        matching = matching + 1
        return matching

def SDR(S):
    """
    System of Distinct representatives
    SDR([[1,3,5,7],[1,2,6],[3,5,6],[2,5,6],[4,6],[3,5],[1,4,7]])
0 1
1 2
2 6
3 5
4 4
5 3
6 7
    """
    def E(u,S):
        return map(lambda v: [u,v], S)
    Dom = range(len(S))
    Ran = set([])
    for e in S:
        Ran = Ran.union(set(e))
    Ran = list(Ran)
    Bi = []
    i = 0
    for e in S:
        Bi += E(i,e)
        i += 1
    hk = HopcroftKarp(Dom,Ran,Bi)
    d = hk.GetMap()
    for key in d.keys():
        print key, d[key]
    return d

