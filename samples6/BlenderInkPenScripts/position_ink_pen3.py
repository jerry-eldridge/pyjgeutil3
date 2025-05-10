import bpy
import sys
sys.path.insert(0,r"C:/Users/jerry/Desktop/Write3D/")
import mini_my_universes as mmu
import numpy as np
import math
from copy import deepcopy
import random

seed0 = 12345
random.seed(seed0)

def position_pen(cursor_t_new,cursor_t_last,cursor_R,frame_number):
    InkPen = bpy.data.objects.get("InkPen")
    if InkPen is not None:
        O1 = list(InkPen.location)
        tip1 = cursor_t_last
        shape0 = [O1,tip1]
        V1 = np.array(O1)-np.array(tip1)
        shape1 = mmu.Translate(shape0, V1[0],V1[1],V1[2],align=False)
        O2,tip2 = shape1
        R0 = list(InkPen.rotation_euler)
        R = tuple([math.degrees(x) for x in R0])
        q0 = mmu.FromEuler(*R)
        q1 = mmu.FromEuler(*cursor_R)
        dq = q1*q0.inv()
        
        shape2 = mmu.Rotate(shape1, dq, align=False)
        O3,tip3 = shape2
        V2 = np.array(tip3) - np.array(O3)
        shape3 = mmu.Translate(shape2, V2[0],V2[1],V2[2],align=False)
        O4,tip4 = shape3
        
        dcursor = np.array(cursor_t_new)-np.array(cursor_t_last)
        tip4 = np.array(tip4) + dcursor
        O4 = np.array(O4) + dcursor
        tip4 = list(map(float,list(tip4)))
        O4 = list(map(float,list(O4)))
        InkPen.location = tuple(O4)
            
                
        cursor_R_2 = tuple([math.radians(deg) for deg in cursor_R])
        InkPen.rotation_euler = cursor_R_2
        InkPen.keyframe_insert(\
            data_path="location",
                frame=frame_number)
        InkPen.keyframe_insert(\
            data_path="rotation_euler",
                frame=frame_number)
        InkPen.keyframe_insert(\
            data_path="scale",
                frame=frame_number)
    return tip4

def PutSymbolTransform(x,y, sx,sy):
    xx = x/200.0
    yy = y/200.0
    x = xx*sx
    y = yy*sy
    return [x,y]

def PutSymbol(ch,cx,cy,font,sx,sy,z_down,z_up):
    x = 0
    y = 0
    c = ord(ch)
    fn = f"{font}/{c}.txt"
    f = open(fn,'r')
    txt = f.read()
    f.close()
    done = False
    pen_down = False
    lines = txt.split('\n')
    pts = []
    z = z_up
    while (not done):
        command = ' '
        buff = ""
        line = lines[0].strip()
        lines = lines[1:]
        toks = line.split(' ')
        cmd = toks[0]
        if cmd == 'D':
            x,y = list(map(float,toks[1:]))
            y = 200 - y
            x = x - 100
            y = y - 100
            x,y = PutSymbolTransform(x,y,sx,sy)
            x = x + cx
            y = y + cy
            z = z_down
            pt = [x,y,z]
            pts.append(pt)
            last_pt = pt
            pen_down = True
            done = False
        elif cmd == "M":
            x,y = list(map(float,toks[1:]))
            y = 200 - y
            x = x - 100
            y = y - 100
            x,y = PutSymbolTransform(x,y,sx,sy)
            x = x + cx
            y = y + cy
            pt = [x,y,z]
            pts.append(pt)
            done = False
        elif cmd == "U":
            pt = pts[-1]
            x,y,z = pt
            z = z_up
            pt = [x,y,z]
            pts.append(pt)
            pen_down = False
            z = z_up
            done = False
        elif cmd == "E":
            done = True
    return pts

# Cube that is 1 x 1 x 1

# sheet of paper (this was the transform for
# the sheet of paper created from a cube)
T = [0,0,0]
R = [0,0,0]
S = [0.850, 1.100, 0.001]

