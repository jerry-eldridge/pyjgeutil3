import numpy as np
from math import fmod,pi,sin,cos

import vector_calculus as vc

BIGDATA = r"./"

fn_obj_1 = BIGDATA + "Sphere-01.obj"
A = vc.Container_3D_Object(fn_obj_1)
A.create()
AC = A.C

def F(r):
    x,y,z = r
    v = [10*cos(y),10*sin(y), 50]
    return v

flx = A.flux(F)
print(f"flux(F) = {flx}")



