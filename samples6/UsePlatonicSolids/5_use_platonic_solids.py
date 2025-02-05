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
import universes.shapes.platonic_solids as plas
import universes.canvas2d.graphics_cv as racg

import numpy as np
from functools import reduce
from copy import deepcopy
import time

from math import sqrt

# fire (tetrahedron)
flag_tetrahedron = True
if flag_tetrahedron:
    BIGDATA = r"./"
    fn_save = BIGDATA+"tetrahedron1.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = plas.create_tetrahedron()
    Sce.add(G,"tetrahedron1",
        "tetrahedron1.mtl","tetrahedron1")
    Sce.select("tetrahedron1")
    C = aff.Center(G['pts'])
    T = list(map(float,list(-np.array(C))))
    R = [270,0,0]
    S = [1,1,1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

# earth (cube)
flag_cube = True
if flag_cube:
    BIGDATA = r"./"
    fn_save = BIGDATA+"cube1.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = plas.create_cube()
    Sce.add(G,"cube1",
        "cube1.mtl","cube1")
    Sce.select("cube1")
    C = aff.Center(G['pts'])
    T = list(map(float,list(-np.array(C))))
    R = [270,0,0]
    S = [1,1,1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

# air (octahedron)
flag_octahedron = True
if flag_octahedron:
    BIGDATA = r"./"
    fn_save = BIGDATA+"octahedron1.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = plas.create_octahedron()
    Sce.add(G,"octahedron1",
        "octahedron1.mtl","octahedron1")
    Sce.select("octahedron1")
    C = aff.Center(G['pts'])
    T = list(map(float,list(-np.array(C))))
    R = [270,0,0]
    S = [1,1,1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

# water (icosahedron)
flag_icosahedron = True
if flag_icosahedron:
    BIGDATA = r"./"
    fn_save = BIGDATA+"icosahedron1.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = plas.create_icosahedron()
    Sce.add(G,"icosahedron1",
        "icosahedron1.mtl","icosahedron1")
    Sce.select("icosahedron1")
    C = aff.Center(G['pts'])
    T = list(map(float,list(-np.array(C))))
    R = [0,0,0]
    S = [1,1,1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

# ether (dodecahedron)
flag_dodecahedron = True
if flag_dodecahedron:
    BIGDATA = r"./"
    fn_save = BIGDATA+"dodecahedron1.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = plas.create_dodecahedron()
    Sce.add(G,"dodecahedron1",
        "dodecahedron1.mtl","dodecahedron1")
    Sce.select("dodecahedron1")
    C = aff.Center(G['pts'])
    T = list(map(float,list(-np.array(C))))
    R = [0,0,0]
    S = [1,1,1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()
