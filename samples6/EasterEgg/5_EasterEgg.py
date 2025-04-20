import math
import cv2
import numba.cuda as cuda
import numpy as np
import warnings
import time

from math import fmod,sin,cos,pi


warnings.simplefilter("ignore")

@cuda.jit
def bgr_to_hsv_jit(dx,dy):
    i,j = cuda.grid(2)
    if i < dx.shape[0] and j < dx.shape[1]:
        B = dx[i,j,0]
        G = dx[i,j,1]
        R = dx[i,j,2]
        Rp = R/255
        Gp = G/255
        Bp = B/255
        cmax = max(Rp,Gp,Bp)
        cmin = min(Rp,Gp,Bp)
        delta = cmax - cmin
        if delta == 0:
            H = 0
        elif cmax == Rp:
            H = 60 * math.fmod((Gp-Bp)/delta,6)
        elif cmax == Gp:
            H = 60 * ((Bp-Rp)/delta + 2)
        elif cmax == Bp:
            H = 60 * ((Rp-Gp)/delta + 4)
        if cmax == 0:
            S = 0
        else:
            S =delta/cmax
        V = cmax
        dy[i,j,0] = np.uint16(H)
        dy[i,j,1] = np.uint16(100*S)
        dy[i,j,2] = np.uint16(100*V)
    return

@cuda.jit
def hsv_to_bgr_jit(dx,dy):
    i,j = cuda.grid(2)
    if i < dx.shape[0] and j < dx.shape[1]:
        H = dx[i,j,0]
        S = dx[i,j,1]/100
        V = dx[i,j,2]/100
        Sp = S
        Vp = V
        C = Vp * Sp # chroma
        X = C * (1 - abs(math.fmod(H/60,2)-1))
        m = Vp - C
        if 0 <= H and H < 60:
            Rp = C
            Gp = X
            Bp = 0
        elif 60 <= H and H < 120:
            Rp = X
            Gp = C
            Bp = 0
        elif 120 <= H and H < 180:
            Rp = 0
            Gp = C
            Bp = X
        elif 180 <= H and H < 240:
            Rp = 0
            Gp = X
            Bp = C
        elif 240 <= H and H < 300:
            Rp = X
            Gp = 0
            Bp = C
        elif 300 <= H and H < 360:
            Rp = C
            Gp = 0
            Bp = X
        R = int((Rp + m)*255)
        G = int((Gp + m)*255)
        B = int((Bp + m)*255)
        dy[i,j,0] = B
        dy[i,j,1] = G
        dy[i,j,2] = R
    return

@cuda.jit
def replace_color_jit(dx,x1,x2,y1,y2):
    i,j = cuda.grid(2)
    if i < dx.shape[0] and j < dx.shape[1]:
        H = dx[i,j][0]
        if ( x1 <= H and H <= x2 ):
            m = 1.0*(y2-y1)/(x2-x1)
            H2 = m*(H-x1) + y1
            H2 = math.fmod(H2,360)
            H2 = np.uint16(H2)
        else:
            H2 = H
        dx[i,j][0] = H2
    return

def bgr_to_hsv(x):
    dx = cuda.to_device(x) # copy to GPU from CPU
    dy = cuda.to_device(np.zeros(dx.shape,dtype=np.uint16))
    bgr_to_hsv_jit[blockspergrid,threadsperblock](dx,dy)
    z = dy.copy_to_host()
    return z

def hsv_to_bgr(x): 
    dx = cuda.to_device(x) # copy to GPU from CPU
    dy = cuda.to_device(np.zeros(dx.shape,dtype=np.uint8))
    hsv_to_bgr_jit[blockspergrid,threadsperblock](dx,dy)
    z = dy.copy_to_host()
    return z

def replace_color(x, x1,x2,y1,y2):
    dx = cuda.to_device(x) # copy to GPU from CPU
    replace_color_jit[blockspergrid,threadsperblock](\
        dx,x1,x2,y1,y2)
    y = dx.copy_to_host()
    return y   
    

# Hues: Red around 0 or 360, Orange around 30,
# Yellow around 60, Green around 120, Cyan around 180,
# Blue around 250, Violet/Indigo around 270, with
# S,V both around 100 in range[0,100].
def blue_to_orange(im):
    z1 = bgr_to_hsv(im)
    x1 = 195 # blue
    x2 = 305
    y1 = 27 # orange
    y2 = 34
    z2 = replace_color(z1, x1,x2,y1,y2) # H in [0,360], blue
    im2 = hsv_to_bgr(z2)
    return im2

def blue_to_yellow(im):
    z1 = bgr_to_hsv(im)
    x1 = 205 # blue
    x2 = 295
    y1 = 50 # yellow
    y2 = 75
    z2 = replace_color(z1, x1,x2,y1,y2) # H in [0,360], red
    im2 = hsv_to_bgr(z2)
    return im2

def green_to_yellow(im):
    z1 = bgr_to_hsv(im)
    x1 = 70 # green
    x2 = 170
    y1 = 50 # yellow 
    y2 = 75
    z2 = replace_color(z1, x1,x2,y1,y2) # H in [0,360], green
    im2 = hsv_to_bgr(z2)
    return im2

def green_to_red(im):
    z1 = bgr_to_hsv(im)
    x1 = 70 # green
    x2 = 170
    y1 = -20 # red 
    y2 = 20
    z2 = replace_color(z1, x1,x2,y1,y2) # H in [0,360], green
    im2 = hsv_to_bgr(z2)
    return im2

print("Press 'e' to exit")
cv2.namedWindow("result")
fn_read = f"./easter_eggs_02.jpg"
im0 = cv2.imread(fn_read,1)
flag = False
t = 0
dt = .01

fps = 30
dt = 1/fps
h,w,c = im0.shape

n_images = 0

sz = (w,h) # scale down the images to sz
fn_video = "./easter-video.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video = cv2.VideoWriter(fn_video,
            fourcc, fps, sz)
duration = n_images / fps

while True:
    t = fmod(t,1)
    try:
        image = im0.copy()
        im = np.zeros((image.shape[0], \
                       image.shape[1], 3), np.uint8)
        im = image
        if flag is False:
            flag = True
            im0 = im.copy()
            threadsperblock = (16, 16)
            blockspergrid_w = math.ceil(\
                im.shape[0] / threadsperblock[0])
            blockspergrid_h = math.ceil(\
                im.shape[1] / threadsperblock[1])
            blockspergrid = (blockspergrid_w, blockspergrid_h)
    except:
        continue
    h,w,c = im.shape

    z1 = bgr_to_hsv(im)
    x1 = -20 # white
    x2 = 20
    y1 = 90 + 180*sin(2*pi*t/5) 
    y2 = 100 + 180*sin(2*pi*t/5) 
    z2 = replace_color(z1, x1,x2,y1,y2) # H in [0,360], green
    im1 = hsv_to_bgr(z2)
    
    n = int(time.time()*1000)
    cv2.imshow("result",im1)
    video.write(im1)
    ch = cv2.waitKey(15)
    if ch == ord('e'): # exit
        break
    if ch == ord('s'):
        fn_save = f"snapshot-12350-{n:05d}.jpg"
        print(f"Saving snaphot... fn_save = {fn_save}")
        cv2.imwrite(fn_save,im1)

    t = t + dt
    n_images = n_images + 1
    if n_images > 30*15:
        break

video.release()        
cv2.destroyWindow("result")


