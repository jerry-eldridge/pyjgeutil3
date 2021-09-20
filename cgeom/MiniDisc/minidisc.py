import random
import numpy as np

from math import sqrt

from copy import deepcopy

lerp = lambda A,B,t : list((1-t)*np.array(A)+t*np.array(B))
dist = lambda A,B: np.linalg.norm(np.array(A)-np.array(B))

# Ball about x of radius r
class Disc:
    def __init__(self,x,r):
        self.x = x
        self.r = r
    def member(self,y):
        flag = dist(self.x,y) < self.r
        return flag

def Calc2Pt(p1,p2):
    x = lerp(p1,p2,0.5)
    r = dist(p1,p2)/2.0
    D_2 = Disc(x,r)
    return D_2

# https://en.wikipedia.org/wiki/Circumscribed_circle
def Circumcenter(A,B,C):
    points = np.array([A,B,C])
    a = dist(B,C)
    b = dist(A,C)
    c = dist(A,B)
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

####################################################
# [1] Computational Geometry, de Berg et al, 2008,
# Springer

# Given a list of points P, this finds the smallest
# enclosing disc D for the points P.
def MiniDisc(Q):
    P = deepcopy(Q)
    random.shuffle(P)
    assert(len(P) >= 2)
    n = len(P)
    D_prev = Calc2Pt(P[0],P[1])
    for i in range(2,n):
        if D_prev.member(P[i]):
            D_next = D_prev
        else:
            D_next = MiniDiscWithPoint(P[:i],P[i])
        D_prev = D_next
    return D_next

def MiniDiscWithPoint(Q,q):
    P = deepcopy(Q)
    random.shuffle(P)
    n = len(P)
    D_prev = Calc2Pt(q,P[0])
    for j in range(1,n):
        if D_prev.member(P[j]):
            D_next = D_prev
        else:
            D_next = MiniDiscWith2Points(P[:j],P[j],q)
        D_prev = D_next
    return D_next

def MiniDiscWith2Points(Q,q1,q2):
    P = deepcopy(Q)
    random.shuffle(P)
    n = len(P)
    D_prev = Calc2Pt(q1,q2)
    for k in range(0,n):
        if D_prev.member(P[k]):
            D_next = D_prev
        else:
            x = Circumcenter(q1,q2,P[k])
            r = dist(x,q1)
            D_next = Disc(x,r)
        D_prev = D_next
    return D_next

#####################################################
