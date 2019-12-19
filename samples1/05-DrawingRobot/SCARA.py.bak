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

def q2R(q):
    q = HH.Quaternion(q)
    R3 = q.rotation_matrix()
    R = np.identity(4)
    R[:3,:3] = R3
    return R

def theta2q(theta):
    a = np.linalg.norm(theta)
    degrees = a*180/pi
    epsilon = 1e-8
    if abs(a) > epsilon:
        axis = np.array(theta)/a
    else:
        axis = np.array([0,0,1])
        degrees = 0
    q = HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    return q

def Center(pts,flag2d = False):
    PTS = map(lambda pt: np.array(pt), pts)
    X = map(lambda pt: pt[0], PTS)
    Y = map(lambda pt: pt[1], PTS)
    if flag2d:
        C = [np.mean(X),np.mean(Y)]
    else:
        Z = map(lambda pt: pt[2], PTS)
        C = [np.mean(X),np.mean(Y),np.mean(Z)]
    return C
class RobotArm:
    def __init__(S,pt,L,Theta):
        S.pt = pt
        S.L = L
        S.Theta = Theta
        S.pts = None
        return
    def Transforms(S):
        T = []

        h,l1,l2 = S.L
        theta1,theta2,theta3,d = S.Theta

        Ti = v.translation_matrix(0,0,h)
        T.append(Ti)

        T1 = v.translation_matrix(l1,0,0)
        T2 = v.rotation_matrix(theta1,0,0,1)
        Ti = Mul(T2,T1)
        T.append(Ti)

        T1 = v.translation_matrix(l2,0,0)
        T2 = v.rotation_matrix(theta2,0,0,1)
        Ti = Mul(T2,T1)
        T.append(Ti)

        T1 = v.translation_matrix(0,0,-d)
        T2 = v.rotation_matrix(theta3,0,0,1)
        Ti = Mul(T2,T1)
        T.append(Ti)

        T.reverse()
        return T
    def Graph(S):
        A = S.pt
        Tr = S.Transforms()
        N = len(Tr)
        G = g.Pn(N+1)
        T = I(4)
        G['pts'] = [A]
        for i in range(N):
            Ti = Tr[i]
            T = Mul(T,Ti)
            B = list(np.array(A)+np.array(MapPoint(T,[0,0,0])))
            G['pts'].append(B)
        return G
    def Display(S,gr,ms=-1,color=[0,0,0]):
        G = P.Graph()
        gr.Clear()
        PlotGraph(gr,G,color)
        ch = gr.Show("result",ms)
        return ch
    def p(S,Theta):
        pts0 = S.pts
        Theta0 = deepcopy(S.Theta)
        S.Theta = deepcopy(Theta)
        G = S.Graph()
        pt = G['pts'][-1]
        S.Theta = Theta0
        S.pts = pts0
        return pt
    def Jacobian(self,x0):
        N = len(self.Theta)
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
