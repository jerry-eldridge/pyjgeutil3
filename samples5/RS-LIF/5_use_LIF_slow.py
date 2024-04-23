import numpy as np
from math import cos,pi,fmod
import matplotlib.pyplot as plt

import scipy.optimize as so

## Delta-Dirac function is d/dx H(x) where H(x) is
## the Heaviside function. The integral of the Dirac-Delta
## function should be always 1.0 for any dx.
def DiracDelta(x,dx=0.1):
     epsilon = 1.5*dx
     if x < -epsilon:
         return 0
     elif (-epsilon <= x) and (x <= epsilon):
         return 1.0/(2*epsilon) + \
                1.0/(2*epsilon)*cos(pi*x/epsilon)
     elif epsilon < x:
         return 0

################################################
# solve_ode_system.py excerpt

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
#####################################################

class LIF:
    def __init__(self, v_init, vth, I, dt, du, C, R):
        self.C = C
        self.R = R
        self.v_init = np.array([v_init])
        self.vth = vth
        self.v = self.v_init
        self.dt = dt
        self.du = du # charge pulses width
        self.t = 0
        self.spike_out = np.zeros(self.v_init.shape)
        self.I_inj = lambda t: I(self,t)
        self.nspikes = 0
    def get_nspikes(self):
        return self.nspikes
    def set_nspikes(self,val):
        self.nspikes = val
        return
    def get_v(self):
        return self.v[0]
    def f(self,t,y):
        dvdt = np.zeros(y.shape)
        v = y.copy()
        current = self.I_inj(t)
        for i in range(y.shape[0]):
             dvdt = (-v/self.R +\
                        current)/self.C
        dydt = dvdt
        return dydt
    def step(self):
        y = self.v
        self.spike_out = np.zeros(y.shape)
        t,y = RK4_step(self.f,self.t,y,self.dt)
        self.t = t
        self.v = y
        flags = self.v >= self.vth
        n = len(y)
        if flags[0]:
             self.spike_out[0] = 1
             self.set_nspikes(self.get_nspikes() + 1)
             self.v[0] = self.v_init[0]
        return

class Dense:
    def __init__(self,n,m):
        self.g = np.zeros((n,m),dtype=np.float32)
    def set_g(self,i,j,g):
        self.g[i,j] = g
    def unset_g(self,i,j):
        self.g[i,j] = 0
    def get_g(self,i,j):
        return self.g[i,j]

def I_helper(t,q,T,du):
    val = 0
    for i in range(len(T)):
        ti = T[i]
        val_i = q*DiracDelta(t-ti,du)
        val = val + val_i
    return val

def I_multi(L):
     def I(net,t):
          vals = 0
          for i in range(len(L)):
               qi = L[i][0]
               Ti = L[i][1]
               val_i = I_helper(t,qi,Ti,net.du)
               vals = vals + val_i
          vec = np.array([vals])
          return vec
     return I

# the indicator function for I = [a,b]
def indicator(I):
    def f(t):
        a,b  = I
        if a <= t and t <= b:
            return 1
        else:
            return 0
    return f

# simple function y = Sum_i a(i)*indicator_I(I_i)
# where Js is a list of [a(i),I_i].
def simple(Js):
    def f(t):
        val = 0
        for i in range(len(Js)):
            vs,Ii = Js[i]
            vali = vs*indicator(Ii)(t)
            val = val + vali
        return val
    return f
     
dt0 = .01
du0 = .3
tmax = 20
ni = 2
no = 1
nabla_t = .2
c_max = 2
gamma = .3
xtol = .01
ftol = 0.05
maxiter = 20

def myrange(q,a,b,dt):
     return (q,np.arange(a,b+dt,dt))

def d(x,y):
     return np.linalg.norm(np.array(y)-np.array(x))

# create ni = 2 input leaky integrate and fire
# neurons
I1 = I_multi(L=[myrange(q=.6,a=1,b=7,dt=1),
                 myrange(q=.1,a=8,b=11,dt=1)])
I2 = I_multi(L=[myrange(q=.9,a=2,b=13,dt=2)])
vth0 = 0.5
lif1 = LIF(v_init=0,
          vth=vth0, I = I1, dt=dt0, du=du0,
           C=.1,
           R=1)

lif2 = LIF(v_init=0,
          vth=vth0, I = I2, dt=dt0, du=du0,
           C=.3,
           R=2)

# create synaptic Dense(ni,no) network between ni = 2
# input neurons and no = 1 output neurons
dense = Dense(ni,no)

# For the output neuron, sum up input neurons using
# formula I3 = g00*V1 + g10*V2

# Kirchoff's rule of additive currents
I3 = lambda net,t: dense.get_g(0,0)*lif1.get_v() +\
     dense.get_g(1,0)*lif2.get_v()

# create output neuron using that current I3
lif3 = LIF(v_init=0,
          vth=vth0, I = I3, dt=dt0, du=du0,
          C=.1,R=2)

