from copy import deepcopy
from math import sqrt,acos

class Polynomial:
    def __init__(S,L,x):
        """
        p = Polynomial([1,2,0,4],'x')
        """
        S.dat = deepcopy(L)
        S.n = len(L)
        S.x = x
        S.type = "Polynomial"
        return
    def __str__(S):
        """
        convert polynomial p to str say for "print p"
        p = Polynomial([1,2,0,4],'x')
        print p
        >>> (4*x**3+0*x**2+2*x**1+1*x**0)
        """
        s = ''
        if len(S.dat) < 1:
            return None
        if len(S.dat) == 1:
            return str(S.dat[0])
        for i in range(len(S.dat)-1,-1,-1):
            u = str(S.dat[i])+'*'
            if u == '1*':
                u = ''
            if u == '0*':
                t = ''
            elif i == 0:
                t = '%s + ' % (str(S.dat[i]))
            elif i == 1:
                t = '%s%s + ' % (u,S.x)
            else:
                t = '%s%s**%d + ' % (u,S.x,i)
            s += t
        if s == '':
            return '0 + '
        s = "("+s[:-3]+")"
        return s
    def degree(S):
        """
        p.degree() - degree of polynomial p
        This is not quite implemented. Now it
        returns the length of S.dat but should
        be the highest index plus one of a non-zero
        coefficient.
        """
        S = S.trim()
        S.n = len(S.dat)
        deg = S.n - 1
        return deg
    def trim(S,epsilon=1e-8):
        def f(x):
            if abs(x)>epsilon:
                return False
            else:
                return True
        n = len(S.dat)
        for i in range(S.n-1,-1,-1):
            if f(S.dat[i]):
                n -= 1
            else:
                break
        if n == 0:
            return S.zero()
        q = Polynomial(S.dat[:n],S.x)
        return q
    def add(S,p):
        """
        p + q - adds polynomial p to q
        This is polynomial addition as well as the
        vector space addition.
        """
        # if S.x == p.x then add
        # else one could make p.x a constant polynomial
        # in S.x though unclear about the details
        assert(S.x == p.x)
        n2 = max(S.n,p.n)
        q = Polynomial([0]*n2,S.x)
        # see which is polynomial list is longer
        # copy longer end and add common terms
        if p.n > S.n:
            for i in range(p.n):
                q.dat[i] = p.dat[i]
            for i in range(S.n):
                q.dat[i] += S.dat[i]
        else:
            for i in range(S.n):
                q.dat[i] = S.dat[i]
            for i in range(p.n):
                q.dat[i] += p.dat[i]
        q = q.trim()
        return q
    def __add__(S,p):
        """
        p + q - adds polynomial p to q
        This is polynomial addition as well as the
        vector space addition.
        """
        x = Polynomial([0,1],'x')
        if type(p) == type(x):
            return S.add(p)
        else:
            # when p is a scalar
            q = Polynomial([p],S.x)
            return S.add(q)
    def smul(S,a):
        """
        p.smul(a) does a*p where a is a scalars
        where polynomials are a vector space.
        """
        # multiply a times each term in polynomial list dat
        # a problem might occur in computing ai*a
        # if ai is a polynomial and a a rational number
        # for now, I set this to a*ai
        p = Polynomial(map(lambda ai: ai * a, S.dat),S.x)
        p = p.trim()
        return p
    def mul(S,p):
        assert(S.x == p.x)
        n2 = p.n + S.n
        q = Polynomial([0]*n2,S.x)
        N = n2
        M = p.n
        for t in range(N):
            I = 0
            for tau in range(M):
                support = (t - tau >= 0) and (t - tau < S.n)
                if support:
                    I += p.dat[tau]*S.dat[t-tau]
            q.dat[t] = I
        q = q.trim()
        return q
    def __mul__(S,a):
        """
        p * q - multiplies polynomial p to q
        This is polynomial multiplication or if
        q is a scalar its scalar multiplication in
        vector space of polynomials.
        """
        x = Polynomial([0,1],'x')
        try:
            t = a.type
        except:
            t = ''
        if t == '':
            return S.smul(a)
        else:
            return S.mul(a)
    def __neg__(S):
        # negative polynomial
        return S.smul(-1)
    def __sub__(S,p):
        assert(S.x == p.x)
        q = S + -(p)
        q = q.trim()
        return q
    # https://en.wikipedia.org/wiki/Polynomial_long_division
    def lead(S):
        # S = S.trim() is assumed before
        x = Polynomial([0,1],S.x)
        p = x**S.degree() * S.dat[-1]
        return p        
    def __div__(S,d):
        assert(S.x == d.x)
        x = Polynomial([0,1],S.x)
        if d.degree() == 0:
            assert(d != S.zero())
            q = S
            r = x*0
            return (q,r)
        q = S.zero()
        r = S
        d = d.trim()

        while (r != S.zero()) and (r.degree() >= d.degree()):
            r = r.trim()
            rl = r.lead()
            dl = d.lead()
            k = rl.degree() - dl.degree()
            a = 1.0*rl.dat[-1]/dl.dat[-1]
            t = x**k * a
            q = q + t
            r = r - t * d
        q = q.trim()
        return (q,r)
    def __pow__(S,n):
        assert(n >= 0)
        p = Polynomial([1],S.x)
        for i in range(n):
            p *= S
        return p
    def __eq__(S,p):
        epsilon=1e-8
        flag = norm(S-p)<epsilon
        return flag
    def zero(S,x='x'):
        return Polynomial([0],x)
    def one(S,x='x'):
        return Polynomial([1],x)
    def norm(S):
        I = 0
        for i in range(S.n):
            I += S.dat[i]**2
        return sqrt(I)
    def inner(S,p):
        return norm(S-p)
    def angle(S,xp):
        A = S.norm()
        B = xp.norm()
        epsilon = 1e-6
        if A*B < epsilon:
            return 0
        theta = acos(S.inner(xp)/(A*B)) # radians
        return theta
    def normalize(S):
        A = S.norm()
        if A < epsilon:
            return S
        else:
            p = S.smul(1/A)
            return p
    def Round(S):
        p = Polynomial(map(round,S.dat),S.x)
        return p
    def down(S):
        p = Polynomial(S.dat[::2],S.x)
        return p
    def up(S):
        p = Polynomial([0]*S.n*2,S.x)
        for i in range(p.n):
            p.dat[i] = S.dat[i/2]
        return p
    def rotate(S,val):
        assert(type(val) == type(3))
        L = map(lambda i: S.dat[(i-val+S.n)%(S.n)],range(S.n))
        p = Polynomial(L,S.x)
        return p
    def thresholdsmall(S,thresh):
        def f(i):
            if abs(S.dat[i]<thresh):
                return 0
            else:
                return round(S.dat[i])
        L = map(f,range(S.n))
        p = Polynomial(L,S.x)
        return p
    def nonzero(S):
        def f(x):
            epsilon = 1e-8
            if abs(x)>epsilon:
                return 1
            else:
                return 0
        return sum(map(f,S.dat))   
