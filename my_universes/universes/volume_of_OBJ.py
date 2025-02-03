from .shapes.common import polygon_area as pa
from .shapes.common import QuaternionGroup as QG

import numpy as np
from math import pi,acos
from copy import deepcopy

import time

def array(A):
     return np.array(A,dtype=np.float64)

def area(pts):
     C,A = pa.PolygonCentroid(pts)
     return A

def get_polygon(G,face):
     polygon1 = []
     for v in face:
        if type(v) == type([]):
           if v[0] == '':
              continue
           n = int(v[0])-1
        elif type(v) == type(1):
           n = v
        pt = G['pts'][n]
        polygon1.append(pt)
     return polygon1

def AddNormals(G):
     G['N'] = []
     for face in G['F']:
         polygon = get_polygon(G,face)
         A,B,C = polygon[:3]
         A = array(A)
         B = array(B)
         C = array(C)
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
     V1 = array(V1)
     V2 = array(V2)
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
     C = array([0,0,0])
     for pt in polygon2:
         C = C + array(pt)
     C = C/(1.0*len(polygon2))
     for i in range(len(polygon2)):
         pt = polygon2[i]
         pt2 = list(array(pt)-C)
         polygon2[i] = pt2
     return polygon2

def area3d(G,i):
     face = G['F'][i]
     
     polygon1 = get_polygon(G,face)
     A,B,C = polygon1[:3]
     A = array(A)
     B = array(B)
     C = array(C)
     V1 = A-B
     V2 = C-B
     N = np.cross(V1,V2)
     N_mag = np.linalg.norm(N)
     epsilon = 1e-8
     if N_mag < epsilon:
          normal1 = [1,0,0]
     else:
          normal1 = list(N/N_mag)

     polygon2 = Transform_3D_to_2D(polygon1,normal1)
     A = area(polygon2)
     C = array([0,0,0])
     N = len(polygon1)
     for pt in polygon1:
         C = C + array(pt)
     C /= 1.0*N
     C = list(C)
     return C,A,normal1

def volume(G):
     V = 0
     # First make sure volume is not signed volume
     M = 1e3 # use big number to translate graph
     G = Translate(G,[M,M,M])

     for i in range(len(G['F'])):
         C,dS,n = area3d(G,i)
         face = G['F'][i]
         polygon1 = get_polygon(G,face)
         F = array(C)/3.0
         val = -np.inner(F,n)*abs(dS)
         V = V + val
     return V

def Translate(G,t):
     for i in range(len(G['pts'])):
         pt = G['pts'][i]
         pt[0] = pt[0] + t[0]
         pt[1] = pt[1] + t[1]
         pt[2] = pt[2] + t[2]
         G['pts'][i] = pt
     return G

def OBJ2Graph(OBJ,flag_edges=True,verbose=False):
     if verbose:
          print(f"OBJ2Graph:")
     t0 = time.time()
     lines = OBJ.split("\n")
     t1 = time.time()
     if verbose:
          print(f"  OBJ.split: dt = {t1 - t0} seconds")
     G = {}
     G['pts'] = []
     G['N'] = []
     G['T'] = []
     t0 = time.time()
     for line in lines:
         line = line.strip()
         tokens = line.split(' ')
         if tokens[0] == 'v':
             c,x,y,z = tokens
             x = float(x)
             y = float(y)
             z = float(z)
             G['pts'].append([x,y,z])
         elif tokens[0] == 'vn':
             c,nx,ny,nz = tokens
             nx = float(nx)
             ny = float(ny)
             nz = float(nz)
             G['N'].append([nx,ny,nz])
         elif tokens[0] == 'vt':
             c,uu,vv = tokens
             uu = float(uu)
             vv = float(vv)
             G['T'].append([uu,vv])
     t1 = time.time()
     if verbose:
          print(f"  for1: dt = {t1 - t0} seconds")
     G['V'] = range(len(G['pts']))
     G['F'] = []
     G['E'] = []
     t0 = time.time()
     ES = set()
     for line in lines:
         tokens = line.split(' ')
         if tokens[0] == 'f':
             L = tokens[1:]
             face = []
             for tok in L:
                v = tok.split('/')
                face.append(v)
             
             G['F'].append(face)
             N = len(face)
             if flag_edges:
                  for i in range(N):
                      u = face[i]
                      v = face[(i+1)%N]
                      e = (u,v)
                      ES.add(str(e))
                      if str(e) not in ES:
                           G['E'].append(e)
     t1 = time.time()
     if verbose:
          print(f"  for2: dt = {t1 - t0} seconds")
     t0 = time.time()
     if len(G['N']) == 0:
          G = AddNormals(G)
     t1 = time.time()
     if verbose:
          print(f"  Addnormals: dt = {t1 - t0} seconds")

     F2 = []
     for f in G['F']:
         f2 = []
         for tup in f:
             if tup != ['']:
                 f2.append(tup)
         F2.append(f2)
     G['F'] = deepcopy(F2)
          
     return G
    
