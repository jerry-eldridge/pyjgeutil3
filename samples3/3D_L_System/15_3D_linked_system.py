import BasicShapes as bs
import extrusion as ext
import affine as aff
import grammar_system as gsm
import linked_system as lsm

import numpy as np
from copy import deepcopy

from functools import reduce

from math import cos,sin,pi,fmod

import random

seed = 123123123
random.seed(seed)

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

# Note Sigma is 'A','B','x','i','y','j','z','k','[',
# and ']'.
start = "S"

# A rule is a list (LHS,RHS,p) where
# LHS -> RHS with probability p.
start1 = "S"
rules1 = [
    ("S","[DxDxDx]",.9),
    ("D","[EyEyEy]",.9),
    ("E","[FzFzFz]",.9),
    ("F","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start2 = "S"
rules2 = [
    ("S","o[HHH]",1),
    ("H","FoG",1),
    ("G","zFxx",1),
    ("F","[DDDDD]",.9),
    ("D","Exyz",.9),
    ("E","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start3 = "D"
rules3 = [
    ("D","N",1),
    ("N","[E]O",1),
    ("O","ffffff",1),
    ("E","XZF",1),
    ("F","XZG",1),
    ("G","XZH",1),
    ("H","XZIX", 1),
    ("I","YJ",1),
    ("J","XWK",1),
    ("K","XWL",1),
    ("L","XWM",1),
    ("M","XW", 1),
    ("X","aaaa",1),
    ("Y","yyyy",1),
    ("Z","zzzz",1),
    ("W","xxxx",1),
    ("[","<(",1),
    ("]",")>",1)
    ]

start4 = "S"
rules4 = [
    ("S","[CC]",1),
    ("C","BBBB",1),
    ("B","aO",1),
    ("O","xGy",1),
    ("G","FFFF",1),
    ("F","ffff",1)
    ]

start5 = "S"
rules5 = [
    ("S","[CC]",1),
    ("C","BBBB",1),
    ("B","aO",1),
    ("O","xGy",1),
    ("G","FFFF",1),
    ("F","f",1),
    ("[","<(",1),
    ("]",")>",1)
    ]

start6 = "S"
# x-axis is one a, y-axis is two a's, z-axis is three a's
# x-axis is [a], y-axis is [zzzzaa], z-axis is [jjjjaaa].
rules6 = [
    ("S","o[a][zzzzaa][jjjjaaa]",1),
    ("[","<(",1),
    ("]",")>",1)
     ]

#line2 = gsm.Grammar_to_line2(start1,rules1,
#                gsm.line,gsm.point,flag=False,n=2)
s_sys1 = lsm.E("a**4")
print("There are |s_sys1| = ",len(s_sys1),"segments.")
print("s_sys1 = ",s_sys1)
s10 = lsm.PathSystem(s_sys1,
            [(0,0,0),(0,0,0),(0,0,0)])
s11 = lsm.PathSystem(s_sys1,
            [(0,1,0),(0,0,0),(0,0,0)])
s12 = lsm.PathSystem(s_sys1,
            [(0,1,0),(1,0,0),(0,0,0)])
s13 = lsm.PathSystem(s_sys1,
            [(0,1,0),(2,0,0),(0,0,0)])
s14 = lsm.PathSystem(s_sys1,
            [(0,1,0),(2,0,0),(0,0,-1)])


line2 = gsm.Grammar_to_line2(
    start6,rules6,gsm.line,gsm.point,
                flag=True,n=2)

G,Gs = gsm.Shape0(start5,rules5,line2,
                    gsm.point,flag=True,n=2)

line2 = gsm.String_to_line2(s10,gsm.point,gsm.point,
                flag=False,n=2)
#G2,Gs2 = gsm.Shape0(start5,rules5, line2, gsm.point,
#              flag=True, n=2)
print("|pts(G)| = ",len(G['V']))
    
# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"3D_L_system_7.obj",Gs,"scene")

# Double-Click on OBJ file
import os
os.system(BIGDATA+"3D_L_system_7.obj")
