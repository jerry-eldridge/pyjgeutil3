import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import graph

G = {}
G['V'] = range(7)
G['E'] = [[0,1],[1,2],[0,2],[2,3],[3,4],[4,5],
          [5,6],[4,6]]
print(f"Graph G = {G}")
# 0 ~ 0, 1 ~ 1, 5 ~ 5, 6 ~ 6, 2 ~ 3 ~ 4 defines
# equivalence relation ~.
R = [[0],[1],[5],[6], [2,3,4]] # glue 2,3,4 together
print(f"Equivalence Relation R = {R}")
# G2 = G/~ where ~ defined by R.
G2 = graph.QuotientGraph(G, R)
print(f"G2 = graph.QuotientGraph(G,R) = \n{G2}")
