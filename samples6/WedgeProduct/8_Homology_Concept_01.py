import diff_forms as dff

import sympy as sp

vn = sp.symbols('t,x,y,z')
t,x,y,z = vn
n0 = len(vn)
d = dff.d
Form = dff.Form
star = dff.star
curvature = dff.curvature
inner_k = dff.inner_k
g_k = dff.g_k
delta = dff.delta
Delta = dff.Delta
hodge_dirac = dff.hodge_dirac
box = Delta # for (t,x,y,z) space, d'alembertian operator

wpt = dff.WedgeProductTerm
names0 = ["d"+str(vn[i]) for i in range(len(vn))]

f0 = lambda t,x,y,z: x**2 + y*x*t + z*t**2
f1 = lambda t,x,y,z: x*y*t + z
a0 = wpt(f0(t,x,y,z),[],n0,names0)
a1 = wpt(f1(t,x,y,z),[],n0,names0)
A0 = Form([a0,a1],n0,names0).reduce()
print(f"A0 = {A0}")
F0 = d(A0)
print(f"F0 = d(A0) = {F0}")
omega1 = Form([wpt(t*z,[1],n0,names0)],n0,names0)
print(f"omega1 = {omega1}")
A2 = (F0 + omega1).reduce()
print(f"A2 = F0 + omega1 = {A2}")
F2 = d(A2)
print(f"F2 = d(A2) = {F2}")
omega2 = Form([wpt(x*z,[1,2],n0,names0)],n0,names0)
print(f"omega2 = {omega2}")
A4 = (F2 + omega2).reduce()
print(f"A4 = F2 + omega2 = {A4}")
F4 = d(A4)
print(f"F4 = d(A4) = {F4}")
omega3 = Form([wpt(t**2*x+y**3,[0,3,1],n0,names0)],
              n0,names0)
print(f"omega3 = {omega3}")
A6 = (F4 + omega3).reduce()
print(f"A6 = F4 + omega3 = {A6}")
F6 = d(A6)
print(f"F6 = d(A6) = {F6}")

# [1] https://en.wikipedia.org/wiki/D%27Alembert_operator
# d'Alembert operator denoted box
e = A0.L[0].expr
print(f"e = A0.L[0].expr = {e}")
# signature is [1,-1,-1,-1] for spacetime here
box = lambda e: sp.diff(e,t,t)-sp.diff(e,x,x)-\
        sp.diff(e,y,y)-sp.diff(e,z,z)
print(f"box(e) = {box(e)}")
print(f"Delta(A0) = {Delta(A0)}")
