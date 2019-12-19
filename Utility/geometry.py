from math import pi,sqrt

# volume of 3D shapes

# volume of a sphere
def VolumeSphere(r):
    return 4*pi/3.0*r**3

# volume of a box
def VolumeBox(w,h,d):
    return w*h*d

def VolumeCylinder(r,h):
    return pi*r**2*h

def VolumeEllipsoid(a,b,c):
    return 4*pi/3.0*a*b*c

def VolumeTorus(r,R):
    return 2*pi**2*R*r**2

def VolumePyramidRect(l,w,h):
    return 1/3.0*l*w*h

def VolumeCone(r,h):
    return 1/3.0*pi*r**2*h

def VolumeTetrahedron(a):
    return sqrt(2)/12.0*a**3

#http://en.wikipedia.org/wiki/Surface_area
# area of 3D shape

def AreaSphere(r):
    return 4.0*pi*r**2
def AreaTorus(R,r):
    return 4.0*pi*R*r
def AreaCylinderClosed(r,h):
    return 2.0*pi*r*(r+h)
def AreaCone(r,h):
    """
    r = radius of base
    h = height of cone
    """
    s = sqrt(r**2+h**2)
    return pi*r*(r+s)
def AreaPyramid(b,h):
    """
    b = base height
    h = vertical height
    """
    s = sqrt((b/2.0)**2+h**2)
    return b**2 + 2*b*s

def AreaCircle(r):
    return pi*r**2

def LengthCircle(r):
    return 2*pi*r

def LengthArc(r,theta):
    """
    Length of an arc of circle with theta in radians
    """
    return r*theta

def CompleteElliptic2nd(k,dt=0.001):
    """
    E(k) the complete elliptic integral
    of the second kind
    http://en.wikipedia.org/wiki/Elliptic_integral#Complete_elliptic_integral_of_the_second_kind
    """
    S = 0
    t = 0
    k2 = k**2
    
    while t < 1-dt:
        t2 = t**2
        val = sqrt(1-k2*t2)/sqrt(1-t2)
        S += val*dt
        t += dt
    return S
    
def LengthEllipse(a,b):
    A = max(a,b)
    B = min(a,b)
    e = sqrt(1-1.0*B**2/A**2)
    C = 4*A*CompleteElliptic2nd(e)
    return C