txt_paper = """
o Paper
v -0.850000 -0.001000 1.100000
v -0.850000 0.001000 1.100000
v -0.850000 -0.001000 -1.100000
v -0.850000 0.001000 -1.100000
v 0.850000 -0.001000 1.100000
v 0.850000 0.001000 1.100000
v 0.850000 -0.001000 -1.100000
v 0.850000 0.001000 -1.100000
vn -1.0000 -0.0000 -0.0000
vn -0.0000 -0.0000 -1.0000
vn 1.0000 -0.0000 -0.0000
vn -0.0000 -0.0000 1.0000
vn -0.0000 -1.0000 -0.0000
vn -0.0000 1.0000 -0.0000
vt 0.375000 0.000000
vt 0.625000 0.000000
vt 0.625000 0.250000
vt 0.375000 0.250000
vt 0.625000 0.500000
vt 0.375000 0.500000
vt 0.625000 0.750000
vt 0.375000 0.750000
vt 0.625000 1.000000
vt 0.375000 1.000000
vt 0.125000 0.500000
vt 0.125000 0.750000
vt 0.875000 0.500000
vt 0.875000 0.750000
s 0
f 1/1/1 2/2/1 4/3/1 3/4/1
f 3/4/2 4/3/2 8/5/2 7/6/2
f 7/6/3 8/5/3 6/7/3 5/8/3
f 5/8/4 6/7/4 2/9/4 1/10/4
f 3/11/5 7/6/5 5/8/5 1/12/5
f 8/5/6 4/13/6 2/14/6 6/7/6
"""

lines = txt_paper.split('\n')
pts = []
for line in lines:
    if len(line) == 0:
        continue
    toks = line.split(' ')
    if toks[0] == 'v':
        x,y,z = list(map(float,toks[1:]))
        pt = [x,y,z]
        pts.append(pt)
P = np.array(pts)

# create bounding box and we note that the sheet of paper
# has not been rotated and has a simple bounding
# box that reflects the sheet of paper better
xmin = float(np.min(P[:,0]))
xmax = float(np.max(P[:,0]))
ymin = float(np.min(P[:,1]))
ymax = float(np.max(P[:,1]))
zmin = float(np.min(P[:,2]))
zmax = float(np.max(P[:,2]))
bbox = [[xmin,xmax],[ymin,ymax],[zmin,zmax]]
print(f"bbox = {bbox}")
O = np.mean(P,axis=0)
O = list(map(float,list(O)))
print(f"O = {O}")

# These points are just some of the points P making
# up the sheet of paper. Because the sheet of paper's
# bounding box is the same as the points P:

# bottom left
A_BL = [xmin,ymin,zmax]
# bottom right
A_BR = [xmax,ymin,zmax]
# top left
A_TL = [xmin,ymax,zmax]
# top right
A_TR = [xmax,ymax,zmax]

# which also have indices idx of the points P[idx,:].

# form vector space for paper
# basis vector on x-axis
xhat = np.array(A_BR)-np.array(A_BL)
xhat = xhat/np.linalg.norm(xhat)
# basis vector on y-axis
yhat = np.array(A_TL)-np.array(A_BL)
yhat = yhat/np.linalg.norm(yhat)
# basis vector on z-axis, depth of on paper at 0
# or above paper with pen
yhat = np.array(A_TL)-np.array(A_BL)
yhat = yhat/np.linalg.norm(yhat)

# thus a coordinate of a point written on paper
# will be [x,y,z] as meaning
# pt = x*xhat + y*yhat + z*zhat
width = xmax - xmin
height = ymax - ymin
depth = zmax - zmin
# where x ranges from 0 to width-1, y ranges from
# 0 to height-1, and z ranges from 0 to depth-1.


font = f"c:/users/jerry/desktop/Write3D/emma_font3/"
z_down = 0.4
z_up = 0.45
word = "apple"
cx,cy = [-.5,0]
pts = []
for i in range(len(word)):
    ch = word[i]
    sx = 1/4
    sy = 1/4
    pts_i = PutSymbol(ch,cx,cy,font,sx,sy,z_down,z_up)
    cx,cy,z = pts_i[-1]
    cx = cx + .1
    pts = pts + pts_i

InkPen = bpy.data.objects.get("InkPen")
if InkPen is not None:
    if InkPen.animation_data and InkPen.animation_data.action:
        action = InkPen.animation_data.action
        fcurves = action.fcurves
        for fcurve in fcurves:
            if fcurve.data_path in {"location","rotation_euler","scale"}:
                fcurve.keyframe_points.clear()

start_frame = 1
end_frame = len(pts)+1
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end = end_frame


pen_t = [0,0,0]
pen_R = [90,0,0]
pen_s = [.4,.4,.4]

if InkPen is not None:
    InkPen.location = tuple(pen_t)
    pen_R_2 = tuple([math.radians(deg) for deg in pen_R])
    InkPen.rotation_euler = tuple(pen_R_2)
    InkPen.scale = tuple(pen_s)

cursor_t = [0,0,0.000736]
cursor_t_last = deepcopy(cursor_t)

for i in range(len(pts)):
    pt = pts[i]
    x,y,z = pt
    z = z - .1
    pt = [x,y,z]
    cursor_t_new = pt
    cursor_R = [50,0,0]
    cursor_t_last = position_pen(\
        cursor_t_new,cursor_t_last,cursor_R,i+1)

