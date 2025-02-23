import sys
#sys.path.insert(0,"C:/Users/jerry/Desktop/AlgTopo/")

## import the file 'AT_singular_theory.py'
import AT_singular_theory as atst

import numpy as np

def line_integral(omega_1q,f1):
    s = 0
    for i in range(len(omega_1q.S)):
        sigma = omega_1q.S[i]
        if sigma.q != 1:
            continue
        facet1 = sigma**1
        facet2 = sigma**2
        orientation = omega_1q.V[i].x
        A = facet1.P()[0]
        B = facet2.P()[0]
        ds = orientation*d(A,B)
        s = s + f1(A)*ds
    return s

def vector_area_triangle(P):
    epsilon = 1e-8
    Q = np.array(P)
    v1 = Q[1]-Q[0]
    v2 = Q[2]-Q[0]
    v = np.cross(v1,v2)
    v_mag = np.linalg.norm(v)
    if abs(v_mag) > epsilon:
        normal = v/v_mag
    else:
        normal = v
    dA = 0.5*v_mag*normal
    return dA,normal

def surface_integral(omega_2q,f2):
    s = 0
    for i in range(len(omega_2q.S)):
        sigma = omega_2q.S[i]
        if sigma.q != 2:
            continue
        P = sigma.P()
        orientation = omega_2q.V[i].x
        dA = vector_area_triangle(P)[0]
        pt = P[0]
        s = s + orientation*np.inner(f2(pt),dA)
    return s

mu1 = lambda f1: lambda omega: \
               line_integral(omega,f)

import numpy as np
d = lambda A,B: np.linalg.norm(np.array(B)-np.array(A))

C0 = [[0,0,0],[1,0,0],[1,1,0],[0,1,0]] # pts,, square
E0 = [[0,1],[1,2],[2,3],[3,0]] # closed curve
C = C0
E = E0

# define q-form omega
for i in range(len(E0)):
    edge = E[i]
    pts = [C[i] for i in edge] # edge
    val = atst.S_q(1, atst.func(pts))*atst.R(1)
    if i == 0:
        omega_1q = val
    else:
        omega_1q = omega_1q + val

print(f"omega_1q = \n{omega_1q}")
print()
f0 = lambda A: 1
I0 = line_integral(omega_1q,f0)
print(f"I0 = line_integral(omega_1q,f0) = {I0}")
print(f"="*30)

# omega_2q version 1
#                   *3
#                /;/
#            /;;; /
#       *2 ;;;;;/
#       /|;;;;;/
#     /..|;;;;/
#   /....|;;/
# *0-----*1
#
#    z
#    |
#   / \
# x    y
C1 = [[0,0,0],[1,0,0],[1,1,0],[1,1,1]] # pts
F1 = [[0,1,2],[1,2,3]] # faces (indices to pts)
# area should be 0.5*1*1 + 0.5*1*1 = 1.0

# omega_2q version 2
# *3-----*2
# |...../|
# |.../oo|
# |./oooo|
# *0-----*1
#
#
#    z
#    |
#   / \
# x    y
C2 = [[0,0,0],[10,0,0],[10,10,0],[0,10,0]] # pts
F2 = [[0,1,2],[0,2,3]] # faces (indices to pts)
# area should be 0.5*10*10 + 0.5*10*10 = 100.0

# choose version 2
C = C2
F = F2

# define q-form omega
for i in range(len(F)):
    face = F[i]
    pts = [C[i] for i in face] # face
    val = atst.S_q(2, atst.func(pts))*atst.R(1)
    if i == 0:
        omega_2q = val
    else:
        omega_2q = omega_2q + val

print(f"omega_2q = \n{omega_2q}")
f2 = lambda A: np.array([1,1,1])
I1 = surface_integral(omega_2q,f2)
print()
print(f"I1 = surface_integral(omega_2q,f2) = {I1}")
print(f"="*30)

def Indices(sigma):
    L = []
    for i in range(len(sigma.S)):
        f = sigma.S[i]
        v = sigma.V[i]
        P = f.P()
        Q = [pts.index(p)+1 for p in P]
        L.append((Q,v.x))
    return L

# build cube volumetric mesh of tets
w = 2
h = 3
d = 4
pts1 = [[-w/2,-h/2,-d/2],[w/2,-h/2,-d/2],
           [w/2,h/2,-d/2],[-w/2,h/2,-d/2],
           [-w/2,-h/2,d/2],[w/2,-h/2,d/2],
           [w/2,h/2,d/2],[-w/2,h/2,d/2]]
pts = pts1
# tetrahedrons to a cube volumetric mesh
tets = [[0, 1, 3, 5],
        [0, 3, 4, 5],
        [1, 2, 3, 6],
        [1, 3, 5, 6],
        [3, 4, 5, 7],
        [3, 5, 6, 7],
        ]

for i in range(len(tets)):
    tet = tets[i]
    pts_tet = [pts[i] for i in tet]
    val = atst.S_q(3,atst.func(pts_tet))*atst.R(1)
    if i == 0:
        omega_3q = val
    else:
        omega_3q = omega_3q + val

def volume(omega_3q):
    s = 0
    for i in range(len(omega_3q.S)):
        # omega_3d contains tetrahedrons so
        # iterate through tetrahedrons sigma
        sigma = omega_3q.S[i]
        if sigma.q != 3:
            continue
        # get boundary to each tetrahedron bdysigma
        bdysigma = atst.bdy(sigma)
        # bdysigma contains faces tau
        for j in range(len(bdysigma.S)):
            tau = bdysigma.S[j]
            if tau.q != 2:
                continue
            P = sigma.P()
            orientation = bdysigma.V[j].x
            dA,n = vector_area_triangle(P)
            C = np.mean(P,axis=0)
            F = C/3.0
            val = -np.inner(F,dA)*orientation
            s = s + abs(val)
    val = np.linalg.norm(s)
    return s

print(f"omega_3q = \n{omega_3q}")
print()
I3 = volume(omega_3q)
print(f"I3 = volume(omega_3q) = {I3}")
print(f"Formula for Cube, Vol = w*h*d = {w*h*d}")
print(f"="*30)
