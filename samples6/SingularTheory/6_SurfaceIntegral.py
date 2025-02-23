import AT_singular_theory as atst
import singular_q_chain_measures as sqm

import numpy as np

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
I0 = sqm.line_integral(omega_1q,f0)
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
I1 = sqm.surface_integral(omega_2q,f2)
print()
print(f"I1 = surface_integral(omega_2q,f2) = {I1}")
print(f"="*30)



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



print(f"omega_3q = \n{omega_3q}")
print()
I3 = sqm.volume(omega_3q)
print(f"I3 = volume(omega_3q) = {I3}")
print(f"Formula for Cube, Vol = w*h*d = {w*h*d}")
print(f"="*30)
