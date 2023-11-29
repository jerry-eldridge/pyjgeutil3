import numpy as np
from functools import reduce

from math import fmod,sqrt,pi

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
def F(H):
    def G(t,y):
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
    return G


