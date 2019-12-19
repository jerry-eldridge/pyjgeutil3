import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import polynomial

Polynomial = polynomial.Polynomial

#https://en.wikipedia.org/wiki/Polynomial_greatest_common_divisor
def gcd_nonrecursive(a,b):
     r0 = a
     r1 = b
     s0 = a.one()
     s1 = a.zero()
     t0 = a.zero()
     t1 = a.one()
     i = 1
     while (r1.degree()>0):
          q,r = r0 / r1
          r2 = r0 - q*r1
          s2 = s0 - q*s1
          t2 = t0 - q*t1
          r0 = r1
          r1 = r2
          s0 = s1
          s1 = s2
          t0 = t1
          t1 = t2
          i += 1
     g = r0
     u = s0
     v = t0
     a1 = t1*(-1)**(i-1)
     b1 = s1*(-1)**i
     q,r = a / g
     if r.norm() > 0:
          g = a.one()
     else:
          q,r = b / g
          if r.norm() > 0:
               g = b.one()
     g = g.trim()
     an = g.dat[-1]
     epsilon = 1e-8
     if abs(an) > epsilon:
          g = g * (1/an)
     return g

def gcd(a,b):
     g = gcd_nonrecursive(a,b)
     return g

def lcm(a,b):
     p,q = (a*b) / gcd(a,b)
     return p
    
# https://docs.python.org/2/library/operator.html
class RationalPoly:
    def Reduce(self):
        if self.b.degree() == 0:
             return
        c = gcd(self.a,self.b)
        if c.degree() == 0:
             return
        aq,ar = self.a / c
        bq,br = self.b / c
        self.a = aq
        self.b = bq
        return
    def __init__(self,a,b):
        if b.degree() == 0:
             assert(b.dat[0] != 0)
        self.a = a
        self.b = b
        self.Reduce()
        return
    def __str__(self):
        s = '%s/%s' % (str(self.a),str(self.b))
        return s
    def __add__(self,q):
        a = self.a*q.b + q.a*self.b
        b = self.b*q.b
        return RationalPoly(a,b)
    def __neg__(self):
        a = -self.a
        b = self.b
        return RationalPoly(a,b)
    def __sub__(self,q):
        q2 = self + (-q)
        return q2
    def __mul__(self,q):
        a = self.a*q.a
        b = self.b*q.b
        return RationalPoly(a,b)
    def __div__(self,q):
        a = self.a*q.b
        b = self.b*q.a
        return RationalPoly(a,b)
    def __pow__(self,n):
        """
        n is a whole number
        >>> help(Rational.__pow__)
        """
        a = self.a**n
        b = self.b**n
        return RationalPoly(a,b)
    def __eq__(self,q):
        flag = (self.a*q.b == q.a*self.b)
        return flag
    def __ne__(self,q):
        return not (self == q)
