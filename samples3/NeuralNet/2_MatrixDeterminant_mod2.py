from copy import deepcopy

from math import factorial as fa

#import numpy as np

def perm(n):
    if n <= 1:
        P = [[0]]
        return P
    P = perm(n-1)
    Q = []
    for pi in P:
        for i in range(n):
            pi2 = deepcopy(pi)
            pi2.insert(i,n-1)
            Q.append(pi2)
    return Q

class Permutation:
    def __init__(self,L):
        self.L = L
        self.n = len(L)
    def __str__(self):
        s = str(self.L)
        return s
    # https://en.wikipedia.org/wiki/Bubble_sort
    # each time a transposition (a swap) is done
    # add one to s and when done determine if
    # even or odd. If even return 1 if odd return -1.
    def sign(self):
        s = 0
        n = self.n
        M = deepcopy(self.L)
        while True:
            swapped = False
            for i in range(1,n):
                if M[i-1] > M[i]:
                    tmp = M[i-1]
                    M[i-1] = M[i]
                    M[i] = tmp
                    swapped = True
                    s = (s + 1)%2
            if not swapped:
                break
        return [1,-1][s % 2]
    def g(self,i):
        return self.L[i]
    
class Mat:
    def __init__(self,A):
        self.A = deepcopy(A)
        self.shape = (len(A),len(A[0]))
        return
    def zero(self, n,m):
        A = []
        for i in range(n):
            B = []
            for j in range(m):
                B.append(0)
            A.append(B)
        return Mat(A)
    def identity(self, n):
        Z = self.zero(n,n)
        for i in range(n):
            Z.s(i,i,1)
        return Z
    def g(self,i,j):
        return self.A[i][j]
    def s(self,i,j,val):
        self.A[i][j] = val
        return
    def dot(self,B):
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
    def __str__(self):
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
    def det(self):
        a,b = self.shape
        assert(a == b)
        P = perm(a)
        s = 0
        for pi in P:
            pi2 = Permutation(pi)
            sgn = pi2.sign()
            Prod = 1
            for i in range(a):
                j = pi2.g(i)
                v = self.g(i,j)
                Prod = Prod*v
            v = sgn*Prod
            s = s + v
        return s
    def copy(self):
        B = deepcopy(self.A)
        return Mat(B)
    def transpose(self):
        n,m = self.shape
        B = self.zero(m,n)
        for i in range(n):
            for j in range(m):
                B.s(j,i,self.g(i,j))
        return B
    # cramer's rule
    # https://en.wikipedia.org/wiki/Cramer%27s_rule
    def solve(self,b):
        n,m = self.shape
        i,j = b.shape
        assert((n == i) and (j == 1))
        
        x = self.zero(n,1)
        D = self.det()
        for j in range(n):
            B = self.copy()
            for i in range(n):
                B.s(i,j,b.g(i,0))
            v = 1.0*B.det()/D
            x.s(j,0,v)
        return x
    # solution of A*X = I has X = A.inv()
    def inv(self):
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
##    def arr(self):
##        return np.array(self.A)            

A = Mat([[5,4,5],[1,2,3],[4,3,2]])
B = Mat([[5,4],[1,2],[2,4]])
C = A.dot(B)
b = Mat([[1,3,2]]).transpose()
print("A =\n",A)
print("B =\n",B)
print("C = A*B =\n",C)
print(A.g(0,0),A.g(0,1))
print("det(A) = ",A.det())
print("A.inv() =\n",A.inv())
