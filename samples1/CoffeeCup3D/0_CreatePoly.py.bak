import graphics_cv as racg

import numpy as np
import cv2

def Scale(im,scale=1):
     sh = im.shape
     h = sh[1]
     w = sh[0]
     sh = (int(h*scale),int(w*scale))
     im2 = cv2.resize(im,sh)
     return im2

use_mouse = True
pt_mouse = [0,0,0]
pts = []
wn = "result"
if use_mouse:
    import cv2
    def getxy(event, x, y, flags, param):
        global pt_mouse,a
        if (event == cv2.EVENT_MOUSEMOVE):
            pt_mouse = [x,y,0]
            return
        if (event == cv2.EVENT_LBUTTONDOWN):
            pt = [x,y]
            print pt
            pts.append(pt)
    def StartMouse():
        cv2.namedWindow(wn)
        cv2.setMouseCallback(wn,getxy)
        return
    StartMouse()

im = cv2.imread('./coffee_cup/canvas-snapshot-22587.jpg')
h,w,c = im.shape

gr = racg.Graphics(w=w,h=h)
gr.canvas = im.copy()
while True:
    ch = gr.Show("result",15)
    if ch == ord('e'):
        break
gr.Close()

