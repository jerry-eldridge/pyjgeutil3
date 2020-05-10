from copy import deepcopy

from math import factorial as fa
from math import sqrt

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
    def __str__(self): # print(sigma) or str(sigma)
        s = str(self.L)
        return s
    # https://en.wikipedia.org/wiki/Bubble_sort
    # each time a transposition (a swap) is done
    # add one to s and when done determine if
    # even or odd. If even return 1 if odd return -1.
    def sign(self): # s = pi.sign()
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
    def g(self,i): # j = sigma.g(i), get or map i to j
        return self.L[i]
    
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
    def det(self): # A.det()
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
##    def arr(self):
##        return np.array(self.A)            

A = Mat([[5,4,5],[1,2,3],[4,3,2]])
I = A.identity(A.shape[0])
B = Mat([[5,4],[1,2],[2,4]])
C = A.dot(B)
b = Mat([[1,3,2]]).transpose()
print("A =\n",A)
print("B =\n",B)
print("C = A*B =\n",C)
print("I =\n",I)
print(A.g(0,0),A.g(0,1))
print("det(A) = ",A.det())
print("A.inv() =\n",A.inv())
print("abs(A) =",abs(A))
print("C - B =",C-B)
print("abs(C-B) =",abs(C-B))

flag = True # or False
if flag:
    print("Using sympy - if error, then 'pip install sympy'")
    import sympy
    I = A.identity(A.shape[0])
    x = sympy.symbols('x')
    p = (A - x*I).det()
    p = p.expand()
    print("p = (A - x*I).det() =",p)
    L = p.as_poly(x).all_coeffs()
    print("Using numpy - if error, then 'pip install numpy'")
    import numpy as np
    roots = np.roots(L)
    print("roots = ",roots)

f = lambda x: -x**3 + 9*x**2 + 9*x - 10

# https://en.wikipedia.org/wiki/Bisection_method
# root finding method: Bisection method
def bisection(f,a,b,tol=.1,nmax=1000,epsilon=1e-3):
    n = 1
    while n <= nmax:
        c = (a+b)/2.
        if abs(f(c)) < epsilon or abs(b-a)/2. < tol:
            return c
        n = n + 1
        if f(c)*f(a) > 0:
            a = c
        elif f(c)*f(a) < 0:
            b = c
        else:
            return c
    return None

def Derivative(f,x,dx):
     slope = 1.0*(f(x+dx)-f(x))/dx
     return slope

# root-finding method Newton's method
# https://en.wikipedia.org/wiki/Newton%27s_method
def Newtons(f,df,x0, nmax = 1000, epsilon=1e-3):
    n = 0
    x = x0
    oo = 1e8
    x_last = -oo
    count = 0
    
    while True:
        if abs(x - x_last) < epsilon:
            break
        x_last = x
        if abs(df(x)) < epsilon:
            break
        x = x - f(x)/df(x)
    return x

df = lambda x: Derivative(f,x,dx=.01)

# required f(a)*f(b) < 0
print("Only finding real roots ... ")
x1 = bisection(f,-10,0,tol=.1,nmax=1000,epsilon=1e-3)
x2 = bisection(f,0,2,tol=.1,nmax=1000,epsilon=1e-3)
x3 = bisection(f,2,10,tol=.1,nmax=1000,epsilon=1e-3)
print("Finds only real eigenvalues...")
print("eigvals(A) = Roots by bisection =",x1,x2,x3)

if flag:
    print("eigvals(A) by numpy = ",np.linalg.eigvals(np.array(A.A)))
    # (a,b) is graphing range here
    a = -7
    b = 12
    X = np.arange(a,b,(b-a)/100.)
    Y = list(map(f,X))
    print("If error then 'pip install matplotlib'")
    import matplotlib.pyplot as plt    
    plt.plot(X,Y,'b')
    L = [x1,x2,x3]
    print("Optimal Values of x =",L)
    plt.scatter(L,list(map(f,L)))
    plt.axhline(y=0,color='k')
    plt.show()
    
