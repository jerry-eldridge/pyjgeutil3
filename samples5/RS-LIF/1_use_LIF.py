import numpy as np

from math import cos,pi,fmod

import matplotlib.pyplot as plt

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
             self.v[0] = self.v_init[0]
        return

class Dense:
    def __init__(self,n,m):
        self.g = np.zeros((n,m),dtype=np.float32)
    def set(self,i,j,g):
        self.g[i,j] = g
    def unset(self,i,j):
        self.g[i,j] = 0
    def get_g(self,i,j):
        return self.g[i,j]

def I_helper(t,q,T,du):
    val = 0
    for i in range(len(T)):
        ti = T[i]
        val_i = DiracDelta(t-ti,du)
        val = val + val_i
    return val

def I_multi(q,T):
     def I(net,t):
          vals = []
          for i in range(len(q)):
               val_i = I_helper(t,q[i],T[i],net.du)
               vals.append(val_i)
               vec = np.array(vals)
          return vec
     return I


dt0 = .01
du0 = .3
tmax = 20
ni = 2
no = 1

# create ni = 2 input leaky integrate and fire
# neurons
I1 = I_multi(q=[.1,.3],
              T=[[1,3,5,7],[2,4,6]])
I2 = I_multi(q=[.9],
              T=[[7,9]])
lif1 = LIF(v_init=0,
          vth=1.0, I = I1, dt=dt0, du=du0,
           C=.1,
           R=1)

lif2 = LIF(v_init=0,
          vth=1.0, I = I2, dt=dt0, du=du0,
           C=.3,
           R=2)

# create synaptic Dense(ni,no) network between ni = 2
# input neurons and no = 1 output neurons
dense = Dense(ni,no)
dense.set(0,0, .1)
dense.set(1,0, .2)

# For the output neuron, sum up input neurons using
# formula I3 = g00*V1 + g10*V2

# Kirchoff's rule of additive currents
I3 = lambda net,t: dense.get_g(0,0)*lif1.get_v() +\
     dense.get_g(1,0)*lif2.get_v()

# create output neuron using that current I3
lif3 = LIF(v_init=0,
          vth=1.0, I = I3, dt=dt0, du=du0,
          C=.1,R=2)

# simulate probing / monitoring data
T = []
V1a = []
V1b = []
V2 = []
t = lif3.t
while t < tmax:
    T.append(lif1.t)
    V1a.append(lif1.get_v())
    V1b.append(lif2.get_v())
    V2.append(lif3.get_v())
    lif1.step()
    lif2.step()
    lif3.step()
    t = lif3.t

# plot results
fig,axs = plt.subplots(3)
axs[2].set_xlabel('Time t')
axs[2].set_ylabel('V2(t)')
axs[1].set_ylabel('V1b(t)')
axs[0].set_ylabel('V1a(t)')
axs[0].set_title(f' LIF(2) - Dense(2,1) - LIF(1)')
axs[0].plot(T, V1a)
axs[1].plot(T, V1b)
axs[2].plot(T, V2, 'b')
plt.show()
