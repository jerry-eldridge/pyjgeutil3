from .common import affine as aff
from . import extrusion as ext
from . import BasicShapes as ba
from . import wire as wi
from . import hairy_ball as hb

from math import pi,sin,cos,acos,sqrt,fmod

def create_cube():
    w,h,d = 100,100,100
    t = [0,50,0]
    s = [1,1,1]
    degrees = 0
    q = aff.HH.rotation_quaternion(degrees,0,1,0)
    H1 = ext.CubeObj(w,h,d,t,q,s)
    return H1

def create_cylinder():
    r = 50
    h = 100
    t = [0,50,0]
    s = [1,1,1]
    degrees = 90
    q = aff.HH.rotation_quaternion(degrees,1,0,0)
    H1 = ba.Cylinder(r,h,t,q,s,m=10,n=10)
    return H1

create_hairy_ball = hb.create_hairy_ball
