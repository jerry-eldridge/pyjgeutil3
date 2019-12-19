import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import SCARA as RA
from copy import deepcopy
import graphics_cv as racg
import image2polygon as i2p
import mapto
from math import fmod,pi,sin,cos

H = 10
a = 100
b = 150
l1 = a*400/200.0
l2 = b*400/200.0
theta1 = 0
theta2 = 0
theta3 = 0
d = 0

L = [H,l1,l2]
Theta = [theta1,theta2,theta3,d]
P = RA.RobotArm([0,0,0],deepcopy(L),deepcopy(Theta))
maxiters = 20
goal = deepcopy(P.Start())
epsilon = 0.1
i = 0

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)
P.pt = [w*.25,h*.25,0]

def PlotShape(gr,shape):
    pts,idxs = shape
    for i in range(len(idxs)-1,-1,-1):
        a = idxs[i]
        b = idxs[(i+1)%len(idxs)]
        if b != 0:
            pts0 = pts[a:b]
        else:
            pts0 = pts[a:]
        n0 = len(pts0)
        v = 3
        for j in range(n0/v+1):
            A = pts0[(v*j)%n0]
            B = pts0[(v*(j+1))%n0]
            gr.Line(A,B,"black")
    return

def DrawShape(P,shape):

    return

def LoadChar(ch):
    n = ord(ch)
    #root = "C:/emma/fonts/font3/"
    root = "./font3/"
    fn = root+"%d.txt" % n
    
    f = open(fn,'r')
    txt = f.read()
    f.close()
    lines = txt.split("\n")
    wrcmds = []
    for line in lines:
        wrcmd = line.split(' ')
        wrcmds.append(wrcmd)
    return wrcmds

def TransformFont(pt,s):
    x,y = pt
    x *= s
    y *= s
    pt = [x,y]
    return pt

def WritingGraph(pts_writing):
    PTS = []
    for pts in pts_writing:
        PTS = PTS + pts
    stroke = 0
    pts = pts_writing[stroke]
    G = g.Pn(len(pts))
    for stroke in range(1,len(pts_writing)):
        pts = pts_writing[stroke]
        Gi = g.Pn(len(pts))
        G = g.GraphUnionPseudo(G,Gi)
    G = g.PseudoToGraph(G)
    G['pts'] = PTS
    return G

def PlotGraph(gr,G,color):
    for e in G['E']:
        A,B = map(lambda v: G['pts'][v],e)
        gr.Line(A,B,color)
    for v in G['V']:
        A = G['pts'][v]
        gr.Point(A,color)
    return

use_mouse = True
pt_mouse = [0,0,0]
pt_select = [0,0,0]
selected = False
wn = "result"
if use_mouse:
    import cv2
    def getxy(event, x, y, flags, param):
        global pt_mouse,pt_select,selected
        if (event == cv2.EVENT_MOUSEMOVE):
            pt_mouse = [x,y,0]
            return
        if (event == cv2.EVENT_LBUTTONDOWN):
            pt_select = [x,y,0]
            selected = True
            return
    def StartMouse():
        cv2.namedWindow(wn)
        cv2.setMouseCallback(wn,getxy)
        return
    StartMouse()

black = [0,0,0]
blue = [0,0,255]
red = [255,0,0]
t = 0
dt = 1
z_down = 0
z_up = H
z_thresh = 2
A_last = P.Start()


i2p.im2poly("t.jpg","t_123.txt")
shape = i2p.readpoly("t_123.txt")
    
pts,idxs = shape
print "Press 'e' to exit"
for i in range(len(idxs)-1,-1,-1):
    a = idxs[i]
    b = idxs[(i+1)%len(idxs)]
    if b != 0:
        pts0 = pts[a:b]
    else:
        pts0 = pts[a:]
    n0 = len(pts0)
    v = 3
    for j in range(n0/v+1):
        if j == n0/v:
            z = z_up
        else:
            z = z_down
        x,y = pts0[(v*j)%n0]
        a = 1
        x = w/4+mapto.MapTo(0,0,200,300,x)
        y = h/3+mapto.MapTo(0,300,200,0,y)
        # map canvas [0,200]x[0,200] to gr canvas
        # [0,200]x[300,500]
        C = [x,y,z]
        G = P.Graph()
        A = P.Start()
        if A[2]<=z_thresh and A_last[2]<=z_thresh:
            gr.Line(A_last[:2],A[:2],blue)
        im_pre = deepcopy(gr.canvas)
        PlotGraph(gr,G,black)
        A_last = deepcopy(A)
        theta1 = fmod(P.Theta[0],360)
        theta2 = fmod(P.Theta[1],360)
        theta3 = fmod(P.Theta[2],360)
        d = P.Theta[3]
        s = "Theta = (%.1f,%.1f,%.1f,%.2f)" % (theta1,theta2,theta3,d)
        gr.Text(s,50,50,black,scale=.5)
        # uses OpenCv canvas for drawing, note
        # gr.canvas is height x width.
        ch = gr.Show("result",5)
        gr.canvas = deepcopy(im_pre)
        if ch == ord('e'):
            break
        # Reach Robot Arm for point C
        P,flag = RA.Reach(P,C)
    if ch == ord('e'):
        break
gr.Show("result",-1)
gr.Close()

