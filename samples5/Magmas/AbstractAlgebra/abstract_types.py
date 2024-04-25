from typing import TypeVar,NewType
import mixed_fraction as mf
from copy import deepcopy
import language as lang

class MTstr:
    def __init__(self, s):
        self.val = s
        self.t = 'mystring'
        self.s = NewType(self.t, TypeVar(self.t))
        self.x = self.s(self.val)
    def __mul__(self, y):
        s = '(' + str(self.val) + '*' + str(y.val) + ')'
        return MTstr(s)
    def __str__(self):
        return self.val
    def __repr__(self):
        return str(self)
    def eval(self):
        try:
            return float(self.val)
        except:
            return self.val

def app(f,x):
    return f(x)

class MT:
    def __init__(self, x, t):
        self.val = x
        self.t = t
        self.s = NewType(self.t, TypeVar(self.t))
        self.x = self.s(self.val)
        self._d_add = {}
        self._d_mul = {}
        self.build()
    def define_add(self, tup, f):
        self._d_add[tup] = f
        return
    def define_mul(self, tup, f):
        self._d_mul[tup] = f
        return
    def eval(self):
        return self.x.eval()
    def __str__(self):
        return '('+str(self.val)+':'+str(self.t)+')'
    def __repr__(self):
        return str(self)
    def __add__(self, y):
        tup = (self.t, y.t)
        for key in self._d_add.keys():
            if tup == key:
                return self._d_add[key](self,y)
        print(f"Error: add, tup = {tup}")
        return MTstr('undefined')
    def __mul__(self, y):
        tup = (self.t, y.t)
        for key in self._d_mul.keys():
            if tup == key:
                return self._d_mul[key](self,y)
            # implement counting
            if tup[0] == 'myint':
                n = int(self.x.eval())
                if n >= 1:
                    s = y
                    for i in range(1,n):
                        s = s + y
                    return s
        print(f"Error: mul, tup = {tup}")
        return MTstr('undefined')
    def build(self):
        # define addition operators
        def f(self,y):
            return myreal(str(self.eval() + y.eval()))
        self.define_add(('myreal','myreal'),f)
        
        def f(self,y):
            a = self.x
            b = y.x
            c = a + b
            return mymixed(c.q,c.r,c.b)
        self.define_add(('mymixed','mymixed'),f)

        def f(self,y):
            a = self.x
            b = y.x
            c = a + b
            return mydipole(c.s,c.t)
        self.define_add(('mydipole','mydipole'),f)

        # somewhat difficult to define since
        # types use the value of key globally so
        # specifications should always define the
        # bound variable key.
        for key in mycurrency_names:
            def f(key):
                def g(self,y):
                    a = int(self.x.eval())
                    b = int(y.x.eval())
                    c = a + b
                    return mycurrency(key)(str(c))
                return g
            self.define_add((key,key),f(key))

        def f(self,y):
            x1 = self.x.val
            x2 = y.x.val
            x3 = x1 + x2
            q = x3.q
            r = x3.r
            b = x3.b
            precision = 10000
            val = precision*r/b
            r2 = int(val)
            b2 = precision
            return myucurrency(q,r2,b2) 
        self.define_add(("myucurrency","myucurrency"),f)

        # define multiplication operators
        def f(self,y):
            x1 = self.x.val
            x2 = y.x.val
            x3 = x1 * x2
            q = x3.q
            r = x3.r
            b = x3.b
            precision = 10000
            val = precision*r/b
            r2 = int(val)
            b2 = precision
            return myucurrency(q,r2,b2) 
        self.define_mul(("mypercent","myucurrency"),f)
        
        def f(self,y):
            return MT(self.x+y.x, 'mystring')
        self.define_mul(('mystring','mystring'),f)
        
        def f(self,y):
            a = self.x
            b = y.x
            c = a * b
            return mymixed(c.q,c.r,c.b)
        self.define_mul(('mymixed','mymixed'),f)
    
        def f(self,y):
            return self * myreal(y.x)
        self.define_mul(('myreal','mystring'),f)
        
        def f(self,y):
            try:
                return myreal(str(self.eval() * y.eval()))
            except:
                return myreal(str(self)+'*'+str(y))
        self.define_mul(('myreal','myreal'),f)
        
        def f(self,y):
            return MT(app(self.x,y),'myreal')
        self.define_mul(('myfunction','mystring'),f)
        
        def f(self,y):
            return MT(app(self.x,y.x),'myreal')
        self.define_mul(('myfunction','myreal'),f)
        
        def f(self,y):
            return MT(app(self.x,y),'myfunction')
        self.define_mul(('my-L-operator','myfunction'),f)
        
        def f(self,y):
            return MT(lambda z: app(self.x,app(y.x,z)),
                      'my-L-operator')
        self.define_mul(\
            ('my-L-operator','my-L-operator'),f)
        
        def f(self,y):
            return MT(lambda z: app(self.x,app(y.x,z)),
                    'myfunction')
        self.define_mul(\
            ('myfunction','myfunction'),f)
        
        def f(self,y):
            return app(self.x,y)
        self.define_mul(\
            ('myfunctional','myfunction'),f)
        
        return
    def __call__(self, y):
        return self.x(y)

myint = lambda s: MT(MTstr(s), 'myint')
myreal = lambda s: MT(MTstr(s),'myreal')
myfunc0 = lambda s: MT(s,'myfunction')
mymixed = lambda q,r,b: MT(mf.MixedFraction(q,r,b),
                'mymixed')

def myfunc(f):
    def F(x):
        x = x.eval()
        y = f(x)
        y = myreal(str(y))
        return y
    G = myfunc0(F)
    return G

R = lambda t: lambda s: MT(lambda z: z * s,t)
L = lambda t: lambda s: MT(lambda z: s * z,t)

def Integral0(f,a,b,dx):
     if a > b:
          return -Integral0(f,b,a,dx)
     x = a
     s = myreal(0)
     while x < b:
         s += f(myreal(x))*myreal(dx)
         x += dx
     return s

def Derivative0(f,x,dx):
     slope = 1.0*(f(x+dx)-f(x))/dx
     return slope

def Integral(f,a,b):
    return Integral0(f,a,b,dx=1e-1)

def measure(f):
    def F(A):
        val = Integral(f,*A)
        return val
    return F

def dform(A):
    def F(f):
        return measure(f)(A)
    return F

myfunctional = lambda f: MT(f,'myfunctional')

# define currency
# Note: you cannot use a dictionary to define
# mycurrency[name]. You must use a function
# mycurrency(name) defining the all variables in MT
# by bound variables.
mycurrency_names = ['mypenny','mynickel','mydime',
         'myquarter','myhalf','mydollar',
         'myfive','myten','myhundred']

mycurrency = lambda key: lambda s: MT(MTstr(s),key)

myucurrency = lambda q,r,b: MT(mymixed(q,r,b),
                    "myucurrency")
mypercent = lambda q,r,b: MT(mymixed(q,r*100,b*100),
                    "mypercent")
mydipole = lambda s,t: MT(lang.Dipole(s,t),
                'mydipole')

