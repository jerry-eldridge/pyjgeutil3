import affine as aff
import extrusion as ext
import elevation_map as em

import numpy as np
import cv2

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

# image to Elevation map. Image should have equal
# width and height so crop and resize.
im = cv2.imread("wavesource-b.jpg",0) # grayscale
blur = cv2.blur(im,(10,10))

m = 50
w,h,d = 100,100,1.

t = [-80.,0.,50.]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
# n is length
H0 = em.ElevationMap(blur,w,h,d,t,q,s,m)
Gs = ext.Append(Gs,H0)
G = ext.GraphUnionS(G,H0)
#################################

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"ElevationMap1.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"ElevationMap1.obj")
