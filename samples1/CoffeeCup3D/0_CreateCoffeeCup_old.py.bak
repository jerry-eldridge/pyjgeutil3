import RevolveCurve as rc
import extrusion as ext
import affine as aff
import graph as g
import mapto

from copy import deepcopy

# Add Water Bottle scene (WBS)
def WaterBottleScene(G,Gs,t,q,s):
     f_ = open("WaterBottle.obj",'r')
     txt = f_.read()
     f_.close()
     G_small = ext.OBJ2Graph(txt)
     pts = G_small['pts']
     C = aff.Center(pts)
     pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
     G_small['pts'] = pts

     # Add special textbook to scene
     pts2 = G_sp['pts']
     C2 = aff.Center(pts2)
     pts2 = aff.Translate(pts2,-C2[0],-C2[1],-C2[2],align=False)
     degrees = 90+30
     axis = [0,0,1]
     q_sp = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     pts2 = aff.Rotate(pts2,q_sp,align=False)
     t2 = [180.,180.,rec_sp.d/2.]
     pts2 = aff.Translate(pts2,t2[0],t2[1],t2[2],align=False)
     G_sp['pts'] = pts2
     
     G_small = GraphUnionS(G_small,G_sp)

     pts = G_small['pts']
     C = aff.Center(pts)
     pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
     pts = aff.Rotate(pts,q,align=False)
     pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
     pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
     G_small['pts'] = pts
     Gs = Append(Gs,G_small)
     G = GraphUnionS(G,G_small)
     return G,Gs

