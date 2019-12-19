import polynomial as poly
from math import sqrt,cos,sin,atan2

from copy import deepcopy

P = poly.Polynomial

def Re(p):
    if len(p.dat) == 0:
        return 0
    else:
        return p.dat[0]
def Im(p):
    if len(p.dat) == 0:
        return 0
    elif len(p.dat) == 1:
        return 0
    else:
        return p.dat[1]
def Reduce(q):
    # p = x**2 + 1
    p = P([1,0,1],'x')
    Q,R = q/p
    return R
    
# https://docs.python.org/2/library/operator.html
class PolyComplex:
    def __init__(self,a,b):
        # p = b*x + a
        self.p = P([a,b],'x')
        return
    # p.dat is [a,b]
    def real(self):
        return Re(self.p)
    def imag(self):
        return Im(self.p)
    def __str__(self):
        a,b = self.p.dat
        s = '(%s+%sj)' % (str(a),str(b))
        return s
    def conjugate(self):
        z = PolyComplex(Re(self.p),-Im(self.p))
        return z
    # first make PolyComplex into a vector space
    # with add,sub and smul
    def __add__(self,z):
        try:
            z2 = self.p + z.p
        except:
            z2 = self.p + z
        z2 = Reduce(z2)
        z3 = PolyComplex(Re(z2),Im(z2))
        return z3
    def smul(self,x):
        z2 = self.p * x
        z2 = Reduce(z2)
        z3 = PolyComplex(Re(z2),Im(z2))
        return z3
    def __neg__(self):
        return self.smul(-1)
    def __sub__(self,z):
        z2 = self + -(z)
        return z2
    # make PolyComplex into field by adding mul,div
    # where 1 is PolyComplex(1,0) and 0 is PolyComplex(0,0)
    def __mul__(self,z):
        try:
            z2 = self.p * z.p
        except:
            z2 = self.p * z
        z2 = Reduce(z2)
        z3 = PolyComplex(Re(z2),Im(z2))
        return z3
    # norm for PolyComplex
    def __abs__(self):
        v = sqrt(self.real()**2 + self.imag()**2)
        return v
    def __div__(self,z):
        epsilon = 1e-8
        assert(abs(z) > epsilon)
        # self/z * (z.conj/z.conj) = (self*z.conj)/(z*z.conj) 
        z2 = self * z.conjugate() # is complex
        # c = z * z.conj = abs(z)**2 is real
        c = 1.0*abs(z)**2
        z3 = z2*(1.0/c)        
        return z3
    def __pow__(self,n):
        z2 = self.p**n
        z2 = Reduce(z2)
        z3 = PolyComplex(Re(z2),Im(z2))
        return z3
    def __eq__(self,q):
        epsilon = 1e-8
        flag = abs(self-q)<epsilon
        return flag
    def __ne__(self,q):
        return not (self==q)
    def __lt__(self,q):
        print "Error: No order relation on PolyComplex"
        assert(False)
        return
    # imagine these came about after trigonometry
    def arg(self):
        theta = atan2(self.imag(),self.real())
        return theta
    def to_polar(self):
        p = [abs(self),self.arg()]
        return p
    def from_polar(self,p):
        r,theta = p
        real = r*cos(theta)
        imag = r*sin(theta)
        z = PolyComplex(real,imag)
        self = z
        return self

