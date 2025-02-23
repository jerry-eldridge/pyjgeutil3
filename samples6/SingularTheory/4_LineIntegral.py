import sys
#sys.path.insert(0,"C:/Users/jerry/Desktop/AlgTopo/")

## import the file 'AT_singular_theory.py'
import AT_singular_theory as atst

import numpy as np

def line_integral(omega,f):
    s = 0
    for i in range(len(omega.S)):
        sigma = omega.S[i]
        facet1 = sigma**1
        facet2 = sigma**2
        orientation = omega.V[i].x
        A = facet1.P()[0]
        B = facet2.P()[0]
        ds = d(A,B)
        s = s + orientation*f(A)*ds
    return s

mu = lambda f: lambda omega: \
               line_integral(omega,f)

import numpy as np
d = lambda A,B: np.linalg.norm(np.array(B)-np.array(A))

C = [[0,0],[10,0],[10,10],[0,10]]
f = lambda A: 1

# define q-form omega
for i in range(len(C)):
    A = C[i]
    B = C[(i+1)%len(C)]
    pts = [A,B] # edge
    val = atst.S_q(1, atst.func(pts))*atst.R(1)
    if i == 0:
        omega1 = val
    else:
        omega1 = omega1 + val


# traverse omega in opposite direction for omega2
omega2 = -omega1

print(f"""
omega1 is a singular 1-chain or curve.
omega1 is just a square with length 10.

=========================================
omega1 = \n{omega1}"
=========================================

Calculating the integral of f along omega1.

Define omega2 = -omega1

This will be the length I of the curve omega1.

I = mu(f)(omega1) = {mu(f)(omega1)}

which is just the signed perimeter of omega.

=========================================
omega2 = -omega1 = \n{omega2}"
=========================================

Calculating the integral of f along omega2.

This will be the length I of the curve omega2.

I = mu(f)(omega2) = {mu(f)(omega2)}

which is just the signed perimeter of omega2.
This will relate to the perimeter of omega1 since
we changed the orientation of omega2 = -omega1.

Note:

I = mu(f)(omega2) = orientation * mu(f)(omega1)
""")
      
# define q-form omega
for i in range(1,len(C)):
    A = C[i]
    B = C[(i+1)%len(C)]
    O = C[0]
    pts = [O,A,B] # edge
    val = atst.S_q(2, atst.func(pts))*atst.R(1)
    if i == 1:
        omega3 = val
    else:
        omega3 = omega3 + val

omega4 = atst.bdy(omega3)

print(f"""
========================================
omega3 = \n{omega3}
======================================

=========================================
omega4 = bdy(omega3) = \n{omega4}
=========================================

Calculating the integral of f along omega2.

This will be the length I of the curve omega2.

I = mu(f)(omega4) = {mu(f)(omega4)}

which is just the signed perimeter of omega4 =
bdy(omega3). This will relate to the perimeter
of omega3.

""")
