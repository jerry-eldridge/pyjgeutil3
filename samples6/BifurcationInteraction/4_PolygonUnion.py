import sys
sys.path.insert(0,
    r"C:/Users/jerry/Desktop/_Art/my_universes/")
import universes
import universes.shapes.common.graph as gra
import universes.shapes.common.a_star_doc_nd as asdn
import universes.shapes.common.graphic_matroid as gmat
import universes.canvas2d.graphics_cv as racg
import universes.shapes.common.mapto as mapto
import universes.shapes.common.polygon_area as pa
import universes.shapes.common.connected_components as cc

import numpy as np
from math import log,exp

import point_labeler as plabr

from copy import deepcopy

# sign of a real number.
def sign(x):
     if x < 0:
         return -1
     else:
         return 1

# Better would be a parallel algorithm if possible
# applied to each i,j pixel.
# Implicit Function F(x,y) to an image.
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

# Better would be a parallel algorithm if possible
# applied to each i,j pixel.
# Threshold of an image with im[j,i] = 1 when greater_eq
# than threshold and im[j,i] = 0 if not.
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

     return L,im2

def PlotGraph(gr,G,color=[0,0,0]):
     for e in G['E']:
         u,v = e
         A,B = list(map(lambda w: G['pts'][w],[u,v]))
         gr.Line(A,B,color)
     return

# Laplacian of a graph
def Laplacian(G):
     # the laplacian of a graph assumes G is a simple graph
     # which has no loops e = [u,u], multiple copies of e
     # and undirected edges e = [u,v] and f = [v,u] both would
     # be edges.
     G = gra.MakeUndirected(G)

     D = np.diag(list(map(lambda v: gra.Degree(G,v),G['V'])))
     A = gra.AdjMatrix(G)
     L = D - A
     return L
def NumberOfComponents(G):
     # calculate the graph Laplacian
     L = Laplacian(G)
     a = list(np.linalg.eigvals(L))
     epsilon = 0.001
     # the multiplicity of eigenvalue 0 of laplacian
     # matrix L
     c = len(list(filter(lambda x: abs(x)<epsilon, a)))
     return c

def ShowLevelSet(gr,im,isoval,color=[0,0,0],fillcolor=[255,0,0],
                  interior=True,
                  istep=1,jstep=1,
                  fillistep=15,filljstep=15):
     # Get list of lines [line_i] with line=[A,B] with A and B points.
     L,im2 = LevelSet(im,isoval,istep=istep,jstep=jstep)

     # Label all Points in the lines. Don't have too many points.
     # Adjust plab.epsilon = 20 to use bigger radius to include less points.
     # And, create a graph G for the labeled points based
     # on connectivity from a set of lines L
     plab = plabr.PointLabeler([])
     plab.epsilon = 20
     G = {}
     # Define the vertices V of the graph G.
     V = []
     for line in L:
         A,B = line
         lA = plab.Add(A)
         lB = plab.Add(B)
         if lA not in V:
             V.append(lA)
         if lB not in V:
             V.append(lB)

     # Define the edges E of the graph G.
     E = []
     for line in L:
         A,B = line
         dA,jA = plab.NearestNeighbor(A)
         dB,jB = plab.NearestNeighbor(B)
         A2 = plab.pts[jA]
         B2 = plab.pts[jB]
         gr.Line(A2,B2,color)
         u = plab.labels[jA]
         v = plab.labels[jB]
         e = [u,v]
         f = [v,u]
         if (e not in E) and (f not in E) and (u != v):
             E.append(e)

     # define graph for implement function level set
     G['V'] = V
     G['E'] = E
     # Turn pseudograph G into graph G
     G = gra.PseudoToGraph(G)
     # And define points pts in graph G afterwards.
     G['pts'] = list(map(lambda pt: list(map(float,pt)),plab.pts))

     # Plot the graph
     PlotGraph(gr,G)

     # Display number of vertices |V| and edges |E|
     s = "|V|=%d,|E|=%d" % (len(G['V']),len(G['E']))
     gr.Text(s,10,20,color,scale=.5)

     # Display number of connected components c
     C = cc.ConnectedComponentsBrute(G)
     c = len(C)
     c2 = NumberOfComponents(G)
     s = "|C| = %d,%d" % (c,c2)
     y0 = 40
     gr.Text(s,10,y0,color,scale=.5)

     # Plot Interior Region with fillcolor colored circles
     # of radius r at each point (i,j) in interior.
     sh = im2.shape
     h,w = sh
     r = fillistep/4.0
     if interior:
         sgn = 1
     else:
         sgn = -1
     for j in range(y0+10,h,filljstep):
         for i in range(0,w,fillistep):
             if sgn*(im[j,i] - isoval) < 0:
                 C = [i,j]
                 gr.Circle(C,r,fillcolor)
     return G

# Implicit Function of a line through points (x1,y1)
# and (x2,y2)
def Line(x1,y1,x2,y2):
     def F(x,y):
         return (y-mapto.MapTo(x1,y1,x2,y2,x))/10.0
     return F

# Implicit Function of a polygon defined by a list
# L of points [xi,yi] making lines (not line segments).
def PolygonReg(L):
     def F(x,y):
         val = 1
         n = len(L)
         for i in range(n):
             A = L[i%n]
             B = L[(i+1)%n]
             v = Line(A[0],A[1],B[0],B[1])(x,y)
             val = val*v
         return val
     return F

# Implicit Function of a polygon like before but only
# allow region to be interior to polygon line segments.
def Polygon(L):
     F = PolygonReg(L)
     def G(x,y):
         val = F(x,y)
         if pa.PointInPolygonTest(L,x,y):
             val = -abs(val)
         else:
             val = abs(val)
         return val
     return G

black = [0,0,0]
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
w = 500
h = 500

def F1(x,y):
     a = 100
     b = 200
     r = 70
     val = (x-a)**2 + (y-b)**2 - r**2
     return val
def F2(x,y):
     a = 200
     b = 300
     r = 70
     val = (x-a)**2 + (y-b)**2 - r**2
     return val
# Implicit Function Union
def Join(F1,F2):
     def F(x,y):
         return min(F1(x,y),F2(x,y))
     return F
# Implicit Function Intersection
def Meet(F1,F2):
     def F(x,y):
         return max(F1(x,y),F2(x,y))
     return F
# Implicit Function Complement
def Comp(F1):
     def F(x,y):
         return -F1(x,y)
     return F
# Implicit Function Difference
def Diff(F1,F2):
     return Meet(F1,Comp(F2))

def F(x,y):
     return Join(F2,F1)(x,y)

print("Please Wait...computing Function to Image...")
im = F2im(F,w,h)
print("Completed.")

print("Displaying graphics...")
# display list of line segments from contouring routine
gr = racg.Graphics(w=w,h=h)
gr.Clear()
s = -4
print("""
This displays connected component number and
number of edges and vertices
""")
print("Press 'e' to exit. Displaying 150 iterations")
for k in range(0,450,20):
     gr.Clear()
     G = ShowLevelSet(gr,im,k*s,color=black,
            fillcolor=blue,interior=True,
            istep=5,jstep=5,fillistep=15,
            filljstep=15)
     ch = gr.Show("result",15)
     if ch == ord('e'):
         break
print(f"G={G}")
gr.Close()
