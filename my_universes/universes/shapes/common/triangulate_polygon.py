import scipy.spatial as ss
from copy import deepcopy

import numpy as np

# Q is assumed to be a list [...(pts,sgn)...]
# where pts is the points of the polygon and
# sgn is either 1 (exterior) or -1 (interior)
# but it is assumed that only polygons 1 can
# contain -1 polygons. And polygon -1 cannot
# contain any polygons.

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

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
    return F,pts_Q,tri

def triangulate_polygons(Q,t=0.0001):
    tt = t
    #print(f"|Q| = {len(Q)}")
    # filter interior faces
    F,pts_Q,tri = triangulate_polygons_helper(Q)
    I = []
    G = []
    for i in range(len(Q)):
        tup = Q[i]
        pts_i,sgn_i = tup
        if sgn_i == -1:
            pts_i2 = np.array(pts_i)
            C_i = np.mean(pts_i2,axis=0)
            pts_i3 = []
            for j in range(len(pts_i)):
                A = pts_i[j]
                B = C_i
                pt = lerp(A,B,tt)
                pts_i3.append(pt)
            pts_i3a = np.array(pts_i3)
                
            Ii = []
            Ii = tri.find_simplex(pts_i3a)
            Ii = list(map(int,list(Ii)))
            Ii = list(set(Ii))
            Ii2 = [idx for idx in Ii if idx != -1]
            I = I + Ii2

    F3 = [F[i] for i in range(len(F)) \
                  if i not in I]
    return F3,pts_Q

