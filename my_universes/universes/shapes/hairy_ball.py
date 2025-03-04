from .common import affine as aff
from . import BasicShapes as ba
from . import extrusion as ext
from . import wire as wi
from . import centrosome as ce

from math import sin,cos,pi,sqrt,acos,fmod

import random
import time

seed = 12345

#seed = time.time()
random.seed(seed)

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
    t = tmin
    while t <= tmax:
        pt = F.curve(t)
        L.append(pt)
        t = t + dt
    return L

def sgn(y):
    if y < 0:
        return -1
    else:
        return 1

# https://en.wikipedia.org/wiki/Spherical_coordinate_system
def Spherical2Cartesian(r,theta,phi):
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return [x,y,z]

def Cartesian2Spherical(x,y,z):
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

def HairyBallTangent(t):
    x,y,z = t
    r,theta,phi = Cartesian2Spherical(x,y,z)
    theta2 = theta + pi/2.
    axis1 = t
    axis2 = Spherical2Cartesian(r,theta2,phi)
    q = ext.AimAxis(axis1,axis2)
    return q

def CreateCentrosomeShape(C,r):
    G = {}
    G['V'] = []
    G['E'] = []
    G['F'] = []
    G['N'] = []
    G['pts'] = []
    # add sphere for centrosome
    t = C.O
    degrees = 0
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,
                axis[0],axis[1],axis[2])
    scale = 1
    s = [scale,scale,scale]
    H0 = ba.Sphere(r,t,q,s,m=30,n=30)
    G = ext.GraphUnionS(G,H0)

    tmin = 0
    tmax = 1
    dt = .1

    # add wire shapes for microtubules
    N = len(C.B) # number of fibers
    # create 3D objects for each fiber and add to scene
    for i in range(N):
        # Ellipsoid Object
        ri = 1 # radius of cross section

        ppath = GetFiber(C,i,dt,tmin,tmax)
        t = C.B[i].O
        degrees = 0
        axis = [0,1,0]
        #q = aff.HH.rotation_quaternion(degrees,
        #                axis[0],axis[1],axis[2])
        q = HairyBallTangent(t)
        scale = .15
        s = [scale,scale,scale] # the same scale as previous for caps
        # n is length
        H1 = wi.Wire(ri,ppath,t,q,s,m=5,n=5)
        G = ext.GraphUnionS(G,H1)
    return G

def create_hairy_ball(nfibers=15):
    C = ce.Centrosome(O=[0,0,0])
    r = 8
    #nfibers = 350
    nsubunits = 15
    dr = 5

    for i in range(nfibers):
        theta = random.uniform(0,180)
        phi = random.uniform(0,360)
        O_F = Spherical2Cartesian(r,
                    Deg2Rad(theta),Deg2Rad(phi))
        C.add_fiber(O=O_F)
        C.B[i].push_plus(O_F)
        for j in range(nsubunits):
            a = 15
            b = 5
            theta_j = random.uniform(-a,a)
            phi_j = random.uniform(-b,b)
            theta2 = theta + theta_j
            phi2 = phi + phi_j
            theta2 = fmod(theta2,180)
            phi2 = fmod(phi2,360)
            pt_j = Spherical2Cartesian(dr,
                        Deg2Rad(theta2),Deg2Rad(phi2))
            C.B[i].push_plus(pt_j)
            theta = theta2
            phi = phi2  
    G = CreateCentrosomeShape(C,r)
    return G

