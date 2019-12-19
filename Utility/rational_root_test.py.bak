import polynomial as P
import integer_UFD as IU
import Rational as QQ

def EvalPoly(p,x):
    Q = QQ.Rational
    s = Q(0,1)
    for i in range(len(p.dat)):
        ai = p.dat[i]
        a = x**i * Q(ai,1)
        s += a
    return s        

def factor(p):
    """
    factor(p) - returns a list of polynomials and
    so print with L = factor(p) and print map(str,L)
    but if len(L) > 0, print L[0] and L[0] and L[i]
    are polynomial class types. This uses
    the rational root test and only finds factors
    that are binomials with rational roots and
    a remaining polynomial to factor. That is,
    p = (x**2 * 1 + x * 1 + 1)**2 would present
    problems for factor(p).
    """
    a = p.dat[0]
    b = p.dat[-1]
    L = IU.rational_factors(a,b)
    Q = QQ.Rational
    Polynomial = P.Polynomial
    R = map(lambda tup: Q(tup[0],tup[1]), L)
    roots = []
    for x in R:
        s = EvalPoly(p,x)
        if s == Q(0,1):
            roots.append(x)
            break
    x = Polynomial([0,1],p.x)
    F = []
    if len(roots) > 0:
        x0 = roots[0]
        # define factor q
        q = x * x0.b + -x0.a
        # convert polynomial p in ZZ[x] to p2 in QQ[z]
        L2 = p.dat
        L3 = map(lambda a: Q(a,1), L2)
        p2 = Polynomial(L3,p.x)       
        a,b = p / q
        return [q] + factor(a)
    else:
        return [p]
