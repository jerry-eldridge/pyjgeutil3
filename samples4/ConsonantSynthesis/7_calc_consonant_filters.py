import re
import time
import os
import fnmatch
import os.path
from datetime import datetime

import numpy as np
import scipy.integrate as si
import scipy.optimize as so
import scipy.fft as sf
import scipy.signal as ss

from scipy import signal
import matplotlib.pyplot as plt

from math import fmod,log,exp,sqrt,pi

from math import fmod,log,exp,sqrt,pi

def Date(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def Seconds(year,month,day):
     sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
     return sec


def ListFiles(folder,pattern):
    L = []
    for root, dire, files in os.walk(folder):
        for fn in fnmatch.filter(files, pattern):
            try:
                root = root.replace('\\','/')
                fn = fn.replace('\\','/')
                filename = root + '/' + fn
                L.append(filename)
            except:
                continue
    return L

def load2(fn):
    f = open(fn, 'r')
    txt = f.read()
    f.close()
    lines = txt.split('\n')
    lines = lines[1:]
    L = []
    for line in lines:
        if len(line) == 0:
            continue
        toks = line.split('\t')
        if len(toks) != 2:
            continue
        v_freq = float(toks[0])
        v_db = float(toks[1])
        tup = (v_freq,v_db)
        L.append(tup)
    return L

def Integral0(f,a,b,dx):
     if a > b:
          return -Integral(f,b,a,dx)
     x = a
     s = 0
     while x < b:
         s += f(x)*dx
         x += dx
     return s

#Integral = lambda f,a,b: si.quad(f,a,b)[0]
Integral = lambda f,a,b: Integral0(f,a,b,dx=10)

def inner(a,b):
    def F(f,g):
        h = lambda x: f(x)*g(x)
        val = Integral(h,a,b)
        return val
    return F

def norm(a,b):
    def F(f):
        val = inner(a,b)(f,f)
        return sqrt(val)
    return F

def distance(a,b):
    def F(f,g):
        h = lambda x: abs(f(x) - g(x))
        return norm(a,b)(h)
    return F

# model the glottis signal x.
chunk = 512
sampling_rate = 8000
dt = 1/sampling_rate
t = np.arange(0, dt*chunk, dt)
fft_freq = lambda i: 1.0*sampling_rate*i/chunk

# [`] Flanagan, J. L, "Some Properties of the Glottal
# Sound Source", J. Sp. Hrng. Dis., 1, 1958, 99-116
# t is seconds and u(t) is volume flow in
# cm**3 per second. volume flow of air through
# the glottis per second from lungs to lips.

# [2] Willard R. Zemlin, "Speech and Hearing Science:
# Anatomy and Physiology", Fourth Ed., Allyn and
# Bacon, 1997, pg 295-302

# [3] Ray D. Kent, Charles Read, "The Acoustic Analysis of Speech",
#Singular Publishing Group, Inc, 1992

# [4] Alan V. Oppenheim, Ronald W. Schafer, "Discrete-Time Signal
#Processing", Prentice-Hall, 1989

# (glottal area and derived volume velocity. [`]
# Flanagan, 1958). We approximate with line segments
# below the u(t) curve. [1] We also add a modification
# so that freq0 = 124 Hz could be used or some
# other frequency but this modifies Flanagan to
# unknown interpretation.
def signal_glottis0(t,freq=124,y_low=0,y_high=700):
    ms = 1e-3
    period = 1/freq
    x1 = 0*ms # second
    y1 = y_low # cm**3/second
    x2 = (3/8.0)*period # second
    y2 = y_high #cm**3/second
    x3 = (6.5/8.0)*period # second
    y3 = y_low # cm**3/second
    x4 = period # second
    y4 = y_low # cm**3/second
    t = fmod(t,x4)
    if 0 <= t < x2:
        y = MapTo(x1,y1,x2,y2,t)
    elif x2 <= t < x3:
        y = MapTo(x2,y2,x3,y3,t)
    elif x3 <= t < x4:
        y = MapTo(x3,y3,x4,y4,t)
    else:
        y = 0
    return y
signal_glottis_air = lambda t: signal_glottis0(t,
                            freq=124,
    y_low = 0, # [1] 0
    y_high = 700, # [1] 700 cm**3/second
            )
signal_glottis_air = np.vectorize(signal_glottis_air)

# two-point form of line
#
# With x1 -> y1 and x2 -> y2, given x, return y using linear map
def MapTo(x1, y1, x2, y2, x):
    epsilon = 0.0001
    if abs(x2 - x1) > epsilon:
        m = 1.*(y2-y1)/(x2-x1)
    else:
        m = 1
    y = m*(x-x1)+y1
    return y

# https://en.wikipedia.org/wiki/Decibel
def dB(P,P0=1e5):
    eps = 1e-5
    val = 10*log((P+eps)/(P0+eps))/log(10)
    return val

def Get_idx(freq,epsilon):
    for k in range(chunk):
        if abs(fft_freq(k) - freq) < epsilon:
            break
    return k

def Find_Filter(fn,typ = "bandpass"):
     # speech of "J" consonant
     L = load2(fn)
     xp = list(map(lambda tup: tup[0], L))
     fp = list(map(lambda tup: tup[1], L))
     f2 = lambda x: np.interp(x, xp, fp)

     # model the glottis signal x
     freq_i = 124 # Hz (obtained from above)
     x = lambda freq=124: lambda t: signal_glottis0(t,
                         freq,
                         y_low = 0, # [1] 0
                         y_high = 700, # [1] 700 cm**3/second
                         )
     x2 = lambda freq: np.vectorize(x(freq))
     chunk = 512
     sampling_rate = 4000
     fft_freq = lambda i: 1.0*sampling_rate*i/chunk
     dt = 1/sampling_rate
     t = np.arange(0, dt*chunk, dt)
     xx = x2(freq_i)(t)
     # glottis signal
     X = sf.fft(xx)

     # User to Bing Chat: write python3 code to
     # implement a band-pass filter to pass signal
     # through frequency interval freq = 100 to
     # freq = 400. Show frequencies 0 to 1000.
     # Use scipy.signal .

     ##from scipy import signal
     ##import matplotlib.pyplot as plt
     ##import numpy as np
     ##
     ### Define the sampling frequency
     ##fs = 1000
     ##
     ### Define the frequency interval
     ##freq = [100, 400]
     ##
     ### Design the filter
     ##b, a = signal.butter(4, freq, btype='bandpass', fs=fs)
     ##
     ### Plot the frequency response
     ##w, h = signal.freqz(b, a)
     ##plt.plot(w * fs / (2 * np.pi), 20 * np.log10(abs(h)))
     ##plt.xlim([0, 1000])
     ##plt.title('Band-pass Filter Frequency Response')
     ##plt.xlabel('Frequency [Hz]')
     ##plt.ylabel('Amplitude [dB]')
     ##plt.grid()
     ##plt.show()

     def func(A):
         aa = A[0]
         bb = A[1]
         aa2 = max(1,min(aa,bb))
         bb2 = min(sampling_rate/2.-1,max(aa,bb))
         freq = [aa2,bb2]
         A1 = freq
         num1, den1 = signal.butter(4, A1,
                    btype=typ,
                    fs=sampling_rate)

         w1,H1 = ss.freqz(num1,den1) # bandpass
         
         Y = H1 * X
         Xm = list(map(abs, Y))
         Xlm = list([dB(x) for x in Xm])
         
         freq1 = [fft_freq(i) for i in range(len(Xlm))]
         n0 = 2
         g = lambda x: np.interp(x, freq1[n0:], Xlm[n0:])

         val = distance(43,4000)(f2,g)
         A = A1
         #print(f"A = {A}, val = {val}")
         return val

     A_opt = so.fmin(func, [1,sampling_rate/2-1,
                            1,sampling_rate/2-1],
                     disp=0,
                     xtol = 0.1,
                     ftol=5.0)
     #print(A_opt)
     #print(func(A_opt))

     # Define the transfer function
     A = A_opt
     aa = A[0]
     bb = A[1]
     aa2 = max(1,min(aa,bb))
     bb2 = min(sampling_rate/2.0-1,max(aa,bb))
     freq = [aa2,bb2]
     A1 = [aa2,bb2,typ]
     return A1

def Calc_Filter(k,A1, col='r',label=''):
     A1 = freq
     num1, den1 = signal.butter(4, A1,
               btype='bandpass',
               fs=sampling_rate)

     print()
     print("="*30)
     print(f"BandPass: num1 = {list(num1.flatten())},"+\
           f" den1 = {list(den1.flatten())}")
     print("="*30)
     print()
     w,H1 = ss.freqz(num1,den1) # bandpass
     Y = H1 * X
     Ym = list(map(abs, Y))
     Ylm = np.array(list([dB(x) for x in Ym]))
     f = np.array([fft_freq(i) for i in range(len(X))])
     plt.plot(f, Ylm + k,col,label=label)
     return

root = "./JGE"
L = ListFiles(root, pattern="*.txt")
L.sort(key=lambda tup: tup[0])

for fn in L:
    #A = Find_Filter(fn,typ="bandpass")
    A = Find_Filter(fn,typ="bandstop")
    aa,bb,t = A
    s = f"\"{fn}\",{aa},{bb},\"{t}\""
    print(s)


    
