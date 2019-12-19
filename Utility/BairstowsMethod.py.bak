import polynomial as poly
P = poly.Polynomial

import numpy as np
from copy import deepcopy
from math import sqrt

def clamp(x,lo,hi):
    return min(max(x,lo),hi)

# [Wikipedia,Bairstow Method]
# https://en.wikipedia.org/wiki/Bairstow%27s_method
#
# [Gerald and Wheatley] Applied Numerical Analysis,
# 5th Edition, Gerald, Curtis F & Wheatley, Patrick O.
# Addison-Wesley, 1994
def Iter(f,u,v,epsilon=1e-6):
    n = f.degree()
    x = P([0,1],'x')
    f.x = 'x'
    q = x**2 + x*(-u) + (-v)
    
    Q,r = f/q
    b = [0]*(n+1)
    L = deepcopy(Q.dat)
    L = L + [0]*clamp(n-1-len(L),0,n-1)
    L.reverse()
    i = n+1
    b[:i] = deepcopy(L)
    L = deepcopy(r.dat)
    L = L + [0]*clamp(2-len(L),0,2)
    L.reverse()
    b[i:i+2] = deepcopy(L)
    
    c = [0]*(n)
    c[0] = b[0]
    c[1] = b[1] + u*c[0]
    for i in range(2,n):
        c[i] = b[i] + u*c[i-1] + v*c[i-2]

    D = (c[n-2]*c[n-2]-c[n-1]*c[n-3])
    du = 1.0*((-b[n-1]*c[n-2]) - (-b[n]*c[n-3]))/D
    dv = 1.0*((-c[n-2]*b[n]) - (-c[n-1]*b[n-1]))/D
    u += du
    v += dv
    if (abs(du) < epsilon) and (abs(dv) < epsilon):
        flag = True
    else:
        flag = False
    return u,v,flag

def FindFactor(f,epsilon=1e-6,u=-2,v=-2):
    n = f.degree()
    flag = False
    for i in range(50):
        u,v,flag = Iter(f,u,v,epsilon=epsilon)
        if flag:
            break
    x = P([0,1],f.x)
    q = x**2 + x*(-u) + (-v)
    Q,r = f/q
    return [q,Q]

def factor(f,epsilon=1e-6,u=-2,v=-2):
    q,Q = FindFactor(f,epsilon=epsilon,u=u,v=v)
    if Q.degree() <= 2:
        return [q,Q]
    else:
        return [q] + factor(Q,epsilon=epsilon,u=u,v=v)

def roots(f,epsilon=1e-6,u=-2,v=-2):
    P = factor(f,epsilon=epsilon,u=u,v=v)
    R = []
    for p in P:
        # use quadratic formula to solve p = 0 for z's
        # and add roots to R
        if p.degree() == 1:
            b,a = p.dat[:2]
            z = 1.0*-b/a
            R.append(z)
        elif p.degree() == 2:
            c,b,a = p.dat[:3] # x**2 * a + x*b + c = 0
            D = b**2 - 4*a*c # discriminant
            if D == 0: # one real root
                z1 = -1.0*b/(2*a)
                R.append(z1)
            elif D > 0: # two real roots
                z1 = 1.0*(-b + sqrt(D))/(2*a)
                z2 = 1.0*(-b - sqrt(D))/(2*a) 
                R.append(z1)
                R.append(z2)
            else: # two complex roots
                i = complex(0,1)
                z1 = 1.0*(-b + sqrt(-D)*i)/(2*a)
                z2 = 1.0*(-b - sqrt(-D)*i)/(2*a) 
                R.append(z1)
                R.append(z2)
    return R

def roots_numpy(f):
    L = f.dat
    L.reverse()
    return list(np.roots(L))
    


