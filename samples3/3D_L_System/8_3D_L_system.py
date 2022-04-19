import BasicShapes as bs
import extrusion as ext
import affine as aff

import numpy as np
from copy import deepcopy

from functools import reduce

from math import cos,sin,pi,fmod

import random

seed = 123123123
random.seed(seed)

# [1] https://en.wikipedia.org/wiki/L-system
def apply_rule(s,LHS,RHS):
    L = s.split(LHS)
    s2 = RHS
    s3 = s2.join(L)
    return s3

def r(s,rules):
    for rule in rules:
        LHS,RHS, p = rule
        s2 = apply_rule(s,LHS,RHS)
        s = s2
    return s

def extremely_rapid_growth(i,rules):
    def f(s):
        val = reduce(lambda n,m: r(n,rules),
                    range(i), s)
        return val
    return f

def apply_rule2(s,LHS,RHS,p):
    L = s.split(LHS)
    s2 = RHS
    s3 = ''
    flag = False
    for i in range(len(L)-1):
        x = L[i]
        y = RHS
        px = random.uniform(0,1)
        if px <= p:
            s3 = s3 + x + y
            flag = True
        else:
            s3 = s3 + x + LHS
            flag = False
    z = L[-1]
    if flag:
        s3 = s3 + z
    else:
        s3 = s3 + z
    return s3

def r2(s,rules):
    for rule in rules:
        LHS,RHS, p = rule
        s2 = apply_rule2(s,LHS,RHS,p)
        s = s2
    return s

def less_rapid_growth(N,rules):
    def f(t):
        s = t
        for i in range(N):
            s2 = r2(s,rules)
            s = s2
        return s
    return f

def line(G,Gs, A,B,r,q):
    # Ellipsoid Object
    rad = 5.
    height = r
    t = list(aff.lerp(np.array(A),np.array(B),0.5))
    q0 = aff.HH.rotation_quaternion(90,0,1,0)
    q2 = q*q0
    scale = 1.
    s = [scale,scale,scale] # the same scale as previous for caps
    H0 = bs.Cylinder(rad,height,t,q2,s,m=10,n=10)
    Gs = ext.Append(Gs,H0)
    G = ext.GraphUnionS(G,H0)
    return G,Gs

def point(G,Gs, A,B,r,q):
    # Ellipsoid Object
    rx = 10.
    ry = 30.
    height = r
    t = list(aff.lerp(np.array(A),np.array(B),0.5))
    q0 = aff.HH.rotation_quaternion(90,0,1,0)
    q2 = q*q0
    scale = 1.
    s = [scale,scale,scale] # the same scale as previous for caps
    H0 = bs.Ellipsoid(rx,ry,t,q2,s,m=10,n=10)
    Gs = ext.Append(Gs,H0)
    G = ext.GraphUnionS(G,H0)
    return G,Gs



def draw(s):
    ######################### SCENE 1 BEGIN
    G = {}
    G['V'] = []
    G['E'] = []
    G['F'] = []
    G['N'] = []
    G['pts'] = []
    Gs = []

    
    S = []
    pos = [0,0,0]
    axis = [0,0,1]
    heading = 0
    q = aff.HH.rotation_quaternion(heading,
                axis[0],axis[1],axis[2])
    N0 = 8
    angle = 360./N0
    r = 50
    for i in range(len(s)):
        c = s[i]
        if c in ["A","B"]:
            theta = heading*pi/180.
            r2 = 35
            O = [r2,0,0]
            pts = aff.Rotate([O],q,align=False)
            pts = aff.Translate(pts,*pos,align=False)
            B = pts[0]
            G,Gs = line(G,Gs, pos,B,r,q)
            pos = deepcopy(B)
        if c in ["C"]:
            theta = heading*pi/180.
            r2 = 35
            O = [r2,0,0]
            pts = aff.Rotate([O],q,align=False)
            pts = aff.Translate(pts,*pos,align=False)
            B = pts[0]
            G,Gs = point(G,Gs, pos,B,r,q)
            pos = deepcopy(B)
        elif c == 'z':
            axis1 = [0,0,1]
            heading = fmod(heading + angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == 'k':
            axis1 = [0,0,1]
            heading = fmod(heading - angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == 'y':
            axis1 = [0,1,0]
            heading = fmod(heading + angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == 'j':
            axis1 = [0,1,0]
            heading = fmod(heading - angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == 'x':
            axis1 = [1,0,0]
            heading = fmod(heading + angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == 'i':
            axis1 = [1,0,0]
            heading = fmod(heading - angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == '[':
            S.append((pos,q))
        elif c == ']':
            val = S[-1]
            S = S[:-1]
            pt,qq = val
            pos = deepcopy(pt)
            q = qq
        else:
            continue
    return G,Gs


BIGDATA = r"C:/_BigData/_3D/my_scenes/"

# Note Sigma is 'A','B','x','i','y','j','z','k','[',
# and ']'.
start = "S"

# A rule is a list (LHS,RHS,p) where
# LHS -> RHS with probability p.
rules = [
    ("S","[DxDxDx]",.9),
    ("D","[EyEyEy]",.9),
    ("E","[FzFzFz]",.9),
    ("F","ACA",.9)]
# set the parameters one by one until reasonably
# too slow. The growth is exponential like.
# Each character A or B is a cylinder shape which
# has lots of points and triangles in it.

## growth burst
#s = extremely_rapid_growth(3,rules)(start) 

## gradual growth
s = less_rapid_growth(2,rules)(start)

G,Gs = draw(s)

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"3D_L_system_4.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"3D_L_system_4.obj")
