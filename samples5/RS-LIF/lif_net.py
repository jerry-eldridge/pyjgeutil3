import numpy as np
from math import cos,pi,fmod

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
        t,y = Euler_step(self.f,self.t,y,self.dt)
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
        #self.g = np.zeros((n,m),dtype=np.float32)
        self.g = np.random.rand(n,m)
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

def myrange(q,a,b,dt):
     return (q,np.arange(a,b+dt,dt))

def d(x,y):
     return np.linalg.norm(np.array(y)-np.array(x))

# https://en.wikipedia.org/wiki/Directional_derivative
# the rate at which function f changes in direction v
# at point x (t is an arbitrarily small parameter)
# this definition of nabla is the directional derivative
# nabla is a derivation obeying Leibniz rule.
def nabla(v,nabla_t = .2):
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

def grad(f,nabla_t = .2):
    def f1(x):
        n = len(x)
        I = np.identity(n)
        vec = []
        for i in range(n):
            v = list(I[i].flatten())
            val = nabla(v,nabla_t)(f)(x)
            vec.append(val)
        return np.array(vec)
    return f1

clamp0 = lambda x,a,b: max(a,min(x,b))
c = lambda c_max: lambda x: clamp0(x,0,c_max)

def myfmin(F,x0,gamma=10,xtol=1,maxiter=50,
           nabla_t = .2, c_max = 2,
           ftol = 0.05):
     a = np.array(x0)
     # https://en.wikipedia.org/wiki/Gradient_descent
     done = False
     print(f"myfmin(F,x0)")
     i = 0
     count_show = 0
     while not done:
          g = grad(F,nabla_t)(a)
          da = -gamma*g
##          g_mag = np.linalg.norm(g)
##          epsilon = 1e-3
##          if abs(g_mag) > epsilon:
##               g = g/np.linalg.norm(g)
          if count_show <= maxiter:
               #print(f"a = {a}")
               print(f"i = {i}, F(a) = {F(a)}, |da| = {np.linalg.norm(da)}")
               count_show = count_show + 1
          a2 = a + da
          a2 = list(map(c(c_max),a2))
          if np.linalg.norm(da) < xtol:
               done = True
          if abs(F(a2)) < ftol:
               done = True
          if i >= maxiter:
               done = True
          i = i + 1
          a = a2
          if done:
               break
     print(f"Finish: i = {i}, F(a) = {F(a)}")
     iters = i
     X_opt = a
     return X_opt, iters

