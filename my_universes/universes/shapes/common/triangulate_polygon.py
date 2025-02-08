import scipy.spatial as ss
from copy import deepcopy

import numpy as np

# Q is assumed to be a list [...(pts,sgn)...]
# where pts is the points of the polygon and
# sgn is either 1 (exterior) or -1 (interior)
# but it is assumed that only polygons 1 can
# contain -1 polygons. And polygon -1 cannot
# contain any polygons.

lerp = lambda A,B,t: list(map(float,\
            list((1-t)*np.array(A)-t*np.array(B))))

def triangulate_polygons_helper(Q):
    pts_Q = []
    for i in range(len(Q)):
        tup = Q[i]
        pts_i,sgn_i = tup
        pts_Q = pts_Q + pts_i
    pts = np.array(pts_Q)
    tri = ss.Delaunay(pts)
    simplices = tri.simplices.copy()
    V = list(range(len(simplices)))
    F = []
    for s in range(len(simplices)):
        u,v,w = simplices[s]
        u,v,w = list(map(int,[u,v,w]))
        f = [u,v,w]
        F.append(f)
    return tri,F,pts_Q

def triangulate_polygons(Q,t=0.0001):
    tri,F,pts = triangulate_polygons_helper(Q)
    # filter interior faces
    I = []
    for i in range(len(Q)):
        tup = Q[i]
        pts_i,sgn_i = tup
        if sgn_i == -1:
            pts_i = np.array(pts_i)
            C = np.mean(pts_i,axis=0)
            pts_i_2 = []
            for j in range(len(pts_i)):
                pt = lerp(pts_i[j],C,t)
                pts_i_2.append(pt)
            pts_i_2 = np.array(pts_i_2)
            tri_i = tri.find_simplex(pts_i_2)
            F_i = [idx for idx in tri_i if idx != -1]
            I = F_i
    F3 = [F[i] for i in range(len(F)) if i not in I]
    return F3,pts

