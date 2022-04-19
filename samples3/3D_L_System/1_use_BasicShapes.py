import BasicShapes as bs
import extrusion as ext
import affine as aff

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
rx = 10.
ry = 20.
t = [-80.,0.,50.]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
H0 = bs.Ellipsoid(rx,ry,t,q,s,m=30,n=30)
Gs = ext.Append(Gs,H0)
G = ext.GraphUnionS(G,H0)

# Sphere Object
r = 20.
t = [0.,0.,50.]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
H1 = bs.Sphere(r,t,q,s,m=20,n=20)
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

# Cone0 Object
r1 = 5.
h1 = 5.
r2 = 10.
h2 = 20.
t = [0.,50.,50.]
degrees = 90
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
H1 = bs.Cone0(r1,h1,r2,h2,t,q,s,m=20,n=20)
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

# Cone Object
r = 10.
h = 20.
t = [50.,50.,50.]
degrees = 45
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
H1 = bs.Cone(r,h,t,q,s,m=20,n=20)
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

# Cylinder Object
r = 10.
h = 40.
t = [-50.,50.,-50.]
degrees = 90
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
H1 = bs.Cylinder(r,h,t,q,s,m=20,n=20)
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"BasicShapes-1.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"BasicShapes-1.obj")
