import BasicShapes as bs
import extrusion as ext
import affine as aff

import numpy as np
from copy import deepcopy

from functools import reduce

from math import cos,sin,pi,fmod

# [1] https://en.wikipedia.org/wiki/L-system
def apply_rule(s,LHS,RHS):
    L = s.split(LHS)
    s2 = RHS
    s3 = s2.join(L)
    return s3

def r(s):
    s2 = apply_rule(s,"A","B-[A-B]\n")
    s3 = apply_rule(s2,"B","A+[B-A]\n")
    return s3

def S(i):
    def f(s):
        val = reduce(lambda n,m: r(n), range(i), s)
        return val
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
    angle = 26
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
        elif c == '-':
            axis1 = [0,0,1]
            heading = fmod(heading + angle,360)
            degrees = heading
            q = aff.HH.rotation_quaternion(degrees,
                axis1[0],axis1[1],axis1[2])
        elif c == '+':
            axis1 = [2,1,1]
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

start = "A"
s = S(2)(start)
G,Gs = draw(s)

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"3D_L_system_1.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"3D_L_system_1.obj")
