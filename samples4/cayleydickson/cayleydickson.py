class CayleyDickson:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        try:
            self.n = a.n + 1
        except:
            self.n = 1
        return
    def __rmul__(self, scalar):
        a = self.a
        a2 = self.a*scalar
        b = self.b
        b2 = self.b*scalar
        return CayleyDickson(a2,b2)
    def __mul__(self, y):
        if type(y) == type(1) or \
           type(y) == type(1.0):
            return self.__rmul__(y)
        assert(self.n == y.n)
        a = self.a
        b = self.b
        c = y.a
        d = y.b
        try:
            u = a * c - d.conj()*b
            v = d * a + b * c.conj()
        except:
            u = a * c - d * b
            v = d * a + b * c
        return CayleyDickson(u,v)
    def conj(self):
        if self.n - 1 == 1:
            return self
        try:
            u = self.a.conj()
        except:
            u = self.a
        v = -self.b
        return CayleyDickson(u,v)
    def __neg__(self):
        u = -self.a
        v = -self.b
        n = self.n
        return CayleyDickson(u,v)
    def __add__(self, y):
        assert(self.n == y.n)
        a = self.a
        b = self.b
        c = y.a
        d = y.b
        u = a + c
        v = b + d
        return CayleyDickson(u,v)
    def norm(self):
        val = (self * self.conj()).a
        return val
    def __str__(self):
        s = f'<{self.a},{self.b}>'
        return s
    def __repr__(self):
        return str(self)
    def __sub__(self,y):
        return self + -y

from math import log,fmod
def List2CD(L):
    if len(L) == 2:
        return CD(L[0],L[1])
    if len(L) == 1:
        return L[0]
    if len(L) == 0:
        return None
    n = len(L)
    v = log(n)/log(2)
    r = fmod(v,1)
    if abs(r) == 0:
        m = int(n/2)
        L1 = L[:m]
        L2 = L[m:]
        return CD(List2CD(L1),List2CD(L2))
    else:
        print(f"Error: length n = {n} must be 2**p",L)
        return None

CD = CayleyDickson

