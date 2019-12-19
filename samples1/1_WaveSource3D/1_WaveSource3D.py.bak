import mapto

import numpy as np
from math import fmod,pi,cos,sin,log

import cv2 # opencv-python

c_wave = 343. # speed of sound m/s

# https://en.wikipedia.org/wiki/Wave_equation#Spherical_waves
def u(x,k,omega,A):
     def signal(t):
         i = complex(0,1)
         r = np.linalg.norm(x)
         epsilon = 1e-6
         if abs(r) < epsilon:
             r = 1.
         U = 1.0*A/r*cos(omega*t-k*r)
         return U
     return signal

def clamp(x,lo,hi):
     val = min(hi,max(lo,x))
     return val

class WaveSource:
     def __init__(S,x,f,A=1):
         S.lam = 1.0*c_wave/f # meters
         S.omega = 2*pi*f
         S.k = S.omega/c_wave # wavenumber 3-vector
         S.A = A # amplitude real of WaveSource, say 1.0
         S.x = x # position 3-vector of WaveSource
         return
     def signal(S,x,t): # 3-vector x position to sense, real time t
         r = np.array(x) - np.array(S.x)
         U = u(r,S.k,S.omega,S.A)(t)
         val = U
         return val

def Sense(WaveSources,x): # x is 3-vector is sense position
     def signal(t): # t is real, time
         val = 0
         for sp in WaveSources:
             val += sp.signal(x,t)
         return val
     return signal

def SaveKern(fn,im):
    print "Saving file...", fn
    h,w = im.shape
    im *= w*h
    min0 = np.min(im)
    max0 = np.max(im)
    im2 = np.ones((h,w),dtype='uint8')*255
    for j in range(h):
        for i in range(w):
            val = im[j,i]
            im2[j,i] = int(mapto.MapTo(min0,0,max0,255,val))
    cv2.imwrite(fn,im2)
    return im2

w = 600
h = 600

x1 = [100,100,0]
x2 = [400,400,0]
x3 = [300,200,0]
lambda1 = 100.
lambda2 = 100.
lambda3 = 150.
f1 = 1.*c_wave/lambda1
f2 = 1.*c_wave/lambda2
f3 = 1.*c_wave/lambda3
sp1 = WaveSource(x1,f1,A=255)
sp2 = WaveSource(x2,f2,A=255)
sp3 = WaveSource(x3,f3,A=255)
WaveSources = [sp1,sp2,sp3]

t = 0
b = np.zeros((h,w),dtype=np.float)
im = np.zeros((h,w,3))
n = len(WaveSources)
I = 4.
for j in range(w):
    for i in range(h):
        x = [i,j,0]
        sig = Sense(WaveSources,x)
        val = sig(t)
        b[j,i] = clamp(val, -n*I,n*I)

SaveKern("wavesource-b.jpg",b)
im = cv2.imread("wavesource-b.jpg")

cv2.imshow("result",im)
ch = cv2.waitKey()

cv2.destroyAllWindows()


