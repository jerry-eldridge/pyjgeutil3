#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")

########################## Begin Previous routines
import graph as g
import mapto
import affine as aff
import polygon_area as pa
import a_star_digraph as asd

import numpy as np
from copy import deepcopy
from math import pi,acos,fmod
import random

def FacePts(G,i):
     f = G['F'][i]
     pts = map(lambda v: G['pts'][v],f)
     return pts
def FaceNormalABC(A,B,C):
     A = np.array(A)
     B = np.array(B)
     C = np.array(C)
     N = np.cross(A-B,C-B)
     aa = np.linalg.norm(N)
     epsilon = 1e-8
     if aa > epsilon:
          N = N/aa
     try:
          N = list(N)
     except:
          N = [0,0,1]
     return N
def FaceNormal(G,i):
     pts = FacePts(G,i)
     A,B,C = pts[:3]
     N = FaceNormalABC(A,B,C)
     return N

def Cube(ww,hh,dd,mass=1e8):
     G1 = g.Cn(4)
     G2 = g.Pn(2)
     # graph G
     G = g.GraphProduct(G1,G2)
     # points to G
     pts = [[0,0,0],[0,0,dd],[ww,0,0],[ww,0,dd],
            [ww,hh,0],[ww,hh,dd],[0,hh,0],[0,hh,dd]]
     G['pts'] = pts
     # faces to G sorted by normals x,-x,y,-y,z,-z
     F = [[0,1,7,6],[4,5,3,2],[2,3,1,0],
          [6,7,5,4],[2,0,6,4],[1,3,5,7]]
     G['F'] = F
     G['N'] = map(lambda v: FaceNormal(G,v), range(len(F)))
     return G

def clamp(x,lo,hi):
     return min(hi,max(lo,x))

def area(pts):
     C,A = pa.PolygonCentroid(pts)
     return A
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
     q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
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
     C /= 1.0*N
     C = list(C)
     return C,A
def Translate(G,t):
     for i in range(len(G['pts'])):
         pt = G['pts'][i]
         pt[0] += t[0]
         pt[1] += t[1]
         pt[2] += t[2]
         G['pts'][i] = pt
     return G
def volume(G):
     V = 0
     # First make sure volume is not signed volume
     M = 1e7 # use big number to translate graph
     G2 = deepcopy(G)
     G2 = Translate(G2,[M,M,M])
     G2 = AddNormals(G2)
     for i in range(len(G2['F'])):
         C,dS = area3d(G2,i)
         n = G2['N'][i]
         face = G2['F'][i]
         polygon1 = map(lambda v: G2['pts'][v],face)
         F = np.array(C)/3.0
         val = -np.inner(F,n)*abs(dS)
         V += val
     return V

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

def Graph2OBJ(fn,G,name_obj):
    ext = fn[-4:]
    name = fn[:-4]
    assert(ext=='.obj')
    print "Opening name for writing .obj and .mtl files, name=",name
    f = open(name+".mtl",'w')
    s = """
# Material Count: 1

newmtl Material
Ns 96.078431
Ka 0.000000 0.000000 0.000000
Kd 0.640000 0.640000 0.640000
Ks 0.500000 0.500000 0.500000
Ni 1.000000
d 1.000000
illum 2
"""
    f.write(s)
    f.close()
    
    f2 = open(name+".obj",'w')
    s = """
# %s.obj
#

o %s
mtllib %s.mtl

""" % (name, name_obj, name)
    f2.write(s)
    for pt in G['pts']:
        x,y,z = pt
        s = 'v %f %f %f\n' % (x,y,z)
        f2.write(s)
    f2.write('\n')
    for fi in G['F']:
        s = 'f '
        for vi in fi:
            s += str(vi+1)+' '
        s += '\n'
        f2.write(s)
    f2.close()

def CubeObj(w,h,d, t,q,s):
    G = Cube(w,h,d)
    pts = deepcopy(G['pts'])
    C = aff.Center(pts)
    #pts = aff.Translate(pts,-C[0],-C[1],-C[2])
    pts = aff.Rotate(pts,q,align=True)
    pts = aff.Scale(pts, s[0],s[1],s[2],align=True)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=True)
    G['pts'] = pts
    #print "C=",C
    return G   

def BookObj(author,t,q,s):
    rec = SelectRec2(author)[0]
    G = CubeObj(rec.w,rec.h,rec.d, t,q,s)
    #print "volume(G)=",volume(G)
    #print "mass(G)=",kg(rec)
    return G

shift0 = lambda A,n: map(lambda v: v+n, A)
shift1 = lambda A,n: map(lambda f: map(lambda v: v+n, f),A)

