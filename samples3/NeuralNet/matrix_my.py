from copy import deepcopy
import permutation as perm

from math import sqrt

class Mat:
    def __init__(self,A):
        self.A = deepcopy(A)
        self.shape = (len(A),len(A[0]))
        return
    def zero(self, n,m): # zero matrix
        A = []
        for i in range(n):
            B = []
            for j in range(m):
                B.append(0)
            A.append(B)
        return Mat(A)
    def identity(self, n): # identity matrix
        Z = self.zero(n,n)
        for i in range(n):
            Z.s(i,i,1)
        return Z
    def g(self,i,j): # get i,j entry
        return self.A[i][j]
    def s(self,i,j,val): # set i,j entry to val
        self.A[i][j] = val
        return
    def __add__(self,B): # A + B
        a,b = self.shape
        c,d = B.shape
        assert((a == c) and (b == d))
        C = self.zero(a,b)
        for i in range(a):
            for j in range(b):
                s = self.g(i,j) + B.g(i,j)
                C.s(i,j,s)
        return C
    def __mul__(self,v): # A * v with scalar v
        a,b = self.shape
        C = self.zero(a,b)
        for i in range(a):
            for j in range(b):
                s = self.g(i,j)*v
                C.s(i,j,s)
        return C
    def __rmul__(self,v): # v * A with scalar v
        return self.__mul__(v)
    def __sub__(self,B):
        return self + -1*B
    def flatten(self): # assumes n x m matrix
        L = []
        for M in self.A:
            L = L + M
        return Mat([L])
    def reshape(self,sh):
        B = self.flatten().A[0]
        n,m = self.shape
        A = []
        for j in range(sh[0]):
            L2 = []
            for i in range(sh[1]):
                L2.append(B[i+sh[1]*j])
            A.append(L2)
        return Mat(A)
    def norm_L21(self):
        m,n = self.shape
        t = 0
        for j in range(n):
            s = 0
            for i in range(m):
                s = s + abs(self.g(i,j))**2
            v = sqrt(s)
            t = t + v
        return t
    def norm_frobenius(self):
        m,n = self.shape
        t = 0
        for i in range(m):
            s = 0
            for j in range(n):
                s = s + abs(self.g(i,j))**2
            t = t + s
        v = sqrt(t)
        return v
    def norm_inner(self):
        return sqrt(self.inner(self))
    def norm(self): # A.norm()
        return self.norm_frobenius()
    def __abs__(self): # abs(A) or notation |A|
        return self.norm()
    def dist(self,B): # A.dist(B) - distance A to B
        return abs(self - B)
    def dot(self,B): # A.dot(B)
        a,b = self.shape
        c,d = B.shape
        assert(b == c)
        C = self.zero(a,d)
        for i in range(a):
            for j in range(d):
                s = 0
                for k in range(b):
                    s = s + self.g(i,k)*B.g(k,j)
                C.s(i,j,s)
        return C
    def __str__(self): # str(A) or print(A)
        s = 'Mat([[\n'
        a,b = self.shape
        for i in range(a):
            t = '\t'
            for j in range(b):
                u = '%s,' % str(self.g(i,j))
                t = t + u + ' '
            t = t[:-2]
            t = t + '],\n'
            s = s + t
        s = s[:-2]
        s = s + '])\n'
        return s
    def det_perm(self): # A.det()
        a,b = self.shape
        assert(a == b)
        P = perm.perm(a)
        s = 0
        for pi in P:
            pi2 = perm.Permutation(pi)
            sgn = pi2.sign()
            Prod = 1
            for i in range(a):
                j = pi2.g(i)
                v = self.g(i,j)
                Prod = Prod*v
            v = sgn*Prod
            s = s + v
        return s
    def minor(self,i,j):
        n,m = self.shape
        assert(n == m)
        C = self.identity(n-1)
        vv = 0
        for v in range(n):
            uu = 0
            if v == j:
                continue
            for u in range(m):
                if u == i:
                    continue
                val = self.g(u,v)
                C.s(uu,vv,val)
                uu = uu + 1
            vv = vv + 1
        return C
    def cofactor(self,i,j):
        return (-1)**(i+j)*self.minor(i,j).det()
    def det(self):
        n,m = self.shape
        assert(n == m)
        if n <= 0:
            return 1.0
        if n == 1:
            return self.g(0,0)
        else:
            i = 0 # use first row
            t = 0
            for j in range(m): # vary columns
                aij = self.g(i,j)
                Cij = self.cofactor(i,j)
                v = aij*Cij
                t = t + v
            return t
    def tr(self):
        n,m = self.shape
        assert(n == m)
        s = 0
        for i in range(n):
            s = s + self.g(i,i)
        return s
    def inner(self,B):
        return (B.adj().dot(self)).tr()
    def copy(self): # B = A.copy()
        B = deepcopy(self.A)
        return Mat(B)
    def transpose(self): # B = A.transpose()
        n,m = self.shape
        B = self.zero(m,n)
        for i in range(n):
            for j in range(m):
                B.s(j,i,self.g(i,j))
        return B
    # cramer's rule
    # https://en.wikipedia.org/wiki/Cramer%27s_rule
    def solve(self,b): # x = A.solve(b)
        n,m = self.shape
        i,p = b.shape
        #print(self.shape)
        #print(b.shape)
        assert((n == i) and (p == 1))
        
        x = self.zero(n,p)
        #print(x.shape)
        D = self.det()
        for j in range(n):
            B = self.copy()
            for i in range(n):
                B.s(i,j,b.g(i,0))
            v = 1.0*B.det()/D
            x.s(j,0,v)
        return x
    # solution of A*X = I has X = A.inv()
    def inv(self): # B = A.inv()
        n,m = self.shape
        assert(n == m)
        I = self.identity(n)
        B = self.zero(n,n)
        for i in range(n):
            bi = self.zero(n,1)
            for j in range(n):
                bi.s(j,0,I.g(i,j))
            xi = self.solve(bi)
            for j in range(n):
                B.s(j,i, xi.g(j,0))
        return B
    def adj(self):
        # assume real for now and take transpose
        # but if complex would need complex conjugate
        # of entries
        As = self.transpose() # conjugate transpose                    
        return As
    def pinv_right(self):
        n,m = self.shape
        As = self.adj() # conjugate transpose
        B = self.dot(As)
        epsilon = 1e-6
        if abs(B.det()) > epsilon:
            BI = B.inv()
            C = As.dot(BI)
            return C
        else:
            return None
        return
    def pinv_left(self):
        n,m = self.shape
        As = self.adj() # conjugate transpose
        B = As.dot(self)
        epsilon = 1e-6
        if abs(B.det()) > epsilon:
            BI = B.inv()
            C = BI.dot(As)
            return C
        else:
            return None

