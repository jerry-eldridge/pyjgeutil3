from copy import deepcopy
import numpy as np
import scipy.spatial as ss

import random

seed0 = 1235
np.random.seed(seed0)

# [1] "Algebraic Topology: A First Course, Revised",
# Marvin J. Greenberg, John R. Harper,
# 1981, Addison-Wesley.

# R is a unitary ring, main examples R inputs
# int(x),float(x), GF(x,n).
class R:
    def __init__(self, x):
        self.x = x
    def one(self):
        return R('1')
    def __add__(self, y):
        assert(type(self)==type(y))
        return R(self.x + y.x)
    def __neg__(self):
        return R(-self.x)
    def __sub__(self, y):
        assert(type(self)==type(y))
        return self + -y
    def __mul__(self, y):
        assert(type(self) == type(y))
        return R(self.x * y.x)
    def __str__(self):
        s = f"{self.x}"
        return s
    def __repr__(self):
        return str(self)

# geometric q simplex of input points Delta_q
class geometrisingular_q_chain_simplex:
    def __init__(self,q):
        self.q = q
        self.n = q + 1
        E = [[0]*self.n]
        for i in range(self.n):
            E_i = [0]*self.n
            E_i[i] = 1
            E.append(E_i)
        E = E[:-1]
        self.E = E
    def __str__(self):
        s = f'Delta_{self.q}'
        return s
    def __repr__(self):
        return str(self)

Delta = lambda q: geometrisingular_q_chain_simplex(q)

# This is the affine map from Delta(q-1) basis E1
# to Delta(q) basis E2 where one omits E_i from E2.
def F(i,q):
    def f(e):
        E1 = deepcopy(Delta(q-1).E)
        E2 = deepcopy(Delta(q).E)
        try:
            j = E1.index(e)
            if j < i:
                return E2[j]
            else:
                return E2[j+1]
        except:
            return None
    return f

# singular q simplex of input points P where
# sigma : RR**q -> E where E is some space
# of input points P[i] = sigma(E[i]). sigma
# can be just a map from RR**q -> RR**q for
# example if E = RR**q.
class singular_q_simplex:
    def __init__(self, q, sigma):
        assert(q >= 0)
        self.q = q
        self.E = geometrisingular_q_chain_simplex(self.q).E
        self.sigma = sigma
    # update with new singular_q_simplex sigma
    def update(self, sigma):
        self.sigma = sigma
        return
    # this is the map of Delta(q) to sigma(Delta(q))
    # called the points P
    def P(self):
        return [self.sigma(e) for e in self.E]
    def __eq__(self, y):
        P1 = deepcopy(self.P())
        P2 = deepcopy(y.P())
        P1.sort()
        P2.sort()
        flag = P1 == P2
        return flag
    def __ne__(self, y):
        return not(self == y)
    # this is the singular_q_simplex sigma
    def sigma(self, x):
        return self.sigma(x)
    # this is the i-th face of singular_q_simplex
    # which if the simplex is a tetrahedron, the
    # face will be a triangle. If a triangle the
    # face will be an edge. If an edge, the face will
    # be a point. Etc. The face is on the boundary
    # of the q-simplex. This operation face(i)
    # will remove vertex i and create new simplex.
    def face(self, i):
        assert(0 <= i-1 <= self.q)
        sigma = lambda e: self.sigma(F(i-1,self.q)(e))
        return singular_q_simplex(self.q-1,sigma)
    def __pow__(self, i):
        assert(0 <= i-1 <= self.q)
        return self.face(i)
    def __str__(self):
        if self.q == 0:
            name = "vertex"
        elif self.q == 1:
            name = "edge"
        elif self.q == 2:
            name = "face"
        elif self.q == 3:
            name = "tetra"
        else:
            name = f"simplex_{self.q}"
        s = f'<sqs>\nn {name}\n'
        P = self.P()
        for i in range(len(P)):
            pt = P[i]
            tt = ' '.join(list(map(str,list(pt))))
            t = f'v {i+1} {tt}\n'
            s = s + t
        s = s + "</sqs>"
        return s
    def __repr__(self):
        return str(self)

