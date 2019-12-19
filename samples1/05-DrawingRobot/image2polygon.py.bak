import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import mapto

import cv2
import numpy as np

def im2poly(fnimage,fnpoly='polygon.txt',thlo=50,thhi=127):
    assert(fnimage[-4:]==".jpg")
    assert(fnpoly[-4:]=='.txt')
    im = cv2.imread(fnimage,0)
    gray = cv2.bitwise_not(im)
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    th = cv2.Canny(thresh1,100,200)
    connectivity = 8 # 8
    labels = cv2.connectedComponents(th, connectivity, cv2.CV_32S)
    im2, contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    area_min = 10 # square pixels
    cont = filter(lambda contour: cv2.contourArea(contour)>=area_min,contours)
    f = open(fnpoly,'w')
    PTS = []
    I = []
    j = 0
    for contour in cont:
        for i in range(len(contour)):
            pt = contour[i][0]
            PTS.append(pt)
            if i == 0:
                I.append(j)
            j += 1

        
    s = '%d\n' % len(PTS)
    f.write(s)
    for i in range(len(PTS)):
        pt = PTS[i]
        s = '%d %d\n' % (pt[0],pt[1])
        f.write(s)
    s = '%d\n' % len(I)
    f.write(s)
    for i in range(len(I)):
        j = I[i]
        s = '%d\n' % (j)
        f.write(s)
    f.close()
    return

def readpoly(fnpoly='polygon.txt'):
    f = open(fnpoly,'r')
    txt = f.read()
    f.close()

    lines = txt.split("\n")
    n = int(lines[0])
    pts = []
    k = 1
    for i in range(n):       
        pt = lines[k]
        pt = pt.split(' ')
        pt = map(int,pt)
        pts.append(pt)
        k += 1
    PTS = np.array(pts)
    xmax,ymax = np.max(PTS,axis=0)
    pts = []
    for i in range(n):
        x,y = PTS[i]
        w = h = 200
        x = mapto.MapTo(0,0,xmax,w,x)
        y = mapto.MapTo(0,h,ymax,0,y)
        pt = [x,y]
        pts.append(pt)
        
    m = int(lines[k])
    k += 1
    idxs = []
    for i in range(m):
        idx = int(lines[k])
        idxs.append(idx)
        k += 1
    shape = [pts,idxs]
    return shape


