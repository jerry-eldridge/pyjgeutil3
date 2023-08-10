from math import fmod,log,exp,sqrt,pi

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as si

import os

from cmath import exp as expc

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

def eta(x):
    if abs(x) < 1:
        val = exp(-1/(1-abs(x)**2))
    else:
        val = 0
    return val

def delta(x,epsilon=.1):
    val = eta(x/epsilon)/epsilon
    return val


def T_LSFT(s,F1,F2,F3,width):
    val1 = delta(s-F1,width)
    val2 = delta(s-F2,width)
    val3 = delta(s-F3,width)
    scale = 1000
    y = 1 + scale*(val1 + val2 + val3)
    return y

ms = 1e-3

sampling_rate = 44100 # bytes per second
chunk = 1024 # number of bytes to sample at a time
fft_freq = lambda i: 1.0*sampling_rate*i/chunk
dt = 1/sampling_rate # time increment

# [1] Flanagan, J. L, "Some Properties of the Glottal
# Sound Source", J. Sp. Hrng. Dis., 1, 1958, 99-116
# t is seconds and u(t) is volume flow in
# cm**3 per second. volume flow of air through
# the glottis per second from lungs to lips.
# [2] Willard R. Zemlin, "Speech and Hearing Science:
# Anatomy and Physiology", Fourth Ed., Allyn and
# Bacon, 1997, pg 295-302

# (glottal area and derived volume velocity. [1]
# Flanagan, 1958). We approximate with line segments
# below the u(t) curve. [2] We also add a modification
# so that freq0 = 124 Hz could be used or some
# other frequency but this modifies Flanagan to
# unknown interpretation.
def signal_glottis0(t,freq=124,y_low=0,y_high=700):
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

signal_glottis_audio = lambda t: signal_glottis0(t,
                            freq=200,
    y_low = -int(32768/2), # [1] 0
    y_high = int(32767/2), # [1] 700 cm**3/second
            )

signal_glottis_air = lambda t: signal_glottis0(t,
                            freq=124,
    y_low = 0, # [1] 0
    y_high = 700, # [1] 700 cm**3/second
            )
###############################################
# User: "The time-domain signal is not in a file
# and it cannot be saved until the volume is
# normalized. Write python3 code to normalize
# the audio signal of real values that are in
# a list or a numpy array."
# Bing Chat:
##"""
##import numpy as np
##def normalize_audio(audio, target_dBFS):
##    rms = np.sqrt(np.mean(np.square(audio)))
##    target_rms = 10 ** (target_dBFS / 20)
##    gain = target_rms / rms
##    normalized_audio = audio * gain
##    return normalized_audio
##audio = np.array([0.1, 0.2, -0.3, -0.1, 0.4])
##normalized_audio = normalize_audio(audio, -20)
##"""
def normalize_audio(audio, target_dBFS):
    audio2 = np.array(audio,dtype=complex)
    rms = np.sqrt(np.mean(np.abs(audio2)**2))
    P0 = 10**4
    target_rms = P0 * 10 ** (target_dBFS / 10)
    gain = target_rms / rms
    y = audio2 * gain
    y = list(y.flatten())
    return y

