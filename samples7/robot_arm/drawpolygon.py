import SCARA as RA
from copy import deepcopy
from math import fmod,pi,sin,cos

def DrawPolygon(shape):
    pts,idxs = shape
    for i in range(len(idxs)-1,-1,-1):
        a = idxs[i]
        b = idxs[(i+1)%len(idxs)]
        if b != 0:
            pts0 = pts[a:b]
        else:
            pts0 = pts[a:]
        n0 = len(pts0)
        v = 3
        for j in range(n0/v+1):
            A = pts0[(v*j)%n0]
            B = pts0[(v*(j+1))%n0]
            gr.Line(A,B,"black")
    return
