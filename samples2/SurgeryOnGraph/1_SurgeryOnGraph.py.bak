import sys
sys.path.insert(0,r"c:\_PythonJGE\Utility")
import graphics_cv as racg

from numpy import array,zeros,ones
import cv2
import surgery
import graph

flag_moving = False
def getxy(event, x, y, flags, param):
    global pts, flag_moving, pt_move
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append([x,y])
        pt_move = [x,y]
        flag_moving = not flag_moving
        return
    if event == cv2.EVENT_RBUTTONDOWN:
        return
    if event == cv2.EVENT_MBUTTONDOWN:
        return
    if event == cv2.EVENT_MOUSEMOVE and (len(pts) > 0):
        pt_move = [x,y]
        return        
    return

pts = []
pt_move = [0,0]
print "Select the two points on 2D plane"
cv2.namedWindow("result")
cv2.setMouseCallback("result",getxy)

doc = {}
doc["V"] = range(2)
doc["E"] = [[0,1]]
doc["pts"] = [[119, 304],[480, 53]]
doc = graph.Cn(4)
w = 400
h = 400
cx,cy,cz = (w/2,h/2,0)
r = 0.75*w/2
doc = graph.CreateCircleGeometry(doc,cx,cy,cz,r)
doc['_id'] = 1

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)

def PlotGraph(gr,G,color):
    black = [0,0,0]
    for e in G['E']:
        A,B = map(lambda v: G['pts'][v],e)
        gr.Line(A,B,color)
    for v in G['V']:
        A = G['pts'][v]
        gr.Point(A,black)
    return

red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
while True:
    if len(pts) >= 2:
        A,B = pts[:2]
        pts = pts[2:]
        alpha = 0.15
        beta = 0.15
        doc = surgery.SliceWithKnife(doc,A[0],A[1],B[0],B[1],alpha,beta)
    gr.Clear()
    gr.Text("Draw Line with Left Mouse Button and Click",50,50,green,scale=.5)
    PlotGraph(gr,doc,red)
    if flag_moving:
        pt1 = pts[0]
        pt2 = pt_move
        R,G,B = (255,200,200)
        gr.Line((pt1[0],pt1[1]), (pt2[0],pt2[1]), blue,thickness=2)

    ch = gr.Show("result",15)
    if ch == ord('e'):
        break

gr.Close()
