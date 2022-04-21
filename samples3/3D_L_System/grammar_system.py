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
           flag=True, n=2):
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
    s = less_rapid_growth(n,rules)(start)
    print("|s| = ",len(s))
    print("s = \"%s\"" % s)

    ## gradual growth
    #s = less_rapid_growth(2,rules)(start)
    G,Gs = draw(G,Gs,s,line,point,flag)
    return G,Gs

def Shape2(s,line,point,
           flag=True, n=2):
    ######################### SCENE 1 BEGIN
    G = {}
    G['V'] = []
    G['E'] = []
    G['F'] = []
    G['N'] = []
    G['pts'] = []
    Gs = []

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

def Grammar_to_line2(start,rules,line,point,
            flag=False,n=2):
    H0,Gs0 = Shape0(start,rules, line,point,
                flag,n)
    print("|pts(H0)| =",len(H0['pts']))    
    def line2(G,Gs, A,B,r,q, H0=None):
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
    f = lambda G,Gs,A,B,r,q : line2(G,Gs,A,B,r,q,H0=H0) 
    return f

def String_to_line2(s,line,point,
            flag=False,n=2):
    H0,Gs0 = Shape2(s, line,point,
                flag,n)
    print("|pts(H0)| =",len(H0['pts']))    
    def line2(G,Gs, A,B,r,q, H0=None):
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
    f = lambda G,Gs,A,B,r,q : line2(G,Gs,A,B,r,q,H0=H0) 
    return f

