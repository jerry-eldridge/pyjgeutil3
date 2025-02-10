import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Bifurcation:
    def __init__(self, n, curves_initial,
                 curves_final):
        self.ci = curves_initial
        self.cf = curves_final
        self.n = n
        self.T = np.linspace(0, 1, n)
        self.T1 = np.linspace(0, 0.5, n//2)
        self.T2 = np.linspace(0.5+0.001, 1, n//2)
    def particles(self, t):
        epsilon = 1/1000
        pts = []
        if 0 <= t <= 0.5:
            for curve in self.ci:
                pt = curve(2*t)
                pts.append(pt)
        elif 0.5+epsilon <= t <= 1.0:
            for curve in self.cf:
                pt = curve(2*(t-0.5))
                pts.append(pt)
        return pts
    def path_initial(self):
        pts = list(map(self.particles,self.T1))
        pts = np.array(pts)
        return pts
    def path_final(self):
        pts = list(map(self.particles,self.T2))
        pts = np.array(pts)
        return pts

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))
# Parameters
A = [0,0,0]
B = [10,0,0]
C = [20,10,0]
D = [20,-10,0]
curve_AB = lambda t: lerp(A,B,t)
curve_BC = lambda t: lerp(B,C,t)
curve_BD = lambda t: lerp(B,D,t)
Interaction = Bifurcation(100,
                [curve_AB],[curve_BC,curve_BD])
# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot original curve in red
pts = Interaction.path_initial()
for i in range(len(Interaction.ci)):
    ax.plot(pts[:,i,2],pts[:,i,0],pts[:,i,1],
        label=f'p_in_{i}', color='r')

# Plot bifurcated branches in blue
pts = Interaction.path_final()
for j in range(len(Interaction.cf)):
    ax.plot(pts[:,j,2],pts[:,j,0],pts[:,j,1],
        label=f'p_out_{j}', color='b')

ax.set_xlabel('Z')
ax.set_ylabel('X')
ax.set_zlabel('Y')
ax.set_title('Line Bifurcating into Two Lines')
ax.legend()

plt.show()


