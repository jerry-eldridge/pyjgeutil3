import time
from datetime import datetime

from math import pi,cos,sin
import numpy as np
import PSDraw

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
    def __init__(self,w=800,h=800,display_graphics=True,display_commands=False,labeler=None,speed="normal"):
        self.w = w
        self.h = h
        self.f = None
        self.ps = None
        self.display_graphics = display_graphics
        self.display_commands = display_commands
        self.plab = labeler
        self.bkgd = '_'
        self.Clear()
        self.bgset = False
        if self.display_commands:
             s = "gr.__init__(%d,%d,display_graphics=%s,display_commands=%s)" % \
                 (self.w,self.h,display_graphics,display_commands)
             print s
        return
    def Clear(self):
        if self.display_commands:
             s = "gr.Clear()"
             print s
        self.f = open('overwrite-postscript.ps','w')
        self.ps = PSDraw.PSDraw(self.f)
        self.ps.begin_document()
        self.ps.setfont("HelveticaNarrow",14)
        return
    def Line(self,A,B,color,thickness=2):
        A = map(int,A)
        B = map(int,B)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Line(%s,%s,%s)" % (str(A),str(B),str(color))
             else:
                  s = "gr.Line(%s,%s,%s)" % (self.plab.Label(A),self.plab.Label(B),str(color))
             print s
        self.ps.line(tuple(A),tuple(B))
        return 
    def Circle(self,C,r,color,N=60,thickness=2):
        C = map(int,C)
        r = int(r)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Circle(%s,%d,%s)" % (str(C),r,str(color))
             else:
                  s = "gr.Circle(%s,%d,%s)" % (self.plab.Label(C),r,str(color))
             print s
        theta = 0
        dtheta = 360.0/N
        xl = C[0] + r
        yl = C[1] + 0
        while theta <= 360:
             x = C[0] + r*cos(theta*pi/180.0)
             y = C[1] + r*sin(theta*pi/180.0)
             A = [xl,yl]
             B = [x,y]
             A = map(int,A)
             B = map(int,B)
             self.ps.line(tuple(A),tuple(B))
             xl = x
             yl = y
             theta += dtheta
        return
    def Point(self,pt,color):
        pt = map(int,pt)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Point(%s,%s)" % (str(pt),str(color))
             else:
                  s = "gr.Point(%s,%s)" % (self.plab.Label(pt),str(color))
             print s
        self.Circle(pt,3,color)
        return
    def Text(self,s,x,y,color,scale=1):
        pt = [x,y]
        pt = map(int,pt)
        if self.display_commands:
             t = "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
             print t
        #print "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
        self.ps.text((x,y),s)      
        return
    def Label(self,s,pt,colorpt = [0,0,255], colortxt = [0,0,0]):
        pt = map(int,pt)
        x,y = pt
        if self.display_commands:
             if self.plab is None:
                  t = "gr.Label('%s',%s,%s,%s)" % (s,str([x,y]),str(colorpt),str(colortxt))
             else:
                  t = "gr.Label('%s',%s,%s,%s)" % (s,s,str(colorpt),str(colortxt))
             print t
        self.Point(pt,colorpt)
        self.Text(s,x,y,colortxt,scale=0.25)
        return
    def Show(self,wn,ms):
        if self.display_commands:
             s = "gr.Show('%s',%d)" % (wn,ms)
             print s
        if ms < 0:
            self.ps.end_document()
            self.f.close()
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
        print "How do you save screen with turtle graphics?"  
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

