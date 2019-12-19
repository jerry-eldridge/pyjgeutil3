import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
#import graphics_pygame as racg
import graphics_cv as racg
import mapto
import numpy as np
from math import log,exp

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

def F(x,y):
    val = F1(x,y)*F2(x,y)*F3(x,y)
    return val
def F2im(F,w,h):
    # Implicit function F(x,y) to image
    im = np.zeros((h,w))
    xlo = 0
    xhi = w
    ylo = 0
    yhi = h
    for j in range(h):
       y = mapto.MapTo(ylo,0,yhi,h-1,j)
       for i in range(w):
           x = mapto.MapTo(xlo,0,xhi,w-1,i)
           im[j,i] = F(x,y)
    return im
def Threshold(im,thresh):
    # thresholded bit representation for image
    h,w = im.shape
    im2 = np.zeros((h,w))
    for j in range(h):
        for i in range(w):
            if im[j,i] < thresh:
                im2[j,i] = 0
            else:
                im2[j,i] = 1
    return im2

def LevelSet(im,isoval,istep=1,jstep=1):
    # Contouring routine to get Level Set for image im
    # this will return a list of line segments.
    # A level set is where F(x,y) = c for constant c.
    # https://en.wikipedia.org/wiki/Marching_squares
    h,w = im.shape
    im2 = Threshold(im,isoval)
    L = []
    p = []
    p.append([-istep,-jstep])
    p.append([istep,-jstep])
    p.append([istep,jstep])
    p.append([-istep,jstep])
    def interp(i,j,ii,jj,p):
        pt1 = [p[ii][0]+i,p[ii][1]+j]
        pt2 = [p[jj][0]+i,p[jj][1]+j]
        A = np.array(pt1)
        B = np.array(pt2)
        C = 0.5*(A+B)
        return list(C)

    for j in range(jstep,h-jstep,jstep):
        for i in range(istep,w-istep,istep):
            n = 0
            for k in range(len(p)):
                pt = p[k]
                n += (2**k)*int(im2[j+pt[1],i+pt[0]])
            if n == 0b1110 or n == 0b0001:
                A = interp(i,j,0,3,p)
                B = interp(i,j,0,1,p)
                L.append([A,B])
            if n == 0b1101 or n == 0b0010:
                A = interp(i,j,0,1,p)
                B = interp(i,j,1,2,p)
                L.append([A,B])
            if n == 0b1011 or n == 0b0100:
                A = interp(i,j,1,2,p)
                B = interp(i,j,2,3,p)
                L.append([A,B])
            if n == 0b0111 or n == 0b1000:
                A = interp(i,j,2,3,p)
                B = interp(i,j,3,0,p)
                L.append([A,B])

            if n == 0b1100 or n == 0b0011:
                A = interp(i,j,0,3,p)
                B = interp(i,j,1,2,p)
                L.append([A,B])
            if n == 0b1001 or n == 0b0110:
                A = interp(i,j,0,1,p)
                B = interp(i,j,2,3,p)
                L.append([A,B])

    return L
def ShowLevelSet(gr,im,isoval,istep=1,jstep=1,color=[0,0,0]):
    L = LevelSet(im,isoval,istep=istep,jstep=jstep)
    for line in L:
        A,B = line
        gr.Line(A,B,color)
    return

black = [0,0,0]
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
w = 600
h = 600
im = F2im(F,w,h)

# display list of line segments from contouring routine
gr = racg.Graphics(w=600,h=600)
gr.Clear()
s = 0.5*10**8
for k in range(10):
    gr.Clear()
    ShowLevelSet(gr,im,k*s,istep=1,jstep=1,color=black)
    gr.Show("result",-1)
    fn = "ImplicitFunction-Contour-%02d.jpg" % k
    #gr.Save(fn)
gr.Close()
