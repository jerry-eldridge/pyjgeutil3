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

flag_sphere = False
if flag_sphere:
    BIGDATA = r"./"
    fn_save = BIGDATA+"AT_sphere.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = atbs.create_sphere(r=30,ns=30,nt=30,path=None)
    Sce.add(G,"sphere","sphere.mtl","sphere")
    Sce.select("sphere")
    T = [0,0,0]
    R = [0,0,0]
    S = [.03,.03,.03]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

flag_cylinder = False
if flag_cylinder:
    BIGDATA = r"./"
    fn_save = BIGDATA+"AT_cylinder.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = atbs.create_cylinder(rho=30,h=60,
            ns=30,nt=30,path=None)
    Sce.add(G,"cylinder","cylinder.mtl","cylinder")
    Sce.select("cylinder")
    T = [0,0,0]
    R = [0,0,0]
    S = [.03,.03,.03]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

flag_ellipsoid = False
if flag_ellipsoid:
    BIGDATA = r"./"
    fn_save = BIGDATA+"AT_ellipsoid.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = atbs.create_ellipsoid(rx=10,ry=10,rz=15,
            ns=30,nt=30,path=None)
    Sce.add(G,"ellipsoid","ellipsoid.mtl","ellipsoid")
    Sce.select("ellipsoid")
    T = [0,0,0]
    R = [0,0,0]
    S = [.1,.1,.1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

flag_torus = True
if flag_torus:
    BIGDATA = r"./"
    fn_save = BIGDATA+"AT_torus.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = atbs.create_torus(r1=25,r2=110,
            ns=30,nt=30,path=None)
    Sce.add(G,"torus","torus.mtl","torus")
    Sce.select("torus")
    T = [0,0,0]
    R = [0,0,0]
    S = [.1,.1,.1]
    Sce.transform(T,R,S)
    txt = Sce.get_txt()
    g.write(txt)
    g.close()
