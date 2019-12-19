import affine as aff
import extrusion as ext
import helix as he

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
r = 10 # radius of cross section
a = 10 # radius of helix, must be big enough
b = 5*a # pitch
t = [-80.,0.,50.]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
# n is length
H0 = he.Helix(r,a,b,t,q,s,m=10,n=20, N = 3)
Gs = ext.Append(Gs,H0)
G = ext.GraphUnionS(G,H0)
#################################

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"Helix.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"Helix.obj")
