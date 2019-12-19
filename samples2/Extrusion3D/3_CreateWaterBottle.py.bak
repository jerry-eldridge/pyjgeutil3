import extrusion as ext
import graph as g
import affine as aff
import mapto

from math import cos,sin,pi
import numpy as np

from copy import deepcopy

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

x0 = 103
poly_wb = [[103, 6], [124, 6], [140, 12], [144, 26], [144, 42], [137, 48], [140, 59], [152, 74], [169, 96], [183, 118], [195, 136], [200, 154], [199, 166], [192, 170], [197, 179], [198, 205], [198, 218], [198, 228], [198, 246], [200, 261], [198, 280], [196, 288], [198, 300], [198, 316], [198, 326], [194, 338], [194, 353], [194, 362], [187, 370], [186, 376], [191, 382], [194, 389], [195, 400], [192, 404], [192, 409], [196, 415], [197, 420], [198, 428], [198, 434], [198, 440], [194, 445], [199, 450], [200, 458], [200, 466], [199, 470], [199, 474], [199, 479], [202, 486], [202, 494], [198, 500], [201, 508], [201, 515], [202, 522], [199, 540], [196, 552], [191, 560], [183, 570], [171, 576], [161, 580], [137, 584], [124, 579]]

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

def WaterBottle():
     global poly_wb
     pts = map(lambda pt: [0,pt[1],0], poly_wb)
     y_min = min(map(lambda pt: pt[1],poly_wb))
     y_max = max(map(lambda pt: pt[1],poly_wb))
     n = 10
     doc = g.Cn(n)
     cx,cy,cz = [0,0,0]
     r = 1.
     doc1 = CreateCircleGeometry(doc,cx,cy,cz,r)

     spath = []
     path = []
     pti = poly_wb[0]
     xi,yi = pti
     yi_last = yi
     sy = 33./(y_max-y_min)
     for i in range(len(poly_wb)):
         pti = poly_wb[i]
         xi,yi = pti
         r = abs(xi - x0)
         dy = yi-yi_last
         epsilon = .1
         if abs(dy) > epsilon:
             spath.append(r)
             path.append([yi*sy,0,0])
         yi_last = yi

     C = aff.Center(path)
     degrees = 90
     axis = [0,1,0]
     q = aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
     s = [20,20,20] # the same scale as previous for caps
     t = [20,0,0]
     pts = aff.Translate(path,-C[0],-C[1],-C[2],align=False)
     pts = aff.Rotate(pts,q,align=False)
     pts = aff.Scale(pts, s[0],s[1],s[2],align=False)
     pts = aff.Translate(pts,t[0],t[1],t[2],align=False)
     path = pts
     #path = [[0,0,0],[10,1,0],[20,4,0],[30,9,0]]
     H = ext.Extrusion0(doc1,path,spath)
     return H

G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []



#H = ext.TreefoilKnot()
H = WaterBottle()
Gs = ext.Append(Gs,H)
G = ext.GraphUnionS(G,H)

ext.Graph2OBJ(BIGDATA+"WaterBottle-0.obj",G,"scene")
import os
print "Open WaterBottle.obj with 3D Viewer by double-clicking on it"
os.system(BIGDATA+"WaterBottle-0.obj")