clamp0 = lambda x,a,b: max(a,min(x,b))
c = lambda x: clamp0(x,0,c_max)

def F(X,verbose=False, plot=False):
     global y_a, lif1, lif2, dense, y_p

     lif1.v = lif1.v_init
     lif1.nspikes = 0
     lif1.t = 0
     lif2.v = lif2.v_init
     lif2.nspikes = 0
     lif2.t = 0
     lif3.v = lif3.v_init
     lif3.nspikes = 0
     lif3.t = 0

     X = list(map(c,X))

     n = 7
     dtmax = (tmax-0)/n
     tt = np.arange(0,tmax+dtmax,dtmax)
     g00 = simple([(X[0],[tt[0],tt[1]]),
                   (X[1],[tt[1],tt[2]]),
                   (X[2],[tt[2],tt[3]]),
                   (X[3],[tt[3],tt[4]]),
                   (X[4],[tt[4],tt[5]]),
                   (X[5],[tt[5],tt[6]]),
                   ])
     g10 = simple([(X[6],[tt[0],tt[1]]),
                   (X[7],[tt[1],tt[2]]),
                   (X[8],[tt[2],tt[3]]),
                   (X[9],[tt[3],tt[4]]),
                   (X[10],[tt[4],tt[5]]),
                   (X[11],[tt[5],tt[6]]),
                   ])
     # simulate probing / monitoring data
     T = []
     V1a = []
     V1b = []
     V2 = []
     G00 = []
     G10 = []
     t = lif3.t
     while t < tmax:
         dense.set_g(0,0,g00(t))
         dense.set_g(1,0,g10(t))
         G00.append(dense.get_g(0,0))
         G10.append(dense.get_g(1,0))
         T.append(lif1.t)
         V1a.append(lif1.get_v())
         V1b.append(lif2.get_v())
         V2.append(lif3.get_v())
         lif1.step()
         lif2.step()
         lif3.step()
         t = lif3.t

     flag_plot = plot
     if flag_plot:
          # plot results
          fig,axs = plt.subplots(5)
          axs[4].set_xlabel('Time t')
          axs[4].set_ylabel('g10(t)')
          axs[3].set_ylabel('g00(t)')
          axs[2].set_ylabel('V2(t)')
          axs[1].set_ylabel('V1b(t)')
          axs[0].set_ylabel('V1a(t)')
          axs[0].set_title(f' LIF(2) - Dense(2,1) - LIF(1)')
          axs[0].plot(T, V1a)
          axs[1].plot(T, V1b)
          axs[2].plot(T, V2, 'b')
          axs[3].plot(T,G00)
          axs[4].plot(T,G10)
          plt.show()

     x_a = [lif1.get_nspikes(),lif2.get_nspikes()]
     y_p = [lif3.get_nspikes()]
     mx = max(x_a)
     x_a = np.array(x_a)/mx
     y_p = np.array(y_p)/mx
     #print(f"x_a = {x_a}")
     val = d(y_p,y_a)

     if verbose:
          print(f"loss = {val}")
          print(f"g00: {X[0:6]}")
          print(f"g10: {X[6:]}")
          print(f"y_a: {y_a}")
          print(f"y_p = {y_p}")
     return val

# https://en.wikipedia.org/wiki/Directional_derivative
# the rate at which function f changes in direction v
# at point x (t is an arbitrarily small parameter)
# this definition of nabla is the directional derivative
# nabla is a derivation obeying Leibniz rule.
def nabla(v):
    v2 = np.array(v)
    def f1(f):
        def f2(x):
            t = nabla_t
            x2 = np.array(x)
            x3 = x2 + t*v2
            val = (f(list(x3)) - f(list(x2)))/t
            return val
        return f2
    return f1

def grad(f):
    def f1(x):
        n = len(x)
        I = np.identity(n)
        vec = []
        for i in range(n):
            v = list(I[i].flatten())
            val = nabla(v)(f)(x)
            vec.append(val)
        return np.array(vec)
    return f1

def myfmin(F,x0,gamma=10,xtol=1,maxiter=50):
     a = np.array(x0)
     # https://en.wikipedia.org/wiki/Gradient_descent
     done = False
     i = 0
     while not done:
          g = grad(F)(a)
          g_mag = np.linalg.norm(g)
          epsilon = 1e-3
          if abs(g_mag) > epsilon:
               g = g/np.linalg.norm(g)
          a2 = a - gamma*g
          a2 = list(map(c,a2))
          if d(a,a2) < xtol:
               done = True
          if d(F(a),F(a2)) < ftol:
               done = True
          if i > maxiter:
               done = True
          if done:
               break
          a = a2
          i = i + 1
     X_opt = a
     return X_opt

for v in list(np.arange(0,1+.1,.1)):
     y_a = np.array([v])
     a = [0.5]*12
     X_opt = myfmin(F,a,gamma,xtol,maxiter)
     print(f"Results:")
     val = F(X_opt,verbose=True, plot=False)
     print(f"="*30)

