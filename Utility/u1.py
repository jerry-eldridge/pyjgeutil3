from math import pi,atan2
from cmath import sin,cos
def theta(z):
    epsilon = 1e-8
    if abs(z.real) > epsilon:
        return atan2(z.imag,z.real)
    else:
        if abs(z.imag) > epsilon:
            return pi*z.imag/abs(z.imag)
        else:
            return 0
class u1:
    def __init__(S,theta):
        i = complex(0,1)
        e = complex(1,0)
        S.z = e*cos(theta)+i*sin(theta)
        return
    def __add__(S,z):
        return u1(theta(S.z+z.z))
    def __neg__(S):
        return u1(theta(-S.z))
    def __sub__(S,z):
        return u1(theta(S.z-z.z))
    def __mul__(S,z):
        return u1(theta(S.z*z.z))
    def __div__(S,z):
        return u1(theta(S.z/z.z))
    def __str__(S):
        return str(theta(S.z))
    def conjugate(S):
        return u1(theta(S.z.conjugate()))
    def Theta(S):
        return theta(S.z)
