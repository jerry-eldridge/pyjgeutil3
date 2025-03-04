from .common import affine as aff
from .common import graph as gra
from . import alg_topo as topo
from .common import triangulate_polygon as tpo

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

def create_ellipsoid(rx,ry,rz,ns=30,nt=30,path=None):
    def f(s,t):
        # r is in [0,oo)
        theta = pi*s # theta in [0,pi]
        phi = 2*pi*t # phi is in [0,2*pi)
        x = rx*sin(theta)*cos(phi)
        y = ry*sin(theta)*sin(phi)
        z = rz*cos(theta)
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

def create_sphere(r,ns=30,nt=30,path=None):
    G = create_ellipsoid(r,r,r,ns,nt,path)
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

def create_torus(r1,r2,ns=30,nt=30,path=None):
##    print(f"Note: create_torus is experimental")
##    print(f"as currently the ends of cylinder are")
##    print(f"not glued together.")
    def f(s,t):
        # rho is in [0,oo)
        phi = 2*pi*t # phi is in [0,2*pi)
        x = r1*cos(phi)
        y = r1*sin(phi)
        z = 2*pi*r2*s
        pt = [x,y,z]
        return pt
    S = np.linspace(0,1+2/ns,ns)
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
        theta = 2*pi*s
        x = r2*cos(theta)
        y = r2*sin(theta)
        z = 0
        pt_axis = [x,y,z]
        if path is None:
            path2.append(pt_axis)
        
    G = topo.AT_Cylinder(path2, cross_sections,
        bcap=False,ecap=False,closed=True)
    return G

def create_AT_annulus(n,
        a_outer=100,b_outer=200,a_inner=50,b_inner=100,height=100):
    a1 = a_outer
    b1 = b_outer
    a2 = a_inner
    b2 = b_inner
    h = height
    n1 = n
    n2 = n
    m1 = n1+1
    pts1 = []
    for i in range(m1):
        t = i/(m1-1)
        x = a1*cos(2*pi*t)
        y = b1*sin(2*pi*t)
        pt = [x,0,y]
        pts1.append(pt)
    G1 = gra.Cn(m1)

    m2 = n2+1
    pts2 = []
    for i in range(m2):
        t = i/(m2-1)
        x = a2*cos(2*pi*t)
        y = b2*sin(2*pi*t)
        pt = [x,0,y]
        pts2.append(pt)
    G2 = gra.Cn(m2)
    
    P0 = pts1 + pts2
    P1 = P0
    
    G0 = gra.GraphUnion(G1,G2)
    Q_pts1 = [[pt[0],pt[2]] for pt in pts1]
    Q_pts2 = [[pt[0],pt[2]] for pt in pts2]
    Q = [(Q_pts1,1),(Q_pts2,-1)]
    F,F_pts = tpo.triangulate_polygons(Q)
    G0['F'] = deepcopy(F)
    G0['pts'] = deepcopy(F_pts)
    G0['OR'] = [1]*len(G1['E'])+[-1]*len(G2['E'])

    def cross_section(P0,P1,t):
        assert(len(P0)==len(P1))
        P2 = []
        for i in range(len(P0)):
            A = P0[i]
            B = P1[i]
            C = lerp(A,B,t)
            P2.append(C)
        return P2

    smin = 0
    smax = 1
    ds = .1
    s = smin
    cross_sections = []
    path = []
    while s < smax+ds:
        cross_section_s = cross_section(P0,P1,s)
        cross_sections.append(cross_section_s)
        s = s + ds
        pt = [0,h*s,0]
        path.append(pt)
        s = s + ds
    G3 = topo.AT_Graph_Cylinder(path,G0,cross_sections,
                bcap = True, ecap = True, closed=False)
    return G3

def create_AT_annulus_holes(n,k,
        a_outer=300,b_outer=300,r_hole=30,height=100):
    k_min = 2
    k_max = 7
    k = min(k_max,max(k_min,k))
    assert(r_hole < a_outer)
    assert(r_hole < b_outer)
    a1 = a_outer
    b1 = b_outer
    h = height
    n1 = n
    m1 = n1+1
    pts1 = []
    for i in range(m1):
        t = i/(m1-1)
        x = a1*cos(2*pi*t)
        z = b1*sin(2*pi*t)
        pt = [x,0,z]
        pts1.append(pt)
    O = np.mean(pts1,axis=0)
    O = list(map(float,list(O)))
    G1 = gra.Cn(m1)
    P0 = deepcopy(pts1)
    G0 = copy_graph(G1)
    Q_pts1 = [[pt[0],pt[2]] for pt in pts1]
    Q = [(Q_pts1,1)]
    OR = [1]*len(G1['E'])
    r_hole = min(r_hole,a1/10)
    for j in range(k):
        m2 = 10
        pts_k = []
        t2 = 2*pi*j/k
        cx = 0.5*a1*cos(t2) - O[0]
        cz = 0.5*b1*sin(t2) - O[2]
        for i in range(m2):
            t = i/(m2-1)
            x = r_hole*cos(2*pi*t)+cx
            y = 0
            z = r_hole*sin(2*pi*t)+cz
            pt = [x,y,z]
            pts_k.append(pt)
        G_k = gra.Cn(m2)
        P0 = P0 + pts_k
        G0 = gra.GraphUnion(G0,G_k)
        Q_pts_k = [[pt[0],pt[2]] for pt in \
                   pts_k]
        Q = Q + [(Q_pts_k,-1)]
        OR = OR+[-1]*len(G_k['E'])
        
    P1 = P0
    F = []
    F,F_pts = tpo.triangulate_polygons(Q,t=0.001)
    G0['F'] = deepcopy(F)
    G0['pts'] = deepcopy(P0)
    G0['OR'] = deepcopy(OR)

    def cross_section(P0,P1,t):
        assert(len(P0)==len(P1))
        P2 = []
        for i in range(len(P0)):
            A = P0[i]
            B = P1[i]
            C = lerp(A,B,t)
            P2.append(C)
        return P2

    smin = 0
    smax = 1
    ds = .1
    s = smin
    cross_sections = []
    path = []
    while s < smax+ds:
        cross_section_s = cross_section(P0,P1,s)
        cross_sections.append(cross_section_s)
        s = s + ds
        pt = [0,h*s,0]
        path.append(pt)
        s = s + ds
    G3 = topo.AT_Graph_Cylinder(path,G0,cross_sections,
                bcap = True, ecap = True, closed=False)
    return G3
