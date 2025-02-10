import sys
sys.path.insert(0,
    r"C:/Users/jerry/Desktop/_Art/my_universes/")
import universes
import universes.shapes.common.graph as gra
import universes.shapes.common.a_star_doc_nd as asdn
import universes.shapes.common.graphic_matroid as gmat
import universes.canvas2d.graphics_cv as racg

from copy import deepcopy

def PlotGraph(gr,G,color=[0,0,0]):
     for v in G['V']:
         A = G['pts'][v][:2]
         gr.Label(str(v),A,colorpt = color,
                  colortxt = color)
     for e in G['E']:
         u,v = e
         A,B = list(map(lambda w: G['pts'][w], [u,v]))
         gr.Line(A,B,color=color)
     return

G1 = gra.Cn(4)
G2 = gra.Cn(3)
G3 = gra.Cn(4)
print(f"G1 = {G1}")
print(f"G2 = {G2}")
print(f"G3 = {G3}")
print("Computing graph union, \/ Gi = G1 \/ G2 \/ G3")
G = deepcopy(G1)
G = gra.GraphUnionPseudo(G,G2)
G = gra.GraphUnionPseudo(G,G3)
G = gra.PseudoToGraph(G)
print(f"""
G is kept as an undirected graph to reduced |E| count
G = PseudoToGraph(\/ Gi) = {G}
Adding edges [0,6] and [1,7] to G['E']
""")
Es = [[0,4],[1,5],[4,5]]
print(f"Es = {Es}")
for e in Es:
     u,v = e
     f = [v,u]
     if not (e in G['E'] or f in G['E']):
         G['E'].append(e)
print(f"G = G \/ Es = {G}")
CC = gmat.GraphCycles(G)
w = 600
h = 600
gr = racg.Graphics(w=w,h=h)
cx = w/2
cy = h/2
cz = 0
r = 200
G = gra.CreateCircleGeometry(G,cx,cy,cz,r)
black = [0,0,0]
red = [255,0,0]
for ES in CC:
     print(f"Cycle= {ES}")
     gr.Clear()
     PlotGraph(gr,G,color=black)
     for e in ES:
         u,v = e
         A,B = list(map(lambda w: G['pts'][w], [u,v]))
         gr.Line(A,B,color=red)
     ch = gr.Show("result",-1)
     if ch == ord('e'):
         break
gr.Close()
