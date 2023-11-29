import numpy as np
from functools import reduce

from math import fmod,sqrt,pi

D = 3

# [1] @book{Hall13,
# author = "Hall, Brian C.",
# title = "Quantum Theory for Mathematicians",
# publisher = "Springer; 2013 edition",
# year = "2013"
# }

# https://en.wikipedia.org/wiki/Euler_method
def Euler_step(f,t,y,h):
    y = y + h*f(t,y)
    t = t + h
    return t,y

# https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
# Runge-Kutta RK4
def RK4_step(f,t,y,h):
    k1 = f(t,y)
    k2 = f(t + h/2, y + h*k1/2)
    k3 = f(t + h/2, y + h*k2/2)
    k4 = f(t + h, y + h*k3)
    y = y + 1/6.*h*(k1+2*k2+2*k3+k4)
    t = t + h
    return t,y

# derivative of f at x with increment h
deriv = lambda h: lambda f: lambda x: (f(x+h)-f(x))/h

# partial derivative of A(x) with respect to x_i
# with increment h
def grad_i(A,x,i,h):
    I = np.identity(len(list(x)),dtype=np.float64)
    v = I[i]
    x2 = list(np.array(x,dtype=np.float64) + h*v)
    val = (A(x2) - A(x))/h
    return val

# poisson bracket of f and g
def bracket(f,g):
    def h(L):
        dx = 1e-5
        s = 0
        n = int(len(L)/2)
        for j in range(n):
            a = grad_i(f,L,j,dx)*grad_i(g,L,n+j,dx)
            b = grad_i(f,L,n+j,dx)*grad_i(g,L,j,dx)
            s = s + a - b
        return s
    return h

# Do not change. This is Hamilton's equations
# from symplectic manifolds (smooth manifolds)
# and classical dynamics.
def F(t,y):
    L = list(y)
    n = int(len(L)/2)
    dx = 1e-5
    dxdt = [0]*n
    dpdt = [0]*n
    for j in range(n):
        dxdt[j] = grad_i(H,L,n+j,dx)
        dpdt[j] = -grad_i(H,L,j,dx)
    dydt = dxdt + dpdt
    return np.array(dydt,dtype=np.float64)

def sim(tmin,tmax,y0,dt,verbose=False):
    epsilon = dt
    TT = [] # store time t
    YY = [] # store (x(t),p(t))
    t = tmin
    y = y0
    print(f"t = {t}")
    #print(f" y = {list(y)}")
    print(f" Conservation of H: H(y) = {H(y)}")
    epsilon = dt
    while t <= tmax:
        TT.append(t)
        YY.append(y)
        # for accuracy of conserved quantity,
        # we should use a good ode_step. Here we
        # use RK4 (Runge-Kutta4) instead of Euler.
        t,y = RK4_step(F,t,y,dt)
        if verbose and fmod(t,.5) < epsilon:
            print(f"t = {t}, H0(y) = {H0(y)}")
    print(f"t = {t}")
    #print(f" y = {list(y)}")
    print(f" Conservation of H: H(y) = {H(y)}")

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    N = int(len(YY[0])/(2*D))
    print(f"N = {N}")
    for i in range(N):
        pts = list(map(lambda v: YY[v][D*i:D*(i+1)],
                   range(len(YY))))
        xx = list(map(lambda tup: tup[0], pts))
        yy = list(map(lambda tup: tup[1], pts))
        zz = list(map(lambda tup: tup[2], pts))
        ax.plot3D(xx,yy,zz)
    plt.show()
    return

############################################
#
# define conserved quantities
def H0(L):
    freq = 2 # frequency of oscillation
    omega = 2*pi*freq # angular frequency
    m = 3 # mass
    k = m*omega**2 # spring constant

    E = 0 # initial total energy to zero
    # kinetic energy
    KE = lambda p: np.linalg.norm(p)**2/(2*m)
    # potential energy between particle 0 and 1
    V = lambda x0,x1: \
            -m/np.linalg.norm(x1-x0)
    n = int(len(L)/2)
    N = int(n/D)
    X = [] # list of positions for particles
    P = [] # list of momentums for particles
    for i in range(N):
        # generalized position of i-th particle
        x_i = np.array(L[i*D:(i+1)*D],
                       dtype=np.float64)
        # append to list of particles
        X.append(x_i)
        # generalized momentum of i-th particle
        p_i = np.array(L[i*D+n:(i+1)*D+n],
                       dtype=np.float64)
        P.append(p_i)
        # hamiltonian function of total energy
        E_i = KE(p_i)
        # total energy
        E = E + E_i
    # add attraction potential between X[0] and X[1]
    # to total energy

    # conserve total energy val
    val1 = [E + V(X[0],X[1])]

    # conserve momentum
    val2 = list(sum(P).flatten())

    # conservation of all quantities
    val = np.array(val1 + val2,dtype=np.float64)
    return val

# combine two conserved quantities into one
# conserved quantity
def H(L):
    return np.linalg.norm(H0(L))

#
# initial conditions y0 = [x0,x1,x2,p0,p1,p2].
# we could also simulate n particles with
# y0 = [x00,x01,x02, # x's
#       x10,x11,x12,
#       ...,
#       xn0,xn1,xn2,
#       p00,p01,p02, # p's
#       p10,p11,p12,
#       ...,
#       pn0,pn1,pn2]
# with x = [x00,x01,x02,x10,x11,x12,...,xn0,xn1,xn2]
# and p = [p00,p01,p02,p10,p11,p12,...,pn0,pn1,pn2]'

# two-body problem, n = 2
y0 = np.array([1,0,0, # x0 particle 0 position
               1,1,1, # x1 particle 1 position
               0,0,1, # p0 particle 0 momentum
               1,1,1, # p1 particle 1 momentum
               ],dtype=np.float64)

tmin = 0 # start time
tmax = 5 # end time
dt = .005 # time increment
sim(tmin,tmax,y0,dt,verbose=True)
#
##############################################


