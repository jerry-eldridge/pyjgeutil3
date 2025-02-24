import AT_singular_theory as atst
import numpy as np
from copy import deepcopy

def mesh_equate_tet_u_v(tet,u,v, pi):
    tet2 = [pi[tet[i]] for i in range(len(tet))]
    if len(set(tet2)) == len(set(tet)):
        return tet2
    else:
        return None
    
def mesh_map_u_v(I, u, v):
    I2 = []
    # shift all non-{u,v} to left
    # and shift {u,v} as {a} to far right
    a = min(u,v)
    pi = {}
    for i in I:
        if i in [u,v]:
            pi[i] = a
        else:
            pi[i] = i
    return pi

def mesh_contract_edge(M,A,B):
    pts,tets = M
    if A in pts:
        u = pts.index(A)
    else:
        return [pts,tets]
    if B in pts:
        v = pts.index(B)
    else:
        return [pts,tets]
    # shift u and v to the last two values
    I = range(len(pts))
    pi = mesh_map_u_v(I, u, v)
    pts2 = [pts[pi[i]] for i in I]
    pts[pi[u]] = deepcopy(A)
    pts[pi[v]] = deepcopy(A)
    # identify index u and index v
    # with equivalence u ~ v.
    tets2 = []
    for i in range(len(tets)):
        tet_i = tets[i]
        tet_i_2 = mesh_equate_tet_u_v(tet_i,u,v, pi)
        if tet_i_2 is None:
            continue
        else:
            tets2.append(tet_i_2)
    return [pts2,tets2]

def lerp(A,B,t):
    C = (1-t)*np.array(A) + t*np.array(B)
    C = list(map(float,list(C)))
    return C

def mesh_clean(M):
    pts,tets = M

    S = set([])
    for tet in tets:
        S = S | set(tet)
    print(f"S = {S}")
    I = list(S)
    I.sort()
    print(f"I = {I}")
    pts2 = []
    for i in range(len(pts)):
        pt = pts[i]
        if i in I:
            pts2.append(pt)
    tets2 = []
    for i in range(len(tets)):
        tet = tets[i]
        tet2 = []
        for j in range(len(tet)):
            u = tet[j]
            pt = pts[u]
            v = pts2.index(pt)
            tet2.append(v)
        tets2.append(tet2)
    
    M2 = [pts2,tets2]
    return M2

def mesh_merge(M,pts0, C = None):
    pts,tets = M
    # copy M to M2
    pts2 = deepcopy(pts)
    tets2 = deepcopy(tets)

    # find center of input pts0
    M2 = [pts2,tets2]
    if C is None:
        C = np.mean(np.array(pts0),axis=0)
        C = list(map(float, list(C)))
    A = pts0[0]
    # merge all points in pts0 to center
    for i in range(1,len(pts0)):
        B = pts0[i]
        M2 = mesh_contract_edge(M2,A,B)
    u = M2[0].index(A)
    M2[0][u] = C
    M2 = mesh_clean(M2)
    return M2

def Indices(sigma):
    L = []
    for i in range(len(sigma.S)):
        f = sigma.S[i]
        v = sigma.V[i]
        P = f.P()
        Q = [pts.index(p)+1 for p in P]
        L.append((Q,v.x))
    return L

def mesh_display(M):
    pts,tets = M
    print(f"="*30)
    for i in range(len(pts)):
        A = pts[i]
        s = f"v {A[0]} {A[1]} {A[2]}"
        print(s)
    for i in range(len(tets)):
        tet = tets[i]
        s = f"f {tet[0]} {tet[1]} {tet[2]} {tet[3]}"
        print(s)
    print(f"="*30)
    return

# build cube volumetric mesh of tets
w = 1
h = 1
d = 1
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
M = (pts,tets)

mesh_display(M)

# define equivalence relation class by
# specifying list of points to be
# equated. R = [3,4] means 3 ~ 4.
R = [3,4] # equivalence class
# define points that R represents in
# M
pts0 = [M[0][i] for i in R]
# Merge points pts0 to point C
M2 = mesh_merge(M,pts0, C = pts0[0])
mesh_display(M2)
# use M2 as the current mesh
pts,tets = M2
    
for i in range(len(tets)):
    tet = tets[i]
    pts_tet = [pts[i] for i in tet]
    val = atst.S_q(3,atst.func(pts_tet))*atst.R(1)
    if i == 0:
        v = val
    else:
        v = v + val
        
bdy = atst.partial_q # boundary of sigma in S_q

def write_normals(f,pts,tet):
    for tup in Indices(bdy(tet)):
        I,sgn = tup
        pts_I = [pts[i-1] for i in I]
        if sgn == -1:
            pts_I.reverse()
        pts_I = np.array(pts_I)
        v1 = pts_I[1] - pts_I[0]
        v2 = pts_I[2] - pts_I[0]
        N = np.cross(v1,v2)
        N = N / np.linalg.norm(N)
        line = f'vn {N[0]} {N[1]} {N[2]}\n'
        f.write(line)
    return f
def write_vertices(f,pts):
    n = len(pts)
    i = 1
    for j in range(n):
        s = f'v {pts[j][0]} {pts[j][1]} {pts[j][2]}\n'
        f.write(s)
    return f
def write_faces(f,tet):
    I = Indices(bdy(tet))
    for tup in I:
        face,orientation = tup
        if orientation == -1:
            face.reverse()
        s = 'f '+' '.join(map(str,face))+'\n'
        f.write(s)
    return f
f = open("cube_volume_mesh2.obj",'w')
f.write("o shape2\n")
f = write_vertices(f,pts)

for i in range(len(tets)):
    tet = tets[i]
    pts_tet = [pts[j] for j in tet]
    val = atst.S_q(3,atst.func(pts_tet))*atst.R(1)
    if i == 0:
        sigma = val
    else:
        sigma = sigma + val

f = write_normals(f,pts,sigma)
f = write_faces(f,sigma)
f.close()
