import lif_net as lifn
import numpy as np

import matplotlib.pyplot as plt

dt0 = 0.05 # action potential time resolution
du0 = 0.3 # injection current spike width
tmax = 50 # duration to simulate
ni = 2 # number of input neurons
no = 2 # number of output neurons
nm = 3 # number of middle neurons
nabla_t = .2 # must be large enough to contain spikes
c_max = 5 # maximum conductance value on synapses
xtol = .1 # x tolerance in dimensions of X
ftol = 0.05 # f tolerance for loss function
maxiter = 10 # maximum iterations in gradient descent
g_n = 6 # number of conductances learned is ni*no*(g_n-2)
vth0 = 0.5 # threshold on LIF neurons
gamma = 0.05 # learning rate for gradient descent

# create ni leaky integrate and fire input neurons
myrange = lifn.myrange

lif_in = []
for i in range(ni):
     qi = np.random.rand(1)[0]
     I1 = lifn.I_multi(L=[
                 myrange(q=qi,a=8,b=11,dt=1)])
     lif_i = lifn.LIF(v_init=0,
          vth=vth0, I = I1, dt=dt0, du=du0,
           C=.1,
           R=1)
     lif_in.append(lif_i)

# create synaptic Dense(ni,no) network between ni
# input neurons and no output neurons
dense0 = lifn.Dense(ni,nm)
dense1 = lifn.Dense(nm,no)
dense = [dense0,dense1]

# For the j output neuron, sum up input neurons using
# formula Im(j) = g00*V1 + g10*V2

# Kirchoff's rule of additive currents
def Im(j,dense):
     def I(net,t):
          val = 0
          for i in range(ni):
               val_i = dense.get_g(i,j)*lif_in[i].get_v()
               val = val + val_i
          return val
     return I

# create output neuron using that current I3
lif_mid = []
for i in range(nm):
     lif_i = lifn.LIF(v_init=0,
          vth=vth0, I = Im(i,dense0), dt=dt0, du=du0,
           C=.1,
           R=1)
     lif_mid.append(lif_i)
lif_out = []
for i in range(no):
     lif_i = lifn.LIF(v_init=0,
          vth=vth0, I = Im(i,dense1), dt=dt0, du=du0,
           C=.1,
           R=1)
     lif_out.append(lif_i)

ds = lifn.Dense_solve(lif_in, lif_mid, lif_out,
          dense, g_n, tmax, gamma, xtol,maxiter,
          nabla_t,c_max,ftol)

print(f"Neuromorphic Computing simulation:")
for v in [[50,100],[100,50]]:
     y_a = np.array(v)
     x_v = ds.find_X(y_a)
     g_v = ds.build_g(x_v)
