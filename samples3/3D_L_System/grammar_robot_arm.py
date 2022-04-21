import linked_system as lsm
import graph as gra

import numpy as np
from copy import deepcopy

N0 = 16 # fixed based on linked_system

def I(n):
    return np.identity(n)

def T_n(n):
    theta = 360.*n/N0
    return theta

def T_th(theta):
    n = int(round(theta*N0/360.))
    return n

def T_ja(ja):
    L = []
    for tup in ja:
        nx,ny,nz = tup
        L = L + [T_n(nx),T_n(ny),T_n(nz)]
    return L

def T_L(L):
    n = len(L)
    m = int(n/3)
    ja = []
    for i in range(m):
        tup = L[3*i:3*(i+1)]
        thetax,thetay,thetaz = tup
        nx = T_th(thetax)
        ny = T_th(thetay)
        nz = T_th(thetaz)
        ja.append((nx,ny,nz))
    return ja

class RobotArm:
    def __init__(self,
                 s_sys, joint_angles,
                 subj = "",obj="a"):
        self.subj = subj
        self.obj = obj
        self.s_sys = s_sys
        self.ja = deepcopy(joint_angles)
        self.Theta = T_ja(joint_angles)
        self._s = lsm.PathSystem(self.s_sys,
                    self.ja)
        return
    def get_ja(self):
        self.ja = T_L(self.Theta)
        return self.ja
    def get_s(self):
        self._s = lsm.PathSystem(self.s_sys,
                    self.get_ja())
        return self._s
    def p(self, Theta, flag=True):
        ja = T_L(Theta)
        v_s = lsm.PathSystem(self.s_sys,
                    ja)
        S = lsm.Sentence(s=self.subj,v=v_s,
                o=self.obj,verbose=False)
        ss0 = str(S)
        t0,q0,pt_c,q_c = lsm.Shape0(ss0,flag)
        return pt_c[-1]
    def Start(self, flag=True):
        pt = self.p(self.Theta, flag)
        return pt
    def Jacobian(self,x0):
        N = len(self.Theta)
        M = 3
        V = I(N)
        h = 360./N0
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
    def dTheta(self,goal):
        start = self.Start()
        dp = np.array(goal)-np.array(start)
        x0 = self.Theta
        Jinv = self.JacobianInv(x0)
        dx = list(np.einsum('ij,j->i',Jinv,dp))
        return dx
    def Graph(self,flag=True):
        ja = T_L(self.Theta)
        v_s = lsm.PathSystem(self.s_sys,
                    ja)
        S = lsm.Sentence(s=self.subj,v=v_s,
                o=self.obj,verbose=False)
        ss0 = str(S)
        t0,q0,pt_c,q_c = lsm.Shape0(ss0,flag)
        N = len(pt_c)
        G = gra.Pn(N)
        G['pts'] = deepcopy(pt_c)
        return G

def d(A,B):
    return np.linalg.norm(np.array(A)-np.array(B))

def clamp(x,lo,hi):
    return max(lo,min(x,hi))

def Reach(P,goal,flag=True):
    #https://en.wikipedia.org/wiki/Programmable_Universal_Machine_for_Assembly#
    N = 10
    for i in range(N):
        si = P.get_s()
        print(i,si)
        #print N
        Theta = deepcopy(P.Theta)
        start = P.Start(flag)
        t = 0.35 # 0.05
        alpha = 0.14 # 0.04
        goal2 = list(np.array(start)*(1-t)+np.array(goal)*t)
        dtheta = P.dTheta(goal)
        Theta = list(np.array(Theta)+alpha*np.array(dtheta))
        P.Theta = deepcopy(Theta)
        near = P.Graph(flag)['pts'][-1]
        d0 = d(goal,near)
        #print i,"d(goal,current) = ",d0
        if d0 < 5:
            flag = True
            break
        else:
            flag = False
    return P,flag

def SetGoal(P,Theta,flag):
    Theta0 = deepcopy(P.Theta)
    P.Theta = deepcopy(Theta)
    start = P.Graph(flag)['pts'][-1]
    P.Theta = Theta0
    return start

