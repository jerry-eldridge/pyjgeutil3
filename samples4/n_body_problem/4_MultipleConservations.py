import numpy as np

import n_body_problem as nbp

D = 3

# conserve two quantities val1 and val2
def H0(L):
    n = int(len(L)/2)
    x = L[:n]
    p = L[n:]
    val1 = x[0] + x[2] * p[0]
    val2 = x[1] * p[1]
    val = np.array([val1,val2],dtype=np.float64)
    return val

# combine two conserved quantities into one
# conserved quantity
def H(L):
    return np.linalg.norm(H0(L))

y0 = np.array([1,2,3, 4,1,6])
tmin = 0
tmax = 5
dt = .1
y = y0
t = tmin
while t <= tmax:
    print(f"t = {t}")
    print(f" y = {list(y.flatten())}")
    print(f" Conservation of H: H0(y) = "+\
          f"{list(H0(y))}")
    t,y = nbp.RK4_step(nbp.F(H),t,y,dt)
