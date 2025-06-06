import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#############################################
# [1] the author JGE

def grad(F,h=1e-6):
    def f(x):
        n = len(x)
        L = []
        
        for i in range(n):
            v = np.array([0]*n)
            v[i] = 1
            xp = np.array(x) + h*v
            w = (F(list(xp))-F(list(x)))/h
            w = float(w)
            L.append(w)
        return L
    return f

##########################################

def f(X):
    return (3*X[0] + 4*X[1] + 2)

def g(X):
    return X[0]**2/9 + (X[1]/5 - 1)**2 - 1

def inf(g):
    def F(f):
        def G(X0):
            def lagrangian(X):
                lam = X[-1]
                X = X[:-1]
                val = f(X) + abs(lam)*g(X)
                return val

            def grad_lagrangian(X):
                v = np.array(grad(lagrangian)(X))
                val = np.sum(v**2)
                return val
            num_steps = 6000

            lam = 1
            X = X0 + [lam]
            eta = .04
            epsilon = 1e-10
            for i in range(num_steps):
                gg = np.array(grad(grad_lagrangian)(X))
                gg_mag = np.linalg.norm(gg)
                if gg_mag < epsilon:
                    break
                action = -eta*gg
                X = np.array(X) + action
                X = list(map(float,list(X)))
            X_opt = X[:-1]
            return X_opt
        return G
    return F

sup = lambda g: lambda f: lambda X0:\
      inf(g)(lambda X: -f(X))(X0)
inner = lambda x,y: np.inner(x,y)
def linprog_fmin(c,A_ub,b_ub):
    n,m = A_ub.shape
    f = lambda x: inner(c,x) # <c,x>
    def relu(x):
        return max(0,x)
    def g(x):
        y = A_ub @ np.array(x).reshape(m,1) - b_ub
        z = list(map(float,list(y.flatten())))
        return z
    def lagrangian(X):
        lam = X[-n:]
        lam = list(map(relu,lam))
        X = X[:-n]
        val = f(X) + inner(lam,g(X))
        return val
    def grad_lagrangian(X):
        v = np.array(grad(lagrangian)(X))
        val = np.sum(v**2)
        return val
    num_steps = 1000

    lam = [1]*n
    X0 = [1]*m
    X = X0 + lam
    eta = .03
    epsilon = 1e-8
    for i in range(num_steps):
        gg = np.array(grad(grad_lagrangian)(X))
        gg_mag = np.linalg.norm(gg)
        if gg_mag < epsilon:
            break
        action = -eta*gg
        X = np.array(X) + action
        X = list(map(float,list(X)))
        Xo = X[:-n]
        if i % 150 == 0:
            print(f".",end='.')
    print()
    return Xo

## minimize -3*x - 6*y - 3*z
## subject to
## -3*x + 1*y + 2*z <= 6
## 1*x + 4*y + 1*z <= 10
## 3*x + 2*y + 1*z <= 3

print(f"JGE version:")
c = [-3, -6, -3]
A = [[-3,1,2],
     [1,4,1],
     [3,2,1]]
b = [6,10,3]
bounds = [(None,None)]*len(c) # used in scipy version
A_ub = np.array(A)
n,m = A_ub.shape
b_ub = np.array(b).reshape(n,1)
Xo = linprog_fmin(c,A_ub,b_ub)
print(f"Xo = {Xo}")
print(f"<c,Xo> = {inner(c,Xo)}\n"+\
      f"A_ub*Xo = "+\
      f"{(A_ub @ np.array(Xo).reshape(m,1)).flatten()} "+\
      f"<= b_ub = {b_ub.flatten()}?")
print()
print(f"scipy version:")
import scipy.optimize as so
res = so.linprog(c,A_ub=A,b_ub=b,
                      bounds=bounds)
Xo = list(map(float,list(res.x.flatten())))
print(f"Xo = {Xo}")
print(f"<c,Xo> = {inner(c,Xo)}\n"+\
      f"A_ub*Xo = "+\
      f"{(A_ub @ np.array(Xo).reshape(m,1)).flatten()} "+\
      f"<= b_ub = {b_ub.flatten()}?")
