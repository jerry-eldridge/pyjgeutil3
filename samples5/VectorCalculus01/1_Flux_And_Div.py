import numpy as np
from math import fmod,pi,sin,cos

import vector_calculus as vc

r0 = [1,0,0]
r1 = [-1,0,0]
F = lambda r: vc.F_helper(r0,5)(r) + vc.F_helper(r1,-10)(r)

r = [0,0,0]
dr = [.1]*3
print(f"r = {r}")
print(f"F(r) = {F(r)}")

R = 15
print(f"Formula: area(Ball(R)) = {4*pi*R**2}")
print(f"Integral: area(Ball(R)) = "+\
      f"{vc.sphere_surface_area(R)}")
dV = (4/3)*pi*R**3
flx = vc.flux(F,R)(r)
print(f"divergence = {flx/dV}")
print(f"div(F)(r) = {vc.div(F,r,dr)}")
print(f"flux(F,R)(r) = {flx}")
print(f"div(F)*dV = {vc.div(F,r,dr)*dV}")
