import lif_net2 as lifn
import numpy as np

import matplotlib.pyplot as plt

ni = 2 # number of input neurons
no = 2 # number of output neurons
c_max = 100 # maximum conductance value on synapses
xtol = 1e-8 # x tolerance in dimensions of X
ftol = 0.05 # f tolerance for loss function
g_n0 = 6
g_n = g_n0 + 2 # number of conductances learned
vth0 = 0.5 # threshold on LIF neurons

dt0 = 0.05 # action potential time resolution
du0 = 0.3 # injection current spike width
tmax = 50 # duration to simulate

nm = 8 # number of middle neurons

nabla_t = 10 # must be large enough to contain spikes
maxiter = 15 # maximum iterations in gradient descent
gamma = 2 # learning rate for gradient descent

# create ni leaky integrate and fire input neurons
myrange = lifn.myrange

lif_in = []
for i in range(ni):
     qi = [20,5]
     I1 = lifn.I_multi(L=[
                 myrange(q=qi[i],a=0,b=tmax/3.0,dt=1)])
     Ci = [.2,.2] # tau[i] = Ci[i]*R[i]
     Ri = [1,1]
     lif_i = lifn.LIF(v_init=0,
          vth=vth0, I = I1, dt=dt0, du=du0,
           C=Ci[i],
           R=Ri[i])
     lif_in.append(lif_i)

# create synaptic Dense(ni,no) network between ni
# input neurons and no output neurons
dense0 = lifn.Dense(ni,nm)
dense1 = lifn.Dense(nm,no)
dense = [dense0,dense1]

# For the j output neuron, sum up input neurons using
# formula Im(j) = g00*V1 + g10*V2

# Kirchoff's rule of additive currents
def Im(j,lif,densei):
     def I(net,t):
          val = 0
          n = len(lif)
          for i in range(n):
               val_i = densei.get_g(i,j)*lif[i].get_v()
               val = val + val_i
          return val
     return I

# create output neuron using that current I3
lif_mid = []
for j in range(nm):
     Ci = [.1]*nm
     Ri = [1]*nm
     lif_j = lifn.LIF(v_init=0,
          vth=vth0, I = Im(j,lif_in,dense[0]),
          dt=dt0, du=du0,
           C=Ci[j],
           R=Ri[j])
     lif_mid.append(lif_j)
lif_out = []
for j in range(no):
     Ci = [.1,.1]
     Ri = [1,1]
     lif_j = lifn.LIF(v_init=0,
          vth=vth0, I = Im(j,lif_mid,dense[1]),
          dt=dt0, du=du0,
           C=Ci[j],
           R=Ri[j])
     lif_out.append(lif_j)

ds = lifn.Dense_solve(lif_in, lif_mid, lif_out,
          dense, g_n, tmax, gamma, xtol,maxiter,
          nabla_t,c_max,ftol)

print(f"Neuromorphic Computing simulation:")
for v in [[50,100],[100,50]]:
     y_a = np.array(v)
     x_v = ds.find_X(y_a)
     g_v = ds.build_g(x_v)
