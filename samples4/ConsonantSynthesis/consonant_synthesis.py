import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import scipy.fft as sf
import scipy.io as si

from math import fmod,log,exp,sqrt,pi

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

signal_glottis_air = lambda t: signal_glottis0(t,
                            freq=124,
    y_low = 0, # [1] 0
    y_high = 700, # [1] 700 cm**3/second
            )
signal_glottis_air = np.vectorize(signal_glottis_air)
signal_glottis_audio = lambda t: signal_glottis0(t,
                            freq=124,
    y_low = -int(32768/2), # [1] 0
    y_high = int(32767/2), # [1] 700 cm**3/second
            )
signal_glottis_audio = np.vectorize(signal_glottis_audio)

root = r"./JGE/"
fn_phoneme = lambda c: root + f"spectrum_JGE_{c}.txt"

def load(c):
    fn = fn_phoneme(c)
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

th = 0.25 # dB difference

def positive(f):
    def h(x):
        val = max(0,f(x))
        if val > th:
            val = th
        else:
            val = 0
        return val
    return h
def negative(f):
    def h(x):
        val = max(0,-f(x))
        if val > th:
            val = th
        else:
            val = 0
        return val
    return h

def find_filter(f,g):
    h = lambda x: f(x) - g(x)
    hp = positive(h)
    hn = negative(h)

    secs_fin = 4000
    X = np.arange(0,secs_fin,1)
    Y0 = list(map(lambda x: hp(x) - hn(x), X))
    Y1 = list(map(hp, X))
    Y2 = list(map(hn, X))

    D = [(i,Y0[i]) for i in range(len(X))]
    F = np.array([1,-1])
    T = np.array(Y0)
    T2 = np.convolve(T,F)
    T2 = list(T2)[:len(T)]
    T2 = list(map(abs, T2))
    I = list(filter(lambda i: T2[i]!=0, range(len(T2))))
    K = list(set(I))
    D2 = [D[i] for i in K]
    D2.sort(key=lambda tup: tup[0])
    D3 = [0] + [tup[0] for tup in D2] + [secs_fin]
    #print(D3)

    H = []

    sampling_rate = 4000*2

    for i in range(len(D3)-1):
        aa = D3[i]
        bb = D3[i+1]
        if abs(aa-bb) < 1:
            continue
        z = 0.5*(aa+bb)
        aa = max(1,aa)
        bb = min(sampling_rate/2.0-1, bb)
        #print(f"aa = {aa}")
        #print(f"bb = {bb}")
        val = hp(z) - hn(z)
        if val >= th: # bandpass
            freq = [aa,bb]
            A1 = freq
            num1, den1 = ss.butter(4, A1,
                    btype='bandpass',
                    fs=sampling_rate)
            H.append((num1,den1,aa,bb,"bandpass"))
        elif val <= -th: # bandstop
            freq = [aa,bb]
            A1 = freq
            num1, den1 = ss.butter(4, A1,
                    btype='bandstop',
                    fs=sampling_rate)
            H.append((num1,den1,aa,bb,"bandstop"))
    return H

def create_consonant(c,verbose=True):
    L1 = load(c)
    xp1 = list(map(lambda tup: tup[0], L1))
    fp0 = list(map(lambda tup: tup[1], L1))
    fp1 = list(ss.savgol_filter(fp0, 5, 2))
    f1 = lambda x: np.interp(x, xp1, fp1)

    x = lambda t: signal_glottis_audio(t)
    x2 = lambda freq: np.vectorize(x)

    # model the glottis signal x.
    freq_i = 124
    chunk = 512
    sampling_rate = 8000
    fft_freq = lambda i: 1.0*sampling_rate*i/chunk
    dt = 1/sampling_rate
    t = np.arange(0, dt*chunk, dt)
    X = sf.fft(x2(freq_i)(t))
    Xm = list(map(abs, X))
    Xlm = list([dB(x) for x in Xm])
    freq1 = [fft_freq(i) for i in range(len(Xlm))]
    g = lambda x: np.interp(x, freq1, Xlm)

    L = find_filter(g,f1)
    if verbose:
        for i in range(len(L)-1):
            print(f"i = {i}, "+\
                  f"(a,b) = {(L[i][2],L[i][3])},\n"+\
                  f" num1 = {list(L[i][0])}\n"+\
                  f" den1 = {list(L[i][1])}\n")
        
    H1 = 0
    H2 = 0
    for i in range(len(L)):
        t = L[i][4]
        if t == 'bandpass':
            num1,den1 = L[i][:2]
            w1,H_i = ss.freqz(num1,den1)
            H1 = H1 + H_i
        if t == 'bandstop':
            num1,den1 = L[i][:2]
            w1,H_i = ss.freqz(num1,den1)
            H2 = H2 + H_i
    H = (H1+H2)/len(L)
    return H,X


def create_consonant_bp_bs(dur,bp,bs,
            verbose=True):
    x = lambda t: signal_glottis_audio(t)
    x2 = lambda freq: np.vectorize(x)

    # model the glottis signal x.
    freq_i = 124
    chunk = 512
    sampling_rate = 8000
    fft_freq = lambda i: 1.0*sampling_rate*i/chunk
    dt = 1/sampling_rate
    t = np.arange(0, dur, dt)
    X = sf.fft(x2(freq_i)(t))
    Xm = list(map(abs, X))
    Xlm = list([dB(x) for x in Xm])
    freq1 = [fft_freq(i) for i in range(len(Xlm))]
    g = lambda x: np.interp(x, freq1, Xlm)

    n = len(X)        

    H = []
    freq = bp
    A1 = freq
    num1, den1 = ss.butter(4, A1,
                    btype='bandpass',
                    fs=sampling_rate)
    H.append((num1,den1,*freq,"bandpass"))
    freq = bs
    A1 = freq
    num1, den1 = ss.butter(4, A1,
                    btype='bandstop',
                    fs=sampling_rate)
    H.append((num1,den1,*freq,"bandstop"))
    L = H
    H1 = 0
    H2 = 0
    for i in range(len(L)):
        t = L[i][4]
        if t == 'bandpass':
            num1,den1 = L[i][:2]
            w1,H_i = ss.freqz(num1,den1,worN=n)
            H1 = H1 + H_i
        if t == 'bandstop':
            num1,den1 = L[i][:2]
            w1,H_i = ss.freqz(num1,den1,worN=n)
            H2 = H2 + H_i
    H = (H1+H2)/len(L)
    return H,X

def Plot_XY(v,X,Y,label0,show_glottis=False):
    y = sf.ifft(Y) # audio signal
    freqs = sf.fftfreq(len(X),t[1]-t[0])
    n = int(len(freqs)/2)
    P0 = 1e5
    if show_glottis:
        plt.plot(freqs[freqs >= 0],
             20 * np.log10((1+np.abs(X[freqs >= 0]))/P0),
             label='glottis')
    plt.plot(freqs[:n],
             v+20 * np.log10((1+np.abs(Y[freqs >= 0]))/P0),
             label=label0)
    return
