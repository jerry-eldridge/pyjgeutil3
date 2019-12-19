import copy
from a_star_digraph import *

from sympy import divisors # optional

"""
You can gain intuition by looking at sympy library
though no (non-included) python libraries are required.

>>> from sympy import factorint
>>> factorint(120)
{2: 3, 3: 1, 5: 1}
>>>
>>> from sympy import divisors
>>> divisors(120)
[1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120]

L is really just divisors(120), but we pick a larger
vertex set [1,2,3,...., 110,111,112, ..., 119,120]
including all integers from 1 to 120 inclusive.

Here we define a lattice (L,join,meet) with join the lcm
and meet the gcd of two integers. L is a range of numbers
from 1 to n. The Bottom is 1 and Top is n. We define
a graph for the lattice using covers, UpCover(a) as
the Up Adjacency. Likewise DownCover(a) defines Down
Adjacency.

"""
n = 120
L = range(1,n+1)
Bottom = 1
Top = n

def gcd(a,b):
    """
    Recursive definition of gcd. Note
    for example if a = 3, and b = 100000,
    there will be lots of recursions and the
    recursion depth might be exceeded. Thus
    you need to use a,b such that the number
    of gcd calls to compute gcd(a,b) is not large.
"""
    s = "gcd(%d,%d)" % (a,b)
    a0 = a
    b0 = b
    a = min(a0,b0)
    b = max(a0,b0)
    if a == 0:
        return b
    if a < 0:
        print "error: a = ",a
        return a
    return gcd(a,b-a)

def lcm(a,b):
    return (a*b)/gcd(a,b)

# define meet and join for divisors lattice
# a /\ b
def meet(a,b):
    return gcd(a,b)
# a \/ b
def join(a,b):
    return lcm(a,b)
# define top and bottom for divisors lattice
# assumes bounded lattice, where top is maximal, and
# bottom minimal element.
def top(L):
    global Top
    # infinity (can't be large else recursion depth exceeded)
    return Top
def bottom(L):
    global Bottom
    return Bottom

# a <= b
def Less(a,b):
    return (meet(a,b) == a)

# a >= b
def Greater(a,b):
    return (join(a,b) == a)

def Infimum(L):
    Top = top(L)
    val = Top
    for c in L:
        val = meet(val,c)
    return val

def inf(L):
    return Infimum(L)

def Supremum(L):
    Bottom = bottom(L)
    val = Bottom
    for c in L:
        val = join(val,c)
    return val

def sup(L):
    return Supremum(L)

# interval [a,b] in Lattice elements L
def Interval(L,a,b):
    I = []
    for u in L:
        if Less(a,u) and Less(u,b):
            I.append(u)
    return I

# left open interval (a,b] in Lattice elements L
def LeftOpenInterval(L,a,b):
    I = Interval(L,a,b)
    if I == []:
        return I
    I.remove(a)
    return I

# right open interval [a,b) in Lattice elements L
def RightOpenInterval(L,a,b):
    I = Interval(L,a,b)
    if I == []:
        return I
    I.remove(b)
    return I

# open interval (a,b) in Lattice elements L
def OpenInterval(L,a,b):
    I = Interval(L,a,b)
    if I == []:
        return I
    I.remove(a)
    if I == []:
        return I
    I.remove(b)
    return I

def UpCover(L,a):
    Top = top(L)
    cover = LeftOpenInterval(L,a,Top)
    for v in cover:
        for w in cover:
            if w == v: continue
            if Greater(w,v):
                try:
                    cover.remove(w)
                except:
                    continue
            if Greater(v,w):
                try:
                    cover.remove(v)
                except:
                    continue
    return cover

def DownCover(L,a):
    Bottom = bottom(L)
    cover = RightOpenInterval(L,Bottom,a)
    for v in cover:
        for w in cover:
            if w == v: continue
            if Less(w,v):
                try:
                    cover.remove(w)
                except:
                    continue
            if Less(v,w):
                try:
                    cover.remove(v)
                except:
                    continue
                
    return cover

def GetGraph(L):
    V = copy.deepcopy(L)
    E = []
    for u in V:
        for v in UpCover(L,u):
            E.append([u,v])
    G = [V,E]
    return G

def cost(a,b):
    global G
    E = G[1]
    if ([a,b] in G):
        return 1
    else:
        return 0

r = {}
def rank_reset():
    global r
    r = {}
    return

def rank(G,a):
    global r
    try:
        return r[a]
    except:
        L = G[0]
        Bottom = bottom(L)
        path = A_star_digraph(G,Bottom,a, cost=cost)
        val = len(path)-1
        r[a] = val
        return r[a]

def rank_set_all(G):
    V = G[0]
    for a in V:
        val = rank(G,a)
    return

def get_rank_level(G,k, setall=True):
    if setall:
        rank_set_all(G)
    V = G[0]
    L = []
    for v in V:
        if rank(G,v) == k:
            L.append(v)
    return L

def GetPts(G, width, height, setall=True):
    
    global n
    V = G[0]
    if setall:
        rank_set_all(G)
    pts = []
    N = rank(G,top(V))
    margins = 0.85
    for v in V:
        j = rank(G,v)
        L = get_rank_level(G,j, setall=False)
        i = L.index(v)
        dy = 1.0*height*margins/(N+1)
        y = height - (1.0*j*dy + height*(1-margins)/2)
        try:
            dx = 1.0*width*margins/(len(L)-1)
            x = i*dx
        except:
            x = width/2
        x = x + (1-margins)/2.0*width

        pts.append([x,y, 0])
    def roundpt(pt):
        return [int(round(pt[0])),int(round(pt[1])), int(round(pt[2]))]
    pts = map(lambda pt: roundpt(pt),pts)
    return pts

G = GetGraph(L)
G[0] = divisors(n) # optional
V = G[0]
E = G[1]

rank_reset()

width = 800
height = 800
pts = GetPts(G, width, height)
Vnames = [""]*len(V)


