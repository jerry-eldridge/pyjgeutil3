
# [1] https://en.wikipedia.org/wiki/Euclidean_algorithm
def gcd(a,b):
    if a == 0 and b == 0:
        return 1
    if a == 0 or b == 0:
        return max(a,b)
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

class Fraction:
    def __init__(self,a,b):
        a = int(a)
        b = int(b)
        c = gcd(a,b)
        self.a = int(a/c)
        self.b = int(b/c)
    def __add__(self,y):
        # a/b + c/d = a*d/b*d + b*c/b*d = (a*d+b*c)/b*d
        a = self.a
        b = self.b
        c = y.a
        d = y.b
        a2 = a*d + b*c
        b2 = b*d
        return Fraction(a2,b2)
    def __mul__(self,y):
        # a/b * c/d = a*c/b*d
        a = self.a
        b = self.b
        c = y.a
        d = y.b
        a2 = a*c
        b2 = b*d
        return Fraction(a2,b2)
    def __str__(self):
        s = f"({str(self.a)}/{str(self.b)})"
        return s
    def __repr__(self):
        return str(self)

class MixedFraction:
    def __init__(self,q,r,b):
        self.q = q
        self.r = r
        self.b = b
    def __add__(self,y):
        a = self.r + self.q*self.b
        b = self.b
        f1 = Fraction(a,b)
        c = y.r + y.q*y.b
        d = y.b
        f2 = Fraction(c,d)
        f3 = f1 + f2
        a2 = f3.a
        b2 = f3.b
        q4 = int(a2/b2)
        r4 = a2 % b2
        b4 = b2
        return MixedFraction(q4,r4,b4)
    def __mul__(self,y):
        a = self.r + self.q*self.b
        b = self.b
        f1 = Fraction(a,b)
        c = y.r + y.q*y.b
        d = y.b
        f2 = Fraction(c,d)
        f3 = f1 * f2
        a2 = f3.a
        b2 = f3.b
        q4 = int(a2/b2)
        r4 = a2 % b2
        b4 = b2
        return MixedFraction(q4,r4,b4)      
    def __str__(self):
        s = f"({self.q} {self.r}/{self.b})"
        return s
    def __repr__(self):
        return str(self)
