import time
from datetime import datetime
from math import sin,cos,pi
import numpy as np
import sys
#sys.path.insert(0,r"C:\_opencv2\opencv\build\python\2.7") #20130702 version
import pygame

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
        pygame.init()
        self.size = w,h
        self.speed = [60,60]
        self.font = pygame.font.Font(None,23)
        self.screen = pygame.display.set_mode(self.size)
        self.r = pygame.mouse.get_rel()
        self.Clear()
        if self.display_commands:
             s = "gr.__init__(%d,%d,display_graphics=%s,display_commands=%s)" % \
                 (w,h,display_graphics,display_commands)
             print s
    def Clear(self):
        if self.display_commands:
             s = "gr.Clear()"
             print s
        self.screen.fill((255,255,255))
    def Line(self,A,B,color,thickness=4):
        A = map(int,A)
        B = map(int,B)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Line(%s,%s,%s)" % (str(A),str(B),str(color))
             else:
                  s = "gr.Line(%s,%s,%s)" % (self.plab.Label(A),self.plab.Label(B),str(color))
             print s
        pygame.draw.line(self.screen,tuple(color),tuple(A[:2]),tuple(B[:2]),thickness)
        return 
    def Circle(self,C,r,color,thickness=4):
        C = map(int,C)
        r = int(r)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Circle(%s,%d,%s)" % (str(C),r,str(color))
             else:
                  s = "gr.Circle(%s,%d,%s)" % (self.plab.Label(C),r,str(color))
             print s
        display_commands = self.display_commands
        self.display_commands = False
        angle = 0
        dangle = 2*pi/100.0
        while angle < 2*pi:
             x1 = r*cos(angle) + C[0]
             y1 = r*sin(angle) + C[1]
             angle += dangle
             x2 = r*cos(angle) + C[0]
             y2 = r*sin(angle) + C[1]
             self.Line([x1,y1],[x2,y2],color,thickness=thickness)
        self.display_commands = display_commands
        return
    def Point(self,pt,color):
        pt = map(int,pt)
        if self.display_commands:
             if self.plab is None:
                  s = "gr.Point(%s,%s)" % (str(pt),str(color))
             else:
                  s = "gr.Point(%s,%s)" % (self.plab.Label(pt),str(color))
             print s
        display_commands = self.display_commands
        self.display_commands = False
        r = 7
        self.Circle([pt[0],pt[1]],r/2,[color[2],color[1],color[0]],thickness=r)
        self.display_commands = display_commands
        return
    def Text(self,s,x,y,color,scale=1):
        pt = [x,y]
        pt = map(int,pt)
        if self.display_commands:
             t = "gr.Text('%s',%d,%d,%s,scale=%d)" % (s,x,y,str(color),scale)
             print t
        # scale doesn't scale font size
        txt = self.font.render(s,int(round(scale)),tuple(color))
        txtpos = txt.get_rect()
        txtpos.x = pt[0]
        txtpos.y = pt[1]
        self.screen.blit(txt,txtpos)
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
        if ms == -1:
             while True:
                  mouse_pos = pygame.mouse.get_pos()
                  ch = None
                  for ev in pygame.event.get():
                      if ev.type == pygame.KEYDOWN:
                           ch = ev.key
                  pygame.display.update()
                  if not (ch is None):
                       break
        else:
             mouse_pos = pygame.mouse.get_pos()
             ch = None
             for ev in pygame.event.get():
                 if ev.type == pygame.KEYDOWN:
                      ch = ev.key
             pygame.display.update()
       
        
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
        pygame.image.save(self.screen,filename)
        return
    def Load(self,filename):
        if self.display_commands:
             s = "gr.Load('%s')" % (filename)
             print s
        img = pygame.image.load(filename)
        imgrect = img.get_rect()
        self.screen.blit(img,imgrect)
        return
    def Close(self):
        if self.display_commands:
             s = "gr.Close()"
             print s
        pygame.quit()
        return
