from copy import deepcopy
from math import sqrt

import numpy as np

class Mat:
    def __init__(self,A):
        self.B = np.array(A)
        self.A = list(map(list,list(self.B)))
        self.shape = (len(A),len(A[0]))
        return
    def zero(self, n,m):
        return Mat(list(np.zeros((n,m))))
    def identity(self, n):
        return Mat(list(np.identity(n)))
    def g(self,i,j):
        return self.B[i,j]
    def s(self,i,j,val): # set i,j entry to val
        self.B[i,j] = val
        return
    def __add__(self,B): # A + B
        C = self.B + B.B
        return Mat(list(C))
    def __mul__(self,v): # A * v with scalar v
        C = self.B*v
        return Mat(list(C))
    def __rmul__(self,v): # v * A with scalar v
        return self.__mul__(v)
    def __sub__(self,B):
        return self + -1*B
    def flatten(self): # assumes n x m matrix
        L = list(self.A.flatten())
        return Mat([L])
    def reshape(self,sh):
        B = list(self.B.reshape(sh))
        return Mat(B)
    def norm_L21(self):
        return np.linalg.norm(self.B)
    def norm_frobenius(self):
        return np.linalg.norm(self.B)
    def norm_inner(self):
        return sqrt(self.inner(self))
    def norm(self): # A.norm()
        return self.norm_frobenius()
    def __abs__(self): # abs(A) or notation |A|
        return self.norm()
    def dist(self,B): # A.dist(B) - distance A to B
        return abs(self - B)
    def dot(self,B): # A.dot(B)
        C = self.B.dot(B.B)
        return Mat(list(C))
    def __str__(self): # str(A) or print(A)
        return str(self.B)
    def det_perm(self): # A.det()
        return np.linalg.det(self.B)
    def det(self):
        return np.linalg.det(self.B)
    def tr(self):
        return np.linalg.tr(self.B)
    def inner(self,B):
        return (B.adj().dot(self)).tr()
    def copy(self): # B = A.copy()
        B = deepcopy(self.B)
        return Mat(B)
    def transpose(self): # B = A.transpose()
        B = self.B.transpose()
        return Mat(list(B))
    # cramer's rule
    # https://en.wikipedia.org/wiki/Cramer%27s_rule
    def solve(self,b): # x = A.solve(b)
        A = self.B
        B = b.B
        x = np.linalg.solve(A,B)
        return Mat(list(x))
    # solution of A*X = I has X = A.inv()
    def inv(self): # B = A.inv()
        A = self.B
        B = np.linalg.inv(A)
        return Mat(list(B))
    def adj(self):
        # assume real for now and take transpose
        # but if complex would need complex conjugate
        # of entries
        As = self.transpose() # conjugate transpose                    
        return As
    def pinv_right(self):
        A = self.B
        B = np.linalg.pinv(A)
        return Mat(list(B))
    def pinv_left(self):
        return self.pinv_right()
