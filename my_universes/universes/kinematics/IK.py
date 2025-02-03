from . import RobotArm as RA
from . import linkedpart as lp

import numpy as np
from math import acos,pi

def Angle(A,B,C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    V1 = A - B
    V2 = C - B
    v1 = np.linalg.norm(V1)
    v2 = np.linalg.norm(V2)
    theta = acos(np.inner(V1,V2)/(1.0*v1*v2))
    theta = theta*180/pi
    return theta

# assumes that other graph vertices are independent
# from the IK rig
class IK:
    def __init__(S,G,u,v):
        S.G = G
        S.u = u
        S.v = v
        S.path = lp.PathPart(G,u,v)
        S.linked = lp.LinkedPart(G,u,v)
        # assert that path from u to v
        # in graph is all the dependent vertices of
        # that part in the linked system. This requires
        # choosing u and v in graph such that that holds.
        assert(S.path == S.linked)
        S.L,S.Theta,S.ik = S.Build()
        return
    def Build(S):
        L = S.GetL()
        Theta = S.GetTheta()
        ik = RA.RobotArm(S.G['pts'][S.u],L,Theta)
        return L,Theta,ik
    def GetL(S):
        pts = [S.G['pts'][v] for v in S.path]
        L = []
        for i in range(len(pts)-1):
            val = RA.d(pts[i],pts[i+1])
            L.append(val)
        return L
    def GetTheta(S):
        pts = [S.G['pts'][v] for v in S.path]
        pts = [[0,1,0]]+pts
        Theta = [0]*len(S.GetL())
        for i in range(len(pts)-2):
            Theta[i] = Angle(pts[i],pts[i+1],pts[i+2])
        return Theta
    def Update(S):
        for i in range(len(S.path)):
            v = S.path[i]
            G = S.ik.Graph()
            S.G['pts'][v] = G['pts'][i]
        S.Build()
        return
    def Reach(S,goal):
        S.ik,flag = RA.Reach(S.ik,goal)
        S.Update()
        return

