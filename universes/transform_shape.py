import numpy as np
import math
from math import sqrt,pi,cos,sin,acos,asin,tan,atan
import random
from copy import deepcopy
import scipy.stats as ss
import time

seed0 = 12345678
seed0 = int(time.time())
random.seed(seed0)
np.random.seed(seed0)

###############################################
# implementation of 3D rotations
#

# multipy two square n x n matrices A and B together
def MatMul(A,B):
    return np.einsum('ij,jk->ik',A,B)

# https://en.wikipedia.org/wiki/Quaternion#Matrix_representations
class Quaternion:
    # use S to mean self instance of Quaternion class.
    def __init__(S,L):
        assert(len(L)==4)
        S.L = deepcopy(L)
        S.I = np.identity(4)
        # note that i**2 = j**2 = k**2 = -I
        # and other quaternion group algebra rules hold
        S.i = np.array([
            [0,-1,0,0],
            [1,0,0,0],
            [0,0,0,-1],
            [0,0,1,0]])
        S.j = np.array([
            [0,0,-1,0],
            [0,0,0,1],
            [1,0,0,0],
            [0,-1,0,0]])
        S.k = np.array([
            [0,0,0,-1],
            [0,0,-1,0],
            [0,1,0,0],
            [1,0,0,0]])
        S.A = L[0]*S.I + L[1]*S.i + L[2]*S.j + L[3]*S.k
        S.q = np.array(L)
        return
    # S + q
    def __add__(S,q):
        A = S.A + q.A
        q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
        return q2
    # -S where S is quaternion
    def __neg__(S):
        A = -S.A
        q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
        return q2
    # S - q
    def __sub__(S,q):
        q2 = S + (-q)
        return q2
    # turn quarternions into vector space using real scalars
    def right_smul(S,x):
        A = x*S.A
        q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
        return q2
    # multiply quaternions S*q
    def __mul__(S,q):
        if type(q) == type(Quaternion([1,0,0,0])): # quaternion
            A = MatMul(S.A,q.A)
            q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
            return q2
        if type(q) in [type(3.1),type(3)]: # real number
            x = q
            return S.right_smul(x)
    def __pow__(S,n):
        q = Quaternion([1,0,0,0]) # one
        for i in range(1,n):
            q = q*S
        return q
    # string representation of quaternion
    def __str__(S):
        s = '[%.4f,%.4f,%.4f,%.4f]' % tuple(S.q)
        return s
    def __repr__(S):
        return str(S)
    # conjugate of a quaternion
    def conjugate(S):
        q2 = Quaternion([S.q[0],-S.q[1],-S.q[2],-S.q[3]])
        return q2
    def inv(S):
        epsilon = 1e-8
        assert(abs(S)**2 > epsilon)
        qi = S.conjugate()*(1.0/abs(S)**2)
        return qi
    # norm of the quaternion field
    def __abs__(S):
        q = S*S.conjugate()
        return sqrt(q.q[0])
    # create a versor or unit quaternion
    def normalize(S):
        x = 1.0/abs(S)
        q = S*x
        return q
    # S[n] for quaternion S
    def __getitem__(S,n):
        return S.q[n]
    # S[b] = c for quaternion S
    def __setitem__(S,b,c):
        S.q[b] = c 
        q2 = Quaternion([S.q[0],S.q[1],S.q[2],S.q[3]])
        return q2
    def rotation_matrix(S):
##        """
##        Euler-Rodrigues parameters S.q computing
##        3D rotation matrix R = S.rotation_matrix()
##        for quaternion S.
##        """
        q2 = S.normalize()
        a,b,c,d = list(q2.q)
        R = np.array([
            [a**2+b**2-c**2-d**2,2*(b*c-a*d),2*(b*d+a*c)],
            [2*(b*c+a*d),a**2-b**2+c**2-d**2,2*(c*d-a*b)],
            [2*(b*d-a*c),2*(c*d+a*b),a**2-b**2-c**2+d**2]])
        return R
    #https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation
    def set_rotation_matrix(S,R):
        theta = acos((np.trace(R)-1)/2.0)
        omega = np.array([
            R[2,1]-R[1,2],
            R[0,2]-R[2,0],
            R[1,0]-R[0,1]])/(2*sin(theta))
        alpha = theta
        beta = omega
        # https://en.wikipedia.org/wiki/Direction_cosine
        a,b,c = beta/np.linalg.norm(beta)
        q = Quaternion([
             cos(alpha/2.0),
             sin(alpha/2.0)*a,
             sin(alpha/2.0)*b,
             sin(alpha/2.0)*c])
        S = q
        return q
    # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    def ToEuler(self):
        w,x,y,z = self.L
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.atan2(t0, t1)*180/pi

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.asin(t2)*180/pi

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.atan2(t3, t4)*180/pi
        return X,Y,Z

