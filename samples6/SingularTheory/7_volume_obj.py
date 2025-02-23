import numpy as np
import singular_q_chain_measures as sqm
import AT_singular_theory as atst

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

w = 2
h = 3
d = 4
print(f"Forming cube {w} x {h} x {d} of volume {w*h*d}")
omega_3q = create_cube(w,h,d)
print(f"omega_3q = \n{omega_3q}")
I = sqm.volume_3q(omega_3q)
print(f"singular q-chains: vol(cube) = {float(I)}")


