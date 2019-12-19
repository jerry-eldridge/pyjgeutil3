import numpy as np
from math import sqrt,pi,cos,sin,acos,asin,tan,atan

# multipy two square n x n matrices A and B together
def MatMul(A,B):
    return np.einsum('ij,jk->ik',A,B)

class su3:
    # use S to mean self instance of su3 class.
    def __init__(S,L):
        assert(len(L)==8)
        i = complex(0,1)
        # https://en.wikipedia.org/wiki/Gell-Mann_matrices
        S.l1 = np.array([
            [0,1,0],
            [1,0,0],
            [0,0,0]])
        S.l2 = np.array([
            [0,-i,0],
            [i,0,0],
            [0,0,0]])
        S.l3 = np.array([
            [1,0,0],
            [0,-1,0],
            [0,0,0]])
        S.l4 = np.array([
            [0,0,1],
            [0,0,0],
            [1,0,0]])
        S.l5 = np.array([
            [0,0,-i],
            [0,0,0],
            [i,0,0]])
        S.l6 = np.array([
            [0,0,0],
            [0,0,1],
            [0,1,0]])
        S.l7 = np.array([
            [0,0,0],
            [0,0,-i],
            [0,i,0]])
        S.l8 = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,-2]])/sqrt(3)
        A1 = L[0]*S.l1 + L[1]*S.l2 + L[2]*S.l3 + L[3]*S.l4
        A2 = L[4]*S.l5 + L[5]*S.l6 + L[6]*S.l7 + L[7]*S.l8
        A = A1 + A2
        S.A = A
        S.q = L
        return
    # S + q
    def __add__(S,q):
        A = S.A + q.A
        q2 = su3([0,0,0,0, 0,0,0,0]).set_A(A)
        return q2
    # -S where S is in su3
    def __neg__(S):
        A = -S.A
        q2 = su3([0,0,0,0, 0,0,0,0]).set_A(A)
        return q2
    def __sub__(S,q):
        q2 = S + -q;
        return q2
    # turn su3 into vector space using real scalars
    def right_smul(S,x):
        A = x*S.A
        q2 = su3([0,0,0,0, 0,0,0,0]).set_A(A)
        return q2
    # multiply su3 S*q
    def __mul__(S,q):
        try:
            return S.right_smul(q)
        except:
            A = MatMul(S.A,q.A)
            q2 = su3([0,0,0,0, 0,0,0,0]).set_A(A)
            return q2
    # string representation of su3
    def __str__(S):
        s = '[%s,%s,%s,%s,%s,%s,%s,%s]' % tuple(S.q)
        return s
    # conjugate of a su3
    def conjugate(S):
        q2 = -su3(S.q)
        return q2
    # norm of the su3 field
    def __abs__(S):
        q = S*S.conjugate()
        return sqrt(q.q[0])
    # create a versor or unit su3
    def normalize(S):
        x = 1.0/abs(S)
        q = S*x
        return q
    # S[n] for su3 S
    def __getitem__(S,n):
        return S.q[n]
    # S[b] = c for su3 S
    def __setitem__(S,b,c):
        S.q[b] = c 
        q2 = su3(S.q)
        return q2
    def set_A(S,A):
        a = A[0,1].real
        b = A[1,0].imag
        h= -A[2,2].real*sqrt(3)/2.0
        c = A[0,0].real - h/sqrt(3)
        d = A[2,0].real
        e = A[2,0].imag
        f = A[2,1].real
        g = A[2,1].imag        
        S.L = [a,b,c,d,e,f,g,h]
        return su3(S.L)

def bracket(q1,q2):
    q = (q1*q2 - q2*q1)
    return q

def slerp(q1,q2,t):
    """
    q = slerp(q1,q2,t) - spherical lerp two su3
    q1 and q2 blending them for t in interval [0,1].
    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
    creating a path from q1 to q2 parametrized by t.
    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

Q = su3
# you can right scalar multiply by reals these basis su2
l = []
l.append(Q([1,0,0,0,0,0,0,0]))
l.append(Q([0,1,0,0,0,0,0,0]))
l.append(Q([0,0,1,0,0,0,0,0]))
l.append(Q([0,0,0,1,0,0,0,0]))
l.append(Q([0,0,0,0,1,0,0,0]))
l.append(Q([0,0,0,0,0,1,0,0]))
l.append(Q([0,0,0,0,0,0,1,0]))
l.append(Q([0,0,0,0,0,0,0,1]))
# q = l[0]*3 + l[1]*4 + l[2]*3.1 + l[3]*5 is Q([3,4,3.1,5,0,0,0,0])
