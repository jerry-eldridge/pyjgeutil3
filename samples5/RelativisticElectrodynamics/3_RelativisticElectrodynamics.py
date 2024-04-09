from sympy.combinatorics import Permutation
import numpy as np

#from sympy import sqrt
from math import sqrt,fmod,pi,sin,cos

n = 4 # number of dimensions of spacetime

def norm(x):
    x = list(map(float, x))
    val = np.linalg.norm(x)
    return val

def dist(x,y):
    return norm(np.array(y)-np.array(x))

# [1] https://en.wikipedia.org/wiki/Raising_and_lowering_indices
# Minkowski spacetime, metric
eta = np.array([
    [-1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]])


# https://en.wikipedia.org/wiki/Levi-Civita_symbol
def epsilon_civita0(a,b,c,d):
    if len(list(set([a,b,c,d]))) != n:
        return 0
    pi = Permutation([a,b,c,d])
    if pi.is_even:
        return 1
    elif pi.is_odd:
        return -1
    else:
        return 0
epsilon_civita = np.zeros((n,n,n,n))
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                epsilon_civita[a,b,c,d] = \
                    epsilon_civita0(a,b,c,d)

# https://en.wikipedia.org/wiki/Electromagnetic_tensor
# field tensor F contravariant
def F_con(E,B,c):
    val = np.array([
        [0, -E[0]/c, -E[1]/c, -E[2]/c],
        [E[0]/c, 0, -B[2], B[1]],
        [E[1]/c, B[2], 0, -B[0]],
        [E[2]/c, -B[1], B[0],0]])
    return val
# field tensor F covariant
def F_cov(E,B,c):
    val = np.einsum('ad,ba,cb->cd',
            eta,F_con(E,B,c),eta)
    return val

# Faradays tensor's Hodge dual, contravariant
def G_con(E,B,c):
    val = 0.5*np.einsum('abcd,cd->ab',\
            epsilon_civita, F_cov(E,B,c))
    return val

def Lorentz_boost0(v_hat, v_mag, x_spacetime):
    gamma = 1/sqrt(1 - v_mag**2/c**2)
    t = x_spacetime[0]
    r = np.array(x_spacetime[1:4])
    n = np.array(v_hat)
    n = n/np.linalg.norm(n)
    w1 = np.array([n[0],0,0])
    w2 = np.array([0,n[1],0])
    w3 = np.array([0,0,n[2]])
    v = v_mag
    r_parl = (np.inner(r,w1)*w1 + \
             np.inner(r,w2)*w2 + \
             np.inner(r,w3)*w3)
    r_perp = r - r_parl
    beta = v*n/c
    tp = gamma*(t - np.inner(beta,r_parl)/c)
    rp_perp = r_perp
    rp_parl = gamma*(r_parl - beta*c*t)
    rp = rp_parl + rp_perp
    y_spacetime = [tp,
        rp[0],
        rp[1],
        rp[2]]
    return y_spacetime

def Lorentz_boost(v_hat,v_mag):
    I = np.identity(n)
    J = []
    for i in range(n):
        x_spacetime = list(I[i].flatten())
        y_spacetime = Lorentz_boost0(v_hat,v_mag,
                        x_spacetime)
        J.append(y_spacetime)
    return np.array(J)

def get_E_B(F):
    E = np.array([-F[0,1]*c, -F[0,2]*c, -F[0,3]*c])
    B = np.array([-F[2,3],F[1,3],-F[1,2]])
    return E,B

def Transform(v_hat,v_mag,E,B,c):
    print(f"Transformation of E and B")
    v_hat = np.array(v_hat)
    v_hat = list(v_hat/np.linalg.norm(v_hat))
    print(f"="*30)
    print(f"Inputs:")
    print(f"c = {c}")
    print(f"v_hat = {v_hat}")
    print(f"v_mag = {v_mag/c}*c")
    print(f"E = {E}")
    print(f"B = {B}")
    print(f"|E| = {norm(E)} V/m")
    print(f"|B| = {norm(B)*c**2} T*c**2")
    print()
    print(f"Outputs:")
    F = F_con(E,B,c)
    print(f"Field tensor (contravariant): F = \n{F}")
    print()
    G = G_con(E,B,c)
    print(f"Hodge dual (contravariant) G = \n{G}")
    print()

    Lam = Lorentz_boost(v_hat,v_mag)
    print(f"Lorentz boost Lam = \n{Lam}")
    print()

    print(f"Transformed:")
    Fp = np.einsum('ml,ns,ls->mn',
        Lam,Lam,F)
    print(f"Fp = \n{Fp}")
    print()
    Ep,Bp = get_E_B(Fp)
    print(f"Ep = {Ep}")
    print(f"Bp = {Bp}")
    print(f"|Ep| = {norm(Ep)} V/m")
    print(f"|Bp| = {norm(Bp)*c**2} T*c**2")
    print(f"="*30)
    return

