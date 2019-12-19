import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
#import graphics_pygame as racg
import graphics_cv as racg
import mapto
import numpy as np
from math import log,exp,sqrt

import PES as ctr

clamp = lambda x,lo,hi: min(hi,max(lo,x))

def Coulomb(r,r0,Q):
    x,y = r
    x0,y0 = r0
    x = x - x0
    y = y - y0
    R = sqrt(x**2 + y**2)
    a = 1.0
    V = 1.0*a*Q/R
    oo = 100
    V = clamp(V,-oo,oo)
    return V

def AddQ(val, pt, pt0, Q):
    val = val + Coulomb(pt,pt0,Q)
    return val

black = [0,0,0]
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
w = 600
h = 600

L_Q = [
    [[w/2,h/2],1],
    [[100,200],-2],
    [[400,200],-2],
    [[100,450],2],
    [[300,500],2],
    [[500,450],2]
    ]
    
def F(x,y):
    global L_Q
    val = 0
    for tup in L_Q:
        val = AddQ(val,[x,y],tup[0],tup[1])
    return val


# display list of line segments from contouring routine
gr = racg.Graphics(w=600,h=600)
gr.Clear()
s = 0.5*10**8
k = 4
x0,y0 = 200,100
gr.Clear()

G = lambda s: lambda x,y: F(x,y)-s
ix = 100
iy = 100
for y0 in range(1,600,iy):
    for x0 in range(1,600,ix):
        ctr.ShowLevelSet(gr,G(s), x0, y0, blue, tmax = 50)
        gr.Point([x0,y0],red)
        for tup in L_Q:
            pt,q = tup
            color0 = green
            gr.Point(pt,color0)
        ch = gr.Show("result",15)
        if ch == ord('e'):
            break
gr.Show("result",-1)
fn = "ImplicitFunction-ContourVelocity-%02d.jpg" % k
#gr.Save(fn)
gr.Close()
