import RevolveCurve as rc
import extrusion as ext
import BasicShapes as bs
import affine as aff
import graph as g
import mapto

import numpy as np

from copy import deepcopy

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

# Add Water Bottle scene (WBS)
def WaterBottleScene(G,Gs,t,q,s):
     f_ = open(BIGDATA+"WaterBottle.obj",'r')
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

def CoffeeCup0(n=30,m=20,r0=20.):
    flag_cup = True
    flag_handle = True
    H1 = {}
    H1['V'] = []
    H1['E'] = []
    H1['pts'] = []
    H1['F'] = []
    H1['N'] = []
    H2 = {}
    H2['V'] = []
    H2['E'] = []
    H2['pts'] = []
    H2['F'] = []
    H2['N'] = []
    if flag_cup:
         # polygon curve of surface of revolution
         # Create Cup. At present, its imperfect recreating
         # a cover to coffee cup.
         curve1a = [[406, 388], [441, 384], [469, 378], [489, 363], [506, 347],
                   [518, 330], [520, 314], [522, 297], [525, 276], [528, 258],
                   [530, 228], [528, 182], [528, 150], [527, 113], [527, 91],
                   [532, 73], [540, 68]]
         curve1b = [[554, 70], [554, 86], [549, 108],
                   [550, 136], [546, 181], [547, 214], [544, 249], [544, 268],
                   [538, 281], [540, 288], [539, 300], [531, 312], [532, 329],
                   [526, 350], [513, 362], [502, 378], [482, 393], [446, 406],
                   [417, 409]]
         curve1 = curve1a + curve1b
         x0 = curve1[0][0]
         
         x_min = min(map(lambda pt: pt[0]-x0,curve1))
         x_max = max(map(lambda pt: pt[0]-x0,curve1))
         y_min = min(map(lambda pt: pt[1],curve1))
         y_max = max(map(lambda pt: pt[1],curve1))
         degrees = 0
         axis = [0,1,0]
         q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
         scale = 1.
         s = [scale,scale,scale] # the same scale as previous for caps
         t = [0,0,0]
         H1 = rc.RevolveCurve(curve1,t,q,s, n, bcap=False, ecap=False)
    if flag_handle:
         # Create Handle
         curve2 = [[203, 130], [189, 114], [165, 102], [149, 100], [132, 101],
                   [116, 106], [106, 113], [107, 128], [112, 152], [118, 169],
                   [127, 184], [138, 201], [149, 208], [165, 209], [186, 214],
                   [207, 213]]
         # Assume curve has symmetry y-axis
         x0 = curve2[0][0]
         x_min = min(map(lambda pt: pt[0]-x0,curve2))
         x_max = max(map(lambda pt: pt[0]-x0,curve2))
         y_min = min(map(lambda pt: pt[1],curve2))
         y_max = max(map(lambda pt: pt[1],curve2))
         poly_wb = deepcopy(curve2)

         pts = map(lambda pt: [0,pt[1],0], poly_wb)
         y_min = min(map(lambda pt: pt[1],poly_wb))
         y_max = max(map(lambda pt: pt[1],poly_wb))
         doc = g.Cn(m)
         cx,cy,cz = [0,0,0]
         doc1 = rc.CreateCircleGeometry(doc,cx,cy,cz,r0)

         spath = []
         path = []
         pti = poly_wb[0]
         xi,yi = pti
         yi_last = yi
         
         dx = x_max-x_min
         dy = y_max-y_min

         for i in range(len(poly_wb)):
             pti = poly_wb[i]
             xi,yi = pti
             r = abs(xi - x0)
             dy = yi-yi_last
             epsilon = .1
             if abs(dy) > epsilon:
                 spath.append(1.)
                 path.append([xi,yi,0])

         degrees = 90+180
         axis = [1,0,0]
         q0 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
         q = q0
         t = [-184,0,100]
         s = [1,1,1]
         C = aff.Center(path)
         pts = aff.Translate(path,-C[0],-C[1],-C[2],align=False)
         pts = aff.Rotate(pts,q,align=False)
         pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
         pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
         path = pts
         H2 = ext.Extrusion0(doc1,path,spath)

    H = ext.GraphUnionS(H1,H2)
    
    return H

def CoffeeCup(n=30):
    H = CoffeeCup0(n)
    pts = H['pts']
    scale = .15
    s = [scale,scale,scale] # the same scale as previous for caps
    t = [0,0,0]
    degrees = 0
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    C = aff.Center(pts)
    pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    H['pts'] = pts
    return H

######################### SCENE 1 BEGIN
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

# Save Scene 1
ext.Graphs2OBJ(BIGDATA+"WaterBottle.obj",Gs,"scene")
######################### SCENE 1 END

######################## SCENE 2 BEGIN
# Save CoffeeCup into new scene G,Gs to file
# "CoffeeCup.obj" as Scene 2
G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []
# coffee cup
Hcc = CoffeeCup()
ext.Graph2OBJ(BIGDATA+"CoffeeCup.obj",Hcc,"scene")
# add two obj files later to include CoffeeCup.obj
Gs = ext.Append(Gs,Hcc)
G = ext.GraphUnionS(G,Hcc)
ext.Graphs2OBJ(BIGDATA+"CoffeeCup.obj",Gs,"scene")
######################### SCENE 2 END

######################## SCENE 3 BEGIN
# Save Donut into new scene G,Gs to file
# "Donut.obj" as Scene 2
G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []
# Donut
r1 = 13.
r2 = 20.
t = [0.,0.,0.]
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
Hdon = bs.Torus(r1,r2,t,q,s, m=10,n=60)

ext.Graph2OBJ(BIGDATA+"Donut.obj",Hdon,"scene")
Gs = ext.Append(Gs,Hdon)
G = ext.GraphUnionS(G,Hdon)
ext.Graphs2OBJ(BIGDATA+"Donut.obj",Gs,"scene")
######################### SCENE 3 END

################ MERGE BEGIN SCENE 1, 2 and 3

### Open Scene 1
f_ = open(BIGDATA+"WaterBottleTable.obj",'r')
txt = f_.read()
f_.close()
G_scene1 = ext.OBJ2Graph(txt)
# use scene1 as global scene
###


### Open Scene 2
f_ = open(BIGDATA+"CoffeeCup.obj",'r')
txt = f_.read()
f_.close()
G_scene2 = ext.OBJ2Graph(txt)

### Open Scene 3
f_ = open(BIGDATA+"Donut.obj",'r')
txt = f_.read()
f_.close()
G_scene3 = ext.OBJ2Graph(txt)

# position scene2 within global scene
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
t = [100,0,35.]
pts = G_scene2['pts']
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
C = aff.Center(pts)
pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
pts = aff.Rotate(pts,q,align=False)
pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
G_scene2['pts'] = pts
###

# position scene3 within global scene
degrees = 0
axis = [0,1,0]
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
scale = 1.
s = [scale,scale,scale] # the same scale as previous for caps
t = [150,-50,15.]
pts = G_scene3['pts']
q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
C = aff.Center(pts)
pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
pts = aff.Rotate(pts,q,align=False)
pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
G_scene3['pts'] = pts
###

# Merge Scene 1 and Scene 2 and Save
G = ext.GraphUnionS(G_scene1, G_scene2)
G = ext.GraphUnionS(G, G_scene3)
ext.Graph2OBJ(BIGDATA+"CCDonutTable.obj",G,"scene")

# Double-Click on OBJ file
import os
print "Open CCDonutTable with 3D Viewer by double-clicking on it"
os.system(BIGDATA+"CCDonutTable.obj")
