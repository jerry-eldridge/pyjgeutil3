from geometry_defs import N1,N2,N3,dx,dy,dz,N4
from numpy import array, zeros, ones, random, arange
from math import sqrt, log, fmod

def idx(i,j,k, l):
   global N1, N2, N3, N4
   n = l + N4*(k + N3*(j + N2*i))
   return n
def Support(i,lo,hi):
   return (i >= lo) and (i < hi)

# With x1 -> y1 and x2 -> y2, given x, return y using linear map
def MapTo(x1, y1, x2, y2, x):
    epsilon = 0.0001
    if abs(x2 - x1) > epsilon:
        m = 1.*(y2-y1)/(x2-x1)
    else:
        m = 1
    y = m*(x-x1)+y1
    return y

def D(f,idx,dr):
    def g(X,i,j,k):
        val = -1e8
        if idx == 0:
          val = 1.0*(f(X,i+1,j,k) - f(X,i,j,k))/dr[0]
        elif idx == 1:
          val = 1.0*(f(X,i,j+1,k) - f(X,i,j,k))/dr[1]
        elif idx == 2:
          val = 1.0*(f(X,i,j,k+1) - f(X,i,j,k))/dr[2]
        return val
    return g

# d_a d_b f(X,i,j,k) using dr as infinitesmal
def DD(f,idxs,dr):
   a,b = idxs
   return D(D(f,a,dr),b,dr)

def Dt(f,X,X_prev,i,j,k, dt):
   return (f(X,i,j,k) - f(X_prev,i,j,k))/dt

def div(F,dr):
    def g(X,i,j,k):
        val = 0
        for idx in range(3):
          val += D(F[idx],idx,dr)(X,i,j,k)
        return val
    return g

def grad(f,dr):
   L = [D(f,0,dr),D(f,1,dr),D(f,2,dr)]
   return L

def curl(F,dr):
   Fx,Fy,Fz = F
   L = [
       lambda X,i,j,k: D(Fz,1,dr)(X,i,j,k)-D(Fy,2,dr)(X,i,j,k),
       lambda X,i,j,k: -D(Fz,0,dr)(X,i,j,k)+D(Fx,2,dr)(X,i,j,k),
       lambda X,i,j,k: D(Fy,0,dr)(X,i,j,k)-D(Fx,1,dr)(X,i,j,k)]
   return L

def laplace(f,dr):
    def g(X,i,j,k):
        val = 0
        for idx in range(3):
            val += DD(f,[idx,idx],dr)(X,i,j,k)
        return val
    return g

def MaterialDerivativeScalar(f,v,dt,dr):
   def g(X,X_prev,i,j,k):
      val =  Dt(f,X,X_prev,i,j,k, dt) + \
         v[0](X,i,j,k)*D(f,0,dr)(X,i,j,k) + \
         v[1](X,i,j,k)*D(f,1,dr)(X,i,j,k) + \
         v[2](X,i,j,k)*D(f,2,dr)(X,i,j,k)
      return val
   return g

def PrintScalars(F,X):
   global N1,N2,N3
   for k in range(N3):
      for j in range(N2):
         for i in range(N1):
            s = '%0.2f ' % (F(X,i,j,k))
            print s,
         print
      print
   return

def PrintIntScalars(F,X):
   global N1,N2,N3
   for k in range(N3):
      for j in range(N2):
         for i in range(N1):
            s = '%3d ' % (int(F(X,i,j,k)))
            print s,
         print
      print
   return

def PrintVectors(v3,X):
   global N1,N2,N3
   for k in range(N3):
      for j in range(N2):
         for i in range(N1):
            v = [v[0](X,i,j,k), v[1](X,i,j,k), v[2](X,i,j,k)]
            s = '[%0.3f %0.3f %0.3f] ' % tuple(v)
            print s,
         print
      print
   return

def GetValList(X,func):
   global N1, N2, N3
   L = []
   for k in range(N3):
      for j in range(N2):
         for i in range(N1):
            L.append(func(X,i,j,k))
   return L

def meters(inches):
    return 0.3048*inches/12.0

def Getijk(x,y,z):
   global dx,dy,dz
   i = round(x/dx)
   j = round(y/dy)
   k = round(z/dz)
   return i,j,k

def Getxyz(i,j,k):
   global dx,dy,dz
   x = i*dx
   y = j*dy
   z = k*dz
   return x,y,z

def GetX(X,i,j,k,l):
   global N1, N2, N3, N4
   support = Support(i,0,N1) and Support(j,0,N2) and Support(k,0,N3) and Support(l,0,N4)
   err = 0
   if not support: return err
   n = idx(i,j,k,l)
   return X[n]

def SetX(X,i,j,k,l, val):
   global N1, N2, N3, N4
   support = Support(i,0,N1) and Support(j,0,N2) and Support(k,0,N3) and Support(l,0,N4)
   err = 0
   if not support: return X
   n = idx(i,j,k,l)
   X[n] = val
   return X

def SetPhi(X,i,j,k,val):
    SetX(X,i,j,k,0,val)
    return X
def GetPhi(X,i,j,k):
    """
    implicit function Phi
    """
    return GetX(X,i,j,k,0)

def norm(A):
    return sqrt(A[0]**2 + A[1]**2 + A[2]**2)

def kappa(X,i,j,k):
    """
    curvature of Phi (seems to be only -1 for interior
    and 1 for exterior and between for boundary. And values
    on the boundary.

    Formula of curvature kappa = div(grad(phi)/norm(grad(phi)))
    [1] "Level Set Methods and Dynamic Implicit Surfaces",
    Stanley Osher and Ronald Fedkiw, Applied Mathematical
    Sciences, vol 153, Springer

    However this is approximately the same thing
    as the Characteristic function of Phi's negative region
    scaled from [-1,1] to [0,1]. However, it is different on the
    boundary.
    """
    global dx,dy,dz
    G = grad(GetPhi,[dx,dy,dz])
    def F1(X,i,j,k):
        N = array(map(lambda f: f(X,i,j,k),G))
        N = N/(norm(N)+0.000001)
        return N[0]
    def F2(X,i,j,k):
        N = array(map(lambda f: f(X,i,j,k),G))
        N = N/(norm(N)+0.000001)
        return N[1]
    def F3(X,i,j,k):
        N = array(map(lambda f: f(X,i,j,k),G))
        N = N/(norm(N)+0.000001)
        return N[2]
    return div([F1,F2,F3],[dx,dy,dz])(X,i,j,k)

def kappa_scaled(X,i,j,k):
    val = MapTo(-1.05,0,1.05,255,kappa(X,i,j,k))
    return val

def chi(f):
    def g(X,i,j,k):
        if f(X,i,j,k) >= 0:
            return 1.0
        else:
            return 0.0
    return g
