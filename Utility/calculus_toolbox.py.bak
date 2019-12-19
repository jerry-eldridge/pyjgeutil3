"""
calculus_toolbox.py - implements the Calculus 'toolbox'
referred to in:

"Level Set Methods and Dynamic Implicit Surfaces",
Stanley Osher, Ronald Fedkiw, Applied Mathematical Sciences,
Volume 153, Springer

The 'toolbox' mentioned the Heaviside function and Dirac-Delta
function and a method to compute the Volume integral and
Surface Integral of a function.

"""
from geometry_toolbox import norm,grad

from numpy import array,zeros,arange
from math import pi,sin,cos,sqrt

def H(x):
    """
    Heaviside function
    """
    global dx
    epsilon = 1.5*dx
    if x < -epsilon:
        return 0
    elif (-epsilon <= x) and (x <= epsilon):
        return 0.5 + x/(2*epsilon) + 1.0/(2*pi)*sin(pi*x/epsilon)
    elif epsilon < x:
        return 1

def DiracDelta(x):
    """
    Delta-Dirac function is d/dx H(x) where H(x) is
    the Heaviside function. The integral of the Dirac-Delta
    function should be always 1.0 for any dx.
    """
    global dx
    epsilon = 1.5*dx
    if x < -epsilon:
        return 0
    elif (-epsilon <= x) and (x <= epsilon):
        return 1.0/(2*epsilon) + 1.0/(2*epsilon)*cos(pi*x/epsilon)
    elif epsilon < x:
        return 0

def Integral(f,a,b,dx):
    """
    Definite Integral of f on interval [a,b] incrementing
    by dx.

    Note a recursive definition can not be used since
    Python stack limit. Instead the integral was summed up
    directly.
    """
    if a >= b:
        return 0
    x = a
    S = 0
    while (x <= b):
        S += f(x)*dx
        x += dx
    return S
        
def f(x):
    """
    Some function
    """
    return 0.04*x**2 - 4*x* + 5

def Phi_Ellipse(X):
    """
    Implicit function of an ellipse at (50,50) of
    major minor axes of 100 and 200.
    """
    x,y = X
    cx,cy = [250,250]
    global a,b
    phi = 1.0*(x-cx)**2/a**2 + 1.0*(y-cy)**2/b**2 - 1
    return phi

def Phi(X):
    return Phi_Ellipse(X)

def chi_interior(f):
    def g(x):
        if f(x) <= 0:
            return 1
        else:
            return 0
    return g
def chi_exterior(f):
    def g(x):
        if f(x) > 0:
            return 1
        else:
            return 0
    return g

def VolumeIntegral(phi,px,py):
    global dx
    xmin,xmax,dx = px
    ymin,ymax,dy = py
    fxy = lambda x,y: 1-H(phi([x,y]))
    x = xmin
    S = 0
    while x < xmax:
        y = ymin
        while y < ymax:
            S += fxy(x,y)*dx*dy
            y += dy
        x += dx
    return S

def SurfaceIntegral(f,phi,px,py):
    global dx
    xmin,xmax,dx = px
    ymin,ymax,dy = py
    def Phi3d(X,i,j,k):
        x = i*dx
        y = j*dy
        z = k*0
        return Phi([x,y])
    def fxy(x,y):
        val1 = f([x,y])
        val2 = DiracDelta(Phi([x,y]))
        val3 = norm([
            grad(Phi3d,[dx,dy,0.1])[0](None,int(x/dx),int(y/dy),0),
            grad(Phi3d,[dx,dy,0.1])[1](None,int(x/dx),int(y/dy),0),
            grad(Phi3d,[dx,dy,0.1])[2](None,int(x/dx),int(y/dy),0)
            ])
        return val1*val2*val3
    
    x = xmin
    S = 0
    while x < xmax:
        y = ymin
        while y < ymax:
            S += fxy(x,y)*dx*dy
            y += dy
        x += dx
    return S  
