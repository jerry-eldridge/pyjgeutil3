#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
import vectors as v

import numpy as np
from math import sqrt,atan2,pi
from copy import deepcopy

def LineIntersect(A,B,C,D,display_commands=False):
    """
    Uses Projective Geometry and homegeneous coordinates
    A = [x1,y1,1], B = [x2,y2,1], C = [x3,y3,1], D = [x4,y4,1]
    and E = (A x B) x (C x D) as intersection point.
    """
    if display_commands:
         s = "LineIntersect(%s,%s,%s,%s,display_commands=%s)" % \
             (str(A),str(B),str(C),str(D),str(display_commands))
         print s
    l1,l2 = v.cross(A+[1],B+[1]),v.cross(C+[1],D+[1])
    E = v.cross(l1,l2)
    if E[2] == 0:
        return False, E[:2]
    else:
        E = list(np.array(E)/(1.0*E[2]))[:2]
        return True, E

def sgn(x):
    if x < 0:
        return -1
    else:
        return 1

def CircleLineIntersect(line,C,r,display_commands=False):
    """
    [1] http://mathworld.wolfram.com/Circle-LineIntersection.html
    """
    if display_commands:
         s = "CircleLineIntersect(%s,%s,%s,display_commands=%s)" % \
             (str(line),str(C),str(r),str(display_commands))
         print s
    line = map(lambda pt: pt+[0],line)
    h,k = C
    C = C+[0]
    line = Translate(line, -h,-k,0)
    [C] = Translate([C],-h,-k,0)
    [[x1,y1,z1],[x2,y2,z2]] = line
    dx = x2 - x1
    dy = y2 - y1
    dr = sqrt(dx**2 + dy**2)
    epsilon = 1e-8
    if dr < epsilon:
        return -1,[]
    D = x1*y2 - x2*y1
    delta = r**2*dr**2 - D**2
    if delta < 0:
        return delta, []
    if delta == 0:
        xA = 1.0*(D*dy + sgn(dy)*dx*sqrt(delta))/dr**2
        yA = 1.0*(-D*dx + abs(dy)*sqrt(delta))/dr**2
        pts = [[xA,yA,0]]
    else:
        xA = 1.0*(D*dy + sgn(dy)*dx*sqrt(delta))/dr**2
        yA = 1.0*(-D*dx + abs(dy)*sqrt(delta))/dr**2
        xB = 1.0*(D*dy - sgn(dy)*dx*sqrt(delta))/dr**2
        yB = 1.0*(-D*dx - abs(dy)*sqrt(delta))/dr**2
        pts = [[xA,yA,0],[xB,yB,0]]
    pts = Translate(pts,h,k,0)
    line = Translate(line, h,k,0)
    [C] = Translate([C],h,k,0)
    pts = map(lambda pt: pt[:2],pts)
    return delta,pts

def Transform(shape,T):
    shape4 = map(lambda pt: pt+[1], shape)
    SHAPE4 = map(lambda pt: list(np.einsum('ij,j->i',T,pt)), shape4)
    SHAPE = map(lambda pt: pt[:3], SHAPE4)
    return SHAPE
def Rotate(shape,degrees,x,y,z):
    R = v.rotation_matrix(degrees,x,y,z)
    SHAPE = Transform(shape,R)
    return SHAPE
def Translate(shape,x,y,z):
    T = v.translation_matrix(x,y,z)
    SHAPE = Transform(shape,T)
    return SHAPE
def Scale(shape,s):
    T = v.scale_matrix(s,s,s)
    SHAPE = Transform(shape,T)
    return SHAPE
def Center(shape):
    # use average of points as Center, the center of mass
    CM = sum(map(lambda pt: np.array(pt)/len(shape),shape))
    return CM
def Round(shape):
    SHAPE = map(lambda pt: map(lambda x: int(round(x)),pt), shape)
    return SHAPE

def CircleCircleIntersect(C1,r1,C2,r2,display_commands=False):
    """
    [1] http://mathworld.wolfram.com/Circle-CircleIntersection.html
    mentions a method of Circle Circle intersection. We extend
    the calculations.
    """
    if display_commands:
         s = "CircleCircleIntersect(%s,%s,%s,%s,display_commands=%s)" % \
             (str(C1),str(r1),str(C2),str(r2),str(display_commands))
         print s
    C1 = C1+[0]
    C2 = C2+[0]
    V1 = np.array(C2) - np.array(C1)
    V1 = list(V1/v.norm(V1))
    theta = atan2(V1[1],V1[0])*180/pi
    shape = [C1,C2]
    shape = Translate(shape,-C1[0],-C1[1],0)
    shape = Rotate(shape,-theta,0,0,1)
    d = shape[1][0]
    shape = Translate(shape,C1[0],C1[1],0)
    R = r1
    r = r2
    epsilon = 1e-8
    if abs(d) < epsilon:
        pts = []
        return False,pts
    x = 1.0*(d**2 - r**2 + R**2)/(2*d)
    delta = R**2 - x**2
    if delta < 0:
         delta = 0
         return False,[]
    y1 = 1.0*sqrt(delta)
    y2 = -1.0*sqrt(delta)
    pts = [[x,y1,0],[x,y2,0]]
    pts = Rotate(pts,theta,0,0,1)
    pts = Translate(pts,C1[0],C1[1],0)
    pts = map(lambda pt: pt[:2],pts)
    return True,pts


def TriangleCentroid(A,B,C):
    points = np.array([A,B,C])
    # barycentric coordinates scaled where alpha + beta + gamma = 3
    alpha = 1
    beta = 1
    gamma = 1
    s = 1.0*(alpha + beta + gamma)
    epsilon = 1e-8
    alpha /= (s+epsilon)
    beta /= (s+epsilon)
    gamma /= (s+epsilon)
    pt = points[0]*alpha + points[1]*beta + points[2]*gamma
    return pt

def Circumcenter(A,B,C):
    points = np.array([A,B,C])
    a = v.metric(B,C)
    b = v.metric(A,C)
    c = v.metric(A,B)
    alpha = a**2*(b**2+c**2-a**2)
    beta = b**2*(c**2+a**2-b**2)
    gamma = c**2*(a**2+b**2-c**2)
    s = 1.0*(alpha + beta + gamma)
    epsilon = 1e-8
    alpha /= (s+epsilon)
    beta /= (s+epsilon)
    gamma /= (s+epsilon)
    pt = points[0]*alpha + points[1]*beta + points[2]*gamma
    return pt

def Incenter(A,B,C):
    points = np.array([A,B,C])
    a = v.metric(B,C)
    b = v.metric(A,C)
    c = v.metric(A,B)
    alpha = a
    beta = b
    gamma = c
    s = 1.0*(alpha + beta + gamma)
    epsilon = 1e-8
    alpha /= (s+epsilon)
    beta /= (s+epsilon)
    gamma /= (s+epsilon)
    pt = points[0]*alpha + points[1]*beta + points[2]*gamma
    return pt

def Orthocenter(A,B,C):
    points = np.array([A,B,C])
    a = v.metric(B,C)
    b = v.metric(A,C)
    c = v.metric(A,B)
    abmc = a**2+b**2-c**2
    camb = c**2+a**2-b**2
    bcma = b**2+c**2-a**2
    alpha = abmc*camb
    beta = bcma*abmc
    gamma = camb*bcma
    s = 1.0*(alpha + beta + gamma)
    epsilon = 1e-8
    alpha /= (s+epsilon)
    beta /= (s+epsilon)
    gamma /= (s+epsilon)
    pt = points[0]*alpha + points[1]*beta + points[2]*gamma
    return pt
