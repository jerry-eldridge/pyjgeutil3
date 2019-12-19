from sympy import Matrix,symbols,Function,Symbol,zeros,sin,cos,sqrt,tan,atan2,acos, simplify, Function, solve, Derivative
from math import pi,fmod,tan,atan2,acos,sqrt

def Base(i,base, bits):
    L = []
    j = 0
    n = 0
    ii = i
    for j in range(bits):
        a = ii%base
        ii = int(ii/base)
        n = n + a*base**j
        L.append(a)
    L.reverse()
    return L
# Box operator (D'Alembert)
def box(eta,psi,alpha):
    global xx
    n = eta.shape[0]
    sm = 0
    for mu in range(n):
        for nu in range(n):
            sm = sm + eta[mu,nu]*Derivative(psi[alpha],Symbol(xx[mu]),Symbol(xx[nu]))
    return sm

def Christoffel1_s(g,c,a,b):
    global xx
    return simplify(0.5*(g[c,a].diff(Symbol(xx[b])) +
                g[c,b].diff(Symbol(xx[a])) +
                g[a,b].diff(Symbol(xx[c]))).expand())
def Christoffel1(g,c,a,b):
    global christoffel1
    try:
        return christoffel1[c,a,b]
    except:
        christoffel1[c,a,b] = Christoffel1_s(g,c,a,b)
        return christoffel1[c,a,b]
def Christoffel2_s(g,i,k,l):
    ginv = g.inv()
    s = 0
    n = g.shape[0]
    for m in range(n):
        s = s + 0.5*ginv[i,m]*Christoffel1(g,m,k,l)
    return simplify(s.expand())
def Christoffel2(g,i,k,l):
    global christoffel2
    try:
        return christoffel2[i,k,l]
    except:
        christoffel2[i,k,l] = Christoffel2_s(g,i,k,l)
        return christoffel2[i,k,l]
    
def covariant_deriv2(g,v,u,k):
    global xx
    sm = 0
    n = g.shape[0]
    for i in range(n):
        for j in range(n):
            sm = sm + v[i]*u[j]*Christoffel2(g,k,i,j) + \
                 v[i]*u[k].diff(Symbol(xx[i]))
    return sm
def covariant_deriv(g,j,u,i):
    global xx
    sm = 0
    n = g.shape[0]
    for j in range(n):
        for k in range(n):
            sm = sm + u[k]*Christoffel2(g,i,j,k) + \
                 u[i].diff(Symbol(xx[j]))
    return sm

def RectangularCoordinates(reset = True):
    global xx, christoffel1, christoffel2, riemanncurvature, riccitensor
    if reset:
        christoffel1 = {}
        christoffel2 = {}
        riemanncurvature = {}
        riccitensor = {}
    xx = ["x","y","z"]
    dx = ["dt","dx","dy","dz"]
    x,y,z = map(Symbol,xx)
    X = [x,y,z]
    J = zeros((3,3))
    for i in range(3):
        for j in range(3):
            J[i,j] = Derivative(X[i],Symbol(xx[j])).doit()
    g = J.T*J
    n = 3
    for a in range(n):
        for b in range(n):
            g[a,b] = simplify(g[a,b])
    print "g=\n",g
    print "Christoffel2 = "
    for i in range(n**3):
        L = Base(i,n,3)
        lam = L[0]
        mu = L[1]
        nu = L[2]
        s = "%s%s%s : %s" % (lam,mu,nu,Christoffel2(g,lam,mu,nu))
        print s

    u = Symbol("u")
    param = u
    for lam in range(n):
        lhs = Derivative(Symbol(xx[lam]),param,param)
        rhs = 0
        for mu in range(n):
            for nu in range(n):
                rhs = rhs - Christoffel2(g,lam,mu,nu)*\
                      Derivative(Symbol(xx[mu]),param)*\
                      Derivative(Symbol(xx[nu]),param)
        s = "%s == %s" % (lhs,rhs)
        print s
    return

def Spherical_x(r,theta,phi):
    x = r*sin(theta)*cos(phi)
    return x
def Spherical_y(r,theta,phi):
    y = r*sin(theta)*cos(phi)
    return y
def Spherical_z(r,theta,phi):
    return r*cos(theta)
def Spherical_r(x,y,z):
    return sqrt(x**2+y**2+z**2)
def Spherical_theta(x,y,z):
    return acos(z/Spherical_r(x,y,z))
def Spherical_phi(x,y,z):
    return atan2(y,x)

RectangularCoordinates(reset = True)

