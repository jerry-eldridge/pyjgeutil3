from math import exp
import calculus as calc

def Gamma(t,dx=0.001,oo=100):
    """
    Gamma(t,dx,oo) or Gamma(t) is gamma function of t,
    a real or complex number. Gamma(n+1) = n! approximately.
    Eg, Gamma(4), Gamma(4.5), Gamma(complex(1,1)).
    Gamma function interpolates the factorial function
    as described above.
    """
    f = lambda x: x**(t-1)*exp(-x)
    c = 1
    I1 = calc.Integral(f,c,oo,dx)
    I2 = calc.Integral(f,1.0/oo,c,dx)
    return I1 + I2
    
def RiemannZeta(s,dx=0.001,oo=100):
    """
    RiemannZeta(s,dx,oo) or RiemannZeta(s) is the riemann-zeta
    function Sum_{n} 1/n**s where if s = 1 it is the divergent
    harmonic series. Eg, RiemannZeta(2), RiemannZeta(complex(1,1)).
    """
    f = lambda x: 1.0*x**(s-1)/(exp(x)-1)
    c = 1 # some real number between 0 and oo
    I1 = calc.Integral(f,c,oo,dx)
    I2 = calc.Integral(f,1.0/oo,c,dx)
    return (I1+I2)/Gamma(s)

def log(t,dx=0.001):
    """
    Logarithm function (approximation). log(t) for t >= 1 real number.
    """
    f = lambda x: 1.0/x
    return calc.Integral(f,1,t,dx)

def factorial(n):
    """
    factorial(n) = n! = n*(n-1)*(n-2)*...*3*2*1
    with defined 0! = 1. Gamma(n+1) = n! though we define
    it integers more precisely instead as
    factorial(n) = n*factorial(n-1) and factorial(0) = 1
    and factorial(1) = 1.
    """
    if n <= 1:
        return 1
    else:
        return n*factorial(n-1)

def C(n,k):
    """
    C(n,k) - n "choose" k - the number of k-combinations
    of an n-set, or the number of ways to choose a k-subset
    from an n-set.
    Approximates C(n,k) using the factorial(n) function
    approximation that uses Gamma function.
    """
    return 1.0*factorial(n)/(factorial(k)*factorial(n-k))

def P(n,k):
    """
    P(n,k) - the number of k-permutations of an n-set.
    """
    return 1.0*factorial(n)/factorial(n-k)
