import RevolveCurve as rc
import extrusion as ext
import affine as aff
import mapto
import numpy as np
import graph as gra

from copy import deepcopy

from math import pi,cos,sin

def Ellipsoid(rx,ry,t,q,s,m=10,n=10):
    curve = [[0,0]]
    a,b = [0,0]
    for i in range(m):
        val = 1.0*i/(m-1)
        ti = mapto.MapTo(0,-pi/2., 1,pi/2., val) # pi = 180 degrees only half circle
        xi =  a + rx*cos(ti)
        yi =  b + ry*sin(ti)
        pt = [xi,yi]
        curve.append(pt)

    H = rc.RevolveCurve(curve,t,q,s, n=n, bcap=True,ecap=True)
    return H

def Sphere(r,t,q,s,m=10,n=10):
    H = Ellipsoid(r,r,t,q,s,m=m,n=n)
    return H

def Cone0(x1,y1,x2,y2,t,q,s,m=10,n=10):
    curve = [[0,0]]
    for i in range(m):
        ti = 1.0*i/(m-1)
        xi = mapto.MapTo(0,x1,1,x2, ti)
        yi = mapto.MapTo(0,y1,1,y2, ti)
        pt = [xi,yi]
        curve.append(pt)
    curve.append([0,yi])
    H = rc.RevolveCurve(curve,t,q,s, n=n, bcap=True,ecap=True)
    return H

def Cone(r,h,t,q,s,m=10,n=10):
    H = Cone0(0,0,r,h,t,q,s,m=m,n=n)
    return H

def Cylinder(r,h,t,q,s,m=10,n=10):
    H = Cone0(r,0,r,h, t,q,s, m=m, n=n)
    return H

# Note: this torus has a implicit twist
def Torus0(r1,r2,m=10,n=40):
    C = [0,0,0]
    H1 = gra.Cn(m)
    H1 = gra.CreateCircleGeometry(H1,C[0],C[1],C[2],r1)
    t = 0
    dt = 2*pi/n
    path = []
    while t <= 2*pi + dt:
        x = r2*sin(t)
        y = r2*cos(t)
        z = 0
        pt = [x,y,z]
        path.append(pt)
        t = t + dt
    H = ext.Extrusion(H1,path,bcap=False,ecap=False,closed=True)
    return H

def Torus(r1,r2,t,q,s,m=10,n=40):
    H = Torus0(r1,r2,m=m,n=n)
    pts = H['pts']
    C = aff.Center(pts)
    pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts,s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    H['pts'] = pts
    return H

    
