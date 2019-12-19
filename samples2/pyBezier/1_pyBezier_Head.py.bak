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
pts_head = [[334, 57], [266, 58], [193, 64], [156, 88],
       [124, 118], [116, 145], [115, 180], [140, 183],
       [143, 197], [137, 209], [133, 218], [123, 241],
       [107, 264], [86, 295], [60, 330], [61, 354],
       [68, 372], [90, 376], [117, 379], [137, 380],
       [149, 373], [149, 357], [164, 352], [165, 364],
       [166, 379], [162, 390], [160, 402], [159, 408],
       [147, 414], [147, 423], [159, 426], [170, 428],
       [182, 426], [191, 433], [174, 444], [168, 445],
       [159, 448], [153, 455], [159, 461], [165, 464],
       [172, 472], [174, 484], [178, 500], [181, 517],
       [187, 533], [204, 547], [230, 552], [255, 553],
       [301, 552], [353, 542], [399, 527], [427, 492],
       [435, 460], [438, 449], [451, 470], [452, 497],
       [456, 523], [457, 543], [460, 564], [481, 568],
       [511, 562], [545, 547], [570, 520], [587, 474],
       [592, 428], [594, 404], [585, 385], [541, 366],
       [503, 366], [466, 368], [447, 362], [433, 324],
       [441, 265], [467, 201], [493, 149], [482, 96],
       [428, 70], [375, 62], [321, 61], [280, 56],
       [280, 57], [281, 58]]
pts_man = [[298, 20], [268, 24], [259, 34], [263, 51],
           [271, 62], [281, 74], [276, 88], [265, 98],
           [259, 104], [248, 108], [231, 109], [223, 111],
           [212, 116], [202, 122], [198, 129], [193, 141],
           [193, 158], [193, 172], [191, 191], [190, 204],
           [187, 219], [183, 238], [181, 254], [180, 272],
           [174, 295], [170, 311], [170, 320], [169, 332],
           [168, 346], [172, 357], [171, 367], [167, 372],
           [164, 377], [162, 383], [171, 390], [173, 392],
           [175, 394], [183, 393], [197, 386], [195, 380],
           [191, 372], [197, 352], [202, 328], [206, 305],
           [209, 284], [210, 274], [218, 258], [224, 242],
           [231, 214], [231, 200], [235, 180], [241, 170],
           [253, 172], [255, 187], [253, 205], [252, 221],
           [252, 241], [251, 261], [249, 293], [249, 310],
           [248, 325], [246, 335], [246, 349], [249, 370],
           [251, 380], [253, 393], [253, 403], [252, 417],
           [251, 428], [250, 438], [248, 452], [246, 467],
           [246, 477], [243, 505], [242, 518], [241, 532],
           [238, 553], [235, 571], [234, 579], [234, 583],
           [241, 582], [245, 582], [250, 583], [257, 580],
           [265, 571], [270, 560], [280, 546], [289, 519],
           [297, 484], [297, 456], [299, 429], [299, 407],
           [302, 384], [306, 363], [315, 353], [328, 364],
           [335, 382], [338, 405], [342, 435], [348, 464],
           [350, 484], [353, 509], [359, 542], [365, 560],
           [367, 570], [381, 576], [403, 576], [408, 574],
           [411, 559], [409, 546], [407, 525], [402, 497],
           [397, 483], [393, 460], [385, 441], [379, 414],
           [374, 392], [369, 370], [363, 354], [358, 338],
           [355, 324], [355, 312], [355, 296], [355, 280],
           [355, 266], [354, 250], [354, 228], [352, 212],
           [349, 188], [349, 175], [355, 171], [367, 190],
           [372, 213], [377, 234], [381, 255], [384, 268],
           [389, 287], [392, 307], [398, 333], [402, 345],
           [404, 360], [405, 369], [415, 374], [425, 373],
           [432, 370], [438, 364], [434, 350], [425, 348],
           [422, 333], [420, 310], [419, 300], [417, 278],
           [417, 258], [413, 237], [408, 217], [402, 194],
           [396, 164], [391, 150], [388, 135], [383, 121],
           [377, 110], [371, 105], [367, 104], [348, 103],
           [339, 102], [331, 102], [325, 97], [316, 86],
           [317, 77], [320, 72], [323, 62], [323, 55],
           [329, 46], [327, 36], [321, 30], [313, 24],
           [299, 20]]
pts = deepcopy(pts_head)

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
Left-Click mouse button to add points.
Press 'e' to exit. Press 's' to select and 'd' to
move mouse while select set. Press 'c' to clear screen.
Press 'h' to load head. Press 'm' to load man.
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
    if ch == ord('h'):
        pts = deepcopy(pts_head)
    if ch == ord('m'):
        pts = deepcopy(pts_man)

    if select and mouse:
        pts[i_select]= pt_mouse
gr.Close()
