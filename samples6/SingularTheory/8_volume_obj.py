import numpy as np
import singular_q_chain_measures as sqm
import AT_singular_theory as atst

from math import pi,sin,cos,sqrt
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

ns = 9
print(f"ns = {ns}")
nt = 7
print(f"nt = {nt}")
r1 = 10
r2 = 20
print(f"r1 = {r1}")
print(f"r2 = {r2}")
C = 0
for i in range(nt):
    t = i/(nt-1)
    x = r2*cos(2*pi*t)
    y = r2*sin(2*pi*t)
    if i == 0:
        x_lst = x
        y_lst = y
    val = sqrt((x-x_lst)**2 + (y-y_lst)**2)
    x_lst = x
    y_lst = y
    C = C + val
print(f"C = {C}")

# [1] https://en.wikipedia.org/wiki/Regular_polygon
# for area of convex regular n-sided polygon
V3 = (0.5*ns*r1**2*sin(2*pi/ns)) * C

print(f"Formula: V3 = (0.5*ns*r1**2*sin(2*pi/ns)) * C = {V3}")
omega_2q = create_torus(r1,r2,ns=9,nt=4,path=None)
V4 = sqm.volume_2q(omega_2q)
print(f"singular q-chains: V4 = vol(omega_2q) = {float(V4)}")