def create_sound(dur_secs, M1,dB0,
                 fn_save,
                 freq = 124,
                 plot = True, create=False):

    signal_glottis_audio = lambda t: \
            signal_glottis0(t,
            freq=freq,
            y_low = -int(32768/2), # [1] 0
            y_high = int(32767/2), # [1] 700 cm**3/second
            )
    
    dur = dur_secs # seconds
    nchunks = int(round(dur/(chunk*dt)))
    data = None
    for k in range(nchunks):
        t = np.arange(k*chunk*dt,(k+1)*chunk*dt,dt)
        n0 = int(chunk/2) # nyquist frequency
        f_clip = 4000
        n = Get_idx(f_clip,epsilon=50)
        n = min(n,n0)
        #print(f"n = {n}")

        # LPC
        Fs = sampling_rate # sampling frequency
        j = complex(0,1) # sqrt(-1)
        F = list(map(fft_freq, list(range(chunk))))
        def T(f):
            omega = 2*pi*f/F[-1]
            s = expc(j*omega)
            epsilon = 1e-4
            if abs(s) < epsilon:
                w = s
                return w
            a0 = 1 # signal gain G
            prod = 1
            G1 = 1
            for i in range(len(M1)):
                F_i = M1[i]
                r_i = 0.5
                omega_i = 2*pi*F_i/F[-1]
                s2 = expc(j*omega_i)
                a = 1/(1 - r_i*1/(s-s2))
                prod = prod/a
            w = G1*a0*prod
            return w
        def R(f):
            omega = 2*pi*f/F[-1]
            s = expc(j*omega)
            epsilon = 1e-4
            if abs(s) < epsilon:
                w = s
                return w
            G = 1
            RC = 1
            a0 = G*RC*s 
            prod = 1 + RC*s 
            w = a0/prod
            return w
        
        u = list(map(signal_glottis_audio,t))
        U = list(np.fft.fft(u).flatten())
        G = 1e-3
        V = list(map(lambda i: G*U[i]*T(F[i])*R(F[i]),
                    range(len(F))))
        # Um = |U|
        Vm = list(map(abs, V))
        #Ulm = log(|U|)
        Vlm = list([dB(x) for x in Vm])
        dB_max = np.max(Vlm)
        dB1 = dB0
        V2 = normalize_audio(V, dB1)
        # Um = |U|
        Vm = list(map(abs, V2))
        #Ulm = log(|U|)
        Vlm = list([dB(x) for x in Vm])
        
        v2 = list(np.fft.ifft(V2).flatten())
        v2 = list(map(lambda z:z.real,v2))
        if data is None:
            data = np.zeros((len(v2)*nchunks,2),
                dtype=np.int16)
            
        v3 = np.array(v2,dtype=np.int16)
        data[k*chunk:(k+1)*chunk,0] = v3[:chunk]
        data[k*chunk:(k+1)*chunk,1] = v3[:chunk]

    if create:
        si.wavfile.write(fn_save,sampling_rate,
            data.astype(np.int16))

    if plot:    
        plt.plot(F[1:n],Vlm[1:n],'b')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("dB")
        plt.title("Spectrogram - music")
        plt.show()
    return

flag_plot_spec = False
if flag_plot_spec:
    t = np.arange(0,chunk*dt,dt)
    u = list(map(signal_glottis_air,t))
    U = np.fft.fft(u)
    # Um = |U|
    Um = list(map(abs, U))
    #Ulm = log(|U|)
    Ulm = list([dB(x) for x in Um])
    n0 = int(chunk/2) # nyquist frequency
    f_clip = 3300
    n = Get_idx(f_clip,epsilon=50)
    n = min(n,n0)
    print(f"n = {n}")
    F = list(map(fft_freq, list(range(chunk))))
    plt.plot(F[1:n],Ulm[1:n],'b')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("dB")
    plt.title("Spectrogram - music")
    plt.show()

flag_save_wav = False
if flag_save_wav:
    t = np.arange(0,2,dt)
    u = list(map(signal_glottis_audio,t))
    U = np.fft.fft(u)
    V = U.copy()
    F1,F2,F3 = [917,1678,567]
    dt = 1/sampling_rate
    M = []
    fft_freq = lambda i: 1.0*sampling_rate*i/len(u)
    F = [fft_freq(i) for i in range(len(u))]
    for i in range(1,len(u)):
        s = F[i]
        width = 200
        val = T_LSFT(s,F1,F2,F3,width)
        M.append(val)
        V[i] = U[i]*val
    plt.plot(F[1:],M)
    plt.show()
    u2 = list(np.fft.ifft(U).flatten())
    u2 = list(map(lambda z: z.real, u2))
    data = np.zeros((len(u2),2),dtype=np.int16)
    u3 = np.array(u2,dtype=np.int16)
    data[:,0] = u3
    data[:,1] = u3
    si.wavfile.write("U.wav",sampling_rate,
            data.astype(np.int16))
    v2 = list(np.fft.ifft(V).flatten())
    v2 = list(map(lambda z:z.real,v2))
    data = np.zeros((len(v2),2),dtype=np.int16)
    v3 = np.array(v2,dtype=np.int16)
    data[:,0] = v3
    data[:,1] = v3
    si.wavfile.write("V.wav",sampling_rate,
            data.astype(np.int16))
