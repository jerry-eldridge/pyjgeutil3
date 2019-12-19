from math import sqrt,cos,sin,atan2
# https://docs.python.org/2/library/operator.html
class Complex:
    def __init__(self,a,b):
        """
        n is a whole number
        >>> help(Rational.__pow__)
        """
        self.real = a
        self.imag = b
        return
    def __str__(self):
        s = '%.4f+%.4fj' % (self.real,self.imag)
        return s
    def conjugate(self):
        z = Complex(self.real,-self.imag)
        return z
    # first make Complex into a vector space
    # with add,sub and smul
    def __add__(self,z):
        real = self.real + z.real
        imag = self.imag + z.imag
        return Complex(real,imag)
    def smul(self,x):
        real = x*self.real
        imag = x*self.imag
        return Complex(real,imag)      
    def __neg__(self):
        return self.smul(-1)
    def __sub__(self,z):
        return self + -(z)
    # make Complex into field by adding mul,div
    # where 1 is Complex(1,0) and 0 is Complex(0,0)
    def __mul__(self,z):
        real = self.real*z.real - self.imag*z.imag
        imag = self.imag*z.real + self.real*z.imag
        return Complex(real,imag)
    # norm for Complex
    def __abs__(self):
        r = sqrt(self.real**2 + self.imag**2)
        return r
    def __div__(self,z):
        epsilon = 1e-8
        assert(abs(z) > epsilon)
        z2 = self * z.conjugate()
        c = 1.0*abs(z)**2
        z2.real /= c
        z2.imag /= c
        return z2
    def arg(self):
        theta = atan2(self.imag,self.real)
        return theta
    def to_polar(self):
        p = [abs(self),self.arg()]
        return p
    def from_polar(self,p):
        r,theta = p
        real = r*cos(theta)
        imag = r*sin(theta)
        z = Complex(real,imag)
        self = z
        return self
    def __pow__(self,x):
        r,theta = self.to_polar()
        r2 = r**x
        theta2 = theta*x
        z2 = Complex(0,0)
        z2 = z2.from_polar([r2,theta2])
        return z2
    def __eq__(self,q):
        epsilon = 1e-8
        flag = abs(self-q)<epsilon
        return flag
    def __ne__(self,q):
        return not (self==q)
    def __lt__(self,q):
        print "Error: No order relation on Complex"
        assert(False)
        return


