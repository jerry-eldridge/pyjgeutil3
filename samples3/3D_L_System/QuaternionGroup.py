import numpy as np
from math import sqrt,pi,cos,sin,acos,asin,tan,atan

from copy import deepcopy

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
        """
        Euler-Rodrigues parameters S.q computing
        3D rotation matrix R = S.rotation_matrix()
        for quaternion S.
        """
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
        import math
        w,x,y,z = self.L
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.degrees(math.atan2(t3, t4))
        return X,Y,Z

def slerp(q1,q2,t):
    """
    q = slerp(q1,q2,t) - spherical lerp two quaternions
    q1 and q2 blending them for t in interval [0,1].
    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
    creating a path from q1 to q2 parametrized by t.
    Thus q.rotation_matrix() is a path from the
    rotation of q1 to rotation of q2.
    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

# https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def rotation_quaternion(degrees,x,y,z):
    """
    q = rotation_quaternion(degrees,x,y,z) returns
    a quaternion representing a rotation matrix
    of a 3D rotation about axis (x,y,z) by degrees
    angle.
    """
    alpha = degrees*pi/180.0
    beta = np.array([x,y,z])
    # https://en.wikipedia.org/wiki/Direction_cosine
    A0 = np.linalg.norm(beta)
    epsilon = 1e-8
    if A0 > epsilon:
        a,b,c = beta/A0
    else:
        a,b,c = beta
    q = Quaternion([
         cos(alpha/2.0),
         sin(alpha/2.0)*a,
         sin(alpha/2.0)*b,
         sin(alpha/2.0)*c])
    return q

def FromEuler(X,Y,Z):
    alpha,beta,gamma = X,Y,Z
    roll,yaw,pitch = alpha,beta,gamma
    RQ = rotation_quaternion
    roll,yaw,pitch = pitch,yaw,roll
    q = RQ(roll,0,0,1)*RQ(yaw,0,1,0)*RQ(pitch,1,0,0)
    return q

# https://en.wikipedia.org/wiki/Aircraft_principal_axes
# X is pitch axis (right of aircraft)
# Y is yaw axis (down from aircraft)
# Z is roll axis (front of aircraft)
def RollYawPitch(L):
    roll,yaw,pitch = L
    alpha,beta,gamma = roll,yaw,pitch 
    X,Y,Z = alpha,beta,gamma
    q = FromEuler(X,Y,Z)
    return q

Q = Quaternion
# you can right scalar multiply by reals these basis quaternions
e = Q([1,0,0,0])
i = Q([0,1,0,0])
j = Q([0,0,1,0])
k = Q([0,0,0,1])
# q = e*3 + i*4 + j*3.1 + k*5 is Q([3,4,3.1,5])
