import numpy as np
from math import sqrt,pi,cos,sin,acos,asin,tan,atan

# multipy two square n x n matrices A and B together
def MatMul(A,B):
    return np.einsum('ij,jk->ik',A,B)

class su2:
    # use S to mean self instance of su2 class.
    def __init__(S,L):
        assert(len(L)==3)
        # note that i**2 = j**2 = k**2 = -I
        # and other su2 group algebra rules hold
        i = complex(0,1)
        # SU(2) wikipedia article, S.i, S.j, S.k are called
        # the generators of SU(2). With bracket, this is
        # a lie algebra su(2).
        S.i = np.array([
            [0,i],
            [i,0]])
        S.j = np.array([
            [0,-1],
            [1,0]])
        S.k = np.array([
            [i,0],
            [0,-i]])
        S.A = L[0]*S.i + L[1]*S.j + L[2]*S.k
        S.q = np.array(L)
        return
    # S + q
    def __add__(S,q):
        A = S.A + q.A
        q2 = su2([0,0,0]).set_A(A)
        return q2
    # -S where S is in su2
    def __neg__(S):
        A = -S.A
        q2 = su2([0,0,0]).set_A(A)
        return q2
    def __sub__(S,q):
        q2 = S + -q;
        return q2
    # turn su2 into vector space using real scalars
    def right_smul(S,x):
        A = x*S.A
        q2 = su2([0,0,0]).set_A(A)
        return q2
    # multiply su2 S*q
    def __mul__(S,q):
        if type(q) in [type(3.1),type(3)]: # real number
            x = q
            return S.right_smul(x)
        A = S.A
        B = q.A
        C = MatMul(A,B)
        q2 = su2([0,0,0]).set_A(C)
        return q2
    # string representation of su2
    def __str__(S):
        s = '[%.4f,%.4f,%.4f]' % tuple(S.q)
        return s
    # conjugate of a su2
    def conjugate(S):
        q2 = su2([-S.q[0],-S.q[1],-S.q[2]])
        return q2
    # norm of the su2 field
    def __abs__(S):
        #q = S*S.conjugate()
        val = sqrt(S.q[0]**2 + S.q[1]**2 + S.q[2]**2)
        return val
    # create a versor or unit su2
    def normalize(S):
        x = 1.0/abs(S)
        q = S*x
        return q
    # S[n] for su2 S
    def __getitem__(S,n):
        return S.q[n]
    # S[b] = c for su2 S
    def __setitem__(S,b,c):
        S.q[b] = c 
        q2 = su2([S.q[0],S.q[1],S.q[2]])
        return q2
    def set_A(S,A):
        a = A[0,0].real
        b = A[1,0].imag
        c = A[1,0].real
        d = A[0,0].imag
        L = [b,c,d]
        return su2(L)
        

def bracket(q1,q2):
    q = q1*q2 - q2*q1
    return q
   

def slerp(q1,q2,t):
    """
    q = slerp(q1,q2,t) - spherical lerp two su2
    q1 and q2 blending them for t in interval [0,1].
    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
    creating a path from q1 to q2 parametrized by t.
    Thus q.rotation_matrix() is a path from the
    rotation of q1 to rotation of q2.
    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

Q = su2
# you can right scalar multiply by reals these basis su2
i = Q([1,0,0])
j = Q([0,1,0])
k = Q([0,0,1])
# q = ei*4 + j*3.1 + k*5 is Q([4,3.1,5])
