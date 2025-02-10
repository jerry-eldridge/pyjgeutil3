import numpy as np
import matplotlib.pyplot as plt

from math import sqrt,ceil

def circle(a,b,r):
    def f(x,y):
        val = (x-a)**2 + (y-b)**2 - r**2
        return val
    return f

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

# Parameters

# a,b,r
r = 8 # particle radius
p_in_1 = [-10,0, r]
p_in_2 = [10,0, r]
ri = 4 # interaction radius
I = [0,0,ri] # 
p_out_1 = [0,20, r]
p_out_2 = [0,-20, r]
p_out_3 = [30,10, r]

# curves and Interaction
# input particles
curvei_1I = lambda t: circle(*lerp(p_in_1,I,t))
curvei_2I = lambda t: circle(*lerp(p_in_2,I,t))
# output particles
curveo_I1 = lambda t: circle(*lerp(I,p_out_1,t))
curveo_I2 = lambda t: circle(*lerp(I,p_out_2,t))
curveo_I3 = lambda t: circle(*lerp(I,p_out_3,t))
ci = [curvei_1I,curvei_2I]
cf = [curveo_I1,curveo_I2,curveo_I3]
def Interaction(ci,cf):
    def G(x,y):
        def f(t):
            if 0 <= t <= 0.5:
                pi = 1
                for g in ci:
                    a = g(2*t)(x,y)
                    pi = min(pi , a)
            elif 0.5+1e-8 <= t <= 1.0:
                pi = 1
                for g in cf:
                    a = g(2*(t-0.5))(x,y)
                    pi = min(pi , a)
            return pi
        return f
    return G

depth = 32
width = 150
height = 150
xx = np.linspace(-40,40,width)
yy = np.linspace(-40,40,height)
X,Y = np.meshgrid(xx,yy)
sh = X.shape
dataset = np.zeros((depth,sh[0],sh[1]))
for k in range(depth):
    t = k/(depth-1)
    for i in range(width):
        for j in range(height):
            x = X[i,j]
            y = Y[i,j]
            dataset[k,i,j] = \
                    Interaction(ci,cf)(x,y)(t)

m = 8
fig, axes = plt.subplots(nrows=depth//m, ncols=m,
            sharex='col', sharey='row')

z = 0
for i in range(depth):
    ax = axes[i // m, i % m]
    ax.contour(X,Y,dataset[i,:,:],levels=[z])
    #ax.axis("off")

plt.tight_layout()
plt.show()
