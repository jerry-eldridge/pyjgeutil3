
def gcd_recursive(a,b):
     """
     Recursive definition of gcd. Note
     for example if a = 3, and b = 100000,
     there will be lots of recursions and the
     recursion depth might be exceeded. Thus
     you need to use a,b such that the number
     of gcd calls to compute gcd(a,b) is not large.
"""
     a0 = abs(a)
     b0 = abs(b)
     a = min(a0,b0)
     b = max(a0,b0)
     if a == 0:
         return b
     return gcd(a,b-a)

#http://www.vcskicks.com/euclidean-gcd.php
def gcd_nonrecursive(a,b):
     a0 = abs(a)
     b0 = abs(b)
     a = min(a0,b0)
     b = max(a0,b0)
     while (a != 0 and b != 0):
          if a > b:
               a = a % b
          else:
               b = b % a
     if a == 0:
          return b
     else:
          return a

def gcd(a,b):
     return gcd_nonrecursive(a,b)

def lcm(a,b):
     return abs(a*b)/gcd(a,b)
# https://docs.python.org/2/library/operator.html
class Rational:
    def Reduce(self):
        c = gcd(self.a,self.b)
        a = self.a/c
        b = self.b/c
        self.a = a
        self.b = b
    def __init__(self,a,b):
        """
        n is a whole number
        >>> help(Rational.__pow__)
        """
        #assert(type(a)==type(2))
        #assert(type(b)==type(3))
        assert(b != 0)
        self.a = a
        self.b = b
        self.Reduce()
        return
    def __str__(self):
        s = '%d/%d' % (self.a,self.b)
        return s
    def __add__(self,q):
        a = self.a*q.b + q.a*self.b
        b = self.b*q.b
        return Rational(a,b)
    def __neg__(self):
        a = -self.a
        b = self.b
        return Rational(a,b)
    def __sub__(self,q):
        q2 = self + (-q)
        return q2
    def __mul__(self,q):
        a = self.a*q.a
        b = self.b*q.b
        return Rational(a,b)
    def __div__(self,q):
        a = self.a*q.b
        b = self.b*q.a
        return Rational(a,b)
    def __pow__(self,n):
        """
        n is a whole number
        >>> help(Rational.__pow__)
        """
        a = self.a**n
        b = self.b**n
        return Rational(a,b)
    def __eq__(self,q):
        flag = (self.a*q.b == q.a*self.b)
        return flag
    def __ne__(self,q):
        return not (self == q)
    def __lt__(self,q):
        flag = (self.a*q.b < q.a*self.b)
        return flag
    # norm for rationals
    def __abs__(self):
        a = abs(self.a)
        b = abs(self.b)
        return Rational(a,b)
    def real(self):
        return 1.0*self.a/self.b
    def set_real(self,x):
        epsilon = 1e-8
        if abs(x) > epsilon:
             sgn = x/abs(x)
        x = abs(x)
        s = str(x)
        # ignore the scientific notation
        L = s.split('.')
        assert(len(L)==2)
        f = lambda ch: ord(ch)-ord('0')
        L1 = map(f,list(L[0]))
        L1.reverse()
        L2 = map(f,list(L[1]))
        q = Rational(0,1)
        for i in range(len(L1)):
             q = q + Rational(L1[i]*10**i,1)
        for i in range(len(L2)):
             q = q + Rational(L2[i],10**(i+1))
        q.a *= sgn
        self.a = q.a
        self.b = q.b
        return q
