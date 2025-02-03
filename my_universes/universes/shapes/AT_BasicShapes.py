from .common import affine as aff
from . import alg_topo as topo

import numpy as np
from copy import deepcopy

from math import cos,sin,pi,atan2,sqrt,exp

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

def copy_graph(G):
    G2 = {}
    K = list(G.keys())
    for key in K:
        G2[key] = deepcopy(G[key])
    return G2

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

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

def create_sphere(r,ns=30,nt=30,path=None):
    def f(s,t):
        # r is in [0,oo)
        theta = pi*s # theta in [0,pi]
        phi = 2*pi*t # phi is in [0,2*pi)
        x = r*sin(theta)*cos(phi)
        y = r*sin(theta)*sin(phi)
        z = r*cos(theta)
        pt = [x,y,z]
        return pt
    S = np.linspace(1/ns,1,ns)
    T = np.linspace(1/nt,1,nt)

    if path is None:
        path2 = []
    cross_sections = []

    for i in range(len(S)):
        s = float(S[i])
        cross_section = list(map(lambda t: f(s,t), T))
        C = aff.Center(cross_section)
        cross_sections.append(cross_section)

    for i in range(len(S)):
        s = S[i]
        x,y,z = aff.Center([f(s,t) for t in T])
        x = float(x)
        y = float(y)
        z = float(z)
        pt_axis = [x,y,z]
        if path is None:
            path2.append(pt_axis)

    G = topo.AT_Cylinder(path2, cross_sections,
        bcap=True,ecap=True,closed=False)
    return G


def create_cylinder(rho,h,ns=30,nt=30,path=None):
    def f(s,t):
        # rho is in [0,oo)
        phi = 2*pi*t # phi is in [0,2*pi)
        x = rho*cos(phi)
        y = rho*sin(phi)
        z = (h/2)*(2*s-1)
        pt = [x,y,z]
        return pt
    S = np.linspace(0,1,ns)
    T = np.linspace(0,1,nt)

    if path is None:
        path2 = []
    cross_sections = []

    for i in range(len(S)):
        s = float(S[i])
        cross_section = list(map(lambda t: f(s,t), T))
        cross_section.reverse() # needs to reverse
        C = aff.Center(cross_section)

        cross_sections.append(cross_section)

    for i in range(len(S)):
        s = S[i]
        x,y,z = aff.Center([f(s,t) for t in T])
        x = float(x)
        y = float(y)
        z = float(z)
        pt_axis = [x,y,z]
        if path is None:
            path2.append(pt_axis)
        
    G = topo.AT_Cylinder(path2, cross_sections,
        bcap=True,ecap=True,closed=False)
    return G
