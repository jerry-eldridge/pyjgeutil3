import matplotlib.pyplot as plt
import skimage
from skimage.transform import radon,iradon

import BasicShapes as bs
import extrusion as ext
import affine as aff

import numpy as np

from copy import deepcopy

import vector_calculus as vc

clamp = lambda x,lo,hi: min(hi,max(lo,x))

BIGDATA = r"./"

######################### SCENE 1 BEGIN
G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []

### Ellipsoid Object
##rx = 10.
##ry = 20.
##t = [-80.,0.,50.]
##degrees = 0
##axis = [0,1,0]
##q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
##scale = 1.
##s = [scale,scale,scale] # the same scale as previous for caps
##H0 = bs.Ellipsoid(rx,ry,t,q,s,m=30,n=30)
##Gs = ext.Append(Gs,H0)
##G = ext.GraphUnionS(G,H0)

### Sphere Object
##r = 50.
##t = [0.,0.,100.]
##degrees = 0
##axis = [0,1,0]
##q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
##scale = 1.
##s = [scale,scale,scale] # the same scale as previous for caps
##H1 = bs.Sphere(r,t,q,s,m=20,n=20)
##Gs = ext.Append(Gs,H1)
##G = ext.GraphUnionS(G,H1)

### Cone0 Object
##r1 = 5.
##h1 = 5.
##r2 = 10.
##h2 = 20.
##t = [0.,50.,50.]
##degrees = 90
##axis = [0,1,0]
##q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
##scale = 1.
##s = [scale,scale,scale] # the same scale as previous for caps
##H1 = bs.Cone0(r1,h1,r2,h2,t,q,s,m=20,n=20)
##Gs = ext.Append(Gs,H1)
##G = ext.GraphUnionS(G,H1)

## Cone Object
##r = 10.
##h = 20.
##t = [50.,50.,50.]
##degrees = 45
##axis = [0,1,0]
##q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
##scale = 1.
##s = [scale,scale,scale] # the same scale as previous for caps
##H1 = bs.Cone(r,h,t,q,s,m=20,n=20)
##Gs = ext.Append(Gs,H1)
##G = ext.GraphUnionS(G,H1)

### Cylinder Object
##r = 10.
##h = 40.
##t = [-50.,50.,-50.]
##degrees = 90
##axis = [0,1,0]
##q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
##scale = 1.
##s = [scale,scale,scale] # the same scale as previous for caps
##H1 = bs.Cylinder(r,h,t,q,s,m=20,n=20)
##Gs = ext.Append(Gs,H1)
##G = ext.GraphUnionS(G,H1)

# Torus Object
r1 = 10.
r2 = 50.
t = [0.,0.,0.]
degrees = 45
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
H1 = bs.Torus(r1,r2,t,q,s, m=10,n=60)
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

# Save Scene 1
#ext.Graphs2OBJ(BIGDATA+"torus-02.obj",Gs,"scene")

fn_obj_1 = BIGDATA + "torus-02.obj"
A = vc.Container_3D_Object(fn_obj_1)
#A.create()
A.G = G
A.C = np.mean(G['pts'],axis=0)
AC = A.C

N = 20
M = 20

alpha_min = 0
alpha_max = 180
d_alpha = (alpha_max-alpha_min)/(N-1)

t_min = 0
t_max = 1
d_t = (t_max-t_min)/(N-1)

s_min = -100
s_max = 100
d_s = (s_max-s_min)/(M-1)

amount = 1000

theta = np.zeros((N),dtype=np.float32)
sinogram = np.zeros((N,M),dtype=np.float32)

flx_max = abs(5*amount)
for j in range(M):
    s = s_min + j*d_s
    Flx = []
    Alpha = []
    for i in range(N):
        print(f".",end='')
        alpha = alpha_min + i*d_alpha
        theta[i] = alpha
        Alpha.append(alpha)
        q = aff.HH.rotation_quaternion(alpha,0,1,0)
        A1 = [0,s_min,0]
        A2 = [0,s_max,0]
        shape = [A1,A2]
        centroid = aff.Center(shape,flag2d=False)
        shape2 = aff.Translate(shape,
                    -centroid[0],-centroid[1],
                    -centroid[2],align=False)
        shape = aff.Rotate(shape2,q,align=False)
        shape2 = aff.Translate(shape,
                    centroid[0],centroid[1],
                    centroid[2],align=False)        
        A1,A2 = shape2
        t = t_min + i*d_t
        ri = vc.lerp(A1,A2,t)
        F = vc.F_helper(ri,amount)
        flx = A.flux(F)
        flx2 = clamp(flx, -flx_max, flx_max)
        sinogram[i,j] = flx2
    print(end='\n')

img = iradon(sinogram,theta=theta,filter_name='ramp')
fig = plt.imshow(img)
plt.show()

