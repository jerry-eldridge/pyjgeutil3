import matplotlib.pyplot as plt

import vector_calculus as vc

clamp = lambda x,lo,hi: min(hi,max(lo,x))

BIGDATA = r"./"

fn_obj_1 = BIGDATA + "Sphere-01.obj"
A = vc.Container_3D_Object(fn_obj_1)
A.create()
AC = A.C

A1 = [0,0,-100]
A2 = [0,0,150]
amount = 1000
tmin = 0
tmax = 1
t = tmin
N = 50
dx = vc.dist(A1,A2)/N
dt = 1/N
T = []
Flx = []
flx_max = abs(5*amount)
while t < tmax:
    ri = vc.lerp(A1,A2,t)
    T.append(ri[2])
    F = vc.F_helper(ri,amount)
    flx = A.flux(F)
    flx2 = clamp(flx, -flx_max, flx_max)
    Flx.append(flx2)
    t = t + dt

plt.plot(T,Flx,'b')
plt.title(f"Flux(t)")
plt.xlabel(f"z(t)")
plt.ylabel(f"Flux(F)")
plt.show()


