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

def draw(G,Gs,s, line, point, flag=False):
    S1 = []
    S2 = []
    pos = [0,0,0]
    axis = [0,0,1]
    q = aff.HH.rotation_quaternion(0,
                axis[0],axis[1],axis[2])
    if flag:
        N0 = 16
    else:
        N0 = 8
    angle = 360./N0
    heading = 0
    r = 50
    for i in range(len(s)):
        c = s[i]
        if c in ["a","b"]:
            r2 = 35
            O = [r2,0,0]
            pts = aff.Rotate([O],q,align=False)
            pts = aff.Translate(pts,*pos,align=False)
            B = pts[0]
            G,Gs = line(G,Gs, pos,B,r,q)
            pos = deepcopy(B)
        if c in ["c"]:
            r2 = 35
            O = [r2,0,0]
            pts = aff.Rotate([O],q,align=False)
            pts = aff.Translate(pts,*pos,align=False)
            B = pts[0]
            G,Gs = point(G,Gs, pos,B,r,q)
            pos = deepcopy(B)
        elif c == 'z':
            axis1 = [0,0,1]
            heading = fmod(heading + angle, 360)
            if flag:
                degrees = angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'k':
            axis1 = [0,0,1]
            heading = fmod(heading - angle, 360)
            if flag:
                degrees = -angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'y':
            axis1 = [0,1,0]
            heading = fmod(heading + angle, 360)
            if flag:
                degrees = angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'j':
            axis1 = [0,1,0]
            heading = fmod(heading - angle, 360)
            if flag:
                degrees = -angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'x':
            axis1 = [1,0,0]
            heading = fmod(heading + angle, 360)
            if flag:
                degrees = angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'i':
            axis1 = [1,0,0]
            heading = fmod(heading - angle, 360)
            if flag:
                degrees = -angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == '<':
            S1.append(pos)
        elif c == '>':
            val = S1[-1]
            S1 = S1[:-1]
            pt = val
            pos = deepcopy(pt)
        elif c == 'o':
            O = [0,0,0]
            pos = deepcopy(O)
        elif c == 'r':
            q = aff.HH.rotation_quaternion(0,
                axis[0],axis[1],axis[2])
        elif c == '(':
            S2.append(q)
        elif c == ')':
            val = S2[-1]
            S2 = S2[:-1]
            qq = val
            q = qq
        elif c == 'f':
            r2 = 35
            O = [r2,0,0]
            pts = aff.Rotate([O],q,align=False)
            pts = aff.Translate(pts,*pos,align=False)
            B = pts[0]
            pos = deepcopy(B)
        elif c == 'b':
            r2 = 35
            O = [-r2,0,0]
            pts = aff.Rotate([O],q,align=False)
            pts = aff.Translate(pts,*pos,align=False)
            B = pts[0]
            pos = deepcopy(B) 
        else:
            continue
    return G,Gs

def Shape0(start,rules,line,point,
           flag=True):
    ######################### SCENE 1 BEGIN
    G = {}
    G['V'] = []
    G['E'] = []
    G['F'] = []
    G['N'] = []
    G['pts'] = []
    Gs = []
    # set the parameters one by one until reasonably
    # too slow. The growth is exponential like.
    # Each character A or B is a cylinder shape which
    # has lots of points and triangles in it.

    ## growth burst
    s = less_rapid_growth(2,rules)(start)
    print("|s| = ",len(s))
    print("s = \"%s\"" % s)

    ## gradual growth
    #s = less_rapid_growth(2,rules)(start)
    G,Gs = draw(G,Gs,s,line,point,flag)
    return G,Gs

def Shape1(H,t,q,s):
    H2 = deepcopy(H)
    #print("|pts(H2)| = ",len(H2['pts']))
    C = aff.Center(H2['pts'])
    H2['pts'] = aff.Translate(H2['pts'],
                        -C[0],-C[1],-C[2],align=False)
    H2['pts'] = aff.Rotate(H2['pts'],
                        q,align=False)    
    H2['pts'] = aff.Scale(H2['pts'],
                        s[0],s[1],s[2],align=False)
    H2['pts'] = aff.Translate(H2['pts'],
                        t[0],t[1],t[2],align=False)
    return H2

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

# Note Sigma is 'A','B','x','i','y','j','z','k','[',
# and ']'.
start = "S"

# A rule is a list (LHS,RHS,p) where
# LHS -> RHS with probability p.
start1 = "S"
rules1 = [
    ("S","[DxDxDx]",.9),
    ("D","[EyEyEy]",.9),
    ("E","[FzFzFz]",.9),
    ("F","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start2 = "S"
rules2 = [
    ("S","o[HHH]",1),
    ("H","FoG",1),
    ("G","zFxx",1),
    ("F","[DDDDD]",.9),
    ("D","Exyz",.9),
    ("E","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start3 = "D"
rules3 = [
    ("D","N",1),
    ("N","[E]O",1),
    ("O","ffffff",1),
    ("E","XZF",1),
    ("F","XZG",1),
    ("G","XZH",1),
    ("H","XZIX", 1),
    ("I","YJ",1),
    ("J","XWK",1),
    ("K","XWL",1),
    ("L","XWM",1),
    ("M","XW", 1),
    ("X","aaaa",1),
    ("Y","yyyy",1),
    ("Z","zzzz",1),
    ("W","xxxx",1),
    ("[","<(",1),
    ("]",")>",1)
    ]

start4 = "S"
rules4 = [
    ("S","[CC]",1),
    ("C","BBBB",1),
    ("B","aO",1),
    ("O","xGy",1),
    ("G","FFFF",1),
    ("F","ffff",1)

    ]  

rules = rules1
start = start1

G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []
H0,Gs0 = Shape0(start,rules, line,point,
                flag=False)
print("|pts(H0)| =",len(H0['pts']))
    
# Save Scene 1
#ext.Graphs2OBJ(BIGDATA+"3D_L_system_5.obj",Gs0,"scene")

# Double-Click on OBJ file
#import os
#os.system(BIGDATA+"3D_L_system_5.obj")


def line2(G,Gs, A,B,r,q):
    # Ellipsoid Object
    rad = 5.
    height = r
    t = list(aff.lerp(np.array(A),np.array(B),0.5))
    q2 = q
    scale = 1.
    s = [scale,scale,scale] # the same scale as previous for caps
    H1 = Shape1(H0,t,q2,s)
    Gs = ext.Append(Gs,H1)
    G = ext.GraphUnionS(G,H1)
    return G,Gs

G,Gs = Shape0(start4,rules4, line2, point,
              flag=True)
print("|pts(G)| = ",len(G['V']))
    
# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"3D_L_system_5.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"3D_L_system_5.obj")
