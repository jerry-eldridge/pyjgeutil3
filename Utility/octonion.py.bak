import QuaternionGroup as QG

from math import sqrt

HH = QG.Quaternion

# https://en.wikipedia.org/wiki/Octonion
# -- since non-associative, it doesn't have a
# matrix representation.
class Octonion:
    def __init__(S,L):
        """
        Octonion(L) - where L = [ai bi] are real
        numbers defining two Quaternions a and b
        where addition and multiplication and
        conjugate are defined. There are 8 real
        numbers in list L.
        """
        L1 = L[:4]
        L2 = L[4:]
        S.a = HH(L1)
        S.b = HH(L2)
        S.q = list(S.a.q) + list(S.b.q)
        return
    def __add__(S,q):
        a = S.a + q.a
        b = S.b + q.b
        return Octonion(list(a.q)+list(b.q))
    def __neg__(S):
        a = -S.a
        b = -S.b
        return Octonion(list(a.q)+list(b.q))
    def __sub__(S,q):
        q2 = S + (-q)
        return q2
    def right_smul(S,x):
        a = S.a*x
        b = S.b*x
        return Octonion(list(a.q)+list(b.q))
    def __div__(S,x): # scalar division
        assert(x != 0)
        return S.right_smul(1.0/x)
    def inv(S):
        q = S.conjugate()/abs(S)
        return q
    def __mul__(S,q):
        if type(q) == type(2) or type(q) == type(2.1):
            a = S.a*q
            b = S.b*q
        else:
            a = S.a*q.a-(q.b.conjugate())*S.b
            b = q.b*S.a+S.b*(q.a.conjugate())
        return Octonion(list(a.q)+list(b.q))
    def __str__(S):
        s = '[%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f]' % tuple(S.q)
        return s
    def conjugate(S):
        a = S.a
        b = S.b
        a.q *= -1
        b.q *= -1
        a.q[0] *= -1
        return Octonion(list(a.q)+list(b.q))
    def real(S):
        re = (S + S.conjugate())*0.5
        return re
    def imag(S):
        im = (S - S.conjugate())*0.5
        return im
    def __abs__(S):
        val = 0
        for i in range(8):
            val += (S.q[i])**2
        val = sqrt(val)
        return val
    # S[n] for octonion S
    def __getitem__(S,n):
        return S.q[n]
    # S[b] = c for octonoin S
    def __setitem__(S,b,c):
        S.q[b] = c 
        q2 = Octonion([S.q[0],S.q[1],S.q[2],S.q[3],S.q[4],S.q[5],S.q[6],S.q[7]])
        return q2
    
def slerp(q1,q2,t):
    """
    q = slerp(q1,q2,t) - spherical lerp two octonions
    q1 and q2 blending them for t in interval [0,1].
    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
    creating a path from q1 to q2 parametrized by t.
    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

# (Octonion,bracket) is a lie algebra
def bracket(q1,q2):
    return q1*q2 - q2*q1


OO = Octonion
