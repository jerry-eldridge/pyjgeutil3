import time
from datetime import datetime

from math import pi,cos,sin
import numpy as np

def Date(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def Seconds(year,month,day):
     sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
     return sec

def Now():
     t1 = datetime.now()
     secs = time.mktime(t1.timetuple())
     return secs

def DrawLine(arr, N1, N2, x1, y1, x2, y2, val):
     x1,y1,x2,y2 = map(int,[x1,y1,x2,y2])
     XAXIS,YAXIS = range(2)
     # Line is a Point
     dy = y2-y1
     dx = x2-x1
     if ((dy == 0) and (dx == 0)):
          i = int(round(x1))
          j = int(round(y1))
          support = (i<0)or(i>=N1)or(j<0)or(j>=N2)
          if (not support):
               arr[j,i] = val

     rrange = max(abs(dx), abs(dy))
     irange = int(round(rrange))
     if (abs(dx) >= abs(dy)):
          axis = XAXIS
     else:
          axis = YAXIS
     errp = 2*dy-dx
     if dx >= 0:
          dxs = 1
     else:
          dxs = -1
     if dy >= 0:
          dys = 1
     else:
          dys = -1

     xp = int(round(x1))
     yp = int(round(y1))

     if axis == XAXIS:
          for i in range(irange):
               support = (xp<0) or (xp>=N1) or (yp<0) or (yp>=N2)
               if (not support):
                    arr[yp,xp] = val
               if (errp > 0):
                    yp += dys
                    errp += -2*dx*dxs
               xp += dxs
               errp += 2*dy*dys
     elif axis == YAXIS:
          for i in range(irange):
               support = (xp<0) or (xp>=N1) or (yp<0) or (yp>=N2)
               if (not support):
                    arr[yp,xp] = val
               if (errp > 0):
                    xp += dxs
                    errp += -2*dy*dys
               yp += dys
               errp += 2*dx*dxs
     return arr


def DrawCircle(A, ni, nj, cx, cy, r, val):
     A = DrawEllipse(A, ni, nj, cx, cy, r, r, val)
     return A

def DrawEllipse(A, ni, nj, cx, cy, xr, yr, val):
     angle = 0
     dangle = 2*pi/100.0
     while (angle < 2*pi):
          x1 = xr*cos(angle) + cx
          y1 = yr*sin(angle) + cy
          angle += dangle;
          x2 = xr*cos(angle) + cx
          y2 = yr*sin(angle) + cy
          angle += dangle
          A = DrawLine(A, ni, nj, x1, y1, x2, y2, val)
     return A

class Graphics:
    def __init__(self,w=800,h=800,display_graphics=True,display_commands=False,labeler=None):
        self.w = w
        self.h = h
        self.display_graphics = display_graphics
        self.display_commands = display_commands
        self.plab = labeler
        self.bkgd = '_'
        self.Clear()
        if self.display_commands:
             s = "gr.__init__(%d,%d,display_graphics=%s,display_commands=%s)" % \
                 (self.w,self.h,display_graphics,display_commands)
             print s
    def Clear(self):
        if self.display_commands:
             s = "gr.Clear()"
             print s
        self.canvas = np.ones((self.h,self.w,3),dtype='int8')*ord(self.bkgd) # canvas
    def Count(self,color):
        c = 0
        for j in range(self.h):
             for i in range(self.w):
                  if self.GetPixel(i,j) == color:
                       c += 1
        return c
    def Line(self,A,B,color,thickness=2):
        A = map(int,A)
        B = map(int,B)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Line(%s,%s,%s)" % (str(A),str(B),str(color))
             else:
                  s = "gr.Line(%s,%s,%s)" % (self.plab.Label(A),self.plab.Label(B),str(color))
             print s
        self.canvas = DrawLine(self.canvas, self.h, self.w, A[0], A[1], B[0], B[1], ord(color))
        return 
    def Circle(self,C,r,color,thickness=2):
        C = map(int,C)
        r = int(r)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Circle(%s,%d,%s)" % (str(C),r,str(color))
             else:
                  s = "gr.Circle(%s,%d,%s)" % (self.plab.Label(C),r,str(color))
             print s
        self.canvas = DrawCircle(self.canvas, self.w, self.h, C[0], C[1], r, ord(color))
        return
    def Point(self,pt,color):
        pt = map(int,pt)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Point(%s,%s)" % (str(pt),str(color))
             else:
                  s = "gr.Point(%s,%s)" % (self.plab.Label(pt),str(color))
             print s
        self.SetPixel(pt[0],pt[1],color)
        return
    def Text(self,s,x,y,color,scale=1):
        pt = [x,y]
        pt = map(int,pt)
        if self.display_commands:
             t = "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
             print t
        print "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
        L = list(s)
        k = min(len(L),(self.w-1)-x)
        L = L[:k]
        support = (x >= 0) and (x<self.w) and (y >= 0) and (y <self.h)
        if not support:
             return
        self.canvas[y,x:x+k,:] = map(lambda val: [ord(val),ord(val),ord(val)], L)
        return
    def Label(self,s,pt,colorpt = [0,0,255], colortxt = [0,0,0]):
        x,y = map(int,pt)
##        x += 6
##        y += 6
        if self.display_commands:
             if self.plab is None:
                  t = "gr.Label('%s',%s,%s,%s)" % (s,str([x,y]),str(colorpt),str(colortxt))
             else:
                  t = "gr.Label('%s',%s,%s,%s)" % (s,s,str(colorpt),str(colortxt))
             print t
        self.Point(pt,colorpt)
        self.Text(s,x,y,colortxt,scale=0.5)
        return
    def SetPixel(self,i,j,ch):
        c = ord(ch)
        self.canvas[j,i,:] = [c,c,c]
        return
    def GetPixel(self,i,j):
        c = self.canvas[j,i,0]
        ch = chr(c)
        return ch
    def Rectangle(self,A,w,h,color):
        A = map(int,A)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Rectangle(%s,%d,%d,%s)" % (str(A),w,h,str(color))
             else:
                  s = "gr.Rectangle(%s,%d,%d,%s)" % (self.plab.Label(A),w,h,str(color))
             print s
        x,y = A
        for j in range(y,h+y):
             for i in range(x,w+x):
                  self.SetPixel(i,j,color)
        return 
    def Show(self,wn,ms):
        if (not self.display_graphics) and (ms != -1):
             ms = 0
        if self.display_commands:
             s = "gr.Show('%s',%d)" % (wn,ms)
             print s
        s = ''
        for j in range(self.h):
            for i in range(self.w):
                s += self.GetPixel(i,j)
            s += '\n'
        print s
        print "="*30
        if ms == -1:
            print "Press any key to continue (No raw input)"
        ch = ''
        return ch
    def Save(self,filename=None,msg=""):
        if filename is None:
            miliseconds = int(time.time()*1000.0)
            head = miliseconds/1000
            tail = miliseconds%1000
            filename = "canvas-snapshot-%d-%d.jpg" % (head,tail)
        filename += ".txt"
        print "Saving...",filename
        if self.display_commands:
             s = "gr.Save('%s')" % (filename)
             print s
        f = open(filename,'w')
        s = ''
        for j in range(self.h):
            for i in range(self.w):
                s += '%s' % self.GetPixel(i,j)
            s += '\n'
        f.write(s)
        f.close()
        return
    def Load(self,filename):
        if self.display_commands:
             s = "gr.Load('%s')" % (filename)
             print s
        return
    def Close(self):
        if self.display_commands:
             s = "gr.Close()"
             print s
        return