lerp = lambda A,B,t: np.array(A)*(1-t) + np.array(B)*t
deriv = lambda h: lambda f: lambda x: (f(x+h)-f(x))/h

# gradient_4(A,i,j) at spacetime coordinate s (indices)
# = (st,sx,sy,sz) with spatial dr = (dt,dx,dy,dz)
def gradient_4(A,i,j,s,dr):
    L = []
    I = np.identity(n,dtype=np.uint8)
    v = I[i]
    # For example with s = [st,sx,sy,sz] and
    # i = 0, then s2 = [st+1,sx,sy,sz]. For
    # i = 1, then s2 = [st,sx+1,sy,sz]. Etc.
    # partial(A,0,j) =
    # (A[j,st+1,sx,sy,sz] - A[j,st,sx,sy,sz])/dt
    # partial(A,1,j) =
    # (A[j,st,sx+1,sy,sz] - A[j,st,sx,sy,sz])/dx
    # Etc. Also 4-gradient divides partial(A,0,j) by c
    s2 = list(np.array(s) + 1*v)
    val = (A[j,*s2] - A[j,*s])/dr[i]
    if i == 0:
        val = val/c
    return val

def Base(i,base, bits):
    L = []
    j = 0
    n = 0
    ii = i
    for j in range(bits):
        a = ii%base
        ii = int(ii/base)
        n = n + a*base**j
        L.append(a)
    L.reverse()
    return L

def calc_F(A):
    F = np.zeros((n,n,*([m]*n)),dtype=np.float16)
    for mu in range(n):
        for nu in range(n):
            for i in range(m**n):
                s = Base(i,m,n)
                if min(s) == 0:
                    continue
                if max(s) == m-1:
                    continue
                F[mu,nu,*s] = \
                    gradient_4(A,mu,nu,s,dr) - \
                    gradient_4(A,nu,mu,s,dr)
    return F

c = 100 #299792458 # speed of light

m = 10
nt = m # temporal t number of indices
nx = m # spatial x number of indices
ny = m # spatial y number of indices
nz = m # spatial z number of indices

tmin = 0 # t minimum
tmax = 1 # t maximum
xmin = 0 # x minimum
xmax = 100 # x maximum
ymin = 0 # y minimum
ymax = 100 # y maximum
zmin = 0 # z minimum
zmax = 100 # z maximum
dt = (tmax-tmin)/nt # temporal resolution
dx = (xmax-xmin)/nx # spatial resolution x
dy = (ymax-ymin)/ny # spatial resolution y
dz = (zmax-zmin)/nz # spatial resolution z

dr = [dt,dx,dy,dz] # spacetime resolution

# get spacetime coordinate rs
def s_to_rs(*s):
    it,ix,iy,iz = s
    # spacetime coordinate
    rs= [tmin+it*dt,
          xmin+ix*dx,
          ymin+iy*dy,
          zmin+iz*dz]
    return rs

# this should be 4 to make A[n] at (t,x,y,z)
# and to make F[n,n] at (t,x,y,z)

# Maxwell's equations with Lorentz gauge are:
# box A[nu,*x] = J[nu,*x] with solution
# A[nu,*x] = (1/box) J[nu,*x] where (1/box) is
# the Green's function or the propagator PI(x,y)
# propagating from x to y the source J(x) to A(y).

# x is source point indices
x = [1,2,3,2] # spacetime (it,ix,iy,iz) indices

# current density
J = np.zeros((n, *([m]*n)),dtype=np.float16)
A = np.zeros((n, *([m]*n)),dtype=np.float16)
#A = np.random.rand(n,nt,nx,ny,nz)

# make J = (-e/laplace)*dirac_delta at indices x2[1:]
# then A[1:3,*y] = 0 but A[0,*y] = (e/(4*pi))*(1/r)
# with r the distance between x and y.

# calculate A given coulomb's law for a point charge
# of electric charge e.

