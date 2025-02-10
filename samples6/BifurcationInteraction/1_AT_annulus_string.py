import sys
sys.path.append(\
    r"C:/Users/jerry/Desktop/_Art/my_universes")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as bs
import universes.volume_of_OBJ as voo
import universes.transform_shape as ts
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.common.vectors as vec
import universes.shapes.common.CoordSystem as cs
import universes.shapes.common.human_doll as hd
import universes.shapes.common.graph as gra
import universes.shapes.alg_topo as topo
import universes.shapes.AT_BasicShapes as atbs
import universes.canvas2d.graphics_cv as racg
import universes.shapes.common.triangulate_polygon as tpo

import scipy.spatial as ss
import numpy as np
from functools import reduce
from copy import deepcopy
import time
import random

from math import cos,sin,pi,atan2,sqrt,exp,comb

seed0 = 12345
random.seed(seed0)

Sce = so.Scene()

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

def copy_graph(G):
    G2 = {}
    K = list(G.keys())
    for key in K:
        G2[key] = deepcopy(G[key])
    return G2

def bezier_curve(pts):
    pts = np.array(pts)
    n = len(pts)-1
    def f(t):
        s = np.array(pts[0])*0
        for i in range(n+1):
            val = comb(n,i)*\
                  (1-t)**(n-i)*t**i*\
                  pts[i]
            s = s + val
        s = list(map(float,list(s)))
        return s
    return f

def create_strings(ds,n,k,bezier_pts,
        a_outer=300,b_outer=300,r_hole=30):

    ###############################################
    # Create G0
    #
    
    k_min = 1
    k_max = 7
    k = min(k_max,max(k_min,k))
    assert(r_hole < a_outer)
    assert(r_hole < b_outer)
    a1 = a_outer
    b1 = b_outer
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
    if k == 1:
        a1 = 0
        b1 = 0
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
    #
    ###############################################

    ###############################################
    # Create sectionf(t)
    #
    def cross_section(P0,P1,t):
        assert(len(P0)==len(P1))
        P2 = []
        for i in range(len(P0)):
            A = P0[i]
            B = P1[i]
            C = lerp(A,B,t)
            P2.append(C)
        return P2
    sectionf = lambda s: cross_section(P0,P1,s)
    #
    ###############################################

    ###############################################
    # create position vector xf(t)
    #
    xf = lambda s: bezier_curve(bezier_pts)(s)
    ###############################################

    ###############################################
    particle = topo.String_Particle(G0,xf,sectionf,ds)
    return particle

BIGDATA = r"./"
fn_save = BIGDATA+"AT_annulus3.obj"
g = open(fn_save,'w')
thickness = 2

M = 30
pts = []
O = [0,0,0]
v = [0,1,0]
v_mag = np.linalg.norm(v)
v_scale = 30
v = np.array(v)/v_mag
v = list(map(float,list(v)))
for i in range(M):
    # limit curvature
    a = 40
    rx = random.uniform(-a,a)
    ry = random.uniform(-a,a)
    rz = 0
    R_i = [rx,ry,rz]
    q_i = cog.FromEuler(*R_i)
    v2 = aff.Rotate([v],q_i,align=False)[0]
    pt = np.array(O) + v_scale*np.array(v2)
    pt = list(map(float,list(pt)))
    pts.append(pt)
    O = pt
    v = v2
dt = 1/M
P = create_strings(dt,n=20,k=1,bezier_pts=pts,
        a_outer=30,b_outer=30,
        r_hole=30-thickness)
P.reset()
for i in range(M-2):
    P.propagate()
G = P.get_world_sheet(bcap=True,ecap=True)
Sce.add(G,"AT_annulus3","AT_annulus2.mtl","AT_annulus2")
Sce.select("AT_annulus3")
T = [0,0,0]
R = [0,0,0]
S = [1,1,1]
Sce.transform(T,R,S)
txt = Sce.get_txt()
g.write(txt)
g.close()
