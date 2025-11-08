import graphics_3_cv as racg
import cv2 # 'pip install opencv-python' to install
from copy import deepcopy
import numpy as np

import SCARA as RA
import mapto
from math import fmod,pi,sin,cos

def enc(x):
    y = list(x.encode('utf-8'))
    return y
def dec(y):
    z = bytes(y).decode('utf-8')
    return z

class Character:
    def __init__(self, n, x,y,w,h):
        self.bbox = [x,y,w,h]
        self.n = n
    def __str__(self):
        c = dec(self.n)
        return c
    def __repr__(self):
        return str(self)

def PlotGraph(gr,G,color,thickness=40):
    for e in G['E']:
        A,B = [G['pts'][v] for v in e]
        gr.Line(A,B,color,thickness)
    for v in G['V']:
        A = G['pts'][v]
        gr.Point(A,color)
    return

class Page:
    def __init__(self, name, width_in,height_in,
                 sx = 1, sy = 1,
                 font = "../font3/",
                 dpi=180):
        self.dpi = dpi
        self.name = name
        self.sx = sx
        self.sy = sy
        self.width = int(width_in*dpi*sx)
        self.height = int(height_in*dpi*sy)
        self.gr = racg.Graphics(self.width,self.height)
        self.gr2 = racg.Graphics(self.width,self.height)
        self.wn = self.name
        self.font = font
        
        H = 5
        l1 = self.width*.6
        l2 = self.width*.6
        theta1 = 0
        theta2 = 0
        theta3 = 0
        d = 0

        self.L = [H,l1,l2]
        self.Theta = [theta1,theta2,theta3,d]
        O = [self.width*0.75,self.height/2,0]
        self.P = RA.RobotArm(O,deepcopy(self.L),\
                deepcopy(self.Theta))
        self.maxiters = 20
        self.goal = deepcopy(self.P.Start())
        self.epsilon = 0.1

        self.counter = 0
    def draw_char(self,char,
                  color=[10,0,100],
                  thickness=2, show_bbox = False):
        speed = 30
        if show_bbox:
            self.draw_bbox(char,color,thickness)
        n = char.n
        bbox = char.bbox
        x0,y0,w0,h0 = bbox
        cx = self.dpi * x0
        cy = self.dpi * y0
        w = self.dpi * w0
        h = self.dpi * h0
        s = '_'.join(list(map(str,n)))
        fn = f"{self.font}/{s}.txt"
        try:
            f = open(fn,'r')
            txt = f.read()
            f.close()
        except:
            txt = None
            fn2 = f"../font3/{s}.txt"
            try:
                g = open(fn2,'r')
                txt = g.read()
                g.close()
            except:
                txt = None
                #print(f"Error: symbol not implemented")
        if txt == None:
            return
        lines = txt.split('\n')
        pt = None
        pt_last = None
        for line in lines:
            if len(line) == 0:
                continue
            toks = line.split(' ')
            if toks[0] == 'D':
                flag = True
                xx,yy = list(map(int,toks[1:3]))
                pt = [cx + w*xx/200.0,cy + h*yy/200.0]
                pt_last = pt
            elif toks[0] == 'U':
                flag = False
            elif toks[0] == 'M':
                xx,yy = list(map(int,toks[1:3]))
                zz = 0
                pt = [cx + w*xx/200.0,cy + h*yy/200.0]
                C = [pt[0],pt[1], zz]
                if self.counter % speed == 0:
                    G = self.P.Graph()
                    self.gr2.Clear()
                    PlotGraph(self.gr2,G,color)
                    self.P,flag2 = RA.Reach(\
                        self.P,C)
                self.gr.Line(pt_last,pt,\
                    color,thickness)
                self.counter += 1
            elif toks[0] == 'E':
                break
            pt_last = pt
        return
    def draw_bbox(self, char,\
            color=[10,0,100],thickness=1):
        bbox = char.bbox
        x0,y0,w0,h0 = bbox
        x = self.dpi * x0
        y = self.dpi * y0
        w = self.dpi * w0
        h = self.dpi * h0
        UL = [x,y]
        UR = [x+w,y]
        LR = [x+w,y+h]
        LL = [x,y+h]
        O = [x,y+h]
        self.gr.Line(UL,UR,color,thickness)
        self.gr.Line(UR,LR,color,thickness)
        self.gr.Line(LL,LR,color,thickness)
        self.gr.Line(UL,LL,color,thickness)
        return
    def show(self,ms=-1,
             verbose=True,
             width=1000,height=800):
        im0 = self.gr.canvas.copy()
        im1 = self.gr2.canvas.copy()
        alpha = 0.7
        beta = 1.0 - alpha
        ################################
        # [1] Microsoft Copilot
        #
        im01 = cv2.addWeighted(im0, \
                alpha, im1, beta, 0.0)
        #
        ##################################
        im2 = cv2.resize(im01,(width,height),
                    interpolation=cv2.INTER_LINEAR)
        cv2.imshow(self.wn,im2)
        if ms == -1:
            if verbose:
                print("Press any key to continue")
            ch = cv2.waitKey(ms)
            return ch
        else:
            ch = cv2.waitKey(ms)
        return ch

class StackTypewriter:
    def __init__(self, name,color=[10,0,100],
                 thickness=1):
        self.name = name
        self.paper = []
        self.npage = None
        self.color = color
        self.thickness = thickness
            # must be integer, 1 is smallest
    def push_page(self, P):
        self.paper = self.paper + [P]
        self.npage = len(self.paper)-1
        return self.npage
    def pop_page(self):
        P = self.paper[-1]
        self.paper = self.paper[:-1]
        return P
    def save_page(self, fn_save, P):
        print(f"Saving to fn_save = {fn_save}...")
        #yn = input("Enter 'y' to save: ")
        yn = 'y'
        if yn == 'y':
            cv2.imwrite(fn_save, P.gr.canvas)
        return
    def load_page(self, fn_read,name):
        im = cv2.imread(fn_read,1)
        hh,ww,cc = im.shape
        dpi = 180
        width_in = ww/dpi
        height_in = hh/dpi
        sx = 1
        sy = 1
        P = Page(name, width_in,height_in,\
                 sx, sy,dpi)
        npage = self.push_page(P)
        return npage
    def key(self, char, show_bbox = False):
        self.paper[self.npage].draw_char(char,\
            color = self.color,
            thickness = self.thickness,
            show_bbox = show_bbox)
        return
    def advance_bbox(self,bbox, dx,dy):
        bbox = deepcopy(bbox)
        x0,y0,w0,h0 = bbox
        x1 = x0 + dx
        y1 = y0 + dy
        w1 = w0
        h1 = h0
        return [x1,y1,w1,h1]     
    def show(self, npage, ms=-1, verbose=False):
        if 0 <= npage and npage <= self.npage:
            ch = self.paper[npage].show(ms,verbose)
        return ch
    def Circle(self, A, r, color, thickness=2):
        P = self.paper[self.npage]
        Ax = int(A[0]*P.dpi)
        Ay = int(A[1]*P.dpi)
        A2 = [Ax,Ay]
        self.paper[self.npage].gr.Circle(\
            A2,r,color,thickness)
        return
    def Line(self, A, B, color, thickness=2):
        P = self.paper[self.npage]
        Ax = int(A[0]*P.dpi)
        Ay = int(A[1]*P.dpi)
        A2 = [Ax,Ay]
        Bx = int(B[0]*P.dpi)
        By = int(B[1]*P.dpi)
        B2 = [Bx,By]
        self.paper[self.npage].gr.Line(\
            A2,B2,color,thickness)
        return
