#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
import extrusion as ext
import affine as aff
import mapto
import numpy as np
import graph as gra

from copy import deepcopy

from math import pi,cos,sin

# Note: this helix has a implicit twist
def Helix0(r,a,b,m=10,n=40, N = 1):
    C = [0,0,0]
    H1 = gra.Cn(m)
    H1 = gra.CreateCircleGeometry(H1,C[0],C[1],C[2],r)
    t = 0
    dt = 2*pi/n
    path = []
    while t <= 2*pi*N + dt:
        # https://en.wikipedia.org/wiki/Helix
        x = a*sin(t)
        y = a*cos(t)
        z = b*t
        pt = [x,y,z]
        path.append(pt)
        t = t + dt
    H = ext.Extrusion(H1,path,bcap=True,ecap=True,closed=True)
    return H

def Helix(r,a,b,t,q,s,m=10,n=40, N = 1):
    H = Helix0(r,a,b,m=m,n=n, N=N)
    pts = H['pts']
    C = aff.Center(pts)
    pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts,s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    H['pts'] = pts
    return H
