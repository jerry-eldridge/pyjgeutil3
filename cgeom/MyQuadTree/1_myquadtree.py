import random

random.seed(123890123)

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
        self.PTS = None
        self.L = str("n()")
        self.key = key
    def __str__(self):
        self.L = str("n_%d()") % self.key
        return self.L
class p:
    def __init__(self,L,key=0):
        self.PTS = L
        self.L = 'p_%d(%s)' % (key,str(self.PTS))
        self.key = key
    def __str__(self):
        self.L = 'p_%d(%s)' % (self.key,str(self.PTS))
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
class q:
    def __init__(self,a,b,c,d,key=0,str_maxd=10):
        self.QT = [n(),n(),n(),n()]
        self.QT[0] = a
        self.QT[1] = b
        self.QT[2] = c
        self.QT[3] = d
        self.key = key
        self.str_maxd = str_maxd
        self.L = ""
    def __str__(self):
        d = qdepth(self)
        pad = ' '*(self.str_maxd-d)
        M = list(map(str,self.QT))
        s = 'q_%d(\n' % (self.key)
        for m in M:
            t = pad + '%s,\n' % m
            s = s + t
        s = s + pad + ')'
        self.L = s
        return self.L
    def Insert(self, pts, idx, pt, max_depth=7, key = -1):
        depth = qdepth(self)
        m = Find_m(pt)
        if type(self.QT[m]) == type(q(n(),n(),n(),n())):
            self.QT[m].Insert(pts,idx,pt, max_depth-1, key = m)
            return
        elif type(self.QT[m]) == type(n()):
            self.QT[m] = p([idx],key = m)
            return
        elif type(self.QT[m]) == type(p([])) and depth <= max_depth:
            P = self.QT[m].PTS + [idx]
            if len(P) <= 4:
                self.QT[m].PTS = P
                return
            self.QT[m] = q(n(key=0),n(key=1),n(key=2),n(key=3),key=m)
            for i in range(len(P)):
                idx_i = P[i]
                pt_i = pts[idx_i]
                m_i = Find_m(pt_i)
                if type(self.QT[m].QT[m_i]) == type(n()):
                    self.QT[m].QT[m_i] = p([idx_i],key=m_i)
                elif type(self.QT[m].QT[m_i]) == type(p([])):
                    self.QT[m].QT[m_i].PTS.append(idx_i)
                else:
                    self.QT[m].QT[m_i].Insert(pts,
                        idx_i, pt_i, max_depth-1,key=m_i)
            return

ww = 500
hh = 500
N = 10
pts = []
for i in range(N):
    x = random.uniform(0,ww)
    y = random.uniform(0,hh)
    pt = [x,y]
    pt = list(map(int,pt))
    pts.append(pt)
print("pts:")
depth = 4
for i in range(len(pts)):
    pt = pts[i]
    L1,L2 = C(pt,b1=depth,b2=depth)
    bbox = get_bbox(ww,hh,L1,L2,base1=2,base2=2)
    print(i,pt,Find_m(pt))
a = q(
        q(
            p([1,2]),
            n(),
            n(),
            n()
        ),
        p([3]),
        n(),
        n()
    )
print("a =",a)
print("a.QT[0].QT[0].PTS =",a.QT[0].QT[0].PTS)
print("qdepth(a) = ",qdepth(a))

b = q(n(),n(),q(n(),n(),q(n(),p([1]),n(),p([2,3])),n()),q(p([4]),n(),n(),n()))
print("b = ",b)
print("qdepth(b) = ",qdepth(b))

b = q(n(),n(),q(n(),n(),p([1]),n()),n())
print("b = ",b)
print("qdepth(b) = ",qdepth(b))

b = q(n(),n(),p([1]),n())
print("b = ",b)
print("qdepth(b) = ",qdepth(b))

b = q(n(),n(),n(),n())
print("b = ",b)
print("qdepth(b) = ",qdepth(b))

c = q(n(),n(),n(),n())
print(len(pts))
for idx in range(len(pts)):
    pt = pts[idx]
    c.Insert(pts, idx, pt, max_depth=10)
print("c = ",c)
