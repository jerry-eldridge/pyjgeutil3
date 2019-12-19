import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import QuaternionGroup as QG
import vectors
import mapto
import graph
import affine as aff
import graphics_cv as racg

import numpy as np
from math import pi,acos
from copy import deepcopy

def Mul(A,B):
     return np.einsum('ij,jk->ik',A,B)
def Transform3(shape, T):
     shape4 = map(lambda pt: pt+[1], shape)
     SHAPE4 = map(lambda pt: list(np.einsum('ij,j->i',T,pt)), shape4)
     SHAPE = map(lambda pt: list(1.0*np.array(pt)/pt[3]),SHAPE4)
     SHAPE = map(lambda pt: pt[:3], SHAPE)
     return SHAPE

# transform points with 4x4 transformation matrix T
def Transform(shape,T):
     return Transform3(shape,T)

# round-off numbers in list of points shape
def Round(shape):
     shape = map(lambda pt: map(lambda x: int(round(x)),pt), shape)
     return shape

q2R = aff.q2R

def t2T(t):
     T = vectors.translation_matrix(t[0],t[1],t[2])
     return T
def s2S(s):
     S = vectors.scale_matrix(t[0],t[1],t[2])
     return S
def lerp(v1,v2,t):
     A = np.array(v1)
     B = np.array(v2)
     C = A*(1-t) + B*t
     v = list(C)
     return v

def lerptsq(t1,s1,q1, t2,s2,q2, t):
     t3 = lerp(t1,t2,t)
     s3 = lerp(s1,s2,t)
     q3 = lerp(q1,q2,t) # quaternions as 4-vector
     return t3,s3,q3

# rotate points shape with quaternion q
def Rotate(shape,q,align=True):
     R = q2R(q.q)
     SHAPE = Transform(shape,R)
     if align:
         SHAPE = Round(SHAPE)
     return SHAPE

# Translate points shape by [tx,ty,tz]
def Translate(shape,tx,ty,tz,align=True):
     T = vectors.translation_matrix(tx, ty, tz)
     SHAPE = Transform(shape,T)
     if align:
         SHAPE = Round(SHAPE)
     return SHAPE

# Scale points shape by [sx,sy,sz]
def Scale(shape,sx,sy,sz,align=True):
     T = vectors.scale_matrix(sx, sy, sz)
     SHAPE = Transform(shape,T)
     if align:
         SHAPE = Round(SHAPE)
     return SHAPE

# Center of 3D points
def Center(pts,flag2d = False):
     PTS = map(lambda pt: np.array(pt), pts)
     X = map(lambda pt: pt[0], PTS)
     Y = map(lambda pt: pt[1], PTS)
     if flag2d:
         C = [np.mean(X),np.mean(Y)]
     else:
         Z = map(lambda pt: pt[2], PTS)
         C = [np.mean(X),np.mean(Y),np.mean(Z)]
     return C

def AimAxis(axis1,axis2):
    # Create V1 and V2 vectors of polygon1 normal and [0,0,1] z-axis
    V1 = axis1
    V2 = axis2 # z-axis
    V1 = np.array(V1)
    V2 = np.array(V2)
    # create a rotation axis to rotate V1 to V2
    # and compute angle in degrees of rotation, obtain quaternion for this
    axis = np.cross(V1,V2)
    angle = acos(np.inner(V1,V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))
    degrees = angle*180/pi
    q = QG.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    return q

def DrawRay(gr,O,V,color):
    O = np.array(O)
    V = np.array(V)
    t = 500
    A = list(O)
    B = list(O+t*V)
    gr.Line(A,B,color)
    return

def PlotGraph(gr,G,color):
    for e in G['E']:
        A,B = map(lambda v: G['pts'][v],e)
        gr.Line(A,B,color)
    return

def AimGraph(G,s,t,axis1, pt_gaze):
    O = np.array(t)
    B = np.array(pt_gaze)
    V = B - O
    b = np.linalg.norm(V)
    epsilon = 1e-8
    if abs(b) > epsilon:
        V = V/b
    q = AimAxis(axis1,V)
    R = q2R(q.q)
    pts = G['pts']
    C = Center(pts)
    pts2 = Translate(pts,-C[0],-C[1],-C[2])
    pts2 = Scale(pts2,s[0],s[1],s[2])
    pts2 = Transform(pts2,R)
    pts2 = Translate(pts2,t[0],t[1],t[2])
    G2 = deepcopy(G)
    G2['pts']=pts2
    return G2

def DrawTarget(gr,G,s,t,color):
    sx,sy,sz = s
    tx,ty,tz = t
    pts = G['pts']
    C = Center(pts)
    pts2 = Translate(pts,-C[0],-C[1],-C[2])
    pts2 = Scale(pts2,sx,sy,sz)
    pts2 = Translate(pts2,tx,ty,tz)
    G2 = deepcopy(G)
    G2['pts']=pts2
    PlotGraph(gr,G2,color)
    return
     

use_mouse = True
pt_mouse = [0,0,0]
wn = "result"
if use_mouse:
    import cv2
    def getxy(event, x, y, flags, param):
        global pt_mouse
        if (event == cv2.EVENT_MOUSEMOVE):
            pt_mouse = [x,y,0]
            return
    def StartMouse():
        cv2.namedWindow(wn)
        cv2.setMouseCallback(wn,getxy)
        return
    StartMouse()

G0 = {}
G0['pts'] = [[0,0,0],[1,1,0],[1,-1,0]]
G0['V'] = range(len(G0['pts']))
G0['E'] = [[0,1],[1,2],[2,0]]

G = {}
G['pts'] = [[0,1,0],[4,0,0],[0,-1,0]]
G['V'] = range(len(G['pts']))
G['E'] = [[0,1],[1,2],[2,0]]
G_axis = [1,0,0] # direction of graph

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)
black = [0,0,0]
while True:
    gr.Clear()

    c = 100
    s = [15,5,5]

    t = [w/2-c,h/2,0]
    G2 = AimGraph(G,s,t,G_axis,pt_mouse)
    PlotGraph(gr,G2,black)

    t = [w/2+c,h/2,0]
    G3 = AimGraph(G,s,t,G_axis,pt_mouse)
    PlotGraph(gr,G3,black)

    t = [w/2+c,h/2-c,0]
    G4 = AimGraph(G,s,t,G_axis,pt_mouse)
    PlotGraph(gr,G4,black)

    s = [15,5,5]
    DrawTarget(gr,G0,s,pt_mouse,black)

    ch = gr.Show("result",15)
    if ch == ord('e'):
        break
gr.Close()