def slerp(q1,q2,t):
##    """
##    q = slerp(q1,q2,t) - spherical lerp two quaternions
##    q1 and q2 blending them for t in interval [0,1].
##    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
##    creating a path from q1 to q2 parametrized by t.
##    Thus q.rotation_matrix() is a path from the
##    rotation of q1 to rotation of q2.
##    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

# https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def rotation_quaternion(degrees,x,y,z):
##    """
##    q = rotation_quaternion(degrees,x,y,z) returns
##    a quaternion representing a rotation matrix
##    of a 3D rotation about axis (x,y,z) by degrees
##    angle.
##    """
    alpha = degrees*pi/180.0
    beta = np.array([x,y,z])
    # https://en.wikipedia.org/wiki/Direction_cosine
    A0 = np.linalg.norm(beta)
    epsilon = 1e-8
    if A0 > epsilon:
        beta = beta/A0
    q = Quaternion([
         cos(alpha/2.0),
         sin(alpha/2.0)*beta[0],
         sin(alpha/2.0)*beta[1],
         sin(alpha/2.0)*beta[2]])
    return q

def FromEuler(X,Y,Z):
    roll,pitch,yaw = X,Y,Z
    RQ = rotation_quaternion
    q = RQ(yaw,0,0,1)*RQ(pitch,0,1,0)*RQ(roll,1,0,0)
    return q

# https://en.wikipedia.org/wiki/Aircraft_principal_axes
# X is pitch axis (right of aircraft)
# Y is yaw axis (down from aircraft)
# Z is roll axis (front of aircraft)
def RollYawPitch(L):
    roll,yaw,pitch = L
    X,Y,Z = roll,pitch,yaw
    q2 = FromEuler(X,Y,Z)
    return q2

Q = Quaternion
# you can right scalar multiply by reals these basis quaternions
e = Q([1,0,0,0])
i = Q([0,1,0,0])
j = Q([0,0,1,0])
k = Q([0,0,0,1])
# q = e*3 + i*4 + j*3.1 + k*5 is Q([3,4,3.1,5])

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
    q = rotation_quaternion(degrees,
                axis[0],axis[1],axis[2])
    return q

# convert Euler angle in degrees to quaternion.
def degree2q(R):
    f = lambda x: x*pi/180
    R2 = list(map(f,R))
    # convert Euler angles in radians to quaternion
    q = theta2q(R2)
    return q

def AimAxis(axis1,axis2):
    # Create V1 and V2 vectors of polygon1 normal and [0,0,1] z-axis
    V1 = axis1
    V2 = axis2 # z-axis
    V1 = np.array(V1)
    V2 = np.array(V2)
    # create a rotation axis to rotate V1 to V2
    # and compute angle in degrees of rotation, obtain quaternion for this
    axis = np.cross(V1,V2)
    # angle is counter-clockwise direction (I newly added a minus
    # sign to the below angle (11/11/2024).
    angle = acos(np.inner(V1,V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))
    degrees = angle*180/pi
    #print(f"degrees = {degrees}")
    q = rotation_quaternion(degrees,\
                axis[0],axis[1],axis[2])
    return q

# convert quaternion to 4x4 rotation matrix
def q2R(q):
    q = Quaternion(q)
    R3 = q.rotation_matrix()
    R = np.identity(4)
    R[:3,:3] = R3
    return R

def translate_pts(pts,T):
    tx,ty,tz = T
    pts2 = pts + np.array([tx,ty,tz])
    return pts2
def scale_pts(pts,S):
    sx,sy,sz = S
    pts2 = pts * np.array([sx,sy,sz])
    return pts2
def rotate_pts(pts,R):
    q = FromEuler(*R)
    R_mat = q.rotation_matrix()
    pts2 = np.array(pts) @ R_mat.T
    return pts2

