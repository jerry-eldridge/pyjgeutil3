import sys
sys.path.append(r"./my_universes")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as bs
import universes.volume_of_OBJ as voo
from copy import deepcopy
import universes.transform_shape as ts
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.common.vectors as vec
import universes.shapes.common.CoordSystem as cs
import universes.shapes.common.human_doll as hd
from math import pi
import numpy as np
import time
from functools import reduce

import os

from math import sin,cos,pi

##       |y axis
##       |
##       
##       o
##      ---
##       | CM (Center of Mass)
##      / \
##       ---------x axis
##      /O (Origin)
##     /
##    /z axis

## T = [tx,ty,tz], S = [sx,sy,sz], R = [rx,ry,rz]

def pose(P,e,R):
    P.pose(e,idx=0,R=R)
    return

def create_special_cylinder(radius,height,N=10):
    G_cross_section = ext.g.Cn(N)
    pts = []
    t = 0
    dt = 2*pi/(N-1)
    r = radius
    while t < 2*pi + dt:
        xx = r*cos(t)
        yy = 0
        zz = r*sin(t)
        pt = [xx,yy,zz]
        pts.append(pt)
        t = t + dt
    G_cross_section['pts'] = pts
    t = 0
    dt = .1
    path = []
    while t <= 1 + dt:
        pt = aff.lerpa([0,0,0],[0,height,0],t)
        path.append(pt)
        t = t + dt
    G = ext.Extrusion(G_cross_section,
            path,bcap=True,ecap=True,
            closed=False)
    return G

def create_sphere(radius):
    t = [0,0,0]
    s = [1,1,1]
    q = cog.rotation_quaternion(0,0,0,1)
    G = bs.Sphere(radius,t,q,s,m=10,n=10)
    return G

def display(P):
    P.display(sys.stdout)
    BIGDATA = r"./"

    fn_save = BIGDATA+"bodysystem_3d.obj"
    g = open(fn_save,'w')
    Sce = so.Scene()
    # Create and Position floor
    G = ps.create_cube()
    Sce.add(G,"floor","floor.mtl","floor_mat")
    Sce.select("floor")
    T = [0, -35, 0.0]
    R = [0,0,0]
    S = [2, 0.01, 2]
    Sce.transform(T,R,S)

    segments = P.get_segments()
    K = list(segments.keys())
    for key in K:
        name,idx = key
        proximal,mid,distal,x_cm = segments[key]
        v = np.array(distal)-np.array(proximal)
        v_mag = np.linalg.norm(v)
        v = v/v_mag
        axis2 = list(map(float,list(v)))
        axis1 = [0,1,0]
        q = ext.AimAxis(axis1,axis2)
        R = q.ToEuler()
        radius = 1
        height = v_mag
        G = create_special_cylinder(radius,height)
        name_ij = f"{key}_cyl"
        Sce.add(G,name_ij,"floor.mtl","floor_mat")
        Sce.select(name_ij)
        Sce.transform(T=mid,R=R,S=[1,1,1])
        
        G = create_sphere(radius+0.5)
        name_ij = f"{key}_sph_A"
        Sce.add(G,name_ij,"A.mtl","A")
        Sce.select(name_ij)
        Sce.transform(T=proximal,R=[0,0,0],S=[1,1,1])
        
        G = create_sphere(radius+0.5)
        name_ij = f"{key}_sph_M"
        Sce.add(G,name_ij,"M.mtl","M")
        Sce.select(name_ij)
        Sce.transform(T=mid,R=[0,0,0],S=[1,1,1])

        G = create_sphere(radius+0.5)
        name_ij = f"{key}_sph_B"
        Sce.add(G,name_ij,"B.mtl","B")
        Sce.select(name_ij)
        Sce.transform(T=distal,R=[0,0,0],S=[1,1,1])

    G = create_sphere(radius+1)
    name_ij = f"{key}_sph_CM"
    Sce.add(G,name_ij,"CM.mtl","CM")
    Sce.select(name_ij)
    Sce.transform(T=P.center_of_mass(),
                  R=[0,0,0],S=[1,1,1])

    txt = Sce.get_txt()
    g.write(txt)
    g.close()
    return

BIGDATA = r"./"

        
O = [0,0,0] # standing on ground
P = hd.HumanDoll(O,weight_lbs=195,height_in=5*12+8)
P.build()

R_global = {}

def bend(P,joint,typ="extensor",theta=0.0):
    global R_global
    if typ == "extensor":
        sgn = -1
    elif typ == "flexor":
        sgn = 1
    L = None
    R = None
    if joint == "L knee":
        R = [sgn*theta,0,0]
        L = ["L leg","L foot"]
    elif joint == "R knee":
        R = [sgn*theta,0,0]
        L = ["R leg","R foot"]
    elif joint == "L ankle":
        R = [-sgn*theta,0,0]
        L = ["L foot","L foot effector"]
    elif joint == "R ankle":
        R = [sgn*theta,0,0]
        L = ["R foot","R foot effector"]
    elif joint == "L hip":
        L = ["L thigh","L leg"]
        R = [-sgn*theta,0,0]
    elif joint == "R hip":
        L = ["R thigh","R leg"]
        R = [-sgn*theta,0,0]
    elif joint == "neck":
        L = ["neck","head"]
        R = [-sgn*theta,0,0]
    elif joint == "torso":
        L = ["trunk","neck"]
        R = [sgn*theta,0,0]
    elif joint == "L elbow":
        L = ["L arm","L hand"]
        R = [0,-sgn*theta,0]
    elif joint == "R elbow":
        L = ["R arm","R hand"]
        R = [0,sgn*theta,0]
    elif joint == "L shoulder":
        L = ["L upper arm","L arm"]
        R = [0,-sgn*theta,0]
    elif joint == "R shoulder":
        L = ["R upper arm","R arm"]
        R = [0,sgn*theta,0]
    elif joint == "L wrist":
        L = ["L hand","L hand effector"]
        R = [0,-sgn*theta,0]
    elif joint == "R wrist":
        L = ["R hand","R hand effector"]
        R = [0,sgn*theta,0]        
    if L is not None and R is not None:
        u = L[0]
        done = False
        while not done:
            for e in P.E:
                q2 = cog.FromEuler(*R)
                if e[0] == u:
                    if u in R_global.keys():
                        q1 = cog.FromEuler(\
                        *R_global[u])
                        q2 = q2 * q1
                    R_global[u] = q2.ToEuler()
                    P.pose(e,idx=0,R=R_global[u])
                    u = e[1]
                else:
                    done = True
    return

bend(P,"L ankle","extensor",30.0)
bend(P,"torso","flexor",50.0)
bend(P,"L shoulder","flexor",40.0)
bend(P,"L elbow","flexor",30.0)
bend(P,"L wrist","flexor",50.0)
bend(P,"L knee","flexor",50.0)
bend(P,"L hip","flexor",50.0)

# bend truck forward rotating on x-axis by 10 degrees
#pose(P,["trunk","neck"],R=[45,0,0])

display(P)
