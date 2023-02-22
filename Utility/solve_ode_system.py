import numpy as np

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

# Solves d/dt y(t) = f(t,y(t)) for y(t)
def Solver(f,tmin,tmax,dt,y0,step):
    assert(tmin <= tmax)
    assert(dt > 0)
    t = tmin
    y = y0
    T = []
    Y = []
    while t <= tmax+dt:
        T.append(t)
        Y.append(y)
        t,y = step(f,t,y,dt)
    return T,Y

def Solve_Euler(f,tmin,tmax,dt,y0):
    T,Y = Solver(f,tmin,tmax,dt,y0,Euler_step)
    return T,Y

def Solve_RK4(f,tmin,tmax,dt,y0):
    T,Y = Solver(f,tmin,tmax,dt,y0,RK4_step)
    return T,Y

def Solve(f,tmin,tmax,dt,y0,name="None"):
    if name == "RK4":
        #print("RK4")
        T,Y = Solve_RK4(f,tmin,tmax,dt,y0)
    elif name == "Euler":
        #print("Euler")
        T,Y = Solve_Euler(f,tmin,tmax,dt,y0)
    else:
        print("Error: select 'RK4' or 'Euler'")
        T,Y = [],[]
        
    return T,Y
