import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import graphics_cv as racg

from math import sqrt
import myquadtree2 as qtr
import random

random.seed(123890123)

ww = 800
hh = 500

def DrawPolygon(gr,P,color):
    n = len(P)
    for i in range(n):
        A = P[i%n]
        B = P[(i+1)%n]
        gr.Line(A,B,color,thickness=1)
    return

def DrawRectangle(gr,bbox, color):
    x1,y1,x2,y2 = bbox
    A = [x1,y1]
    B = [x2,y1]
    C = [x2,y2]
    D = [x1,y2]
    P = [A,B,C,D]
    DrawPolygon(gr,P,color)
    return

def DisplayRects(gr,Q):
    return

def norm_oo(x):
    return max(abs(x[0]),abs(x[1]))
def dist_oo(A,B):
    C = [0]*len(A)
    for i in range(len(A)):
        C[i] = A[i] - B[i]
    val = norm_oo(C)
    return val

gr = racg.Graphics(w=ww,h=hh)

use_mouse = True
pt_mouse = [0,0,0]
pt_select = [0,0,0]
pt_D = [0,0]
pt_U = [0,0]
pt_dist = 0
flag_radius = False
selected = False
wn = "result"
if use_mouse:
    import cv2
    def getxy(event, x, y, flags, param):
        global pt_mouse,pt_select,selected,\
                pt_D,pt_U,pt_dist,flag_radius,\
                flag_D
        if (event == cv2.EVENT_MOUSEMOVE):
            pt_mouse = [x,y]
            #print("M %d %d" % tuple(pt_mouse))
            return
        if (event == cv2.EVENT_LBUTTONDOWN):
            pt_select = [x,y]
            selected = True
            return
        if (event == cv2.EVENT_LBUTTONUP):
            return
        if (event == cv2.EVENT_RBUTTONDOWN):
            pt_D = [x,y]
            #print("D %d %d" % tuple(pt_D))
            return        
        if (event == cv2.EVENT_RBUTTONUP):
            pt_U = [x,y]
            #print("U %d %d" % tuple(pt_U))
            pt_dist = dist_oo(pt_D,pt_U)
            flag_radius = True
            return
    def StartMouse():
        cv2.namedWindow(wn)
        cv2.setMouseCallback(wn,getxy)
        return
    StartMouse()
class Point:
    def __init__(self,pt,tup):
        self.pt = pt
        self.tup = tup
        return
    def __str__(self):
        s = 'P(pt=%s,tup=%s)' % (str(self.pt),str(self.tup))
        return s
N = 200
pts = []
for i in range(N):
    x = random.uniform(0,ww)
    y = random.uniform(0,hh)
    pt = [x,y]
    pt = list(map(int,pt))
    pts.append(pt)

c = qtr.q(qtr.ROI2([1,1],ww-2,hh-2),capacity=4)
print(len(pts))
for idx in range(len(pts)):
    name = random.choice(["cat","dog","human","mouse","robot"])
    tup = (idx,name)
    A = Point(pts[idx],tup)
    c.insert(A)
    gr.Point(A.pt,color=[0,0,0])
#print("c = \n",c)
w0,h0 = [75,75]
while True:
    gr.Clear()
    if flag_radius:
        w0,h0 = [pt_dist,pt_dist] # mouse window
        #print("w0,h0:",w0,h0)
        flag_radius = False
    for idx in range(len(pts)):
        pt = pts[idx]
        gr.Circle(pt,3,color=[0,0,0],thickness=2)
    
    roi_mouse = qtr.AABB(pt_mouse,w0,h0)
    #print("roi = ",roi.Interval())
    pts_q,bboxes_q = c.query(roi_mouse)
    roi_select = qtr.AABB(pt_select,w0,h0)
    pts_s,bboxes_s = c.query(roi_select)
    if selected:
        print("selected = ")
        for pt in pts_s:
            print(pt)
        selected = False
    for i in range(len(bboxes_q)):
        bbox_i = bboxes_q[i]
        DrawRectangle(gr, bbox_i, color=[0,0,255])
    #print("query results: ", pts_q)
    DrawRectangle(gr, roi_mouse.BoundingBox(), color=[255,0,0])
    ch = gr.Show("result",15)
    if ch == ord('e'):
        break
gr.Close()
