import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")

import vectors as v
import QuaternionGroup as HH
import graph as g

import numpy as np
from copy import deepcopy
import random

from math import pi,fmod,sin,cos

def Transform3(shape, T):
    shape4 = map(lambda pt: pt+[1], shape)
    SHAPE4 = map(lambda pt: list(np.einsum('ij,j->i',T,pt)), shape4)
    SHAPE = map(lambda pt: list(1.0*np.array(pt)/pt[3]),SHAPE4)
    SHAPE = map(lambda pt: pt[:3], SHAPE)
    return SHAPE

def Rotate(shape,q,align=True):
    R = q.rotation_matrix()
    SHAPE = Transform(shape,R)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

def Translate(shape,tx,ty,tz,align=True):
    T = v.translation_matrix(tx, ty, tz)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

def Scale(shape,sx,sy,sz,align=True):
    T = v.scale_matrix(sx, sy, sz)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

def PlotGraph(gr,G,color=[0,0,0]):
    pts = deepcopy(G['pts'])
    pts = map(lambda pt: pt[:2],pts)
    n = len(pts)
##    for v in G['V']:
##        gr.Point(pts[v],color)
    for e in G['E']:
        u,v = e
        gr.Line(pts[u],pts[v],color)
    return

def MapPoint(T,X):
    Y = list(np.einsum('ij,j->i',T,X+[1]))[:-1]
    return Y

def Mul(A,B):
    C = np.einsum('ij,jk->ik',A,B)
    return C
def I(n):
    return np.identity(n)

class Puma560:
    def __init__(S,pt,A,Theta):
        #print "Creating Puma560 with 5 arms and 6 angles"
        assert(len(A) == 6)
        assert(len(Theta) == 6)
        S.pt = pt
        S.A = A # d1,
        S.Theta = Theta
        return
    # http://www.tareksobh.com/html/proj/damir/theory.html
    def Transforms(S):
        T = []
        Ti = v.translation_matrix(S.A[0],S.A[0],S.A[1])
        Ri = v.rotation_matrix(S.Theta[0]+90, 0,1,0)
        T.append(Mul(Ti,Ri))

        Ti = v.translation_matrix(S.A[2],S.A[2],S.A[3])
        Ri = v.rotation_matrix(S.Theta[1],0,0,1)
        T.append(Mul(Ti,Ri))

        Ti = v.translation_matrix(S.A[4],S.A[4],S.A[5])
        Ri = v.rotation_matrix(S.Theta[2]-90, 0,1,0)
        T.append(Mul(Ti,Ri))

        Ri = v.rotation_matrix(S.Theta[3]+90, 0,1,0)
        T.append(Ri)

        Ri = v.rotation_matrix(S.Theta[4]-90, 0,1,0)
        T.append(Ri)

        Ri = v.rotation_matrix(S.Theta[5], 0,0,1)
        T.append(Ri)

        T.reverse()
        return T
    def Graph(S):
        A = S.pt
        Tr = S.Transforms()
        N = len(Tr)
        G = g.Pn(N)
        T = I(4)
        G['pts'] = []
        for i in range(N):
            Ti = Tr[i]
            T = Mul(T,Ti)
            B = list(np.array(A)+np.array(MapPoint(T,[0,0,0])))
            G['pts'].append(B)
        return G
##    def Display(S,gr,ms=-1,color=[0,0,0]):
##        G = P.Graph()
##        gr.Clear()
##        PlotGraph(gr,G,color)
##        ch = gr.Show("result",ms)
##        return ch
    def p(self,Theta):
        Theta0 = deepcopy(self.Theta)
        self.Theta = deepcopy(Theta)
        G = self.Graph()
        pt = G['pts'][-1]
        self.Theta = Theta0
        return pt
    def Jacobian(self,x0):
        N = 6
        M = 3
        V = I(N)
        h = 0.5
        p0 = np.array(self.p(x0))
        def j(k):
            x1 = list(np.array(x0)+V[k]*h)
            p1 = np.array(self.p(x1))
            p = 1.0*(p1-p0)/h
            return p
        J = np.zeros((M,N))
        for k in range(N):
            J[:,k] = j(k)
        return J
    def JacobianInv(self,x0):
        J = self.Jacobian(x0)
        Jinv = np.linalg.pinv(J)
        return Jinv
    def Start(self):
        x0 = self.Theta
        return self.p(x0)
    def dTheta(self,goal):
        start = self.Start()
        dp = np.array(goal)-np.array(start)
        x0 = self.Theta
        Jinv = self.JacobianInv(x0)
        dx = list(np.einsum('ij,j->i',Jinv,dp))
        return dx

def d(A,B):
    return np.linalg.norm(np.array(A)-np.array(B))

def clamp(x,lo,hi):
    return max(lo,min(x,hi))

def Reach(P,goal):
    #https://en.wikipedia.org/wiki/Programmable_Universal_Machine_for_Assembly#
    ThetaMax = [360]*6#[320,266,284,200,280,532]
    N = 10
    for i in range(N):
        #print N
        Theta = deepcopy(P.Theta)
        start = P.Start()
        t = 0.35 # 0.05
        alpha = 0.14 # 0.04
        goal2 = list(np.array(start)*(1-t)+np.array(goal)*t)
        dtheta = P.dTheta(goal)
        Theta = list(np.array(Theta)+alpha*np.array(dtheta))
        Theta = map(lambda i: Theta[i]%ThetaMax[i],range(len(Theta)))
        P.Theta = deepcopy(Theta)
        near = P.Graph()['pts'][-1]
        d0 = d(goal,near)
        #print i,"d(goal,current) = ",d0
        if d0 < 0.1:
            flag = True
            break
        else:
            flag = False
    return P,flag

def SetGoal(P,Theta):
    Theta0 = deepcopy(P.Theta)
    P.Theta = deepcopy(Theta)
    start = P.Graph()['pts'][-1]
    P.Theta = Theta0
    return start

Theta = [0,0,0,0,0,0]
s = 600
P = Puma560([0,0,0],[.12*s,.67*s,.4318*s,.24*s,.4318*s,0.15005*s],Theta)
