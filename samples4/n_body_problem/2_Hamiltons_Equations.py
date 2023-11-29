import numpy as np

import n_body_problem as nbp

D = 3

def H(L):
    n = int(len(L)/2)
    x = L[:n]
    p = L[n:]
    val = x[0] + x[2] * p[0]
    return val

y0 = np.array([1,2,3, 4,1,6])
tmin = 0
tmax = 5
dt = .1
y = y0
t = tmin
while t <= tmax:
    print(f"t = {t}")
    print(f" y = {list(y)}")
    print(f" Conservation of H: H(y) = {H(y)}")
    t,y = nbp.Euler_step(nbp.F(H),t,y,dt)
