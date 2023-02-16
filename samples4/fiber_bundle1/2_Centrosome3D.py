import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import affine as aff
import extrusion as ext
import wire as wi
import BasicShapes as ba

import numpy as np

from copy import deepcopy
from math import pi,sin,cos,acos,sqrt

import centrosome as ce

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

######################### SCENE 1 BEGIN
G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []

###################################################
#
# Create Fiber Bundle of Microtubules. It is
# called a Centrosome.

# [3] https://en.wikipedia.org/wiki/Fiber_bundle
# The continuous surjective map pi : E -> B
# is F(i)(t) = C.B[i].curve(t) where E is [0,1] and
# B is the Microtubule C.B[i]. Below we use i = 0 for
# 0-th Microtubule or Fiber F(i). The Fibers
# have operations push_plus, pop_plus, push_minus,
# and pop_minus, and also cap_plus and cap_minus.

def GetFiber(C,i,dt=.1,tmin=0,tmax=1):
    assert(i in range(len(C.B)))
    F = C.B[i]
    t = tmin # should be in range [0,1]
    L = []
    while t <= tmax:
        pt = F.curve(t)
        L.append(pt)
        t = t + dt
    return L

def AddCentrosomeShape(G,Gs,C,r):
    # add sphere for centrosome
    t = C.O
    degrees = 0
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,
                axis[0],axis[1],axis[2])
    scale = 1
    s = [scale,scale,scale]
    H0 = ba.Sphere(r,t,q,s,m=30,n=30)
    Gs = ext.Append(Gs,H0)
    G = ext.GraphUnionS(G,H0)

    # add wire shapes for microtubules
    N = len(C.B) # number of fibers
    # create 3D objects for each fiber and add to scene
    for i in range(N):
        # Ellipsoid Object
        r = 1 # radius of cross section

        ppath = GetFiber(C,i,dt,tmin,tmax)
        t = C.B[i].O
        degrees = 0
        axis = [0,1,0]
        q = aff.HH.rotation_quaternion(degrees,
                        axis[0],axis[1],axis[2])
        scale = 1.
        s = [scale,scale,scale] # the same scale as previous for caps
        # n is length
        H0 = wi.Wire(r,ppath,t,q,s,m=10,n=50)
        Gs = ext.Append(Gs,H0)
        G = ext.GraphUnionS(G,H0)
    return G,Gs

# https://en.wikipedia.org/wiki/Spherical_coordinate_system
def Spherical2Cartesian(r,theta,phi):
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return [x,y,z]

def Spherical2Cartesian(x,y,z):
    r = sqrt(x**2 + y**2 + z**2)
    epsilon = 1e-8
    if abs(r) < epsilon:
        theta = 0
        phi = 0
    else:
        theta = acos(z/r)
        sgn = 1
        if y < 0:
            sgn = -1
        r2 = sqrt(x**2 + y**2)
        phi = sgn*acos(x/r2)
    return [r,theta,phi]

def Deg2Rad(x):
    y = x*pi/180
    return y
def Rad2Deg(x):
    y = x*180/pi
    return y

tmin = 0
tmax = 1
dt = .1

C = ce.Centrosome(O=[0,0,0])

r = 20

theta = Deg2Rad(30)
phi = Deg2Rad(110)
O_F = Spherical2Cartesian(r,theta,phi)

C.add_fiber(O=O_F)
C.B[0].push_plus([10,30,10])
C.B[0].push_plus([20,35,20])
C.B[0].push_plus([30,50,10])
C.B[0].push_plus([65,30,10])
#ce.DisplayFiber(C,0,dt,tmin,tmax)
C.B[0].pop_minus()
#ce.DisplayFiber(C,0,dt,tmin,tmax)

theta = Deg2Rad(130)
phi = Deg2Rad(150)
O_F = Spherical2Cartesian(r,theta,phi)

C.add_fiber(O=O_F)
C.B[1].push_plus([30,10,10])
C.B[1].push_plus([30,25,0])
C.B[1].push_plus([40,50,20])
C.B[1].push_plus([75,20,30])
#ce.DisplayFiber(C,1,dt,tmin,tmax)

G,Gs = AddCentrosomeShape(G,Gs,C,r)

#################################

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"Centrosome1.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"Centrosome1.obj")
