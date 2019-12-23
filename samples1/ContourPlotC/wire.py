#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
import extrusion as ext
import affine as aff
import mapto
import numpy as np
import graph as gra

from copy import deepcopy

from math import pi,cos,sin,factorial

def B(t,p):
    C = lambda n,i: factorial(n)/(factorial(n-i)*factorial(i))
    n = len(p) - 1
    assert(len(p) >= 3)
    m = len(p[0])
    pt = [0,0,0]
    for j in range(m):
        s = 0
        for i in range(n+1):
            val = C(n,i)*(1-t)**(n-i)*t**i*p[i][j]
            s = s + val
        pt[j] = s
    return pt

# Note: this wire has a implicit twist
# where p is a polygonal path
def Wire0(r,ppath,m=10,n=40):
    assert(len(ppath)>=2)
    C = [0,0,0]
    H1 = gra.Cn(m)
    H1 = gra.CreateCircleGeometry(H1,C[0],C[1],C[2],r)
    t = 0
    dt = 1./n
    path = []
    while t <= 1:
        pt = B(t,ppath)
        path.append(pt)
        t = t + dt
    H = ext.Extrusion(H1,path,bcap=True,ecap=True,closed=True)
    return H

def Wire(r,ppath,t,q,s,m=10,n=40):
    H = Wire0(r,ppath,m=m,n=n)
    pts = H['pts']
    C = aff.Center(pts)
    pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts,s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    H['pts'] = pts
    return H
