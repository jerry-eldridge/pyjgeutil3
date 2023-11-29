import numpy as np
from functools import reduce

from math import fmod,sqrt,pi

import n_body_problem as nbp

D = 3

def sim(H,D,tmin,tmax,y0,dt,verbose=False):
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
        t,y = nbp.RK4_step(nbp.F(H),t,y,dt)
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
dist = lambda A,B: np.linalg.norm(B-A)

def H0(L):
    freq = 2 # frequency of oscillation
    omega = 2*pi*freq # angular frequency
    m = 3 # mass
    k = m*omega**2 # spring constant

    E = 0 # initial total energy to zero
    # kinetic energy
    KE = lambda p,m: np.linalg.norm(p)**2/(2*m)
    # potential energy between particle 0 and 1
    m1 = 5.4
    m2 = 4.0
    G = 10
    m = [m1,m2]
    V = lambda x0,x1,m0,m1: G*m0*m1/dist(x0,x1)
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
        E_i = KE(p_i,m[i])
        # total energy
        E = E + E_i
    # add attraction potential between X[0] and X[1]
    # to total energy
    E = E + V(X[0],X[1],m[0],m[1])
    
    # conserve total energy val
    val1 = [E]

    # conserve momentum
    val2 = list(sum(P).flatten())

    # conservation of all quantities
    val = np.array(val1 + val2,dtype=np.float64)
    return val

# combine two conserved quantities into one
# conserved quantity

def H(L):
    return np.linalg.norm(H0(L)-H0_y0)**2+100

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
H0_y0 = H0(y0)

tmin = 0 # start time
tmax = 10 # end time
dt = .01 # time increment
sim(H,D,tmin,tmax,y0,dt,verbose=True)
#
##############################################


