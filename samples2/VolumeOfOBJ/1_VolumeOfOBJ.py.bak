import polygon_area as pa
import QuaternionGroup as QG

import numpy as np
from math import pi,acos

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

def area(pts):
    C,A = pa.PolygonCentroid(pts)
    return A

def AddNormals(G):
    G['N'] = []
    for face in G['F']:
        polygon = map(lambda v: G['pts'][v],face)
        A,B,C = polygon[:3]
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        V1 = A-B
        V2 = C-B
        N = np.cross(V1,V2)
        N = list(N/np.linalg.norm(N))
        G['N'].append(N)
    return G

def Transform_3D_to_2D(polygon1,normal):
    # Create V1 and V2 vectors of polygon1 normal and [0,0,1] z-axis
    V1 = normal
    V2 = [0,0,1] # z-axis
    V1 = np.array(V1)
    V2 = np.array(V2)
    # create a rotation axis to rotate V1 to V2
    # and compute angle in degrees of rotation, obtain quaternion for this
    axis = np.cross(V1,V2)
    angle = acos(np.inner(V1,V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))
    degrees = angle*180/pi
    q = QG.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    # compute rotation matrix R for quaternion q
    epsilon = 1e-8
    R = q.rotation_matrix()
    # Now transform polygon1 to polygon2 so it
    # has normal [0,0,1] in z-axis using rotation R
    polygon2 = []
    pt0 = list(np.einsum('ij,j->i',R,polygon1[0]))
    z = pt0[2] # z-component of first point
    for pt in polygon1:
        pt2 = list(np.einsum('ij,j->i',R,pt))
        pt2[2] -= z # translate pt2 by [0,0,-z]
        polygon2.append(pt2)
    C = np.array([0,0,0])
    for pt in polygon2:
        C = C + np.array(pt)
    C = C/(1.0*len(polygon2))
    for i in range(len(polygon2)):
        pt = polygon2[i]
        pt2 = list(np.array(pt)-C)
        polygon2[i] = pt2        
    return polygon2

def area3d(G,i):
    face = G['F'][i]
    polygon1 = map(lambda v: G['pts'][v],face)
    normal1 = G['N'][i]
    polygon2 = Transform_3D_to_2D(polygon1,normal1)
    A = area(polygon2)
    C = np.array([0,0,0])
    N = len(polygon1)
    for pt in polygon1:
        C = C + np.array(pt)
    C = C/(1.0*N)
    C = list(C)
    return C,A

def volume(G):
    V = 0
    # First make sure volume is not signed volume
    M = 1e5 # use big number to translate graph 
    G = Translate(G,[M,M,M])
    for i in range(len(G['F'])):
        C,dS = area3d(G,i)
        n = G['N'][i]
        face = G['F'][i]
        polygon1 = map(lambda v: G['pts'][v],face)
        F = np.array(C)/3.0 
        val = -np.inner(F,n)*abs(dS)
        V = V + val
    return V

def Translate(G,t):
    for i in range(len(G['pts'])):
        pt = G['pts'][i]
        pt[0] += t[0]
        pt[1] += t[1]
        pt[2] += t[2]
        G['pts'][i] = pt
    return G

def OBJ2Graph(OBJ):
    lines = OBJ.split("\n")
    G = {}
    G['pts'] = []
    for line in lines:
        line = line.strip()
        tokens = line.split(' ')
        if tokens[0] == 'v':
            c,x,y,z = tokens
            x = float(x)
            y = float(y)
            z = float(z)
            G['pts'].append([x,y,z])
    G['V'] = range(len(G['pts']))
    G['F'] = []
    G['E'] = []
    for line in lines:
        tokens = line.strip().split(' ')
        if tokens[0] == 'f':
            L = tokens[1:]
            face = []
            for tok in L:
               v = tok.split('/')[0]
               v = int(v)-1 # indices start at 0 not 1
               face.append(v)
            G['F'].append(face)
            N = len(face)
            for i in range(N):
                u = face[i]
                v = face[(i+1)%N]
                e = [u,v]
                if e not in G['E']:
                    G['E'].append(e)
    G = AddNormals(G)
    return G


OBJ1 = """
# cube.obj
#
 
o cube
mtllib cube.mtl
 
v -0.500000 -0.500000 0.500000
v 0.500000 -0.500000 0.500000
v -0.500000 0.500000 0.500000
v 0.500000 0.500000 0.500000
v -0.500000 0.500000 -0.500000
v 0.500000 0.500000 -0.500000
v -0.500000 -0.500000 -0.500000
v 0.500000 -0.500000 -0.500000
 
vt 0.000000 0.000000
vt 1.000000 0.000000
vt 0.000000 1.000000
vt 1.000000 1.000000
 
vn 0.000000 0.000000 1.000000
vn 0.000000 1.000000 0.000000
vn 0.000000 0.000000 -1.000000
vn 0.000000 -1.000000 0.000000
vn 1.000000 0.000000 0.000000
vn -1.000000 0.000000 0.000000
 
g cube
usemtl cube
s 1
f 1/1/1 2/2/1 3/3/1
f 3/3/1 2/2/1 4/4/1
s 2
f 3/1/2 4/2/2 5/3/2
f 5/3/2 4/2/2 6/4/2
s 3
f 5/4/3 6/3/3 7/2/3
f 7/2/3 6/3/3 8/1/3
s 4
f 7/1/4 8/2/4 1/3/4
f 1/3/4 8/2/4 2/4/4
s 5
f 2/1/5 8/2/5 4/3/5
f 4/3/5 8/2/5 6/4/5
s 6
f 7/1/6 1/2/6 5/3/6
f 5/3/6 1/2/6 3/4/6
"""

G1 = OBJ2Graph(OBJ1)
print "volume(G1)=",volume(G1)

fn = BIGDATA+"Complex1.obj"
#fn = BIGDATA+"WaterBottle-0.obj"
f = open(fn,'r') # open for reading 'r'
OBJ2 = f.read()
f.close() # close

G3 = OBJ2Graph(OBJ2)
print "volume(G3)=",volume(G3)


