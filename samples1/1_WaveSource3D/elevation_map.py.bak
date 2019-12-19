#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
import affine as aff
import mapto
import numpy as np
import graph as gra

import cv2

from copy import deepcopy

from math import pi,cos,sin,acos,fmod

from copy import deepcopy

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

def clamp(x,lo,hi):
     return min(hi,max(lo,x))

# Note: this wire has a implicit twist
# where p is a polygonal path
def ElevationMap0(im,w,h,d,m=10):
    n = m
    H1 = gra.Gnm(m,n)
    pts = []
    F = []
    N = []

    sh = im.shape
    hh = sh[1]
    ww = sh[0]
    sz = max(hh,ww)
    sh = (sz,sz)
    im = cv2.resize(im,sh)
    hh,ww = im.shape
    I = range(0,ww,ww/m)
    J = range(0,hh,hh/n)
    for j in J:
        y = mapto.MapTo(0,-h/2.,n-1,h/2.,j)
        for i in I:
            x = mapto.MapTo(0,-w/2.,m-1,w/2.,i)
            z = im[j,i]
            pt = [x,y,z*d]
            pts.append(pt)
    H1['pts'] = pts
    idx = lambda u,v: v + n*u
    for tup in H1['object']:
        u,v = tup
        u1 = u
        u2 = clamp(u1 + 1,0,m-1)
        v1 = v
        v2 = clamp(v1 + 1,0,n-1)
        a1 = idx(u1,v1)
        a2 = idx(u2,v1)
        a3 = idx(u2,v2)
        a4 = idx(u1,v2)
        f = [a1,a2,a3,a4] # rectangle
        f1 = [a1,a2,a3] # triangle
        f2 = [a1,a3,a4] # triangle
        #print f
        F.append(f1)
        F.append(f2)
        A,B,C = map(lambda v: H1['pts'][v], f1)
        N1 = FaceNormalABC(A,B,C)
        N.append(N1)
        A,B,C = map(lambda v: H1['pts'][v], f2)
        N2 = FaceNormalABC(A,B,C)
        N.append(N2)
    H1['N'] = N
    H1['F'] = F
    return H1

def ElevationMap(im,w,h,d,t,q,s,m=10):
    H = ElevationMap0(im,w,h,d,m=m)
    pts = H['pts']
    C = aff.Center(pts)
    pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts,s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    H['pts'] = pts
    return H
