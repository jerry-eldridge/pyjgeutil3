import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import graphics_cv as racg

import tracemalloc

from copy import deepcopy
import myquadtree2 as qtr
import random

import sqlite3
import time
from datetime import datetime
import collections
from math import sqrt

random.seed(123890123)

ww = 800
hh = 500

def Milliseconds():
    ms = int(round(time.time()*1000))
    return ms

# With x1 -> y1 and x2 -> y2, given x, return y using linear map
def MapTo(x1, y1, x2, y2, x):
    epsilon = 0.0001
    if abs(x2 - x1) > epsilon:
        m = 1.*(y2-y1)/(x2-x1)
    else:
        m = 1
    y = m*(x-x1)+y1
    return y

def norm_oo(x):
    return max(abs(x[0]),abs(x[1]))

def dist_oo(A,B):
    C = [0]*len(A)
    for i in range(len(A)):
        C[i] = A[i] - B[i]
    val = norm_oo(C)
    return val

class Point:
    def __init__(self,pt,tup):
        self.pt = pt
        self.tup = tup
        return
    def __str__(self):
        s = 'P(pt=%s,tup=%s)' % (str(self.pt),str(self.tup))
        return s

def Transform(pt,bbox1,bbox2):
    x,y = pt
    x1,y1,x2,y2 = bbox1
    x3,y3,x4,y4 = bbox2
    xp = MapTo(x1,x3,x2,x4,x)
    yp = MapTo(y1,y3,y2,y4,y)
    pt2 = [xp,yp]
    return pt2
     
N = 20000
pts = []

scale = 1
bbox_win = qtr.AABB([ww/2,hh/2],ww*scale,hh*scale)

def Build(n,bbox):
    tracemalloc.start()
    ms_start = Milliseconds()
    for i in range(N):
        x = random.uniform(0,ww)
        y = random.uniform(0,hh)
        pt = [x,y]
        pt = list(map(int,pt))
        pts.append(pt)

    c = qtr.q(bbox,capacity=4)
    print("|pts|=",len(pts))
    TT = []
    XX = []
    MB = (10**3)**2
    for idx in range(len(pts)):
        name = random.choice(["cat","dog","human","mouse","robot"])
        tup = (idx,name)
        A = Point(pts[idx],tup)
        c.insert(A)
        val = tracemalloc.get_traced_memory()[0]
        ms_val = Milliseconds()
        t = ms_val - ms_start
        TT.append(t)
        XX.append(val/MB)
    tracemalloc.stop()
    return c,pts, TT,XX

c,pts, TT,XX = Build(pts,bbox_win)

import matplotlib.pyplot as plt
plt.plot(TT,XX,'b')
plt.xlabel("t (ms)")
plt.ylabel("Memory MB")
plt.show()

i = random.choice(range(len(pts)))
scale = .01
bbox_q = qtr.AABB(pts[i],ww*scale,hh*scale)
res = c.query(bbox_q)
for x in list(map(lambda tup: [str(tup[0]),tup[1]], list(zip(res[0],res[1])))):
	print(x)
