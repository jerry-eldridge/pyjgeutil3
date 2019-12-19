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

im = cv2.imread('WaterBottle.jpg')
h,w,c = im.shape

gr = racg.Graphics(w=w,h=h)
gr.canvas = im.copy()
while True:
    ch = gr.Show("result",15)
    if ch == ord('e'):
        break
gr.Close()

x0 = 103
pts = [[103, 6], [124, 6], [140, 12], [144, 26], [144, 42], [137, 48], [140, 59], [152, 74], [169, 96], [183, 118], [195, 136], [200, 154], [199, 166], [192, 170], [197, 179], [198, 205], [198, 218], [198, 228], [198, 246], [200, 261], [198, 280], [196, 288], [198, 300], [198, 316], [198, 326], [194, 338], [194, 353], [194, 362], [187, 370], [186, 376], [191, 382], [194, 389], [195, 400], [192, 404], [192, 409], [196, 415], [197, 420], [198, 428], [198, 434], [198, 440], [194, 445], [199, 450], [200, 458], [200, 466], [199, 470], [199, 474], [199, 479], [202, 486], [202, 494], [198, 500], [201, 508], [201, 515], [202, 522], [199, 540], [196, 552], [191, 560], [183, 570], [171, 576], [161, 580], [137, 584], [124, 579]]