def GraphUnionS(G1,G2):
    n1 = len(G1['V'])
    G = {}
    G['V'] = G1['V']+shift0(G2['V'],n1)
    G['E'] = G1['E']+shift1(G2['E'],n1)
    G['pts'] = G1['pts'] + G2['pts']
    G['F'] = G1['F'] + shift1(G2['F'],n1)
    G['N'] = G1['N'] + G2['N']
    return G

def Append(Gs,Gi):
    n1 = sum(map(lambda Gk: len(Gk['V']), Gs))
    G2 = {}
    G2['V'] = shift0(Gi['V'],n1)
    G2['E'] = shift1(Gi['E'],n1)
    G2['pts'] = Gi['pts']
    G2['F'] = shift1(Gi['F'],n1+1)
    G2['N'] = Gi['N']
    Gs.append(G2)
    return Gs

def AxisObj(Gs,G,t0,q0):
     # create 3 foot long measuring stick
     # X'-axis
     w,h,d =  map(f, [1 , 1 , 35.4])
     s = [1,1,1]
     degrees = 0
     axis = [0,0,1]
     q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     t = [0,0,0]
     t = list(np.array(t)+np.array(t0))
     q = q0*q
     G5 = CubeObj(w,h,d, t,q,s)
     Gs = Append(Gs,G5)
     G = GraphUnionS(G,G5)

     # Z'-axis
     w,h,d =  map(f, [1 , 1 , 12.4])
     s = [1,1,1]
     degrees = -90
     axis = [1,0,0]
     q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     t = [0,0,0]
     t = list(np.array(t)+np.array(t0))
     q = q0*q
     G6 = CubeObj(w,h,d, t,q,s)
     Gs = Append(Gs,G6)
     G = GraphUnionS(G,G6)

     # Y'-axis
     w,h,d =  map(f, [1 , 1 , 12.1])
     s = [1,1,1]
     degrees = 90
     axis = [1,0,0]
     q1 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     degrees = 90
     axis = [0,0,1]
     q2 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     q = q2*q1
     t = [0,0,0]
     t = list(np.array(t)+np.array(t0))
     q = q0*q
     G7 = CubeObj(w,h,d, t,q,s)
     Gs = Append(Gs,G7)
     G = GraphUnionS(G,G7)
     return Gs,G

#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
import QuaternionGroup as HH

import numpy as np
from math import acos,pi

def AimAxis(axis1,axis2):
    # Create V1 and V2 vectors of polygon1 normal and [0,0,1] z-axis
    V1 = axis1
    V2 = axis2 # z-axis
    V1 = np.array(V1)
    V2 = np.array(V2)
    # create a rotation axis to rotate V1 to V2
    # and compute angle in degrees of rotation, obtain quaternion for this
    axis = np.cross(V1,V2)
    angle = acos(np.inner(V1,V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))
    degrees = angle*180/pi
    q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    return q

distance = lambda A,B: np.linalg.norm(np.array(A)-np.array(B))

def FloorStickPolygon(Gs,G,poly,width=1.,height=1.,closed=True):
     assert(len(poly)>=3)
     n = len(poly)
     m = n
     if not closed:
          m = m - 1
     for i in range(m):
          A = poly[i]
          B = poly[(i+1)%n]
          s = [1,1,1]
          axis1 = np.array([1,0,0])
          axis2 = np.array(B) - np.array(A)
          a = np.linalg.norm(axis2)
          epsilon = 1e-2
          if a >= epsilon:
               axis2 = 1.0*axis2/a
          else:
               axis2 = axis1
               
          if distance(axis1,axis2) < epsilon:
               q = aff.HH.Quaternion([1,0,0,0])
          elif np.linalg.norm(axis1 - axis2) >= 2-epsilon:
               s[0] = s[0]*(-1)
               q = aff.HH.Quaternion([1,0,0,0])
          else:
               q = AimAxis(axis1,axis2)
               epsilon = 1e-8
               if abs(q) < epsilon:
                    q = aff.HH.Quaternion([1,0,0,0])
          s = np.array(s) # using 16*in so scale to inches
          t = deepcopy(A)
          # X'-axis
          wk,hk,dk =  map(f, [distance(A,B),height*16., width*16.])
          Gk = CubeObj(wk,hk,dk, t,q,s)
          Gs = Append(Gs,Gk)
          G = GraphUnionS(G,Gk)
     return Gs,G
