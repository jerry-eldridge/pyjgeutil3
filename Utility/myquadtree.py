
def Base(i,base, bits):
    L = []
    j = 0
    n = 0
    ii = i
    for j in range(bits):
        a = ii%base
        ii = int(ii/base)
        n = n + a*base**j
        L.append(a)
    L.reverse()
    return L

def Number(L,base):
    n = 0
    k = len(L)-1
    for i in range(len(L)):
        n = n + L[k-i]*base**i
    return n

clamp = lambda x, lo, hi: max(min(x,hi),lo)

def BB(x,y,w,h):
    bbox = (x-w/2,y-h/2,x+w/2,y+h/2)
    return bbox

def get_bbox(ww,hh,L1,L2,base1=2,base2=2):
    n1 = len(L1)
    n2 = len(L2)
    wi = ww/2**n1
    hi = hh/2**n2
    a = Number(L1,base1)
    b = Number(L2,base2)
    xi = a*wi
    yi = b*hi
    bbox = BB(xi,yi,wi,hi)
    return bbox

def T(x,bits=5):
    x = int(round(x))
    L = Base(x,2,bits)
    return L
def S(L):
    x = Number(L,2)
    return x
def C(pt,b1=5,b2=5):
    L1 = T(pt[0],b1)
    L2 = T(pt[1],b2)
    return L1,L2

class n:
    def __init__(self,key=0):
        self.type = 'n'
        self.PTS = None
        self.L = str("n()")
        self.key = key
    def __str__(self):
        self.L = str("n()")
        return self.L
class p:
    def __init__(self,L,key=0):
        self.type = 'p'
        self.PTS = L
        self.L = 'p(%s)' % (str(self.PTS))
        self.key = key
    def __str__(self):
        self.L = 'p(%s)' % (str(self.PTS))
        return self.L

def Find_m(pt):
    n = 1
    a = S(T(pt[0],n))
    b = S(T(pt[1],n))
    if (a,b) == (0,0):
        m = 0
    elif (a,b) == (0,1):
        m = 1
    elif (a,b) == (1,0):
        m = 2
    elif (a,b) == (1,1):
        m = 3
    return m

def qdepth(x):
    if type(x) == type(n()):
        return 0
    if type(x) == type(p([])):
        return 0
    if type(x) == type(q(n(),n(),n(),n())):
        return max(qdepth(x.QT[0]),
                   qdepth(x.QT[1]),
                   qdepth(x.QT[2]),
                   qdepth(x.QT[3])
                   )+1

def Point_in_bbox(bbox,pt):
    x,y = pt
    flag1 = bbox[0] <= x and x <= bbox[2] 
    flag2 = bbox[1] <= y and y <= bbox[3]
    flag = flag1 and flag2
    return flag

###################################################
# [1] https://en.wikipedia.org/wiki/Quadtree
#
class AABB:
    def __init__(self,center,w,h):
        self.center = center
        self.w = w
        self.h = h
    def __str__(self):
        s = '(%s,[%d,%d])' % (str(self.center),self.w,self.h)
        return s
    def containsPoint(self,pt):
        bbox = BB(self.center[0],self.center[1],
           self.w,self.h)
        flag = Point_in_bbox(bbox,pt)
        return flag
    def BoundingBox(self):
        bbox = BB(self.center[0],self.center[1],
           self.w,self.h)
        return bbox
    def Interval(self):
        bbox = self.BoundingBox()
        s = '[%d,%d]x[%d,%d]' % (bbox[0],bbox[2],
                                 bbox[1],bbox[3])
        return s
    def intersectsAABB(self,other):
        bbox1 = self.BoundingBox()
        bbox2 = other.BoundingBox()
        x1,y1,x2,y2 = bbox1
        x3,y3,x4,y4 = bbox2
        def F(x1,x2,x3,x4):
            if x1 <= x3:
                if x2 < x3:
                    flag1 = False
                if x2 >= x3:
                    flag1 = True
            if x3 <= x1:
                if x4 < x1:
                    flag1 = False
                if x4 >= x1:
                    flag1 = True
            return flag1
        flag1 = F(x1,x2,x3,x4)
        flag2 = F(y1,y2,y3,y4)
        flag = flag1 and flag2
        return flag

class q:
    def __init__(self,boundary,str_maxd=10,
                 capacity=4):
        self.capacity = capacity
        self.boundary = boundary
        self.points = []
        self.bboxes = []
        self.QT = [n(),n(),n(),n()]
        self.str_maxd = str_maxd
        self.L = ""
    def __str__(self):
        M = list(map(str,self.QT))
        s = 'q('
        for m in M:
            t = '%s,' % m
            s = s + t
        aa = str(self.points)
        bb = self.boundary.Interval()
        s = s[:-1] + ",pts=%s,bbox='%s')" % (aa,bb)
        self.L = s
        return self.L
    def insert(self, pt):
        if not self.boundary.containsPoint(pt):
            return False
        if (len(self.points) < self.capacity) and \
           type(self.QT[0]) == type(n()):
            self.points.append(pt)
            bbox = self.boundary.BoundingBox()
            self.bboxes.append(bbox)
            return True
        if type(self.QT[0]) == type(n()):
            self.subdivide()
        flag = False
        for i in range(4):
            if self.QT[i].insert(pt):
                flag = True
                break
        return flag
    def subdivide(self):
        bbox = self.boundary.BoundingBox()
        x1,y1,x2,y2 = bbox
        xm = int(round((x1 + x2)/2))
        ym = int(round((y1 + y2)/2))
        c1x = int(round((x1 + xm)/2))
        c1y = int(round((y1 + ym)/2))
        c2x = int(round((x2 + xm)/2))
        c2y = int(round((y2 + ym)/2))
        pts = []
        pts.append([c1x,c1y])
        pts.append([c2x,c1y])
        pts.append([c1x,c2y])
        pts.append([c2x,c2y])
        for i in range(4):
            b = AABB(pts[i],
                     self.boundary.w/2,
                     self.boundary.h/2)
            self.QT[i] = q(b, self.str_maxd)
        return
    def query(self, x):
        pts = []
        bboxes = []
        if not self.boundary.intersectsAABB(x):
            return pts,bboxes
        for i in range(len(self.points)):
            if (x.containsPoint(self.points[i])):
                pts.append(self.points[i])
                bboxes.append(self.bboxes[i])
        if type(self.QT[0]) == type(n()):
            return pts,bboxes
        for i in range(4):
            pts_i,bbox_i = self.QT[i].query(x)
            pts = pts + pts_i
            bboxes = bboxes + bbox_i
        return pts,bboxes
#
####################################################
    
def ROI2(pt,w,h):
    x,y = pt
    cx = (x + (x + w))/2
    cy = (y + (y + h))/2
    roi = AABB([cx,cy],w,h)
    return roi
