import time
from datetime import datetime
import os

from math import pi,cos,sin
import numpy as np
import sys
import mapto

from math import pi,cos,sin

scr_x_max = 1200
scr_y_max = 1200

WritePoint = lambda x,y : str(int(x)) + "," + str(int(y)) + " "

Text = lambda x,y,sz,msg,color="black" : "<text x = \""+str(int(x))+"\" y = \""+\
       str(int(y))+"\" font-size = \""+str(sz)+"\""+\
       " stroke=\""+color+"\""+\
       ">"+msg+"</text>"

Header = "<?xml version=\"1.0\" standalone=\"no\"?>\n" +\
   "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n" +\
   "\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n" +\
   "<svg width=\"12cm\" height=\"12cm\" viewBox=\"0 0 1200 1200\"\n" +\
   "xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">\n" +\
   "<desc>Polyline</desc>"

PolylineFill = lambda s,pts,color="black" : "<polyline fill=\""+s+\
        "\" stroke=\""+color+"\" stroke-width=\"1\"\npoints=\""+\
	reduce(lambda t,pt: t+WritePoint(pt[0],pt[1]),pts,"") + "\"/>"
Polyline = lambda pts,color="black": PolylineFill("none",pts,color)

Ender = "</svg>"
xa = 0
xb = 1200
ya = 0
yb = 1200
Screen_x = lambda x: int(mapto.MapTo(xa,0,xb,scr_x_max,x))
Screen_y = lambda x: int(mapto.MapTo(ya,0,yb,scr_y_max,x))
Coord_x = lambda x: int(mapto.MapTo(0,xa,scr_x_max,xb,x))
Coord_y = lambda x: int(mapto.MapTo(0,ya,scr_y_max,yb,x))
Drawline = lambda A,B,color="black" : Polyline([map(Screen_x,A),map(Screen_y,B)],color)
def EllipseFill(s,pt,ra,rb,color="black"):
    x,y = pt
    t = range(101)
    xx = map(lambda a: ra*cos(2*pi*a/100)+x,t)
    yy = map(lambda a: rb*sin(2*pi*a/100)+y,t)
    pts = map(list,zip(xx,yy))
    return PolylineFill(s,pts,color)

Ellipse = lambda pt,ra,rb,color="black": EllipseFill("none",pt,ra,rb,color)
Drawpoint = lambda pt,ra,rb,color="black": '<circle fill="fill" stroke="'+color+\
         '" cx="'+str(int(pt[0]))+'" cy="'+str(int(pt[1]))+\
         '" r="'+str(int(ra))+'" />'#Ellipse(pt,r,r,color)
Circle = lambda pt,r,color="black": '<circle fill="none" stroke="'+color+\
         '" cx="'+str(int(pt[0]))+'" cy="'+str(int(pt[1]))+\
         '" r="'+str(int(r))+'" />'#Ellipse(pt,r,r,color)
Text2 = lambda sz,pt,msg,color="black" : Text(Screen_x(pt[0]),Screen_y(pt[1]),
            sz,msg,color=color)
Text_s = lambda pt,msg,color="black" : Text2(50,pt,msg,color=color)


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
                 (self.w,self.h,display_graphics,display_commands)
             print s
    def Clear(self):
        if self.display_commands:
             s = "gr.Clear()"
             print s
        self.canvas = Header
    def Line(self,A,B,color,thickness=2):
        A = map(int,A)
        B = map(int,B)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Line(%s,%s,%s)" % (str(A),str(B),str(color))
             else:
                  s = "gr.Line(%s,%s,%s)" % (self.plab.Label(A),self.plab.Label(B),str(color))
             print s
        self.canvas += Drawline(A, B, color)
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
        self.canvas += Circle(C,r,color)
        return
    def Point(self,pt,color):
        pt = map(int,pt)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Point(%s,%s)" % (str(pt),str(color))
             else:
                  s = "gr.Point(%s,%s)" % (self.plab.Label(pt),str(color))
             print s
        self.canvas += Drawpoint(pt,5,5,color)
        return
    def Text(self,s,x,y,color="black",scale=1):
        pt = [x,y]
        pt = map(int,pt)
        if self.display_commands:
             t = "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
             print t
        self.canvas += Text2(scale*50,pt,s,color=color)
        return
    def Label(self,s,pt,colorpt = "blue", colortxt = "black"):
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
    def Show(self,wn,ms):
        if self.display_commands:
             s = "gr.Show('%s',%d)" % (wn,ms)
             print s
        fn = 'tmp123617283132762187321731237687.svg' # overwritten
        self.Save(fn,"")
        if ms < 0:
            os.system(fn)
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
        filename += ".svg"
        print "Saving...",filename
        if self.display_commands:
             s = "gr.Save('%s')" % (filename)
             print s
        ss = self.canvas + Ender
        f = open(filename,'w')
        f.write(ss)
        f.close()
        fn= filename.split('/')[-1]
        filenamehtml = filename+'.html'
        f = open(filenamehtml,'w')
        ss = """
<!DOCTYPE html>
<html>
  <head>
    <title>Ruler and Compass Construction</title>
  </head>
  <body>
<img width="%d" height="%d" src="%s" onerror="this.src=''">
<br>
%s
</body>
</html>
""" % (1000,1000, fn,msg)
        f.write(ss)
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