def Graphs2OBJ(fn,Gs,name_obj):
    ext = fn[-4:]
    name = fn[:-4]
    assert(ext=='.obj')
    print "Opening name for writing .obj and .mtl files, name=",name
    f = open(name+".mtl",'w')
    mtl_name_fn = "CubeMat"
    s = """
# Material Count: 1

newmtl %s
Ns 96.078431
Ka 0.000000 0.000000 0.000000
Kd 0.640000 0.640000 0.640000
Ks 0.500000 0.500000 0.500000
Ni 1.000000
d 1.000000
illum 2
""" % (mtl_name_fn)
    f.write(s)
    f.close()
    
    f2 = open(name+".obj",'w')
    s = """
# %s.obj
#
g Group1
""" % (name)
    f2.write(s)
    for i in range(len(Gs)):
         Gi = Gs[i]
         name_obj = "obj%03d" % i
         t = """
mtllib %s.mtl
o %s
""" % (name,name_obj)
         f2.write(t)
         for pt in Gi['pts']:
             x,y,z = pt
             s = 'v %f %f %f\n' % (x,y,z) # vertex .obj line
             f2.write(s)
         f2.write('\n')
         t = """
usemtl %s
""" % (mtl_name_fn)
         f2.write(t)
         for j in range(len(Gi['F'])):
             s = 'f '
             fi = Gi['F'][j]
             for k in range(len(fi)):
                 vi = fi[k]
                 s += str(vi) +" " # face .obj line
             s += '\n'
             f2.write(s)
    f2.close()
    return

################### End Previous routines
import itertools

def GraphProduct(doc1,doc2):
     """
     [Bondy,Murty] Graph Theory with Applications,
     North-Holland, 1976

     The product of simple graphs G and H is the simple
     graph G x H with vertex set V(G) x V(H) ('x' cartesian
     product) in which (u,v) is adjacent to (u',v') if and only
     if u = u' and [v,v'] in E(H), or v = v' and [u,u']
     in E(G).

     A simple graph is a graph with no loops [u,u] or
     two parallel edges [u,v] and [u,v] both in E.
     """
     Obj = []
     for el in itertools.product(doc1["V"],doc2["V"]):
         Obj.append(el)
     V = range(len(Obj))
     def LookupObj(Obj,v):
         i = 0
         for obj in Obj:
             if v == obj:
                 return i
             i += 1
         return -1
     E = []
     for i in V:
         u,v = Obj[i]
         for j in V:
             up,vp = Obj[j]
             if (u == up and ([v,vp]in doc2["E"])) or \
                (v == vp and ([u,up] in doc1["E"])):
                 E.append([i,j])
     doc = {}
     doc["V"] = V
     doc["E"] = E
     doc["object"]=Obj
     return doc

def ExtrudeGraph(doc,k):
     """
     Extrude Graph by Multiplying a single edge with the
     doc: doc2 = edge x doc, with doc2["object"] and vertices
     ordered so that (0,doc) and (1,doc) are copies of doc
     and corresponding vertices are edges from (0,doc) and (1,doc).
     """
     doc1 = {"V":range(k),"E":g.PathEdges(range(k))}
     doc2 = GraphProduct(doc1,doc)
     return doc2

# [1] https://github.com/linuxlewis/tripy
# installed by 'pip install tripy' in WinPython27 command shell.
# set 'use_tripy = True' for putting caps on ends of extrusions
use_tripy = True
if use_tripy:
     import tripy

def Triangulate(poly):
     tris = tripy.earclip(poly)
     tris2 = []
     for tri in tris:
          a,b,c = map(list,tri)
          i = poly.index(a)
          j = poly.index(b)
          k = poly.index(c)
          tri2 = [i,j,k]
          tris2.append(tri2)
     return tris2

