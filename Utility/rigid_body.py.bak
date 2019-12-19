import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import line_intersection as li
import graph
import timer
import affine as aff

from math import cos,sin,pi,acos
import numpy as np
from copy import deepcopy

# Rigid Body Particle class
class Particle:
    def __init__(S,x,v,q,omega,m,I,dt):
        S.x = x
        S.v = v
        S.m = m
        S.I = I
        S.omega = omega
        S.dtheta = np.array([0,0,0])
        S.q = q
        S.dt = dt
    def Step(S,F,tau):
        a = F/(1.0*S.m)
        S.v = S.v + a*S.dt
        S.x = S.x + S.v*S.dt
        alpha = tau/(1.0*S.I)
        S.omega = S.omega + alpha*S.dt
        S.dtheta = S.omega*S.dt
        S.omega *= .8
        S.v *= .8
        q0 = aff.theta2q(S.dtheta)
        S.q *= q0
        return

# Circle graph is Cycle with Circular Points pts
def Circle(r,k):
    G = graph.Cn(k)
    C = [0,0,0]
    G = graph.CreateCircleGeometry(G,C[0],C[1],C[2],r)
    return G

# Rigid Body Object class
class Object:
    def __init__(S,k,x,q,dt):
        zero = np.array([0,0,0])
        # mass m
        S.m = 1
        # moment of inertia I ("angular mass")
        S.I = 100
        # animation time increment dt
        S.dt = dt
        # Center of Mass particle of Object at S.P.x
        # q is quaternion rotation for object set to S.P.q
        # v is velocity for Object
        # omega is "angular velocity" for object
        S.P = Particle(x=x,v=zero,q=q,omega=zero,m=S.m,I=S.I,dt=S.dt)
        # Use Regular Polygon Graph for Object with k sides
        # and radius r.
        S.r = 40
        S.G = Circle(S.r,k)
        return
    def pts(S):
        shape = deepcopy(S.G['pts'])
        C = aff.Center(shape)
        shape = aff.Translate(shape,-C[0],-C[1],-C[2])
        shape = aff.Rotate(shape,S.P.q)
        shape = aff.Translate(shape,S.P.x[0],S.P.x[1],S.P.x[2])
        return shape      
    def Step(S,F,tau):
        S.P.Step(F,tau)

class Impulse:
    def __init__(S,dur,F):
        S.tm = timer.Timer()
        S.flag = False
        S.F = F
        S.dur = dur
    def Start(S):
        S.tm.tic()
        S.flag = True
    def Stop(S):
        S.tm.tic()
        S.flag = False
    def Get(S):
        t = S.tm.toc()
        if S.flag:
            if t < S.dur:
                return S.F,t
            else:
                S.Stop()
                return S.F*0,t
        else:
            return S.F*0,t

def Intersect(line1,line2):
    A,B = line1
    C,D = line2
    flag,x,y = li.SegmentIntersect(
        A[0],A[1],
        B[0],B[1],
        C[0],C[1],
        D[0],D[1])
    E = [x,y]
    return flag,E

def Collide(G1, G2):
    L = []
    for e in G1['E']:
        A,B = map(lambda v: G1['pts'][v], e)
        for f in G2['E']:
            C,D = map(lambda v: G2['pts'][v],f)
            flag,E = Intersect([A,B],[C,D])
            if flag:
                L.append([e,f,E])
    return L
