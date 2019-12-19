import numpy as np
from math import cos,sin,pi,fmod,sqrt

from scipy.interpolate import interp1d
from scipy.optimize import bisect

import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import mapto
import line_intersection as li

def cross(A,B):
    return np.cross(A,B)

def LorenzForce(q,v,E,B):
    F = q*(np.array(E)+np.array(cross(v,B)))
    return list(F)
class Ion:
    def __init__(self,x=[0,0,0],v=[0,0,0],m=1,q=1,dt=.05):
        self.x = np.array(x)
        self.v = np.array(v)
        self.a = np.array([0,0,0])
        self.m = m
        self.q = q
        self.dt = dt
        self.t = 0
        return
    def Update(self,F):
        F = np.array(F)
        self.a = F/self.m
        self.v = self.v + self.a*self.dt
        self.x = self.x + self.v*self.dt
        self.t += self.dt
        return
def EMfield(t,lam,E0,B0):
    #global direction
    #c = 1 # speed of light
    #x = 0
    #f = 1.0*c/lam
    #Bz = B0*sin(2*pi/lam*(x - c*t))
    #Ey = E0*sin(2*pi/lam*(x - c*t))
    #B = [0,0,Bz] # assume magnetic field points along z-axis
    #E = [0,direction*Ey,0] # and electric field along y-axis
    E = [0,0,0]
    B = [0,0,B0]
    return E,B
def sgn(x):
    if x < 0:
        return -1
    else:
        return 1

def MassSpectrometer(I,show=True):
    # W,H used in calculation of measurement
    W = 600
    H = 600
    if show:
        gr = racg.Graphics(w=W,h=H)
    E0 = 0
    B0 = 2 # light amplitude
    lam = 5 # light wavelength
    black = [0,0,0]
    blue = [0,0,255]
    pt_last = [0,300]
    direction = 1 # direction y-axis or -(y-axis)
    #print "Press 'e' to exit"
    tmax = 55 # time units maximum
    Z = 0
    while I.t <= tmax:
        # make direction change periodically
        direction = 1
        #gr.Clear()
        r = I.x
        # Screen transformation of r -> [x,y,z]
        xmin = -10
        xmax = 10
        ymin = -10
        ymax = 10
        x = mapto.MapTo(xmin,0,xmax,W,r[0])
        y = mapto.MapTo(ymin,0,ymax,H,r[1])
        z = 0
        # Projective Transformation of [x,y,z] -> [x2,y2]
        pt = [x-W/2,y]
        #gr.Point(pt,color=black)
        #print pt,r
        if show:
            gr.Line(pt,pt_last,color=blue)
        sW = 0.5
        P = [W*sW,0]
        Q = [W*sW,H]
        if show:
            gr.Line(P,Q,color=black)
        flag,X,Y = li.SegmentIntersect(
            pt[0],pt[1],pt_last[0],pt_last[1], # segment 1
            P[0],P[1],Q[0],Q[1])
        s = "Y = %.2f" % (Y)
        if show:
            gr.Text(s,X+10,Y,black)
        pt_last = pt
        if show:
            if fmod(I.t,0.1)<0.001:
                ch = gr.Show("result",5)
            if ch == ord('e'):
                break
        E,B = EMfield(I.t,lam,E0,B0)
        F = LorenzForce(I.q,I.v,E,B)
        I.Update(F)
        if flag:
            Z = Y
            if show:
                m0 = finv(Z)*I.q
                s = "mass m = %.3f" % (m0)
                gr.Text(s,X+10,Y-25,black)
            if show:
                gr.Show("result",-1)
                break
    if show:
        gr.Close()
    return Z

print "Press any key to continue"

use_graphics = True
if use_graphics:
    import graphics_pygame as racg
q0 = 1

def CreateFunction(q0):
    X = range(28,60)
    Y = []
    for m_over_q0 in X:
        m0 = q0*m_over_q0
        I = Ion(x=[0,0,0],v=[0.7,0,0],m=m0,q=q0,dt=0.05)
        Z = MassSpectrometer(I,show=False)
        Y.append(Z)
    f = interp1d(X,Y)
    import matplotlib.pyplot as plt
    plt.plot(X,Y)
    plt.xlabel("m/q")
    plt.ylabel("Z (distance)")
    plt.title("Mass Spectrometer for Ions (m/q in interval [28,60])")
    plt.show()
    return f

def Mass(f,I):
    q0 = I.q # is known from experiment but I.m isn't
    Z = MassSpectrometer(I,show=True)
    print "Mass Spectrometer read Z = ",Z
    m0 = finv(Z)*q0
    print "mass = m0 = ",m0
    return m0

f = CreateFunction(q0)

# These are the same as in MassSpectrometer
W = 600
H = 600

def finv(y):
    def h(x):
        try:
            return f(x)
        except:
            return 1000*x**2
    return bisect(lambda x: h(x)-y,28,60)

print "Ion charge: q0 = ",q0
m_over_q0 = 29
print "m/q0 = ",m_over_q0
m0 = q0*m_over_q0
print "m0 = ", m0
print "Creating ion in ion beam"
I = Ion(x=[0,0,0],v=[0.7,0,0],m=m0,q=q0,dt=0.05)
print
print "The ion's path is bent in a magnetic field"
print "The ion collides with a plate that measures"
print "its position and returns Z in length units"
print "A function from Z to mass m is created for"
print "calibration. The inverse of that function is"
print "used for obtaining the mass"
print
Z_m0 = Mass(f,I)






