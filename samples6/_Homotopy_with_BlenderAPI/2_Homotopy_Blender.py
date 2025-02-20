import sys
sys.path.insert(0,"C:/Users/jerry/Desktop/Blender_Homotopy/")

import blender_create_shape as bcs
import mini_my_universes as mmu

from copy import deepcopy
import numpy as np
from math import exp,cos,sin,pi

create_shape = bcs.create_shape

import bpy
import bmesh

#######################################################################################
# Jerry G Eldridge (JGE), from bean.py
#
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
        C = mmu.Center(cross_section)
        x = x1(s)
        y = x2(s)
        z = x3(s)
        pt_axis = [x,y,z] # [Edwards and Penney]
        if path is None:
            path2.append(pt_axis)
        cross_sections.append(cross_section)
    G = mmu.AT_Cylinder(path2, cross_sections,
        bcap=True,ecap=True,closed=False)
    return G

#
########################################################################

def Degrees2Radians(x):
    val = x*pi/180
    return val

def Euler2Rotation(R):
    R2 = tuple(list(map(Degrees2Radians, list(R))))
    return R2

sPointLight1 = bpy.ops.object.light_add(type='POINT',radius=1,align='WORLD',
    location=(-1.389,-1.2266,-0.22481), scale=(1,1,1))
bpy.context.object.data.energy = 1000

G = create_bean(ns=70,nt=20,
        r_add=0.75,freq=5,path=None)


T = [0,0,0]
R = [0,0,0]
S = [.1,.1,.1]
RGBA = [0.094, 0.49, 0.212, 1]

N1 = 5 # create N1 x N2 worms
N2 = 5
Objs = []
for i in range(N1):
    row = []
    for j in range(N2):
        G_ij = G
        name = f"bean_{i}_{j}"
        mesh_name = f"M_{name}"
        object_name = f"O_{name}"
        V = deepcopy(G['pts'])
        E = deepcopy(G['E'])
        F = deepcopy(G['F'])  
        T = [0.7*(i-N1/2), 0, 0.7*(j-N2/2)]
        R = [15*i,0,35*j]
        S = [.03, .03, .03]
        O_ij = create_shape(mesh_name,object_name, V, E, F, T, R, S, RGBA)
        row.append(O_ij)
    Objs.append(row)


T = [0,1.6,0]    
R = [0,0,0]
S = [5,0.050,5]
sA_Wall = bpy.ops.mesh.primitive_cube_add(size=2,enter_editmode=False,
        align='WORLD',location=tuple(T),scale=tuple(S),rotation=Euler2Rotation(R))
bpy.context.object.name = "A_Wall"

T = [0,-9,0]
R = [90,0,0]
S = [1,1,1]
sA_Cam = bpy.ops.object.camera_add(enter_editmode=False,
         align='WORLD', location = tuple(T), rotation=Euler2Rotation(R), scale=tuple(S))
bpy.context.object.name = "A_Cam"

N = 10
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 100

for i in range(N):
    bpy.context.scene.frame_current = 10*i
    bpy.ops.anim.keyframe_insert_by_name(type="Location")
    
