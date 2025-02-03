import sys
sys.path.append(\
    r"C:/Users/jerry/Desktop/_Art/my_universes")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as bs
import universes.volume_of_OBJ as voo
import universes.transform_shape as ts
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.common.vectors as vec
import universes.shapes.common.CoordSystem as cs
import universes.shapes.common.human_doll as hd
import universes.shapes.common.graph as gra
import universes.shapes.alg_topo as topo
import universes.canvas2d.graphics_cv as racg

import numpy as np
from functools import reduce
from copy import deepcopy
import time

from math import cos,sin,pi,atan2,sqrt,exp


# Creates points of a sphere with N1 along one cross section and N2 on other
# of radius r
def Sphere(r,N1,N2):
     S2 = []
     dtheta = (2*pi)/N1
     dphi = (pi)/N2
     theta = 0
     while theta <= 2*pi:
         phi = 0
         while phi <= pi:
             pt = [r,theta,phi]
             S2.append(pt)
             phi += dphi
         theta += dtheta
     return S2

# Creates points of a sphere with N1 along one cross section and N2 on other
# of radius rho and height h
def Cylinder(rho,h,N1,N2):
     C2 = []
     dphi = (2*pi)/N1
     dz = (1.*h)/N2
     phi = 0
     while phi <= 2*pi:
         z = -.5*h
         while z <= .5*h:
             pt = [rho,phi,z]
             C2.append(pt)
             z += dz
         phi += dphi
     return C2


# map cylinder to sphere assuming same number N1 and N2
def CylinderToSphere(C):
     S = []
     for pt in C:
         # cylinder coords
         rho,phi,z = pt # cylinder
         # map old cylinder coords to new
         r,h,phi = rho,z,phi
         # to spherical
         rho = sqrt(r**2+h**2)
         theta = phi
         phi = atan2(r,h)
         # map sphere coords to old
         r,theta,phi = rho,theta,phi
         pt2 = [r,theta,phi] # sphere
         S.append(pt2)
     return S

# Stereographic projection of 3D sphere to 2D polar plane
def SphereToPolar(S):
     P = []
     for pt in S:
         r,theta,phi = pt
         R,THETA = [cos(phi/2)/(sin(phi/2)+0.00001),theta]
         pt2 = [R,THETA]
         P.append(pt2)
     return P

# map polar coordinates to cartesian coordinates in 2D
def PolarToCartesian(P):
     C = []
     for pt in P:
         r,theta = pt
         x = r*cos(theta)
         y = r*sin(theta)
         pt2 = [x,y]
         C.append(pt2)
     return C

# map cartesian coordinates to complex numbers
def CartesianToComplex(C):
     Z = []
     for pt in C:
         x,y = pt
         z = complex(x,y)
         Z.append(z)
     return Z

# complex numbers transformation from z' = f(z)
def Mobius(a,b,c,d):
     def f(z):
         z2 = 1.0*(a*z+b)/(c*z+d)
         return z2
     return f

# plot points
def Plot(gr,P,color):
     for pt in P:
         gr.Point(pt,color)
     return

def f(S,k=0):
     #print(S[k],'->')
     P = SphereToPolar(S)
     #print(P[k],'->')
     P = PolarToCartesian(P)
     #print(P[k],'->')
     Z = CartesianToComplex(P)
     #print(Z[k],'->')
     return Z

def g1(Z,k=0):
     return Z

def g2(Z,k=0):
     # f(z) = (a*z+b)/(c*z+d)
     a = complex(1,2)
     b = complex(3,2)
     c = complex(1,1)
     d = complex(1,3)
     #print("Mobius:a,b,c,d=",a,b,c,d)
     Z = list(map(lambda z: Mobius(a,b,c,d)(z), Z))
     #print(Z[k],'->')
     return Z

def s(Z,k=0):
     P = list(map(lambda z: [z.real,z.imag,0], Z))
     #print(P[k],'->')
     P = aff.Scale(P,200,200,1)
     #print(P[k],'->')
     P = aff.Translate(P,w/2,h/2,0)
     #print(P[k],'->')
     #print()
     return P

def F1():
     N1 = 7
     N2 = 5
     rho = 20
     height = 10
     C2 = Cylinder(rho,height,N1,N2)
     r = 10
     Sa = Sphere(r,N1,N2)
     Sb = CylinderToSphere(C2)
     return Sa,Sb
def F2(g):
     Sa,Sb = F1()
     Pa = s(g(f(Sa)))
     Pb = s(g(f(Sb)))

     # specify some points on sphere for sphere holes
     r0 = 5
     theta0 = 280*(pi/180.) # 0 to 2*pi or 0 to 360
     phi0 = 100*pi/180. # 0 to pi or 0 to 180
     theta1 = 80*(pi/180.) # 0 to 2*pi or 0 to 360
     phi1 = 30*pi/180. # 0 to pi or 0 to 180
     theta2 = 50*(pi/180.) # 0 to 2*pi or 0 to 360
     phi2 = 130*pi/180. # 0 to pi or 0 to 180
     P = [[r0,theta0,phi0],
          [r0,theta1,phi1],
          [r0,theta2,phi2]]

     # map sphere points to canvas
     P2 = s(g(f(P)))
     return Pa,Pb,P2

def F3(gr,Pa,Pb,P2):
     # Plot canvas points and label sphere points
     gr.Clear()
     # Graphics loop
     red = [255,0,0]
     green = [0,255,0]
     blue = [0,0,255]
     Plot(gr,Pa,red)
     Plot(gr,Pb,blue)
     for i in range(len(P2)):
         gr.Label(str(i+1),P2[i][:2],green)
     ch = gr.Show("result",-1)
     return

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)


Pa,Pb,P2 = F2(g1)
F3(gr,Pa,Pb,P2)

Pa,Pb,P2 = F2(g2)
F3(gr,Pa,Pb,P2)

gr.Close()

