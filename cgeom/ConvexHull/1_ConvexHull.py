import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import graphics_cv as racg

import numpy as np
d = lambda A,B: np.linalg.norm(np.array(A)-np.array(B))
lerp = lambda A,B,t: list((1-t)*np.array(A)+t*np.array(B))

# Returns turned left 1,went straight 0,or turned right -1
# p0,p1,p2 are lists converted in procedure to numpy arrays
def turned_left(p0, p1, p2):
    p0 = p0 + [0]
    p1 = p1 + [0]
    p2 = p2 + [0]
    p0,p1,p2 = list(map(np.array,[p0,p1,p2]))
    v = np.cross(p1-p0,p2-p0)[2]
    if v != 0:
        v = abs(v)/v
    return v

def right_turn(p0,p1,p2):
    v = turned_left(p0,p1,p2)
    flag = v == -1
    return flag

def BubbleSortaHelper(L,n):
    i = 0
    # Swap the first consecutive pair that is not
    # in order
    for i in range(n-1):
        if greater_than(L[i],L[i+1]):
            tmp = L[i]
            L[i] = L[i+1]
            L[i+1] = tmp
            break
    return L

def BubbleSorta(L):
    n = len(L)
    # It takes (n+1) swaps to do first number
    # and so (n+1)*(n+1) to do all n+1 numbers
    # and to make sure use n+1 instead of n
    # The time complexity is O(n**2).
    for j in range((n+1)*(n+1)):
        L = BubbleSortaHelper(L,n)
    return L

def greater_than(x,y):
    flag1 = x[0] == y[0]
    flag2 = x[1] >= y[1]
    flag3 = x[0] > y[0]
    if flag1:
        flag = flag2
    else:
        flag = flag3
    return flag

def DisplayConvexHull(gr,E,P,Q):
    for pt in P:
        color = [0,255,0]
        gr.Point(pt,color)
    for pt in Q:
        color = [0,0,0]
        gr.Point(pt,color)
    for i in range(len(E)):
        e = E[i]
        u,v = e
        A = P[u]
        B = P[v]
        M = list(map(int,lerp(A,B,0.5)))
        gr.Line(P[u],P[v],[255,0,0])
        gr.Text(str(i),M[0],M[1],color=[0,0,255])
    return


####################################################
# [1] Computational Geometry, de Berg et al, 2008,
# Springer

def SlowConvexHull(P, epsilon = 1e-3):
    n = len(P)
    assert(n >= 3)
    V = range(len(P))
    E = []
    for i in V:
        for j in V:
            if d(P[i],P[j]) < epsilon:
                continue
            valid = True
            for k in V:
                if d(P[k],P[i]) < epsilon:
                    continue
                if d(P[k],P[j]) < epsilon:
                    continue
                if turned_left(P[i],P[j],P[k])==1:
                    valid = False
            if valid:
                e = (i,j)
                E.append(e)
    Q = []
    for e in E:
        u,v = e
        Q.append(P[u])
        Q.append(P[v])
    return E, Q

def ConvexHull(P, epsilon = 1e-3):
    n = len(P)
    assert(n >= 3)
    #P.sort(key=lambda tup: tup[0])
    BubbleSorta(P)
    L_u = []
    L_d = []
    L_u.append(0)
    L_u.append(1)
    for i in range(2,n):
        L_u.append(i)
        while len(L_u) > 2 and \
             (not right_turn(P[L_u[-3]],
             P[L_u[-2]], P[L_u[-1]])):
            L_u.remove(L_u[-2])
    L_d.append(n-1)
    L_d.append(n-2)
    for i in range(n-3,-1,-1):
        L_d.append(i)
        while len(L_d) > 2 and \
            (not right_turn(P[L_d[-3]],
             P[L_d[-2]], P[L_d[-1]])):  
            L_d.remove(L_d[-2])
    L_d = L_d[1:-1]
    L = L_u + L_d
    m = len(L)
    E = []
    for i in range(m):
        u = L[i]
        v = L[(i+1)%m]
        e = (u,v)
        E.append(e)
    Q = []
    for e in E:
        u,v = e
        Q.append(P[u])
        Q.append(P[v])
    return E, Q

#####################################################
ww = 800
hh = 500
def GeneratePoints(N):
    pts = np.random.rand(N,2)
    P = []
    for i in range(N):
        pt = pts[i,:]
        pt = [pt[0]*ww,pt[1]*hh]
        pt = list(map(int, list(pt)))
        P.append(pt)
    return P

flag1 = True
if flag1:
    gr = racg.Graphics(w=800,h=500)
    N = 50 # number of points
    J = 20 # number of experiments
    for j in range(J):
        gr.Clear()
        P = GeneratePoints(N)
        E,Q = ConvexHull(P, epsilon = 1e-3)
        DisplayConvexHull(gr,E,P,Q)
        c = gr.Show("result",-1)
        if c == ord('e'):
            break
    gr.Close()

