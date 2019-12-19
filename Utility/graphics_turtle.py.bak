import time
from datetime import datetime

from math import pi,cos,sin
import numpy as np
import turtle
import mapto

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
        self.tc = turtle.Screen()
        self.display_graphics = display_graphics
        self.display_commands = display_commands
        self.plab = labeler
        self.bkgd = '_'
        self.speed = speed
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
        self.tc.canvheight = self.w
        self.tc.canvwidth = self.h
        turtle.clear()
        turtle.penup()
        turtle.home()
        #turtle.hideturtle()
        return
    def SetSpeed(self,speed):
         turtle.speed(speed)
         self.speed = speed
         return
    def T(self,pt):
         x = pt[0]
         y = pt[1]
         s = 0.9
         x = x - self.w*s
         y = y - self.h*s
         return [x,y]
      
    def Line(self,A,B,color,thickness=2):
        A = map(int,A)
        B = map(int,B)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Line(%s,%s,%s)" % (str(A),str(B),str(color))
             else:
                  s = "gr.Line(%s,%s,%s)" % (self.plab.Label(A),self.plab.Label(B),str(color))
             print s
        A = self.T(A)
        B = self.T(B)
        turtle.color(color)
        turtle.penup()
        #turtle.home()
        turtle.goto(A[0],A[1])
        turtle.pendown()
        turtle.goto(B[0],B[1])
        turtle.penup()
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
        C = self.T(C)
        turtle.color(color)
        turtle.penup()
        #turtle.home()
        turtle.goto(C[0],C[1]-r)
        turtle.pendown()
        turtle.circle(r)
        turtle.penup()
        return
    def Point(self,pt,color):
        pt = map(int,pt)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Point(%s,%s)" % (str(pt),str(color))
             else:
                  s = "gr.Point(%s,%s)" % (self.plab.Label(pt),str(color))
             print s
        self.Circle(pt,4,color)
        return
    def Text(self,s,x,y,color,scale=1):
        pt = [x,y]
        pt = map(int,pt)
        if self.display_commands:
             t = "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
             print t
        pt = self.T(pt)
        turtle.color(color)
        turtle.penup()
        #turtle.home()
        turtle.goto(pt[0],pt[1])
        turtle.pendown()
        turtle.write(s,font=("Lucida Console",12),move="True")
        turtle.penup()
        return
    def Label(self,s,pt,colorpt = "blue", colortxt = "black"):
        pt = map(int,pt)
        x = pt[0]
        y = pt[1]
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
            print "Close window to continue"
            turtle.done()
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
        if not self.bgset:
             self.tc.bgpic(filename)
             self.bgset = True
        return
    def Close(self):
        if self.display_commands:
             s = "gr.Close()"
             print s
        return