# right R module of singular_q_chain with the
# example of singular q chains
# being a specific example of singular_q_chain.
class singular_q_chain:
    def __init__(self,V,S):
        assert(len(V) == len(S))
        assert(len(V) > 0)
        self.n = len(S)
        self.S = deepcopy(S)
        self.V = deepcopy(V)
    def __eq__(self, y):
        flag = str(self - y) == '0'
        return flag
    def find(self, s):
        for i in range(len(self.S)):
            if self.S[i] == s:
                return i
        return None
    def zero(self):
        return singular_q_chain([],[])
    def term(self, i):
        assert(0 <= i-1 < len(self.S))
        return self.S[i-1]
    def scalar(self, i):
        assert(0 <= i-1 < len(self.S))
        return self.V[i-1]
    def __str__(self):
        if len(self.V) == 0:
            s = '0'
            return s
        s = '<singular_q_chain>\n'
        epsilon = 1e-8
        for i in range(len(self.V)):
            v = self.V[i]
            if abs(v.x) < epsilon:
                continue
            sigma = self.S[i]
            txt = str(sigma)
            lines = txt.split('\n')
            t = f'<term index = {i+1}>\n'
            for line in lines:
                line = line.strip()
                t2 = f"{line}\n"
                t = t + t2
            t2 = f"<scalar>{v}</scalar>\n"
            t = t + t2
            t = t + "</term>\n"
            s = s + t
        if s == '<singular_q_chain>\n':
            return '0'
        s = s + "</singular_q_chain>"
        return s
    def __repr__(self):
        return str(self)
    def __add__(self, y):
        V = []
        S = []
        for i in range(len(self.S)):
            s = self.S[i]
            v = self.V[i]
            if s not in S:
                S.append(s)
                V.append(v)
            else:
                idx = self.find(s)
                v2 = V[idx]
                V[idx] = v2 + v
        for i in range(len(y.S)):
            s = y.S[i]
            v = y.V[i]
            if s not in S:
                S.append(s)
                V.append(v)
            else:
                idx = self.find(s)
                v2 = V[idx]
                V[idx] = v2 + v
        return singular_q_chain(V,S)
    def __neg__(self):
        S = [self.S[i] for i in range(len(self.S))]
        V = [-self.V[i] for i in range(len(self.V))]
        return singular_q_chain(V,S)
    def __sub__(self, y):
        return self + -y
    def __mul__(self, scalar): 
        if (type(scalar) == type(self.V[0])):
            S = [self.S[i] for i in range(len(self.S))]
            V = [self.V[i]*scalar for \
                     i in range(len(self.V))]
            return singular_q_chain(V,S)
        print(f"Error")
        return None

# define boundary to sigma
def partial_q(x):
    try:
        if x == '0':
            return '0'
    except:
        ii = 0
    if x is None:
        return '0'
    v = None
    # initially define boundary of x for x
    # of type singular q simplex
    # bdy(sigma) = Sum_{i=0..q} (-1)**i * sigma**(i)
    if type(x) == singular_q_simplex:
        # i = 0 to q
        v = None
        sigma = x
        if sigma.q == 0:
            return '0'
        for i in range(sigma.q+1):
            sigma_i = sigma**(i+1)
            scalar = R((-1)**i)
            val = singular_q_chain([scalar],[sigma_i])
            if i == 0:
                v = val
            else:
                v = v + val
    elif type(x) == singular_q_chain:
        # i = 0 to q
        v = None
        for i in range(len(x.S)):
            sigma = x.S[i]
            if sigma.q == 0:
                continue
            v_sigma = x.V[i]
            bdy_sigma = partial_q(sigma)
            if bdy_sigma is None:
                continue
            val = partial_q(sigma)*v_sigma
            if i == 0:
                v = val
            else:
                v = v + val
    if v is None:
        return '0'
    return v
bdy = partial_q

# map from points to singular q chains.
S_q = lambda n,f: \
     singular_q_chain([R(1)],\
            [singular_q_simplex(n,f)])

# columns of matrices A are the points P
# of the simplex and the location or origin
# of the simplex is b.flatten() .

def func(pts):
    # map E[i] to P[i]
    def f(e):
        E = Delta(len(pts)-1).E
        try:
            idx = E.index(e)
        except:
            idx = 0
        y = np.array(pts[idx])
        y = list(map(float,list(y.flatten())))
        return y
    return f


##def f_A31(e):
##    # list of vectors
##    pts = [[1,1,1],[1,2,3],[1,4,1]]
##    y = func(pts)(e)
##    return y
##def f_A41(e):
##    pts = [[0,2,0],[4,1,1],[3,2,2],[1,0,1]]
##    y = func(pts)(e)
##    return y
