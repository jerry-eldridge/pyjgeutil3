#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
from . import vectors
from . import QuaternionGroup as HH

from math import cos,sin,pi,acos
import numpy as np
from copy import deepcopy

# multiply two matrices C = A*B
def Mul(A,B):
    C = np.einsum('ij,jk->ik',A,B)
    return C

# linear interpolate (vectors) A and B with t = 0 to 1
# and lerp(A,B,0) = A and lerp(A,B,1) and lerp(A,B,.5) midpoint.
def lerp(A,B,t):
    return A*(1-t)+B*t

def lerpinv(A,B,C):
    epsilon = 0.0001
    t = 0
    for i in range(3):
        if abs(B[i]-A[i])>epsilon:
            t = 1.0*(C[i]-A[i])/(B[i]-A[i])
            break
    return t

def Transform3(shape, T):
    shape4 = [pt+[1] for pt in shape]
    SHAPE4 = [list(np.einsum('ij,j->i',T,pt)) for pt in shape4]
    SHAPE = [list(1.0*np.array(pt)/pt[3]) for pt in SHAPE4]
    SHAPE = [pt[:3] for pt in SHAPE]
    return SHAPE

# transform points with 4x4 transformation matrix T
def Transform(shape,T):
    return Transform3(shape,T)

# round-off numbers in list of points shape
def Round(shape):
    shape = [[int(round(x)) for x in pt] for pt in shape]
    return shape

# convert quaternion to 4x4 rotation matrix
def q2R(q):
    q = HH.Quaternion(q)
    R3 = q.rotation_matrix()
    R = np.identity(4)
    R[:3,:3] = R3
    return R

# Convert Euler angles theta,the angular position, to quaternion
def theta2q(theta):
    a = np.linalg.norm(theta)
    degrees = a*180/pi
    epsilon = 1e-8
    if abs(a) > epsilon:
        axis = np.array(theta)/a
    else:
        axis = np.array([0,0,1])
        degrees = 0
    q = HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    return q

# rotate points shape with quaternion q
def Rotate(shape,q,align=True):
    R = q2R(q.q)
    SHAPE = Transform(shape,R)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

# Translate points shape by [tx,ty,tz]
def Translate(shape,tx,ty,tz,align=True):
    T = vectors.translation_matrix(tx, ty, tz)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

# Scale points shape by [sx,sy,sz]
def Scale(shape,sx,sy,sz,align=True):
    T = vectors.scale_matrix(sx, sy, sz)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

# Center of 3D points
def Center(pts,flag2d = False):
    PTS = [np.array(pt) for pt in pts]
    X = [pt[0] for pt in PTS]
    Y = [pt[1] for pt in PTS]
    if flag2d:
        C = [np.mean(X),np.mean(Y)]
    else:
        Z = [pt[2] for pt in PTS]
        C = [np.mean(X),np.mean(Y),np.mean(Z)]
    return C
