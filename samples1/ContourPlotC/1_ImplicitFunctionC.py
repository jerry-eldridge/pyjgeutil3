import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
#import graphics_pygame as racg
import graphics_cv as racg
import mapto
import numpy as np
from math import log,exp

import PES as ctr

def F1(x,y):
    return (x-300)**2 + (y-300)**2 - 100**2
def F2(x,y):
    return 3*x-2*y
def F3(x,y):
    return (x-200)**2/600.0 - (y-100)
# 2D implicit function F(x,y).
def sign(x):
    if x < 0:
        return -1
    else:
        return 1

def F4(x,y):
    val = F1(x,y)*F2(x,y)*F3(x,y)
    return val
def F5(x,y):
    val = (x-100)**2 + (y-200)**2
    return val
def F(x,y):
    return F4(x,y)

black = [0,0,0]
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
w = 600
h = 600

# display list of line segments from contouring routine
gr = racg.Graphics(w=600,h=600)
gr.Clear()
s = 0.5*10**8
k = 3
x0,y0 = 200,100
gr.Clear()
G = lambda s: lambda x,y: F(x,y)-s
ix = 50
iy = 50
for y0 in range(1,600,iy):
    for x0 in range(1,600,ix):
        ctr.ShowLevelSet(gr,G(s), x0, y0, blue)
        gr.Point([x0,y0],red)
        ch = gr.Show("result",15)
        if ch == ord('e'):
            break
gr.Show("result",-1)
fn = "ImplicitFunction-ContourVelocity-%02d.jpg" % k
#gr.Save(fn)
gr.Close()
