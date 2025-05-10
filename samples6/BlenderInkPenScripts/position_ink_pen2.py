import bpy
import sys
sys.path.insert(0,r"C:/Users/jerry/Desktop/_Art/3D_Models/InkPen/")
import mini_my_universes as mmu
import numpy as np
import math
from copy import deepcopy

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
        dcursor[2] = 0
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

InkPen = bpy.data.objects.get("InkPen")
if InkPen is not None:
    if InkPen.animation_data and InkPen.animation_data.action:
        action = InkPen.animation_data.action
        fcurves = action.fcurves
        for fcurve in fcurves:
            if fcurve.data_path in {"location","rotation_euler","scale"}:
                fcurve.keyframe_points.clear()

start_frame = 1
end_frame = 60
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end = end_frame


pen_t = [-0.070015, -0, 0.40184]
pen_R = [90,0,0]
pen_s = [.4,.4,.4]

if InkPen is not None:
    InkPen.location = tuple(pen_t)
    pen_R_2 = tuple([math.radians(deg) for deg in pen_R])
    InkPen.rotation_euler = tuple(pen_R_2)
    InkPen.scale = tuple(pen_s)

cursor_t = [-0.5887,0,0.000736]
cursor_R = [90,60,0]
cursor_t_last = deepcopy(cursor_t)
cursor_t_new = [-0.5887,1,0.000736]
cursor_t_last = position_pen(cursor_t_new,cursor_t_last,cursor_R,2)
cursor_t_new = [-0.5887,0,0.000736]
cursor_R = [90,0,0]
cursor_t_last = position_pen(cursor_t_new,cursor_t_last,cursor_R,30)
cursor_t_new = [0.487,0,5.0]
cursor_R = [0,50,0]
cursor_t_last = position_pen(cursor_t_new,cursor_t_last,cursor_R,60)

