# 6/12/2015 added color support for Plot to display lines with an optional color
import cv2
from numpy import array,zeros,ones
from vectors import lerp

vertex_r = 8
_id_undef = 1

def PlotVertex(im1,pt,doc,i):
    try:
        color = doc["colors"][i]
    except:
        color = (0,0,255)
    cv2.circle(im1,(pt[0],pt[1]),vertex_r,(color[2],color[1],color[0]),-1)
    try:
        s = doc["labels"][i]
    except:
        s = str(i)
    cv2.putText(im1, s, (pt[0]+vertex_r,pt[1]+vertex_r), cv2.FONT_HERSHEY_SIMPLEX, vertex_r/15.0, (0,0,0),2)
    return im1

def Show(wn,im1,ms):
    cv2.imshow(wn,im1)
    ch = cv2.waitKey(ms)
    return ch
def End():
    cv2.destroyAllWindows()
    return
def Plot(im1,doc,color=(0,0,0),digraph=False):
    global vertex_r
    old_vertex_r = vertex_r
    try:
        printplain = doc['printplain']
    except:
        printplain = False
    if printplain:
        doc['labels'] = ['']*len(doc['V']) 
        vertex_r = 1

    V = doc['V']
    E = doc['E']
    pts = doc['pts']
    try:
        _id = doc['_id']
    except:
        _id = _id_undef
    s = "Graph: %d" % _id
    cv2.putText(im1, s, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,20,0))
    n = len(V)
    i = 0
    R,G,B = color
    for S in E:
        k = len(S)
        if k == 2:
            idxs = S
            pt1 = pts[idxs[0]]
            pt2 = pts[idxs[1]]
            cv2.line(im1, (pt1[0],pt1[1]), (pt2[0],pt2[1]), (B,G,R), 2)

            if digraph:
                pt = map(int,lerp(pt1,pt2,0.9))
                cv2.circle(im1,(pt[0],pt[1]),6,(0,0,0),-1)

            pt3 = map(int,map(round,(lerp(pt1,pt2,0.4))))
            try:
                if i < len(doc["Enames"]):
                    s = doc["Enames"][i]
                else:
                    s = ""
                cv2.putText(im1, s, (pt3[0]+4,pt3[1]+4), cv2.FONT_HERSHEY_SIMPLEX, vertex_r/15.0, (100,20,255),2)
            except:
                ii = 0
        i += 1 #indent2
    i = 0 #indent1
    for pt in pts:
        pt = map(int,pt)
        im1=PlotVertex(im1,pt,doc,i)
        i += 1
    vertex_r = old_vertex_r
    return im1

def PlotDigraph(im1,doc,color=(0,0,0)):
    global vertex_r
    old_vertex_r = vertex_r
    try:
        printplain = doc['printplain']
    except:
        printplain = False
    if printplain:
        doc['labels'] = ['']*len(doc['V']) 
        vertex_r = 1

    V = doc['V']
    E = doc['E']
    pts = doc['pts']
    try:
        _id = doc['_id']
    except:
        _id = _id_undef
    s = "Graph: %d" % _id
    cv2.putText(im1, s, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,20,0))
    n = len(V)
    i = 0
    R,G,B = color
    for S in E:
        k = len(S)
        if k == 2:
            idxs = S
            pt1 = pts[idxs[0]]
            pt2 = pts[idxs[1]]
            pt = map(int,lerp(pt1,pt2,0.9))
            cv2.line(im1, (pt1[0],pt1[1]), (pt2[0],pt2[1]), (B,G,R), 2)
            cv2.circle(im1,(pt[0],pt[1]),6,(0,0,0),-1)
            pt3 = map(int,map(round,(lerp(pt1,pt2,0.4))))
            try:
                if i < len(doc["Enames"]):
                    s = doc["Enames"][i]
                else:
                    s = ""
                cv2.putText(im1, s, (pt3[0]+4,pt3[1]+4), cv2.FONT_HERSHEY_SIMPLEX, vertex_r/15.0, (100,20,255),2)
            except:
                ii = 0
        i += 1 #indent2
    i = 0 #indent1
    for pt in pts:
        pt = map(int,pt)
        im1=PlotVertex(im1,pt,doc,i)
        i += 1
    vertex_r = old_vertex_r
    return im1
