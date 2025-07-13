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
pullback = dff.pullback


wpt = dff.WedgeProductTerm
names0 = ["d"+str(vn[i]) for i in range(len(vn))]

f0 = lambda t,x,y,z: x**2 + y*x*t + z*t**2
f1 = lambda t,x,y,z: x*y*t + z
a0 = wpt(f0(t,x,y,z),[],n0,names0)
a1 = wpt(f1(t,x,y,z),[],n0,names0)
A0 = Form([a0,a1],n0,names0).reduce()

names_N = ['x','y','z']
names_M = ['u','v']
F_map = lambda u,v: [u**2,v,u-v**2]
# F*(omega) = Fs(omega)
Fs = dff.pullback(F_map,names_M,names_N)
names1 = ['d'+names_N[i] \
                   for i in range(len(names_N))]
omega = Form([
    wpt(y,[0,1],3,names1),
    wpt(z,[1,2],3,names1)],
    3,names1)
print(f"omega = {omega}")
tau = Fs(omega)
print(f"pullback(F)(omega) = Fs(omega) = {tau}")
