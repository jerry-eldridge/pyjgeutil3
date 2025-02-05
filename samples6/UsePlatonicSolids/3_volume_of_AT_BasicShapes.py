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

Sce1 = so.Scene()
r = 30
G1 = atbs.create_sphere(r,ns=30,nt=30,path=None)
Sce1.add(G1,"sphere","sphere.mtl","sphere")
Sce1.select("sphere")
bbox1 = Sce1.bbox()
print(f"bbox1 = {bbox1}")
vol1 = voo.volume(G1)
vol1b = (4/3)*pi*r**3 # volume of sphere formula
print(f"Sphere: r = {r}, vol(G1) = {vol1} using div.")
print(f"Sphere: r = {r}, "+\
      f"vol(G1) = {vol1b} using formula.")
print(f"Accuracy: {100*vol1/vol1b}")

Sce2 = so.Scene()
rho = 30
h = 60
G2 = atbs.create_cylinder(rho,h,
            ns=30,nt=30,path=None)
Sce2.add(G2,"cylinder","cylinder.mtl","cylinder")
Sce2.select("cylinder")
bbox2 = Sce2.bbox()
print(f"bbox2 = {bbox2}")
vol2 = voo.volume(G2)
vol2b = pi*rho**2 * h
print(f"Cylinder: rho = {rho}, h = {h}, "+\
      f"vol(G2) = {vol2} using div.")
print(f"Cylinder: rho = {rho}, h = {h}, "+\
      f"vol(G2) = {vol2b} using formula.")
print(f"Accuracy: {100*vol2/vol2b}")

