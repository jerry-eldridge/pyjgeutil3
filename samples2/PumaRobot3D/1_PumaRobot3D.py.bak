import BasicShapes as bs
import extrusion as ext
import affine as aff
import RevolveCurve as rc

import Puma560b as Puma560

from copy import deepcopy
import numpy as np

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

d = lambda A,B: np.linalg.norm(np.array(A)-np.array(B))
def BodyGraph(G,Gs,Gseg, t,q,s):
    H = {}
    H['V'] = []
    H['E'] = []
    H['F'] = []
    H['N'] = []
    H['pts'] = []
    degrees = 90
    axis = [0,1,0]
    q0 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    A = Gseg['pts'][0]
    Hf = ext.CubeObj(300,5,300,A,q0,s)
    H = ext.GraphUnionS(H,Hf)
    for e in Gseg['E']:
        u,v = e
        A,B = map(lambda w: Gseg['pts'][w],e)
        v1 = np.array(B)-np.array(A)
        v1n = np.linalg.norm(v1)
        epsilon = 1e-5
        if abs(v1n) < epsilon:
            continue
        v1 = v1/np.linalg.norm(v1)
        axis1 = [1,0,0]
        axis2 = list(v1)
        q1 = ext.AimAxis(axis1,axis2)
        q1 = q1*q0

        r = 10
        h = d(A,B)
        t0 = list(np.array(A) + h/2.*v1)
        s0 = [1,1,1]
        He = bs.Cylinder(r,h,t0,q1,s0,n=10,m=10)
        H = ext.GraphUnionS(H,He)
        Hf = bs.Sphere(40,A,q1,s0,n=10,m=10)
        H = ext.GraphUnionS(H,Hf)
    #Hf = bs.Cone(60,150,B,q1,s0,n=10,m=10)
    #H = ext.GraphUnionS(H,Hf)
    degrees = 0 # 180
    axis = [0,0,1]
    q2 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    q = q*q2
    pts = H['pts']
    C = Gseg['pts'][0]
    pts = aff.Translate(pts,-C[0],-C[1],-C[2])
    pts = aff.Rotate(pts,q)
    pts = aff.Scale(pts,s[0],s[1],s[2])
    pts = aff.Translate(pts,t[0],t[1],t[2])
    H['pts'] = pts
    return H

G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []

Puma560.P.pt = [0,0,0]
G1 = Puma560.P.Graph()

#goal = [-140.772457400456574, 406.0018009385133, 139.89926879829596]
#goal = [-300,300,300]
goal = [-600,300,600]
r = 20.
t = deepcopy(goal)
degrees = 90
axis = [0,0,1]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 3.
s = [scale,scale,scale] # the same scale as previous for caps
H1 = rc.WaterBottle(n=30)
pts = H1['pts']
C = aff.Center(pts)
pts = aff.Translate(pts, -C[0],-C[1],-C[2],align=False)
pts = aff.Rotate(pts,q,align=False)
pts = aff.Scale(pts,s[0],s[1],s[2],align=False)
pts = aff.Translate(pts, t[0],t[1],t[2],align=False)
H1['pts'] = pts
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

N = 10
degrees = 0
axis = [0,1,0]
qp = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
sp = [scale,scale,scale] # the same scale as previous for caps
for i in range(N):
    Puma560.P,flag = Puma560.Reach(Puma560.P,goal)
    print i,flag,Puma560.P.Start()
    G1 = Puma560.P.Graph()

    H2 = BodyGraph(G,Gs,G1, Puma560.P.pt,qp,sp)
    Gs = ext.Append(Gs,H2)
    G = ext.GraphUnionS(G,H2)
    if flag:
        break
# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"Puma560-WaterBottle.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"Puma560-WaterBottle.obj")