# y is propagated point A(y) = Integral PI(x,y) * J(x)
# with J(x) = e*dirac_delta(x) and PI = (1/box).
q = 10

A[1:4,:,:,:,:] = 0 # set vector potential A = [0,0,0]
# set A0 = (e/(4*pi))*(1/r)
for i in range(m*m*m*m):
    s = Base(i,m,n)
    if min(s) == 0:
        continue
    if max(s) == m-1:
        continue
    # This calculations the propagation of J(x) to
    # A(s)
    r1 = s_to_rs(*x)[1:] # (r1t,r1x,r1y,r1z)[1:]
    r2 = s_to_rs(*s)[1:] # (r2t,r2x,r2y,r2z)[1:]
    r = dist(r1,r2) # distance between spatial r1 and r2
    oo = 100 # infinity
    epsilon = 1e-4 # epsilon
    if abs(r) > epsilon:
        A[0,*s] = (q/(4*pi))*(1/r) # coulomb's law
    else:
        A[0,*s] = oo # if r = 0, set to oo.

F = calc_F(A)
# indices must be in range(m).

# calculate electric field E and magnetic field
# B at x. This calculates the electric and magnetic
# fields at spacetime indices y.
y = [1,3,2,1] # spacetime indices
E,B = get_E_B(F[:,:,*y])
print(f"E(y) = {E} V/m")
print(f"B(y) = {B*c**2} T*c**2")

## [1]
##@book{Griffiths17,
##author = "Griffiths, David J.",
##title = "Introduction to Electrodynamics - 4th Ed",
##publisher = "Cambridge University Press",
##year = "2017"
##}
## (see page 57, Problem 1.62)
def area_curve(curve,dt=1e-8):
    a = np.array([0,0,0])
    t = 0
    while t < 1:
        # make it a closed curve with fmod
        t1 = fmod(t,1)
        t2 = fmod(t+dt,1)
        r = curve(t1)
        dl = curve(t2)-r
        a = a + np.cross(r,dl)
        t = t + dt
    a = 0.5*a
    return a

def circle(t):
    C = np.array([(xmin+xmax)/2,
                  (ymin+ymax)/2,
                  (zmin+zmax)/2])
    radius = (zmin+zmax)/3
    theta = 2*pi*t
    x = C[0] + radius*cos(theta)
    y = C[1] + radius*sin(theta)
    z = C[2]
    pt = np.array([x,y,z])
    return pt

# See [1] page 253, Magnetic Vector Potential A
# magnetic dipole moment (first approximation to A)
def A_dipole(I,curve,dt):
    a = area_curve(curve,dt)
    #print(f"a = area(curve) = {a}")
    #print(f"|a| = {np.linalg.norm(a)}")
    m = I*a
    #print(f"Magnetic dipole moment: m = {m}")
    def f(r):
        mu0 = 4*pi*1e-7 # N/A**2
        r = np.array(r)
        rmag = np.linalg.norm(r)
        rhat = r/rmag
        A = (mu0/(4*pi))*np.cross(m,rhat)/rmag**2
        return A
    return f

I = 1000 # Amperes
curve = circle
A = np.zeros((n, *([m]*n)),dtype=np.float16)
A[0,:,:,:,:] = 0 # set electric potential V_E = 0
# set A0 = (e/(4*pi))*(1/r)
for i in range(m*m*m*m):
    s = Base(i,m,n)
    if min(s) == 0:
        continue
    if max(s) == m-1:
        continue
    # This calculations the propagation of J(x) to
    # A(s)
    r1 = s_to_rs(*x)[1:] # (r1t,r1x,r1y,r1z)[1:]
    r2 = s_to_rs(*s)[1:] # (r2t,r2x,r2y,r2z)[1:]
    A[1:4,*s] = A_dipole(I,curve,1e-2)(r2) # coulomb's law

F = calc_F(A)
# indices must be in range(m).

# calculate electric field E and magnetic field
# B at x. This calculates the electric and magnetic
# fields at spacetime indices y.
y = [1,3,2,1] # spacetime indices
E,B = get_E_B(F[:,:,*y])
print(f"E(y) = {E} V/m")
print(f"B(y) = {B*c**2} T*c**2")

v_hat = [1,0,0] # particle unit velocity
v_mag = 0.7*c # m/s, particle speed
gamma = 1/sqrt(1-v_mag**2/c**2) # gamma

Transform(v_hat,v_mag,E,B,c)