# TableLeg(height,radius1,radius2,n=10,m=10)
def TableLeg(height,radius1,radius2,n=10,m=10):
    h = height
    r1 = radius1
    r2 = radius2
    curve = []
    x0 = 0
    for i in range(1,m-1):
        r = mapto.MapTo(0,r1,m-1,r2,i)
        xi = r
        yi = mapto.MapTo(0,0,m-1,h,i)
        pt = [xi,yi]
        curve.append(pt)
    yi = mapto.MapTo(0,0,m-1,h,.1)
    curve = [[0,yi]]+curve+[[0,height]]

    # Assume curve has symmetry y-axis
    x0 = curve[0][0]
    x_min = min(map(lambda pt: pt[0]-x0,curve))
    x_max = max(map(lambda pt: pt[0]-x0,curve))
    y_min = min(map(lambda pt: pt[1],curve))
    y_max = max(map(lambda pt: pt[1],curve))
    poly_wb = deepcopy(curve)

    pts = map(lambda pt: [0,pt[1],0], poly_wb)
    y_min = min(map(lambda pt: pt[1],poly_wb))
    y_max = max(map(lambda pt: pt[1],poly_wb))
    doc = g.Cn(n)
    cx,cy,cz = [0,0,0]
    r0 = 1.
    doc1 = rc.CreateCircleGeometry(doc,cx,cy,cz,r0)

    spath = []
    path = []
    pti = poly_wb[0]
    xi,yi = pti
    yi_last = yi
    
    dx = x_max-x_min
    dy = y_max-y_min
    epsilon = 1e-4
    if abs(dx) > epsilon:
        aspect = 1.*dy/dx
    else:
        aspect = 1.*dx/dy

    for i in range(len(poly_wb)):
        pti = poly_wb[i]
        xi,yi = pti
        r = abs(xi - x0)
        dy = yi-yi_last
        epsilon = .1
        if abs(dy) > epsilon:
            spath.append(r)
            path.append([yi,0,0])
        yi_last = yi

    degrees = 90+180
    axis = [0,1,0]
    q0 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    q = q0
    t = [0,0,-height*.4]
    s = [1,1,1]
    C = aff.Center(path)
    pts = aff.Translate(path,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    path = pts
    #path = [[0,0,0],[10,1,0],[20,4,0],[30,9,0]]
    H = ext.Extrusion0(doc1,path,spath)
    return H

def SquareTable1():
    G = {}
    G['V'] = []
    G['E'] = []
    G['F'] = []
    G['N'] = []
    G['pts'] = []

    w,h,d = [500,500,20]
    degrees = 0
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    scale = 1.
    s = [scale,scale,scale] # the same scale as previous for caps
    t = [-w/2.,-h/2.,-d/2.]
    H1 = ext.CubeObj(w,h,d, t,q,s)
    G = ext.GraphUnionS(G,H1)
    def Leg(t,q,s):
        height = w*(3./5.)
        r1 = 8.
        r2 = 12.
        H = TableLeg(height,r1,r2,n=10,m=10)
        pts = H['pts']
        C = aff.Center(pts)
        pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
        pts = aff.Rotate(pts,q,align=False)
        pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
        pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
        H['pts'] = pts
        return H
    N1 = 2
    N2 = 2
    for j in range(N2):
        for i in range(N1):
            height = w*(3./5.)
            t = [2*w*(1.*i/N1)-w/2,2*h*(1.*j/N2)-h/2,-height*.4]
            degrees = 0
            axis = [0,1,0]
            q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
            scale = 1.
            s = [scale,scale,scale] # the same scale as previous for caps
            Hij = Leg(t,q,s)
            G = ext.GraphUnionS(G,Hij)
    return G

def CoffeeCup():
    G = {}
    G['V'] = []
    G['E'] = []
    G['F'] = []
    G['N'] = []
    G['pts'] = []

    scale = 10.
    w,h,d = [3.25*scale,3.25*scale,3.8*scale]
    degrees = 0
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    scale = 1.
    s = [scale,scale,scale] # the same scale as previous for caps
    t = [-w/2.,-h/2.,-d/2.]
    H1 = ext.CubeObj(w,h,d, t,q,s)
    G = ext.GraphUnionS(G,H1)
    return G

G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []

# trefoil knot
H0 = ext.TrefoilKnot()
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
t = [-80,0,50.]
pts = H0['pts']
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
C = aff.Center(pts)
pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
pts = aff.Rotate(pts,q,align=False)
pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
H0['pts'] = pts
Gs = ext.Append(Gs,H0)
G = ext.GraphUnionS(G,H0)

# square table
H1 = SquareTable1()
Gs = ext.Append(Gs,H1)
G = ext.GraphUnionS(G,H1)

# coffee cup
Hcc = CoffeeCup()
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
t = [100,0,30.]
pts = Hcc['pts']
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
C = aff.Center(pts)
pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
pts = aff.Rotate(pts,q,align=False)
pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
Hcc['pts'] = pts

Gs = ext.Append(Gs,Hcc)
G = ext.GraphUnionS(G,Hcc)


# N1 x N2 water bottles
N1 = 1
N2 = 1
for j in range(N2):
    for i in range(N1):
        H2 = rc.WaterBottle(n=10)
        degrees = -90
        axis = [0,1,0]
        q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
        scale = 1.
        s = [scale,scale,scale] # the same scale as previous for caps
        r = 40.
        t0 = [N1*r,-N2*r,55.]

        if j%2 == 0:
            t = [t0[0]+r*i,t0[1]+r*j,t0[2]]
        else:
            t = [t0[0]+r*i + r*0.5,t0[1]+r*j,t0[2]]
        pts = H2['pts']
        q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
        C = aff.Center(pts)
        pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
        pts = aff.Rotate(pts,q,align=False)
        pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
        pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
        H2['pts'] = pts
        Gs = ext.Append(Gs,H2)
        G = ext.GraphUnionS(G,H2)

# floor
w,h,d = [500*2,500*2,5]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
t = [-w/2.,-h/2.,-d/2.-250]
#H3 = ext.CubeObj(w,h,d, t,q,s)
#Gs = ext.Append(Gs,H3)
#G = ext.GraphUnionS(G,H3)

ext.Graphs2OBJ("WaterBottle.obj",Gs,"scene")
f_ = open("WaterBottle.obj",'r')
txt = f_.read()
f_.close()
G_small = ext.OBJ2Graph(txt)

degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = .1
s = [scale,scale,scale] # the same scale as previous for caps
t = [0.,0.,0.]
pts = G_small['pts']
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
C = aff.Center(pts)
pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
pts = aff.Rotate(pts,q,align=False)
pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
G_small['pts'] = pts

G_coffee = deepcopy(G_small)

ext.Graph2OBJ("CoffeeCup.obj",G_coffee,"scene")

import os
print "Open WaterBottle_small.obj with 3D Viewer by double-clicking on it"
os.system("CoffeeCup.obj")
