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

flag_sphere = True
if flag_sphere:
    BIGDATA = r"./"
    fn_save = BIGDATA+"AT_sphere.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = atbs.create_sphere(r=30,ns=30,nt=30,path=None)
    Sce.add(G,"sphere","sphere.mtl","sphere")
    Sce.select("sphere")
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

flag_cylinder = True
if flag_cylinder:
    BIGDATA = r"./"
    fn_save = BIGDATA+"AT_cylinder.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    G = atbs.create_cylinder(rho=30,h=60,
            ns=30,nt=30,path=None)
    Sce.add(G,"cylinder","cylinder.mtl","cylinder")
    Sce.select("cylinder")
    txt = Sce.get_txt()
    g.write(txt)
    g.close()