class Dense_solve:
     def __init__(self,
                  lif_in,
                  lif_mid,
                  lif_out,
                  dense,
                  g_n,
                  tmax,
                  gamma,
                  xtol,
                  maxiter,
                  nabla_t,
                  c_max,
                  ftol
                  ):
          self.lif_in = lif_in
          self.lif_mid = lif_mid
          self.lif_out = lif_out
          self.dense = dense
          self.g_n = g_n
          self.tmax = tmax
          self.gamma = gamma
          self.xtol = xtol
          self.maxiter = maxiter
          self.nabla_t = nabla_t
          self.c_max = c_max
          self.ftol = ftol
          self.ni = len(self.lif_in)
          self.nm = len(self.lif_mid)
          self.no = len(self.lif_out)
     def build_g(self, X):
          n = self.g_n
          dtmax = (self.tmax-0)/n
          tt = np.arange(0,self.tmax+dtmax,dtmax)
          g = {}
          c = 0
          for i in range(self.ni):
               for j in range(self.nm):
                    L00 = []
                    for k in range(self.g_n-2):
                         a = tt[k]
                         b = tt[k+1]
                         tup = (X[c],[a,b])
                         L00.append(tup)
                         c = c + 1
                    
                    g[(i,j,0)] = simple(L00)
          for i in range(self.nm):
               for j in range(self.no):
                    L00 = []
                    for k in range(self.g_n-2):
                         a = tt[k]
                         b = tt[k+1]
                         tup = (X[c],[a,b])
                         L00.append(tup)
                         c = c + 1
                    
                    g[(i,j,1)] = simple(L00)
          return g
     def F(self,y_a,verbose=False,plot=False):
          def f(X):
               for i in range(self.ni):
                    self.lif_in[i].v = \
                              self.lif_in[i].v_init
                    self.lif_in[i].nspikes = 0
                    self.lif_in[i].t = 0

               for j in range(self.nm):
                    self.lif_mid[j].v = \
                         self.lif_mid[j].v_init
                    self.lif_mid[j].nspikes = 0
                    self.lif_mid[j].t = 0
               
               for j in range(self.no):
                    self.lif_out[j].v = \
                         self.lif_out[j].v_init
                    self.lif_out[j].nspikes = 0
                    self.lif_out[j].t = 0

               X = list(map(c(self.c_max),X))

               g = self.build_g(X)
               
               # simulate probing / monitoring data
               t = self.lif_in[0].t
               while t < self.tmax:
                    for i in range(self.ni):
                         for j in range(self.nm):
                             self.dense[0].set_g(i,j,\
                                   g[(i,j,0)](t))
                    for i in range(self.nm):
                         for j in range(self.no):
                             self.dense[1].set_g(i,j,\
                                   g[(i,j,1)](t))
                    for i in range(self.ni):
                         self.lif_in[i].step()
                    for k in range(self.nm):
                         self.lif_mid[k].step()
                    for j in range(self.no):
                         self.lif_out[j].step()
                    t = self.lif_in[0].t

               x_a = [self.lif_in[i].get_nspikes() \
                      for i in range(self.ni)]
               y_p = [self.lif_out[j].get_nspikes() \
                      for j in range(self.no)]
               x_a = np.array(x_a)
               y_p = np.array(y_p)
               val = d(y_p,y_a)
               flag_plot = plot
               return val
          return f
     def find_X(self, y_a):
          a = np.random.rand(\
               (self.g_n-2)*(\
          len(self.lif_in)*len(self.lif_mid)+\
          len(self.lif_mid)*len(self.lif_out)))
          X_opt,iters = myfmin(self.F(y_a),a,
                    self.gamma,
                    self.xtol,
                    self.maxiter,
                    nabla_t=self.nabla_t,
                    c_max = self.c_max,
                    ftol = self.ftol)
          print(f"Find_x: Results:")
          print(f"iterations = {iters}")
          f = self.F(y_a,verbose=True, plot=True)
          X_opt = list(map(c(self.c_max),X_opt))
          val = f(X_opt)
          g = self.build_g(X_opt)
          print(f"Conductances:")
          dtmax = (self.tmax-0)/self.g_n
          tt = np.arange(0,self.tmax+dtmax,dtmax)
          for i in range(self.ni):
               for j in range(self.nm):
                    G = []
                    for k in range(self.g_n-2):
                         a = tt[k]
                         b = tt[k+1]
                         tab = (a+b)*0.5
                         tup = (i,j,0)
                         val = g[tup](tab)
                         G.append(val)
                    print(f"tup = {tup}, g = {G}")
          for i in range(self.nm):
               for j in range(self.no):
                    G = []
                    for k in range(self.g_n-2):
                         a = tt[k]
                         b = tt[k+1]
                         tab = (a+b)*0.5
                         tup = (i,j,1)
                         val = g[tup](tab)
                         G.append(val)
                    print(f"tup = {tup}, g = {G}")
          print()
          x_a = [self.lif_in[i].get_nspikes() \
                      for i in range(self.ni)]
          z_p = [self.lif_mid[i].get_nspikes() \
                      for i in range(self.nm)]
          y_p = [self.lif_out[j].get_nspikes() \
                      for j in range(self.no)]
          x_a = np.array(x_a)
          print(f"Input: x_a = {x_a}")
          print(f"Middle: z_p = {z_p}")
          print(f"Output Desired: y_a = {y_a}")
          y_p = np.array(y_p)
          print(f"Output: y_p = {y_p}")
          print(f"="*30)
          return X_opt
