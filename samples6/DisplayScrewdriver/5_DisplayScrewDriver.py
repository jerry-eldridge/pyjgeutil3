import camera_matrix as cmat
import numpy as np
import graphics_cv as racg
from copy import deepcopy

from math import acos,pi,fmod

mx = 700 # image width
my = 500 # image height

fn = f"./screwdriver2.obj"
pts_3d,F = cmat.read_obj_to_points(fn)
print(f"""
BBOX: {np.min(np.array(pts_3d),axis=0)},
      {np.max(np.array(pts_3d),axis=0)}
""")

##########################################
# Camera 1
R = [0,0,0]
q = cmat.HH.FromEuler(*R)
scale = 1
mm = 1/1000 # m
sfx = 1250
sfy = 1250
fx = sfx*mm
fy = sfx*mm
alpha_x = fx * mx 
alpha_y = fy * my
skew = 0 # skew is zero for eye
Ct = [4,4,4] # position of camera (eye)
cx,cy = [mx/2-800,my/2+300] # center of image (fovea)
cam1 = cmat.Camera(q,scale,alpha_x,alpha_y,skew,\
                cx,cy,Ct,mx,my)
R = cam1.aim([0,1,0],[0,0,0])
cam1.set_focal_lengths(sfx*mm,sfy*mm)

gr = racg.Graphics(w=mx,h=my)
color = [255,0,0]
gr.canvas = cam1.snapshot_of_pts(pts_3d, F, color)
gr.Text(f"f = {cam1.get_focal_lengths()} mm",
        50,50,[0,0,255],scale=0.75)
ch = gr.Show("result",-1)
gr.Save("screwdriver-snapshot.jpg")
gr.Close()

            