def process(txt,R,S,T, idx_v2,idx_vt2,idx_vn2):
    lines = txt.split('\n')
    lines2 = []
    idx_v = 0
    idx_vt = 0
    idx_vn = 0
    pts0 = []
    for line in lines:
        if len(line) == 0:
            continue
        else:
            if line[0:2] == 'v ':
                toks = line.split(' ')
                x,y,z = toks[1:]
                x,y,z = list(map(float,[x,y,z]))
                pt = [x,y,z]
                pts0.append(pt)
            elif line[0:3] == 'vn ':
                continue
            elif line[0:3] == 'vt ':
                continue
            elif line[0:2] == 'f ':
                continue
    pts1 = np.array(pts0)
    O = np.mean(pts1,axis=0)
    pts2 = translate_pts(pts1,list(-O))
    pts3 = scale_pts(pts2,S)
    #print(pts2.shape)
    pts4 = rotate_pts(pts3,R)
    #print(pts3.shape)
    pts5 = translate_pts(pts4,T)
    #print(pts4.shape)
    c = 0
    for line in lines:
        if len(line) == 0:
            lines2.append(line)
            continue
        else:
            if line[0:2] == 'v ':
                idx_v = idx_v + 1
                toks = line.split(' ')
                x,y,z = toks[1:]
                x,y,z = list(map(float,[x,y,z]))
                x,y,z = pts5[c]
                x,y,z = list(map(str,[x,y,z]))
                line2 = ' '.join([toks[0],x,y,z])
                lines2.append(line2)
                c = c + 1
            elif line[0:3] == 'vn ':
                idx_vn = idx_vn + 1
                lines2.append(line)
            elif line[0:3] == 'vt ':
                idx_vt = idx_vt + 1
                lines2.append(line)
            elif line[0:2] == 'f ':
                toks = line.split(' ')
                L = []
                idx = [idx_v2,idx_vt2,idx_vn2]
                for tok in toks[1:]:
                    toks2 = tok.split('/')
                    for k in range(len(toks2)):
                        if toks2[k] == '':
                            continue
                        else:
                            toks2[k] = int(toks2[k]) + idx[k]
                    toks2 = list(map(str,toks2))
                    t = '/'.join(toks2)
                    L.append(t)
                line2 = ' '.join([toks[0]]+L)
                lines2.append(line2)
            else:
                lines2.append(line)
    txt2 = '\n'.join(lines2)
    idx_v2 = idx_v2 + idx_v
    idx_vt2 = idx_vt2 +idx_vt
    idx_vn2 = idx_vn2 + idx_vn
    return txt2, idx_v2,idx_vt2,idx_vn2

def static_process(txt,R,S,T, name_range):
    lines = txt.split('\n')
    lines2 = []
    idx_v = name_range[0][0]
    idx_vt = name_range[0][1]
    idx_vn = name_range[0][2]
    idx_v2 = 0
    idx_vt2 = 0
    idx_vn2 = 0
    pts0 = []
    for line in lines:
        if len(line) == 0:
            continue
        else:
            if line[0:2] == 'v ':
                toks = line.split(' ')
                x,y,z = toks[1:]
                x,y,z = list(map(float,[x,y,z]))
                pt = [x,y,z]
                pts0.append(pt)
            elif line[0:3] == 'vn ':
                continue
            elif line[0:3] == 'vt ':
                continue
            elif line[0:2] == 'f ':
                continue
    pts1 = np.array(pts0)
    O = np.mean(pts1,axis=0)
    pts2 = translate_pts(pts1,list(-O))
    pts3 = scale_pts(pts2,S)
    #print(pts2.shape)
    pts4 = rotate_pts(pts3,R)
    #print(pts3.shape)
    pts5 = translate_pts(pts4,T)
    #print(pts4.shape)
    c = 0
    for line in lines:
        if len(line) == 0:
            lines2.append(line)
            continue
        else:
            if line[0:2] == 'v ':
                idx_v = idx_v + 1
                toks = line.split(' ')
                x,y,z = toks[1:]
                x,y,z = list(map(float,[x,y,z]))
                x,y,z = pts5[c]
                x,y,z = list(map(str,[x,y,z]))
                line2 = ' '.join([toks[0],x,y,z])
                lines2.append(line2)
                c = c + 1
            elif line[0:3] == 'vn ':
                idx_vn = idx_vn + 1
                lines2.append(line)
            elif line[0:3] == 'vt ':
                idx_vt = idx_vt + 1
                lines2.append(line)
            elif line[0:2] == 'f ':
                toks = line.split(' ')
                L = []
                idx = [idx_v2,idx_vt2,idx_vn2]
                for tok in toks[1:]:
                    toks2 = tok.split('/')
                    for k in range(len(toks2)):
                        if toks2[k] == '':
                            continue
                        else:
                            toks2[k] = int(toks2[k]) + idx[k]
                    toks2 = list(map(str,toks2))
                    t = '/'.join(toks2)
                    L.append(t)
                line2 = ' '.join([toks[0]]+L)
                lines2.append(line2)
            else:
                lines2.append(line)
    txt2 = '\n'.join(lines2)
    return txt2