def Extrusion0(G,path, spath, bcap=True,ecap=True,closed=False):
    m = len(G['V'])
    n = len(path)
    k = n
    assert(n>=3)
    H = ExtrudeGraph(G,k)
    C = aff.Center(G['pts'])
    C = np.array(C)
    pts = []
    F = []
    N = []
    G0 = deepcopy(G)
    G0['F'] = [G['V'][:3]]
    N0 = FaceNormal(G0,0)
    nn = n-1
    if closed:
         nn = n
    for i in range(n-1):
        A = np.array(path[i])
        B = np.array(path[(i+1)%n])
        vB = B - A
        axis1 = N0
        axis2 = list(vB)
        q_k = AimAxis(axis1,axis2)
        s_k = [spath[i],spath[i],spath[i]]
        t_k = list(A)
        pts_k = deepcopy(G['pts'])
        C_k = aff.Center(pts_k)
        pts_k = aff.Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
        pts_k = aff.Rotate(pts_k,q_k,align=False)
        pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
        pts_k = aff.Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)
        pts = pts + pts_k
    pts_k = deepcopy(G['pts'])
    C_k = aff.Center(pts_k)
    # use last q_k
    s_k = [1,1,1]
    # use last B
    t_k = list(B)
    pts_k = aff.Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
    pts_k = aff.Rotate(pts_k,q_k,align=False)
    pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
    pts_k = aff.Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)
    pts = pts + pts_k
    for i in range(n-1):
         for e in G['E']:
              u1,v1 = map(lambda u: u + m*i,e)
              u2,v2 = map(lambda u: u + m*(i+1),e)
              f = [u1,u2,v2,v1]
              f1 = [u1,u2,v1]
              f2 = [v1,u2,v2]
              for fi in [f1,f2]:
                   G_f = ExtrudeGraph(G,2)
                   f2i = map(lambda u: u - m*i, fi)
                   G_f['F'] = [deepcopy(f2i)]
                   G_f['pts'] = deepcopy(pts[i*m:(i+2)*m])
                   N_fi = FaceNormal(G_f,0)
                   F.append(fi)
                   N.append(N_fi)
    # add caps onto ends
    flag_a = bcap # begin cap
    flag_b = ecap # end cap
    if flag_a and use_tripy:
         pts_0 = pts[:m]
         C_k = aff.Center(pts_0)
         axis1 = N0
         axis2 = list(vB)
         q_k = AimAxis(axis1,axis2)
         s_k = [1,1,1] # the same scale as previous for caps
         pts_k = aff.Translate(pts_0,-C_k[0],-C_k[1],-C_k[2],align=False)
         pts_k = aff.Rotate(pts_k,q_k,align=False)
         pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
         pts_k = aff.Translate(pts_k,C_k[0],C_k[1],C_k[2],align=False)
         z_k = pts_k[0][2]
         pts_k = map(lambda pt: pt[:2], pts_k)
         tris = Triangulate(pts_k)
         for tri in tris:
              f = map(lambda u: u + 0*m, tri)
              F.append(f)
              A,B,C = map(lambda u: pts_k[u], tri)
              Nk = FaceNormalABC(A,B,C)
              N.append(Nk) # some normal N0
              a,b,c = f
              e1 = [a,b]
              e2 = [b,c]
              e3 = [c,a]
              if e1 not in H['E']:
                   H['E'].append(e1)
              if e2 not in H['E']:
                   H['E'].append(e2)
              if e3 not in H['E']:
                   H['E'].append(e3)
    if flag_b and use_tripy:
         pts_0 = pts[-m:]
         C_k = aff.Center(pts_0)
         s_k = [1,1,1] # the same scale as previous for caps
         t_k = list(B)
         pts_k = aff.Translate(pts_0,-C_k[0],-C_k[1],-C_k[2],align=False)
         pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
         pts_k = aff.Translate(pts_k,C_k[0],C_k[1],C_k[2],align=False)
         z_k = pts_k[0][2]
         pts_k = map(lambda pt: pt[:2], pts_k)
         tris = Triangulate(pts_k)
         for tri in tris:
              f = map(lambda u: u + (n-1)*m, tri)
              F.append(f)
              A,B,C = map(lambda u: pts_k[u], tri)
              Nk = FaceNormalABC(A,B,C)
              N.append(Nk) # some normal N0
              a,b,c = f
              e1 = [a,b]
              e2 = [b,c]
              e3 = [c,a]
              if e1 not in H['E']:
                   H['E'].append(e1)
              if e2 not in H['E']:
                   H['E'].append(e2)
              if e3 not in H['E']:
                   H['E'].append(e3)

    H['pts'] = pts
    H['F'] = F
    H['N'] = N
    return H

def Extrusion(G,path, bcap=True,ecap=True, closed=False):
     spath = [1]*len(path)
     H = Extrusion0(G,path, spath, bcap=bcap,ecap=ecap,closed=closed)
     return H

def Parabola():
     pts = [[0,0,0],[10,0,0],[10,10,0],[0,10,0]]
     doc1 = g.Cn(len(pts))
     doc1['pts'] = pts
     x = 0
     dx = .1
     path = []
     while x <= 10:
          pt = [10*x,x**2,0]
          path.append(pt)
          x = x + dx
     #path = [[0,0,0],[10,1,0],[20,4,0],[30,9,0]]
     H = Extrusion(doc1,path)
     return H

def TrefoilKnot():
     from math import cos,sin,pi
     
     pts = [[0,0,0],[10,0,0],[10,10,0],[0,10,0]]
     doc1 = g.Cn(len(pts))
     doc1['pts'] = pts
     
     t = 0
     dt = .04
     path = []
     while t <= 2*pi + dt:
          # https://en.wikipedia.org/wiki/Trefoil_knot
          x = sin(t) + 2*sin(2*t)
          y = cos(t) - 2*cos(2*t)
          z = -sin(3*t)
          pt = [x,y,z]
          path.append(pt)
          t = t + dt

     C = aff.Center(path)
     degrees = 30
     axis = [0,0,1]
     q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     s = [20,20,20] # the same scale as previous for caps
     t = [20,0,0]
     pts = aff.Translate(path,-C[0],-C[1],-C[2],align=False)
     pts = aff.Rotate(pts,q,align=False)
     pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
     pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
     path = pts
     #path = [[0,0,0],[10,1,0],[20,4,0],[30,9,0]]
     H = Extrusion(doc1,path)
     return H


