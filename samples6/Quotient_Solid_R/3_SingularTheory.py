import AT_singular_theory as atst
import numpy as np

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

for i in range(len(tets)):
    tet = tets[i]
    pts_tet = [pts[i] for i in tet]
    val = atst.S_q(3,atst.func(pts_tet))*atst.R(1)
    if i == 0:
        v = val
    else:
        v = v + val

i1 = 1
tet = v.term(i1) # face 0 of v
i2 = 2
f = tet.face(i2) # face 1 of tet
i3 = 2
e = f.face(i3) # face of f
i4 = 1
pt = e.face(i4) # face of e

bdy = atst.partial_q # boundary of sigma in S_q
names = ['tet']
sigmas = [tet]
for i in range(len(sigmas)):
    print(f"="*30)
    sigma = sigmas[i]
    name = names[i]
    print(f"sigma: {name}")
    I = [pts.index(p)+1 for p in sigma.P()]
    print(f"sigma = {I}")
    print(f"bdy(sigma) = ")
    print(f"{Indices(bdy(sigma))}")
    print(f"="*30)

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
f = open("cube_volume_mesh.obj",'w')
f.write("o shape\n")
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
