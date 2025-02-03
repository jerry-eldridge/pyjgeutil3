import os

emmafont = "C:/emma/fonts/font3/"

def GetChar(ch):
##     """
##     List of font instructions for character ch.
##     Instructions can be 'D X Y' (Pen Down at X Y),
##     'M X Y' (Move Pen to X Y), 'U' (Pen Up),
##     'E' (End character).
##
##     Eg, L = GetChar('A')
##     """
     fn = '%s%d.txt' % (emmafont,ord(ch))
     f = open(fn,'r')
     L = []
     for line in f.readlines():
         line = line.strip()
         M = line.split()
         L.append(M)
     f.close()
     return L

def Strokes(ch):
##     """
##     List of strokes. Each stroke is a list of
##     font instructions (not including 'U') where
##     the pen is entirely down.
##
##     Eg, strokes = Strokes('A')
##     """
     L = GetChar(ch)
     S = []
     strokes = []
     for M in L:
         if M[0] == 'U':
             strokes.append(S)
             S = []
             continue
         S.append(M)
     return strokes

def ScaleStrokes(strokes,sx,sy):
     strokes_new = []
     for stroke in strokes:
         stroke_new = []
         for M in stroke:
             if M[0]=='D' or M[0] =='M':
                 M[1] = str(int(float(M[1])*sx))
                 M[2] = str(int(float(M[2])*sy))
             stroke_new.append(M)
         strokes_new.append(stroke_new)
     return strokes_new

def norm2d(A):
     """
     l**2 norm of 2D vector A
     """
     return sqrt(A[0]**2 + A[1]**2)

def metric2d(A,B):
     """
     distance between 2D vectors A and B
     """
     return norm2d(array(A)-array(B))

def Curve(stroke):
##     """
##     Convert font instructions for a stroke (which
##     is entirely written with pen down) to a list
##     of points the pen tip travels. A point is pt=[x,y]
##     and a curve is [pt,...].
##     """
     down = False
     L = []
     for cmd in stroke:
         if cmd[0]=='U':
             down = False
         if cmd[0]=='E':
             break
         if cmd[0]=='D':
             down = True
             x_last = float(cmd[1])
             y_last = float(cmd[2])
             L.append([x_last,y_last])
         if cmd[0]=='M' and down:
             x = float(cmd[1])
             y = float(cmd[2])
             L.append([x,y])
             x_last = x
             y_last = y
     return L

