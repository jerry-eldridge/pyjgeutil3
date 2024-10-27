from .common import affine as aff
from copy import deepcopy

def transform_graph(G,T,R,S,Pivot=[0,0,0]):
    shape1 = deepcopy(G['pts'])
    C = aff.Center(shape1,flag2d=False)
    q = aff.HH.FromEuler(*R)
    shape2 = aff.Translate(shape1,
                -C[0],-C[1],-C[2],align=False)
    shape3 = aff.Scale(shape2, *S, align=False)
    shape4 = aff.Translate(shape3,
               *Pivot, align=False)
    shape5 = aff.Rotate(shape4,q,align=False)

    shape6 = aff.Translate(shape5,
               *T,align=False)
    G2 = G
    G2['pts'] = deepcopy(shape6)
    return G2

def transform_graph_G(G,G0, T,R,S,Pivot=[0,0,0]):
    shape1 = deepcopy(G['pts'])
    C = aff.Center(G0['pts'],flag2d=False)
    q = aff.HH.FromEuler(*R)
    shape2 = aff.Translate(shape1,
                -C[0],-C[1],-C[2],align=False)
    shape3 = aff.Scale(shape2, *S, align=False)
    shape4 = aff.Translate(shape3,
               *Pivot, align=False)
    shape5 = aff.Rotate(shape4,q,align=False)

    shape6 = aff.Translate(shape5,
               *T,align=False)
    G2 = G
    G2['pts'] = deepcopy(shape6)
    return G2

class GeometricalObject:
    def __init__(self, G, name):
        self.G = G
        self.name = name
    def transform(self, T, R, S, Pivot=[0,0,0]):
        self.G = transform_graph(self.G,
                    T,R,S,Pivot)
        return
    def transform_G(self, G, T, R, S, Pivot=[0,0,0]):
        self.G = transform_graph_G(self.G,
                    G,T,R,S,Pivot)
        return
