import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import graphics_cv as racg

import numpy as np
from math import pi,cos,sin

#  (x*x+y*y-1)**3 - x*x*y*y*y = 0 and
# substitute x = r*cos(theta) and y = r*sin(theta)
# trigonometric simplify and note its a polynomial in
# r given a constant theta and so solve each polynomial
# for each theta. For this there should be just one
def HeartPoly(theta):
    a0 = -1
    a1 = 0
    a2 = 3
    a3 = 0
    a4 = -3
    a5 = sin(theta)**5 - sin(theta)**3
    a6 = sin(theta)**6 + -3*sin(theta)**4 + \
         3*sin(theta)**2 + cos(theta)**6
    # form polynomial p(r) with coefficients
    # p(r) = Sum ai*r**i
    p = [a6,a5,a4,a3,a2,a1,a0]
    # solve polynomial p(r) = 0
    L = list(np.roots(p))
    vals = []
    for r in L:
        if r.imag == 0 and r.real >= 0:
            pt = [r.real, theta]
            vals.append(pt)
    return vals

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)

N = 300
theta = 0
dtheta = 2*pi/N
red = [255,0,0]
while theta <= 2*pi+dtheta:
    vals = HeartPoly(theta)
    ri,thetai = vals[0]
    # convert polar to cartesian
    x = ri*cos(thetai)
    y = ri*sin(thetai)
    tx = w/2
    ty = h/2
    sx = 200
    sy = -200
    x = sx*x
    y = sy*y
    x = tx + x
    y = ty + y
    pt = [x,y]
    if theta == 0:
        last_pt = pt
    gr.Line(last_pt,pt,red)
    theta = theta + dtheta
    last_pt = pt
gr.Show("result",-1)
gr.Save()
gr.Close()
