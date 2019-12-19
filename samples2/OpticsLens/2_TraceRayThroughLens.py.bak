import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import graph
import graphics_cv as racg
import vectors as vec
from line_intersection import SegmentIntersect as SI
import numpy as np
from math import pi,cos,sin,sqrt,atan2,acos
import cv2


p6 = []
p7 = []
L = 50 # really should be 1 but make 50 to expand slightly region
L = max(1,min(50,L))
def getxy(event, x, y, flags, param):
    global p6,p7,L
    if event == cv2.EVENT_LBUTTONDOWN:
        pt = [x,y]
        p6.append(pt)
        p6 = p6[-2:]
        # extend pt1 and pt2
        pt1 = p6[-2]
        pt2 = p6[-1]
        v = np.array(pt2)-np.array(pt1)
        v = v/np.linalg.norm(v)
        pt1 = list(np.array(pt1)-L*v)
        pt2 = list(np.array(pt2)+L*v)
        p6[-2] = pt1
        p6[-1] = pt2
        w = np.array(pt2)-np.array(pt1)
        w = v/np.linalg.norm(v)
        p7 = MapPoints(p6)

        return
    if event == cv2.EVENT_RBUTTONDOWN:
        pt1 = [384.53645833333343, 11.718750000000114]
        pt2 = [437.48437500000006, 557.48958333333337]
        p6 = [pt1,pt2]
        pt1 = p6[-2]
        pt2 = p6[-1]
        v = np.array(pt2)-np.array(pt1)
        v = v/np.linalg.norm(v)
        pt1 = list(np.array(pt1)-L*v)
        pt2 = list(np.array(pt2)+L*v)
        p6[-2] = pt1
        p6[-1] = pt2
        p7 = MapPoints(p6)
    return

def PathGraph(poly):
   G = graph.Pn(len(poly))
   G['pts'] = poly
   return G

def Transform(shape, T):
    shape4 = map(lambda pt: pt+[0,1], shape)
    SHAPE4 = map(lambda pt: list(np.einsum('ij,j->i',T,pt)), shape4)
    SHAPE = map(lambda pt: pt[:2], SHAPE4)
    return SHAPE

def Rotate(shape,theta,align=True):
    R = vec.rotation_matrix(theta, 0, 0, 1)
    SHAPE = Transform(shape,R)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE
def Translate(shape,tx,ty,align=True):
    T = vec.translation_matrix(tx, ty, 0)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

def RotateAbout(shape,theta,tx,ty,align=True):
    SHAPE = Translate(shape,-tx,-ty,align)
    SHAPE = Rotate(SHAPE,theta,align)
    SHAPE = Translate(SHAPE,tx,ty,align)
    return SHAPE

def Round(shape):
    SHAPE = map(lambda pt: map(lambda x: int(round(x)),pt), shape)
    return SHAPE
def Center(shape):
    # use average of points as Center, the center of mass
    CM = sum(map(lambda pt: np.array(pt)/len(shape),shape))
    return CM
def Scale(shape,s):
    T = vec.scale_matrix(s,s,s)
    SHAPE = Transform(shape,T)
    return SHAPE

def MapPoints(pts):
    C = Center(pts)
    pts2 = Translate(pts,-C[0],-C[1])
    s = 1
    pts3 = Scale(pts2,s)
    pts4 = Translate(pts3,C[0],C[1])
    return pts4
    

# estimated curves of glass sphere with water inside, with sphere in air

#p1 = [[177.62500000000006, 279.1875], [187.00000000000006, 233.875], [204.18750000000006, 196.375], [235.43750000000006, 166.6875], [288.56250000000006, 151.0625], [335.43750000000006, 155.75], [372.93750000000006, 179.1875], [404.18750000000006, 218.25], [416.68750000000006, 252.625], [416.68750000000006, 279.1875]]
#p2 = [[187.00000000000006, 276.0625], [196.37500000000006, 240.125], [218.25000000000006, 199.5], [257.31250000000006, 172.9375], [307.31250000000006, 163.5625], [337.00000000000006, 172.9375], [369.81250000000006, 187.0], [391.68750000000006, 213.5625], [404.18750000000006, 237.0], [407.31250000000006, 257.3125], [405.75000000000006, 274.5]]
#p3 = [[187.00000000000006, 277.625], [190.12500000000006, 302.625], [202.62500000000006, 330.75], [219.81250000000006, 354.1875], [237.00000000000006, 368.25], [263.56250000000006, 380.75], [288.56250000000006, 388.5625], [312.00000000000006, 387.0], [351.06250000000006, 371.375], [379.18750000000006, 351.0625], [397.93750000000006, 327.625], [404.18750000000006, 305.75], [408.87500000000006, 280.75]]
#p4 = [[176.06250000000006, 280.75], [182.31250000000006, 312.0], [199.50000000000006, 346.375], [221.37500000000006, 371.375], [247.93750000000006, 387.0], [276.06250000000006, 394.8125], [318.25000000000006, 396.375], [347.93750000000006, 383.875], [379.18750000000006, 363.5625], [401.06250000000006, 337.0], [410.43750000000006, 315.125], [416.68750000000006, 280.75]]
C = [299.50000000000006, 280.75]
r1 = 280.75-162.0
r2 = 280.75-149.5
theta = 180
dtheta = 360/50.0
p1 = []
p2 = []
p3 = []
p4 = []
for theta in np.arange(180,-dtheta,-dtheta):
    pt = [C[0] + r2*cos(theta*pi/180.0),C[1] + r2*sin(theta*pi/180.0)]
    p4.append(pt)
    pt = [C[0] + r1*cos(theta*pi/180.0),C[1] + r1*sin(theta*pi/180.0)]
    p3.append(pt)
