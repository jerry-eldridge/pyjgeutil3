import sys
sys.path.append(\
    r"C:/Users/jerry/Desktop/_Art/my_universes")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as bs
import universes.volume_of_OBJ as voo
import universes.transform_shape as ts
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.common.vectors as vec
import universes.shapes.common.CoordSystem as cs
import universes.shapes.common.human_doll as hd
import universes.shapes.common.graph as gra
import universes.shapes.alg_topo as topo
import universes.shapes.AT_BasicShapes as atbs
import universes.canvas2d.graphics_cv as racg

import numpy as np
from functools import reduce
from copy import deepcopy
import time

from math import cos,sin,pi,atan2,sqrt,exp

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

def copy_graph(G):
    G2 = {}
    K = list(G.keys())
    for key in K:
        G2[key] = deepcopy(G[key])
    return G2

BIGDATA = r"./"
fn_save = BIGDATA+"AT_annulus.obj"
g = open(fn_save,'w')
Sce = so.Scene()
G = atbs.create_AT_annulus(n=20,
        a1=300,b1=300,a2=50,b2=50,h=50)
Sce.add(G,"AT_annulus","AT_annulus.mtl","AT_annulus")
Sce.select("AT_annulus")
T = [0,0,0]
R = [0,0,0]
S = [1,1,1]
Sce.transform(T,R,S)
txt = Sce.get_txt()
g.write(txt)
g.close()
