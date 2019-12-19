import physics_constants
from math import pi
from vectors import dotprod
from numpy import array,zeros,ones

# http://en.wikipedia.org/wiki/Potential_energy

def KE(m,v):
    """
    Kinetic Energy with mass m and velocity v
    """
    KE = 0.5*m*v**2
    return KE

def SpringPE(k_spring,x):
    """
    Spring potential energy given k_spring spring constant
    and change in x.
    """
    U = 0.5*k_spring*x**2
    return U

def GravitationalPE(m,M,r):
    """
    Gravitational Potential Energy given
    two masses M and m and gravitational constant G
    and distance between masses r.
    """
    epsilon = 1e-8
    if abs(r) < epsilon:
        r = epsilon
    G = physics_constants.gravitational_constant
    U = -1.0*G*m*M/r
    return U

def GravityPE(m,h):
    """
    Gravity Potential Energy (see also GravitationalPE(M,m,r)
    for universal Gravitational Potential Energy) on
    earth of object of mass m at altitude h.
    """
    g = -9.80665
    U = m*g*h
    return U

def ElectrostaticPE(Q,q,r):
    """
    Potential Energy between charges Q and q
    at a distance r
    """
    epsilon0 = physics_constants.vacuum_permittivity
    U = 1.0/(4*pi*epsilon0)*Q*q/r
    return U

def MagneticPE(m,B):
    """
    Magnetic potential energy with magnetic
    moment m (vector) and externally produced
    magnetic field B
    """
    U = -dotprod(array(m),array(B))
    return U

def demo():
    from matplotlib.pylab import show,plot

    def U_grav(m,x,bodies):
        U = 0
        for body in bodies:
            U_grav = GravitationalPE(m,body[0],abs(x-body[1]))
            U += U_grav
        return U

    def f(x):
        bodies = [ [100,5], [2000,3], [300,10] ]
        m = 30
        return U_grav(m,x,bodies)

    from numpy import arange
    x = list(arange(-20,20,1))
    y = map(f,x)
    plot(x,y)
    show()
    return



