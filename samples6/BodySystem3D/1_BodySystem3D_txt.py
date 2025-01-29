import sys
sys.path.append(r"./my_universes")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as bs
import universes.volume_of_OBJ as voo
from copy import deepcopy
import universes.transform_shape as ts
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.common.vectors as vec
import universes.shapes.common.CoordSystem as cs
import universes.shapes.common.human_doll as hd
from math import pi
import numpy as np
import time

import sys

##       |y axis
##       |
##       
##       o
##      ---
##       | CM (Center of Mass)
##      / \
##       ---------x axis
##      /O (Origin)
##     /
##    /z axis

## T = [tx,ty,tz], S = [sx,sy,sz], R = [rx,ry,rz]

#fn_save = r"./pose_data_126052.txt"
#print(f"Writing to fn_save = '{fn_save}'")
#f = open(fn_save,'w')
f = sys.stdout

def pose(P,e,R):
    P.pose(e,idx=0,R=R)
    return
        
O = [0,0,0] # standing on ground
P = hd.HumanDoll(O,weight_lbs=195,height_in=5*12+8)
P.build()

P.display(f)

# bend head forward rotating on x-axis by 20 degrees
pose(P,["neck","head"],R=[0,0,0])

# bend truck forward rotating on x-axis by 10 degrees
pose(P,["trunk","neck"],R=[45,0,0])

P.display(f)

f.close()





