import extrusion as ext
import graph as g
import affine as aff
import mapto

from math import cos,sin,pi
import numpy as np

from copy import deepcopy

def CreateCircleGeometry(doc,cx,cy,cz,r):
    doc2 = deepcopy(doc)
    doc2["pts"] = []
    n = len(doc2["V"])
    for i in range(n):
        theta = mapto.MapTo(0,0,n,2*pi,i)
        x = cx + r*cos(theta)
        y = cy + r*sin(theta)
        z = 0
        pt = [x,y,z]
        doc2["pts"].append(pt)
    return doc2

def RevolveCurve(curve,t,q,s, n=20, bcap=True,ecap=True):
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
    doc1 = CreateCircleGeometry(doc,cx,cy,cz,r0)

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

    degrees = 90
    axis = [0,1,0]
    q0 = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    q = q*q0
    C = aff.Center(path)
    pts = aff.Translate(path,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    path = pts
    #path = [[0,0,0],[10,1,0],[20,4,0],[30,9,0]]
    H = ext.Extrusion0(doc1,path,spath,bcap,ecap)
    return H

def WaterBottle0(n=30):
    # polygon curve of surface of revolution
    curve = [[103, 6], [124, 6], [140, 12],[144, 26], [144, 42], [137, 48],
        [140, 59], [152, 74], [169, 96],[183, 118], [195, 136], [200, 154],
        [199, 166], [192, 170], [197, 179],[198, 205], [198, 218], [198, 228],
        [198, 246], [200, 261], [198, 280], [196, 288], [198, 300], [198, 316],
        [198, 326], [194, 338], [194, 353],[194, 362], [187, 370], [186, 376],
        [191, 382], [194, 389], [195, 400],[192, 404], [192, 409], [196, 415],
        [197, 420], [198, 428], [198, 434],[198, 440], [194, 445], [199, 450],
        [200, 458], [200, 466], [199, 470],[199, 474], [199, 479], [202, 486],
        [202, 494], [198, 500], [201, 508], [201, 515], [202, 522], [199, 540],
        [196, 552], [191, 560], [183, 570], [171, 576], [161, 580], [137, 584],
        [124, 579]]
    x0 = curve[0][0]
    x_min = min(map(lambda pt: pt[0]-x0,curve))
    x_max = max(map(lambda pt: pt[0]-x0,curve))
    y_min = min(map(lambda pt: pt[1],curve))
    y_max = max(map(lambda pt: pt[1],curve))
    degrees = 0
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    scale = 1.
    s = [scale,scale,scale] # the same scale as previous for caps
    t = [0,0,0]
    H = RevolveCurve(curve,t,q,s, n)
    return H

def WaterBottle(n=30):
    H = WaterBottle0(n)
    pts = H['pts']
    scale = .2
    s = [scale,scale,scale] # the same scale as previous for caps
    t = [20,0,0]
    degrees = 90
    axis = [0,1,0]
    q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    C = aff.Center(pts)
    pts = aff.Translate(pts,-C[0],-C[1],-C[2],align=False)
    pts = aff.Rotate(pts,q,align=False)
    pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
    pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
    H['pts'] = pts
    return H