for theta in np.arange(180,360+dtheta,dtheta):
    pt = [C[0] + r1*cos(theta*pi/180.0),C[1] + r1*sin(theta*pi/180.0)]
    p2.append(pt)
    pt = [C[0] + r2*cos(theta*pi/180.0),C[1] + r2*sin(theta*pi/180.0)]
    p1.append(pt)

p5 = [[13.562500000000057, 544.8125], [585.4375, 544.8125]]

p1,p2,p3,p4,p5 = map(MapPoints,[p1,p2,p3,p4,p5])
G1,G2,G3,G4,G5 = map(PathGraph,[p1,p2,p3,p4,p5])

lens_glass_1 = p1
lens_water_1 = p2
lens_water_2 = p3
lens_glass_2 = p4
surface = p5

gr = racg.Graphics(w=600,h=600)
wn = "result"
cv2.namedWindow(wn)
cv2.setMouseCallback(wn,getxy)

black = [0,0,0]
red = [255,0,0]
blue = [0,0,255]
green = [0,255,0]

def PlotGraph(gr,G):
    for e in G['E']:
        u,v = e
        A = G['pts'][u]
        B = G['pts'][v]
        gr.Line(A,B,black)
    return

def LineCurveIntersect(pt1,pt2,poly):
    NIL = [-1,-1]
    for i in range(len(poly)-1):
        curv = poly
        pt3 = curv[i]
        pt4 = curv[i+1]
        flag,X,Y = SI(pt1[0],pt1[1],pt2[0],pt2[1],
                      pt3[0],pt3[1],pt4[0],pt4[1])
        if flag:
            C = [X,Y]
            return flag,C,pt3,pt4
    return False,NIL,NIL,NIL

def ShowRefract(pt1,pt2,n_i,n_f,G,L,display=True):
    PlotGraph(gr,G)
    poly = G['pts']
    flag,C,pt3,pt4 = LineCurveIntersect(pt1,pt2,poly)
    if not flag:
        return pt1,pt2
    if flag:
        gr.Point(C,red)
        if display:
            gr.Line(pt3,pt4,blue)
        T = np.array(pt4)-np.array(pt3)
        T = T/np.linalg.norm(T)
        T = np.array(list(T) + [0])
        v_i = np.array(C)-np.array(pt1)
        v_i = v_i/np.linalg.norm(v_i)
        v_i = np.array(list(v_i) + [0])
        v_r = -vec.refract(v_i,T,n_i,n_f)
        D = np.array(C+[0])
        E = list(D + L*v_r)[:2]
        if display:
            gr.Line(pt1,C,red)
    return C,E

def Trace(pt1,pt2):
    # The index of refraction of the cornea is 1.38, aqueous humor 1.33, lens 1.41,
    # and vitreous humor 1.34.
    n_air = 1.00027712
    n_water = 1.33
    n_glass = (1.50+1.54)/2.0
    #gr.Line(pt1,pt2,green)

    pt1,pt2 = ShowRefract(pt1,pt2,n_air,n_glass,G1,500)
    pt1,pt2 = ShowRefract(pt1,pt2,n_glass,n_water,G2,500)
    pt1,pt2 = ShowRefract(pt1,pt2,n_water,n_glass,G3,500)
    pt1,pt2 = ShowRefract(pt1,pt2,n_glass,n_air,G4,500)
    curv = G5['pts']
    flag,C,pt3,pt4 = LineCurveIntersect(pt1,pt2,curv)
    PlotGraph(gr,G5)
    gr.Line(pt1,C,red)
    gr.Point(C,red)
pt1 = [384.53645833333343, 11.718750000000114]
pt2 = [437.48437500000006, 557.48958333333337]
p6 = [pt1,pt2]
p7 = MapPoints(p6)
print "Press 'e' to exit loop"
print "Click each time with Left Mouse Button two points toward retina"
print "The first point should be in air region"
print "it will show blue intersections after the two points clicked"
while True:
    gr.Clear()
    for dx in np.arange(-500,500,45):
        A = p7[0]
        B = p7[1]
        Trace([A[0]+dx,A[1]],[B[0]+dx,B[1]])
    ch = gr.Show(wn,15)
    if ch == ord('e'):
        break
gr.Close()
