import time
from datetime import datetime

import numpy as np
import sys
#sys.path.insert(0,r"C:\_opencv2\opencv\build\python\2.7") #20130702 version
import cv2

def Date(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def Seconds(year,month,day):
     sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
     return sec

def Now():
     t1 = datetime.now()
     secs = time.mktime(t1.timetuple())
     return secs

class Graphics:
    def __init__(self,w=800,h=800,display_graphics=True,display_commands=False,labeler=None):
        self.w = w
        self.h = h
        self.display_graphics = display_graphics
        self.display_commands = display_commands
        self.plab = labeler
        self.Clear()
        if self.display_commands:
             s = "gr.__init__(%d,%d,display_graphics=%s,display_commands=%s)" % \
                 (w,h,display_graphics,display_commands)
             print s
    def Clear(self):
        if self.display_commands:
             s = "gr.Clear()"
             print s
        self.canvas = np.ones((self.h,self.w,3),dtype='uint8')*255 # canvas
    def Line(self,A,B,color,thickness=2):
        A = map(int,A)
        B = map(int,B)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Line(%s,%s,%s)" % (str(A),str(B),str(color))
             else:
                  s = "gr.Line(%s,%s,%s)" % (self.plab.Label(A),self.plab.Label(B),str(color))
             print s
        cv2.line(self.canvas, (A[0],A[1]), (B[0],B[1]), (color[2],color[1],color[0]), thickness)
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
        cv2.circle(self.canvas,(C[0],C[1]),r,(color[2],color[1],color[0]))
        return
    def Point(self,pt,color):
        pt = map(int,pt)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Point(%s,%s)" % (str(pt),str(color))
             else:
                  s = "gr.Point(%s,%s)" % (self.plab.Label(pt),str(color))
             print s
        cv2.circle(self.canvas,(pt[0],pt[1]),6,(color[2],color[1],color[0]),-1)
        return
    def Text(self,s,x,y,color,scale=1):
        pt = [x,y]
        pt = map(int,pt)
        if self.display_commands:
             t = "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
             print t
        cv2.putText(self.canvas, s, (pt[0],pt[1]), cv2.FONT_HERSHEY_SIMPLEX, scale, (color[2],color[1],color[0]))
        return
    def Label(self,s,pt,colorpt = [0,0,255], colortxt = [0,0,0]):
        x,y = map(int,pt)
        x += 6
        y += 6
        if self.display_commands:
             if self.plab is None:
                  t = "gr.Label('%s',%s,%s,%s)" % (s,str([x,y]),str(colorpt),str(colortxt))
             else:
                  t = "gr.Label('%s',%s,%s,%s)" % (s,s,str(colorpt),str(colortxt))
             print t
        self.Point(pt,colorpt)
        self.Text(s,x,y,colortxt,scale=0.5)
        return
    def Show(self,wn,ms):
        if (not self.display_graphics) and (ms != -1):
             ms = 0
        if self.display_commands:
             s = "gr.Show('%s',%d)" % (wn,ms)
             print s
        cv2.imshow(wn,self.canvas)
        if ms == -1:
            print "Press any key to continue"
        ch = cv2.waitKey(ms)
        return ch
    def Save(self,filename=None,msg=""):
        if filename is None:
            miliseconds = int(time.time()*1000.0)
            head = miliseconds/1000
            tail = miliseconds%1000
            filename = "canvas-snapshot-%d-%d.jpg" % (head,tail)
        print "Saving...",filename
        if self.display_commands:
             s = "gr.Save('%s')" % (filename)
             print s
        cv2.imwrite(filename,self.canvas)
        return
    def Load(self,filename):
        if self.display_commands:
             s = "gr.Load('%s')" % (filename)
             print s
        self.canvas = cv2.imread(filename,1)
        self.h,self.w,c = self.canvas.shape
        return
    def Close(self):
        if self.display_commands:
             s = "gr.Close()"
             print s
        cv2.destroyAllWindows()
        return
