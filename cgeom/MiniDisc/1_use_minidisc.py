import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import graphics_cv as racg

import minidisc as mdc
import random

random.seed(23472837492347)

def RndPoint(bbox):
    x = random.uniform(bbox[0],bbox[2])
    y = random.uniform(bbox[1],bbox[3])
    pt = [x,y]
    return pt

def BB(x,y,w,h):
    bbox = (x-w/2,y-h/2,x+w/2,y+h/2)
    return bbox

ww = 500
hh = 500
gr = racg.Graphics(w=ww,h=hh)

M = 40
print("Press 'e' to exit")
for j in range(M):
    gr.Clear()

    N = 20
    pts = []
    rr = random.uniform(100,400)
    bbox = BB(ww/2,hh/2,rr,rr)
    for i in range(N):
        pt = RndPoint(bbox)
        pts.append(pt)
    D = mdc.MiniDisc(pts)
    gr.Circle(D.x,r=3,color=[0,0,0])
    for i in range(len(pts)):
        pt = pts[i]
        gr.Circle(pt,r=2,color=[255,0,0])
    gr.Circle(D.x,D.r,color=[0,0,0])
    ch = gr.Show("result",500)
    if ch == ord('e'):
        break
ch = gr.Show("result",-1)
gr.Close()
