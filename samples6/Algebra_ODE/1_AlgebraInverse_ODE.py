import numpy as np
import matplotlib.pyplot as plt

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

# implement a*b = 1. Think of multiset to multiset
# function. Think of a*b = 1 as {a:1,b:1} -> {a:0,b:0}.
# What about a*a*b? Then a*a*b = a*1 = a or
# {a:2,b:1} -> {a:1,b:0}.

def f(t,y):
    a,b = list(y)
    rab = .3
    da_dt = -rab*a*b
    db_dt = -rab*a*b
    dydt = [da_dt, db_dt]
    return np.array(dydt)

a0 = 2
b0 = 1
y = np.array([a0,b0])
tmin = 0
tmax = 40
dt = 1
t = tmin
T = []
A = []
B = []
while t < tmax:
    T.append(t)
    a,b = list(y)
    A.append(a)
    B.append(b)
    t,y = RK4_step(f,t,y,dt)

fig,axs = plt.subplots(2)
axs[0].plot(T,A,label='A')
axs[1].plot(T,B,label='B')
axs[0].legend()
axs[1].legend()
axs[0].set_title("ODE a*a*b using a*b = 1")
axs[0].set_xlabel("a")
axs[1].set_xlabel("b")
axs[0].set_ylabel("a*b")
plt.show()
