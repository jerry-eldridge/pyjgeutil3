import numpy as np

from math import log

fft_freq = lambda chunk,sampling_rate: lambda i:\
           1.0*sampling_rate*i/chunk
def FFT(x):
    return np.fft.fft(x)
def IFFT(x):
    return np.fft.ifft(x)

def Get_idx(chunk,sampling_rate):
    def f(freq,epsilon):
        for k in range(chunk):
            val = fft_freq(chunk,sampling_rate)(k)
            if abs(val - freq) < epsilon:
                break
        return k
    return f

# https://en.wikipedia.org/wiki/Decibel
def dB(P,P0=1e5):
    eps = 1e-5
    val = 10*log((P+eps)/(P0+eps))/log(10)
    return val

def sample(x,j,chunk):
    a = j*chunk
    b = (j+1)*chunk
    n = len(x)
    a = min(a,n)
    b = min(b,n)
    y = x[a:b]
    return y

