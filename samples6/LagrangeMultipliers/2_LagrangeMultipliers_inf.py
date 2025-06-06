import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#############################################
# [1] the author JGE

def grad(F,h=1e-3):
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

X0 = [15,-10]
X_opt_inf = inf(g)(f)(X0)
X_opt_sup = sup(g)(f)(X0)
print(f"inf(g)(f) = {X_opt_inf}, "+\
      f"f(X) = {f(X_opt_inf)}")
print(f"sup(g)(f) = {X_opt_sup}, "+\
      f"f(X) = {f(X_opt_sup)}")
X_opt1a = [27*sqrt(481)/481, 100*sqrt(481)/481 + 5]
X_opt2a = [-27*sqrt(481)/481, 5 - 100*sqrt(481)/481]
print(f"X_opt1a = {X_opt1a}, f(X_opt1a) = {f(X_opt1a)} ")
print(f"X_opt2a = {X_opt2a},f(X_opt2a) = {f(X_opt2a)} ")
