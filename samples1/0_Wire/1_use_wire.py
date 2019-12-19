import affine as aff
import extrusion as ext
import wire as wi

import numpy as np

from copy import deepcopy

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

######################### SCENE 1 BEGIN
G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []

# Ellipsoid Object
r = 3 # radius of cross section
ppath = [
    [0,0,0],
    [-10,20,0],
    [20,30,10],
    [30,10,20],
    [35,5,30],
    [40,10,20],
    [50,30,10],
    [70,20,20],
    [60,0,30],
    [55,130,40],
    [45,120,50],
    [35,110,45],
    [25,110,30],
    [20,110,-25],
    [10,130,-15],
    [10,110,0]    
    ]
t = [-80.,0.,50.]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
# n is length
H0 = wi.Wire(r,ppath,t,q,s,m=10,n=100)
Gs = ext.Append(Gs,H0)
G = ext.GraphUnionS(G,H0)
#################################

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"Wire1.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"Wire1.obj")
