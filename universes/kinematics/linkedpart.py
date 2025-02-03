from ..shapes.common import graph as g
from ..shapes.common import connected_components as cc
from ..shapes.common import a_star_digraph as asd

from copy import deepcopy
import numpy as np

# Could modify to add to graph.py
def DeleteVerticesPseudo(G,S):
     G2 = g.DeleteVertices(G,S)
     V = deepcopy(G2['subgraph_to_graph_V'])
     while None in V:
         V.remove(None)
     E = deepcopy(G2['subgraph_to_graph_E'])
     while None in E:
         E.remove(None)
     E = [G['E'][ei-1] for ei in E]
     G3 = {}
     G3['V'] = V
     G3['E'] = E
     return G3

# Could modify to add to connected_components.py
def DeleteComponentOfVertexPseudo(G,v):
     C = cc.ConnectedComponentsBrute(G)
     for Cl in C:
         if v in Cl:
             break
     G2 = DeleteVerticesPseudo(G,Cl)
     return G2

def DependentVertices(G,root,v):
     """
     Find the graph G1 before vertex v
     and remove that graph part to get
     remaining graph. Then return G1['V']
     as the vertices including and after
     vertex v such as in joint-bone skeleton
     linked systems such as a rag-doll model.
     For a rotation at v, each of these
     returned vertices are rotated.
     """
     G0 = deepcopy(G)
     def cost(u,v):
         oo = 1e8
         e = [u,v]
         if e in G0['E']:
             return 1
         else:
             return oo
     Gtup = (G0['V'],G0['E'])
     path = asd.A_star_digraph(Gtup,root,v, cost)
     if len(path) >= 2:
         u = path[-2]
         try:
             G0['E'].remove([u,v])
         except:
             i = 0
         try:
             G0['E'].remove([v,u])
         except:
             i = 0
         G1 = DeleteComponentOfVertexPseudo(G0,u)
         return G1['V'],path
     else:
         return G0['V'],path

def Index(G,e):
    u,v = e
    try:
        idx = G1['E'].index(e)
    except:
        idx = -1
    return idx

def LinkedPart(G1,root,v):
     S,path = DependentVertices(G1,root,v)
     P = path[:-1]+S
     return P

def PathPart(G1,root,v):
     G0 = deepcopy(G1)
     def cost(u,v):
         oo = 1e8
         e = [u,v]
         if e in G0['E']:
             return 1
         else:
             return oo
     Gtup = (G0['V'],G0['E'])
     path = asd.A_star_digraph(Gtup,root,v, cost)
     return path
