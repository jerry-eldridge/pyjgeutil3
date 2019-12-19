import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import graphics_cv as racg
import graph

import numpy as np
from copy import deepcopy

def pyBezier4(gr, pts, color):
    assert(len(pts) == 4)
    w = gr.w
    h = gr.h
    M = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]])
    P1 = np.array([pts[0][0], pts[1][0], pts[2][0], pts[3][0]])
    P2 = np.array([pts[0][1], pts[1][1], pts[2][1], pts[3][1]])
    t = 0
    dt = 0.01
    Ma = M
    MP1 = P1
    MP2 = P2
    pt_last = None
    while (t <= 1.0):
        T = np.array([t*t*t, t*t, t, 1])
        Mt = T
        Mb = np.einsum('ij,j->i',Ma,MP1)
        x = np.einsum('i,i->',Mt,Mb)
        Mb = np.einsum('ij,j->i',Ma,MP2)
        y = np.einsum('i,i->',Mt,Mb)

        pt = [x,y]
        if pt_last is None:
            pt_last = pt
        gr.Line(pt_last,pt, color)
        pt_last = pt
        t += dt
    return

def pyBezier(gr, pts, color):
    if len(pts) == 0:
        return
    elif len(pts) == 1:
        gr.Point(pts[0],color)
    elif len(pts) == 2:
        gr.Line(pts[0],pts[1],color)
    elif len(pts) == 3:
        gr.Line(pts[0],pts[1],color)
        gr.Line(pts[1],pts[2],color)
    elif len(pts) == 4:
        pyBezier4(gr, pts, color)
    else:
        pts0 = pts[:4]
        pts1 = pts[3:]
        pyBezier4(gr,pts0,color)
        pyBezier(gr,pts1,color)
    return

def d(A,B):
    A = np.array(A)
    B = np.array(B)
    return np.linalg.norm(A-B)

# k-nearest neighbor, knn, with k = 1
def knn(pts,pt):
    C = pts[0]
    oo = 1e8
    d0 = oo
    for A in pts:
        d1 = d(A,pt)
        if d1 < d0:
            d0 = d1
            C = A
    return C

def PlotGraph(gr,G,color):
    for e in G['E']:
        A,B = map(lambda v: G['pts'][v], e)
        gr.Line(A,B,color)
    return

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)

wn = "result"
use_mouse = True
pt_mouse = [0,0]
flag_lbutton = False
pts = []

select = False
i_select = 0
if use_mouse:
     import cv2
     def getxy(event, x, y, flags, param):
         global pt_mouse,flag_lbutton,pts,i_select
         if (event == cv2.EVENT_LBUTTONDOWN):
             flag_lbutton = not flag_lbutton
             if not select:
                 pts.append([x,y])
             else:
                 C = knn(pts,pt_mouse)
                 i_select = pts.index(C)
             return
         if (event == cv2.EVENT_RBUTTONDOWN):
             return
         if (event == cv2.EVENT_MOUSEMOVE):
             pt_mouse = [x,y]
             return
     def StartMouse():
         cv2.namedWindow(wn)
         cv2.setMouseCallback(wn,getxy)
         return
     StartMouse()


red = [255,0,0]
blue = [0,0,255]
green = [0,255,0]
i = 0
mouse = False
print """
Left-Mouse Click on screen to add points.
Four points creates a bezier curve and not four
a straight line for that segment.
Press 's' for select mode. Press 'd' for
move mouse cursor mode. Press 'c' for clear
screen. Press 'e' to exit.
"""
while True:
    gr.Clear()
    pyBezier(gr, pts, color=red)
    G = graph.Pn(len(pts))
    G['pts'] = deepcopy(pts)
    #PlotGraph(gr,G,color=[240,255,240])
##    for pt in pts:
##        gr.Point(pt,color=blue)
    if select and i_select is not None:
        C = pts[i_select]
        gr.Point(C,green)
        gr.Text("Select",50,50,color=red)
    ch = gr.Show("result",15)
    if ch == ord('e'):
        break
    if ch == ord('a'):
        i = (i+1)%len(pts)
    if ch == ord('s'):
        select = not select
        mouse = False
    if ch == ord('d'):
        mouse = not mouse
    if ch == ord('c'):
        pt_mouse = [0,0]
        flag_lbutton = False
        pts = []
        select = False
        i_select = 0
        mouse = False
    if select and mouse:
        pts[i_select]= pt_mouse
gr.Close()
