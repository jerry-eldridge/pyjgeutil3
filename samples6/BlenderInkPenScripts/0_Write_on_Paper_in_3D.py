import numpy as np

def PutSymbolTransform(x,y, sx,sy):
    xx = x/200.0
    yy = y/200.0
    x = xx*sx
    y = yy*sy
    return [x,y]

def PutSymbol(N1,N2,ch,x0,y0,font,sx,sy,
        color):
    x = 0
    y = 0
    pt_start = [x0,y0]
    c = ord(ch)
    fn = f"{font}/{c}.txt"
    f = open(fn,'r')
    txt = f.read()
    f.close()
    done = False
    pen_down = False
    lines = txt.split('\n')
    pts = []
    while (not done):
        command = ' '
        buff = ""
        line = lines[0].strip()
        lines = lines[1:]
        toks = line.split(' ')
        cmd = toks[0]
        if cmd == 'D':
            x,y = list(map(float,toks[1:]))
            x,y = PutSymbolTransform(x,y,sx,sy)
            x = x + pt_start[0]
            y = x + pt_start[1]
            pt = [x,y]
            last_pt = pt
            pen_down = True
        elif cmd == "M":
            x,y = list(map(float,toks[1:]))
            x,y = PutSymbolTransform(x,y,sx,sy)
            x = x + pt_start[0]
            y = x + pt_start[1]
            pt = [x,y]
            if pen_down:
                pts.append(pt)
                last_pt = pt
        elif cmd == "U":
            pen_down = False
        elif cmd == "E":
            done = True
        else:
            print(f"Error in font command")
            done = True
    return pts

# Cube that is 1 x 1 x 1

# sheet of paper (this was the transform for
# the sheet of paper created from a cube)
T = [0,0,0]
R = [0,0,0]
S = [0.850, 1.100, 0.001]

txt_paper = """
o Paper
v -0.850000 -0.001000 1.100000
v -0.850000 0.001000 1.100000
v -0.850000 -0.001000 -1.100000
v -0.850000 0.001000 -1.100000
v 0.850000 -0.001000 1.100000
v 0.850000 0.001000 1.100000
v 0.850000 -0.001000 -1.100000
v 0.850000 0.001000 -1.100000
vn -1.0000 -0.0000 -0.0000
vn -0.0000 -0.0000 -1.0000
vn 1.0000 -0.0000 -0.0000
vn -0.0000 -0.0000 1.0000
vn -0.0000 -1.0000 -0.0000
vn -0.0000 1.0000 -0.0000
vt 0.375000 0.000000
vt 0.625000 0.000000
vt 0.625000 0.250000
vt 0.375000 0.250000
vt 0.625000 0.500000
vt 0.375000 0.500000
vt 0.625000 0.750000
vt 0.375000 0.750000
vt 0.625000 1.000000
vt 0.375000 1.000000
vt 0.125000 0.500000
vt 0.125000 0.750000
vt 0.875000 0.500000
vt 0.875000 0.750000
s 0
f 1/1/1 2/2/1 4/3/1 3/4/1
f 3/4/2 4/3/2 8/5/2 7/6/2
f 7/6/3 8/5/3 6/7/3 5/8/3
f 5/8/4 6/7/4 2/9/4 1/10/4
f 3/11/5 7/6/5 5/8/5 1/12/5
f 8/5/6 4/13/6 2/14/6 6/7/6
"""

lines = txt_paper.split('\n')
pts = []
for line in lines:
    if len(line) == 0:
        continue
    toks = line.split(' ')
    if toks[0] == 'v':
        x,y,z = list(map(float,toks[1:]))
        pt = [x,y,z]
        pts.append(pt)
P = np.array(pts)

# create bounding box and we note that the sheet of paper
# has not been rotated and has a simple bounding
# box that reflects the sheet of paper better
xmin = float(np.min(P[:,0]))
xmax = float(np.max(P[:,0]))
ymin = float(np.min(P[:,1]))
ymax = float(np.max(P[:,1]))
zmin = float(np.min(P[:,2]))
zmax = float(np.max(P[:,2]))
bbox = [[xmin,xmax],[ymin,ymax],[zmin,zmax]]
print(f"bbox = {bbox}")
O = np.mean(P,axis=0)
O = list(map(float,list(O)))
print(f"O = {O}")

# These points are just some of the points P making
# up the sheet of paper. Because the sheet of paper's
# bounding box is the same as the points P:

# bottom left
A_BL = [xmin,ymin,zmax]
# bottom right
A_BR = [xmax,ymin,zmax]
# top left
A_TL = [xmin,ymax,zmax]
# top right
A_TR = [xmax,ymax,zmax]

# which also have indices idx of the points P[idx,:].

# form vector space for paper
# basis vector on x-axis
xhat = np.array(A_BR)-np.array(A_BL)
xhat = xhat/np.linalg.norm(xhat)
# basis vector on y-axis
yhat = np.array(A_TL)-np.array(A_BL)
yhat = yhat/np.linalg.norm(yhat)
# basis vector on z-axis, depth of on paper at 0
# or above paper with pen
yhat = np.array(A_TL)-np.array(A_BL)
yhat = yhat/np.linalg.norm(yhat)

# thus a coordinate of a point written on paper
# will be [x,y,z] as meaning
# pt = x*xhat + y*yhat + z*zhat
width = xmax - xmin
height = ymax - ymin
depth = zmax - zmin
# where x ranges from 0 to width-1, y ranges from
# 0 to height-1, and z ranges from 0 to depth-1.

N1 = 100
N2 = 100
ch = "L"
x0,y0 = [0,0]
font = f"./emma_font3/"
sx = width
sy = height
color = [255,0,0]
rx,ry = 1,1
pts = PutSymbol(N1,N2,ch,x0,y0,font,sx,sy,
        color)
print(pts)
