import numpy as np
from math import fmod,pi,sin,cos

lerp = lambda A,B,t: np.array(A)*(1-t) + np.array(B)*t

deriv = lambda h: lambda f: lambda x: (f(x+h)-f(x))/h

def grad_i(A,x,i,h):
    I = np.identity(3)
    v = I[i]
    x2 = list(np.array(x) + h*v)
    val = (A(x2) - A(x))/h
    return val

# https://en.wikipedia.org/wiki/Nabla_symbol
# https://en.wikipedia.org/wiki/Del
def grad(f,r,dr):
    f_x = grad_i(f,r,0,dr[0])
    f_y = grad_i(f,r,1,dr[1])
    f_z = grad_i(f,r,2,dr[2])
    val = np.array([f_x,f_y,f_z])
    return val

def div(F,r,dr):
    Fx = lambda r: F(r)[0]
    Fy = lambda r: F(r)[1]
    Fz = lambda r: F(r)[2]
    Fx_x = grad_i(Fx,r,0,dr[0])
    Fy_y = grad_i(Fy,r,1,dr[1])
    Fz_z = grad_i(Fz,r,2,dr[2])
    val = sum([Fx_x,Fy_y,Fz_z])
    return val    

def curl(F,r,dr):
    Fx = lambda r: F(r)[0]
    Fy = lambda r: F(r)[1]
    Fz = lambda r: F(r)[2]
    Fz_y = grad_i(Fz,r,1,dr[1])
    Fy_z = grad_i(Fy,r,2,dr[2])
    a = Fz_y - Fy_z
    Fx_z = grad_i(Fx,r,2,dr[2])
    Fz_x = grad_i(Fz,r,0,dr[0])
    b = Fx_z - Fz_x
    Fy_x = grad_i(Fy,r,0,dr[0])
    Fx_y = grad_i(Fx,r,1,dr[1])
    c = Fy_x - Fx_y
    val = np.array([a,b,c])
    return val

##X1 = x1*sp.cos(x3)*sp.sin(x2)
##X2 = x1*sp.sin(x3)*sp.sin(x2)
##X3 = x1*sp.cos(x2)
def sphere_surface_area(R):
    # the change of variables |J| with J the
    # jacobian of the spherical coordinates
    # transformation is |J| = x1**2*sin(x2)
    # thus dV = |J|*dx1*dx2*dx3 = dX1*dX2*dX3
    # and dS = |J|*dx2*dx3 with x1 = epsilon fixed
    # with x2 in [0,pi] and x3 in [0,2*pi]
    x2min = 0
    x2max = pi
    x3min = 0
    x3max = 2*pi
    dx2 = .01
    dx3 = .01
    area = 0
    x2 = x2min
    while x2 < x2max:
        x3 = x3min
        while x3 < x3max:
            # sphere
            x1 = R
            dS = x1**2*sin(x2)*dx2*dx3            
            area = area + dS
            x3 = x3 + dx3
        x2 = x2 + dx2
    return area

def flux(F,R):
    def G(r):
        # the change of variables |J| with J the
        # jacobian of the spherical coordinates
        # transformation is |J| = x1**2*sin(x2)
        # thus dV = |J|*dx1*dx2*dx3 = dX1*dX2*dX3
        # and dS = |J|*dx2*dx3 with x1 = epsilon fixed
        # with x2 in [0,pi] and x3 in [0,2*pi]
        x2min = 0
        x2max = pi
        x3min = 0
        x3max = 2*pi
        dx2 = .01
        dx3 = .01
        flx = 0
        x2 = x2min
        r = np.array(r) # center of sphere
        x1 = R
        while x2 < x2max:
            x3 = x3min
            while x3 < x3max:
                # spherical coordinates
                # [X1,X2,X3] is local cartesian
                # coordinates of sphere
                X1 = x1*cos(x3)*sin(x2)
                X2 = x1*sin(x3)*sin(x2)
                X3 = x1*cos(x2)
                # r2 is global coordinates of sphere
                r2 = np.array([X1,X2,X3]) + r
                # dS is infinitesimal surface area
                dS = x1**2*sin(x2)*dx2*dx3
                # n is radial from center of sphere
                # r to point on sphere r2 is normal
                # to surface area S
                n = r2 - r
                # magnitude of n
                n_mag = np.linalg.norm(n)
                # n_hat is radial direction vector
                # normal.
                n_hat = n/n_mag
                # Integral(S)(F*n_hat,dS)
                flx = flx + np.inner(F(r2),n_hat)*dS
                x3 = x3 + dx3
            x2 = x2 + dx2
        return flx
    return G

def flux2(F,R):
    def G(r):
        # the change of variables |J| with J the
        # jacobian of the spherical coordinates
        # transformation is |J| = x1**2*sin(x2)
        # thus dV = |J|*dx1*dx2*dx3 = dX1*dX2*dX3
        # and dS = |J|*dx2*dx3 with x1 = epsilon fixed
        # with x2 in [0,pi] and x3 in [0,2*pi]
        x2min = 0
        x2max = pi
        x3min = 0
        x3max = 2*pi
        x1min = 0
        x1max = R
        dx1 = .1
        dx2 = .05
        dx3 = .05
        dr = [1e-8]*3
        flx = 0
        x1 = x1min
        r = np.array(r) # center of sphere
        # Using Fubini's theorem
        while x1 < x1max:
            x2 = x2min
            while x2 < x2max:
                # dV is infinitesimal volume
                dV = x1**2*sin(x2)*dx1*dx2*dx3
                x3 = x3min
                while x3 < x3max:
                    # spherical coordinates
                    # [X1,X2,X3] is local cartesian
                    # coordinates of sphere
                    X1 = x1*cos(x3)*sin(x2)
                    X2 = x1*sin(x3)*sin(x2)
                    X3 = x1*cos(x2)
                    # r2 is global coordinates of sphere
                    r2 = np.array([X1,X2,X3]) + r
                    flx = flx + div(F,r2,dr)*dV
                    x3 = x3 + dx3
                x2 = x2 + dx2
            x1 = x1 + dx1
        return flx
    return G

def F_helper(ri,amount):
    def G(r):
        v = np.array(r) - np.array(ri)
        v_mag = np.linalg.norm(v)
        v_hat = v/v_mag
        w = amount*v_hat/v_mag**2
        return w
    return G

def dist(A,B):
    return np.linalg.norm(np.array(B)-np.array(A))

class Container:
    def __init__(self, center, radius):
        self.C = center
        self.R = radius
    def __contains__(self, r):
        flag = dist(self.C,r) <= self.R
        return flag
    def qty(self, F):
        flx = flux(F,self.R)(self.C)/(4*pi)
        return flx

# Describe containers
# Container A
C_A = [10,3,4]
C_B = [20,1,3] 
A = Container(center=C_A,
              radius=3)
B = Container(center=C_B,
              radius=4)

tmin = 0
tmax = 1
N = 10
dx = dist(C_A,C_B)/N
dt = 1/N
t = tmin
# transport quantity qty from center A.C to center B.C
curve = lambda t: lerp(A.C,B.C,t)
qty = 10
while t < tmax:
    F = F_helper(curve(t),qty)
    flx_A = A.qty(F)
    flx_B = B.qty(F)
    print(f"t = {t}, flx_A = {flx_A}, flx_B = {flx_B}")
    t = t + dt
