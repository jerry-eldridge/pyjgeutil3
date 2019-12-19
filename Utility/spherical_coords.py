from math import sin,cos,sqrt,atan2,acos

def Spherical_x(r,theta,phi):
    x = r*sin(theta)*cos(phi)
    return x
def Spherical_y(r,theta,phi):
    y = r*sin(theta)*sin(phi)
    return y
def Spherical_z(r,theta,phi):
    return r*cos(theta)
def Spherical_r(x,y,z):
    return sqrt(x**2+y**2+z**2)
def Spherical_theta(x,y,z):
    return acos(z/Spherical_r(x,y,z))
def Spherical_phi(x,y,z):
    return atan2(y,x)
