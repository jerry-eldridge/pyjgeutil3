import cv2
import numpy as np

from math import pi,sin,cos


def PixelImage(sheet,nx,ny,gray, txt_save,
               reverse=False):
    sheet = Set(sheet, nx,ny, ' ')
    img2 = cv2.resize(gray, (nx,ny))
    shades = " ,_1>+k2SO6BW@"
    L = list(shades)
    if reverse:
        L.reverse()
    shades = ''.join(L)
    ns = len(shades)
    for j in range(ny):
        for i in range(nx):
            Y = img2[j,i]
            idx = int(round(1.0*Y*(ns-1)/255.))
            sheet[i + nx*j] = shades[idx]
    ShowImage(sheet,nx,ny)
    #SaveImage(sheet,nx,ny, txt_save)
    return

def GetImage(sheet,ni,nj):
    txt = ""
    for j in range(nj):
        s = ""
        for i in range(ni):
            c = sheet[i + ni*j]
            s = s + c
        s = s + '\n'
        txt = txt + s
    return txt

def ShowImage(sheet,ni,nj):
    txt = GetImage(sheet,ni,nj)
    print(txt,end='')
    return

def SaveImage(sheet,ni,nj,fn_save):
    txt = GetImage(sheet,ni,nj)
    print(("Saving file to fn_save=",fn_save))
    f = open(fn_save,'w')
    f.write(txt)
    f.close()
    return

def DrawCircle(sheet,ni,nj,cx,cy,radius,val):
    sheet = DrawEllipse(sheet,ni,nj,cx,cy,radius,radius,val)
    return sheet

def DrawEllipse(sheet,ni,nj,cx,cy,xr,yr,val):
    angle = 0
    dangle = 2*pi/100
    while angle < 2*pi:
        x1 = xr*cos(angle) + cx
        y1 = yr*sin(angle) + cy
        angle = angle + dangle
        x2 = xr*cos(angle) + cx
        y2 = yr*sin(angle) + cy
        angle = angle + dangle
        sheet = DrawLine(sheet,ni,nj,x1,y1, x2,y2, val)
    return sheet

def PutText(sheet, ni,nj, x,y, s):
    n = len(s)
    for i in range(n):
        sheet[(x+i)+ni*y] = s[i]
    return sheet

def Set(sheet, ni, nj, c):
    sheet = [c]*(ni*nj)
    return sheet

def DrawLine(a, N1,N2, x1,y1, x2,y2, val):
    XAXIS = 0
    YAXIS = 1
    dy = y2 - y1
    dx = x2 - x1
    if ((dy == 0) and (dx == 0)):
        i = int(round(x1))
        j = int(round(y1))
        support = (i<0) or (i>=N1) or (j<0) or (j>=N2)
        if not support:
            a[i+N1*j] = val
    rg = max(abs(dx),abs(dy))
    irg = int(round(rg))
    if (abs(dx) >= abs(dy)):
        axis = XAXIS
    else:
        axis = YAXIS
    errp = 2*dy - dx
    if dx >= 0:
        dxs = 1
    else:
        dxs = -1
    if dy >= 0:
        dys = 1
    else:
        dys = -1
    xp = int(round(x1))
    yp = int(round(y1))
    if axis == XAXIS:
        for i in range(irg):
            support = (xp<0) or (xp>=N1) or (yp<0) or \
                      (yp>=N2)
            if not support:
                a[xp+N1*yp] = val
            if errp > 0:
                yp = yp + dys
                errp = errp - 2*dx*dxs
            xp = xp + dxs
            errp = errp + 2*dy*dys
    elif axis == YAXIS:
        for i in range(irg):
            support = (xp<0) or (xp>=N1) or (yp<0) or \
                      (yp>=N2)
            if not support:
                a[xp+N1*yp] = val
            if errp > 0:
                xp = xp + dxs
                errp = errp - 2*dy*dys
            yp = yp + dys
            errp = errp + 2*dx*dxs
    return a


