import sys
sys.path.append(\
    r"C:/_Art/my_universes")
import universes
from copy import deepcopy
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.alg_topo as topo
import numpy as np

from math import sin,cos,pi,exp

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))


def create_bean(ns=30,nt=30,r_add = 0.25,freq=10,path=None):
    def f(s,t):
        w = 2*s - 1
        w = 2*w
        r = exp(-w**2/2)
        r2 = r*(1+r_add*(sin(2*pi*freq*s)+1)/2.0)
        x,z = [r2*cos(2*pi*t),r2*sin(2*pi*t)]
        pt = [x,0,z]
        return pt
    S = np.linspace(0,1,ns)
    T = np.linspace(0,1,nt)

    if path is None:
        path2 = []
    cross_sections = []
    a = 3
    b = 20
    omega = 2*pi
    def x1(t):
        x = a*cos(omega*t)
        return x
    def x2(t):
        y = a*sin(omega*t)
        return y
    def x3(t):
        z = b*t
        return z
    for i in range(len(S)):
        s = S[i]
        cross_section = list(map(lambda t: f(s,t), T))
        C = aff.Center(cross_section)
        x = x1(s)
        y = x2(s)
        z = x3(s)
        pt_axis = [x,y,z] # [Edwards and Penney]
        if path is None:
            path2.append(pt_axis)
        cross_sections.append(cross_section)
    G = topo.AT_Cylinder(path2, cross_sections,
        bcap=True,ecap=True,closed=False)
    return G




