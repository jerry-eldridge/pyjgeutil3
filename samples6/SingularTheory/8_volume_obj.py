import numpy as np
import singular_q_chain_measures as sqm
import AT_singular_theory as atst

from math import pi
from copy import deepcopy

import sys
root = f"C:/Users/jerry/Desktop/_Art/my_universes/"
sys.path.insert(0,root)
import universes
import universes.shapes.AT_BasicShapes as atbs
import universes.volume_of_OBJ as voo

def create_cube(w,h,d):
    pts = [[-w/2,-h/2,-d/2],[w/2,-h/2,-d/2],
           [w/2,h/2,-d/2],[-w/2,h/2,-d/2],
           [-w/2,-h/2,d/2],[w/2,-h/2,d/2],
           [w/2,h/2,d/2],[-w/2,h/2,d/2]]
    F = [[0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5],
         [7, 6, 2], [7, 2, 3], [4, 7, 3], [4, 3, 0],
         [7, 4, 5], [7, 5, 6], [0, 3, 2], [0, 2, 1]]
    O = np.mean(pts,axis=0)
    O = list(map(float, O.flatten()))
    # sum of tetrahedrons based on adding a point O
    # to list of points of each face in F.
    for i in range(len(F)):
        tri = F[i]
        # create a tetrahedron by adding
        # the centroid O to pts to each triangle
        pts_tet = [O]+[pts[i] for i in tri]
        q = 3
        val = atst.S_q(q, atst.func(pts_tet))*atst.R(1)
        if i == 0:
            omega_3q = val
        else:
            omega_3q = omega_3q + val
    return omega_3q

def create_torus(r1,r2,ns=30,nt=30,path=None):
    G = atbs.create_torus(r1,r2,ns,nt,path)
    print(f"vol(G) = {voo.volume(G)}")
    pts = deepcopy(G['pts'])
    F = deepcopy(G['F'])
    # sum of faces
    for i in range(len(F)):
        tri = F[i]
        pts_tet = [pts[i] for i in tri]
        q = 2
        val = atst.S_q(q, atst.func(pts_tet))*atst.R(-1)
        if i == 0:
            omega_2q = val
        else:
            omega_2q = omega_2q + val
    return omega_2q

w = 2
h = 3
d = 4
V1 = w * h * d
print(f"Formula: w * h * d = {V1}")
omega_3q = create_cube(w,h,d)
V2 = sqm.volume_3q(omega_3q)
print(f"singular q-chains: vol(omega_3q) = {float(V2)}")

r1 = 10
r2 = 20
#################################################
# [1] formula R and V1 by Microsoft Copilot, a
# large language model.
R = (r1 + r2)/2.0
V1 = 2*pi**2*(r2**2 - r1**2)*R
#################################################

print(f"r1 = {r1}")
print(f"r2 = {r2}")
print(f"Formula: V = pi * r**2 * 2 * pi * R = {V1}")
omega_2q = create_torus(r1,r2,ns=8,nt=8,path=None)
V2 = sqm.volume_2q(omega_2q)
print(f"singular q-chains: vol(omega_2q) = {float(V2)}")


