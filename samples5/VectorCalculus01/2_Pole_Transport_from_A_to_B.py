import numpy as np
from math import fmod,pi,sin,cos

import vector_calculus as vc

# Describe containers
# Container A
C_A = [10,3,4]
C_B = [20,1,3] 
A = vc.Container(center=C_A,
              radius=3)
B = vc.Container(center=C_B,
              radius=4)

tmin = 0
tmax = 1
N = 10
dx = vc.dist(C_A,C_B)/N
dt = 1/N
t = tmin
# transport quantity qty from center A.C to center B.C
curve = lambda t: vc.lerp(A.C,B.C,t)
qty = 10
while t < tmax:
    F = vc.F_helper(curve(t),qty)
    flx_A = A.qty(F)
    flx_B = B.qty(F)
    print(f"t = {t}, flx_A = {flx_A}, flx_B = {flx_B}")
    t = t + dt
