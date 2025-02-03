from .common import affine as aff
from copy import deepcopy

def transform_graph(G,T,R,S,Pivot=[0,0,0]):
    shape = deepcopy(G['pts'])
    C = aff.Center(shape,flag2d=False)
    q = aff.HH.FromEuler(*R)
    shape2 = aff.Translate(shape,
                -C[0],-C[1],-C[2],align=False)
    shape = aff.Scale(shape2, *S, align=False)
    shape2 = aff.Translate(shape,
               *Pivot, align=False)
    shape = aff.Rotate(shape2,q,align=False)

    shape2 = aff.Translate(shape,
               *T,align=False)
    G2 = G
    G2['pts'] = shape2
    return G2

class GeometricalObject:
    def __init__(self, G, name):
        self.G = G
        self.name = name
    def get_C(self):
        shape = deepcopy(self.G['pts'])
        C = aff.Center(shape,flag2d=False)
        return C
    def transform(self, T, R, S, Pivot=[0,0,0]):
        self.G = transform_graph(self.G,
                    T,R,S,Pivot)
        return

