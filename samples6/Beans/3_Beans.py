import sys
sys.path.append(\
    r"C:_Art/my_universes")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as bs
import universes.volume_of_OBJ as voo
from copy import deepcopy
import universes.transform_shape as ts
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.common.vectors as vec
import universes.shapes.common.CoordSystem as cs
import universes.shapes.common.human_doll as hd
import universes.shapes.common.graph as gra
import universes.shapes.alg_topo as topo
from math import pi
import numpy as np
import time
from functools import reduce
import bean

def copy_graph(G):
    G2 = {}
    K = list(G.keys())
    for key in K:
        G2[key] = deepcopy(G[key])
    return G2

BIGDATA = r"./"
fn_save = BIGDATA+"Beans.obj"
g = open(fn_save,'w')
Sce = so.Scene()

G = bean.create_bean(ns=70,nt=20,
        r_add=0.75,freq=5,path=None)

N1 = 5 # create N1 x N2 worms
N2 = 5
for i in range(N1):
    for j in range(N2):
        G_ij = copy_graph(G)
        name = f"bean_{i}_{j}"
        Sce.add(G_ij,name,"bean.mtl","bean")
        Sce.select(name)
        T = [0.7*(i-N1/2), 0, 0.7*(j-N2/2)]
        R = [15*i,0,35*j]
        S = [.03, .03, .03]
        Sce.transform(T,R,S)

txt = Sce.get_txt()
g.write(txt)
g.close()
