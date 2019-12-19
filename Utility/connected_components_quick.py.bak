import graph as g
import numpy as np

# Laplacian of a graph
def Laplacian(G):
    # the laplacian of a graph assumes G is a simple graph
    # which has no loops e = [u,u], multiple copies of e
    # and undirected edges e = [u,v] and f = [v,u] both would
    # be edges.
    G = g.MakeUndirected(G)

    D = np.diag(map(lambda v: g.Degree(G,v),G['V']))
    A = g.AdjMatrix(G)
    L = D - A
    return L

def NumberOfComponents(G):
    # calculate the graph Laplacian
    L = Laplacian(G)
    try:
        a = list(np.linalg.eigvals(L))
    except:
        return 0
    epsilon = 0.001
    # the multiplicity of eigenvalue 0 of laplacian matrix L
    c = len(filter(lambda x: abs(x)<epsilon, a))
    return c

def IsAForest(doc):
    c = NumberOfComponents(doc)
    V = doc["V"]
    E = doc["E"]
    e = len(E)/2 # we assume undirected edges
    v = len(V)
    residue = e - (v - c)
    return residue == 0

def IsATree(doc):
    #c = NumberOfComponents(doc)
    V = doc["V"]
    E = doc["E"]
    e = len(E)/2 # we assume undirected edges
    v = len(V)
    residue = e - (v - 1)
    return residue == 0
