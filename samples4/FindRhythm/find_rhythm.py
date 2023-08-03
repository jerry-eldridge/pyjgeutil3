import scipy.io as si
import numpy as np
from fractions import Fraction as QQ

music_fraction = {}
def reduce_fraction(n,epsilon=1e-1):
    K = list(music_fraction.keys())
    if n in K:
        return music_fraction[n]
    a = n
    def C(a,b):
        L = []
        while b!= 0:
            q = int(a / b)
            r = a % b
            a = b
            b = r
            L.append(q)
        return L
    q = QQ.from_float(a)
    #print(f"q = {q}")
    L = C(q.numerator, q.denominator)
    #print(f"L = {L}")
    def f(L,idx):
        if idx <= 0:
            return QQ(L[0],1)
        elif idx == 1:
            return f(L,0) + QQ(1,L[1])
        elif idx == 2:
            return f(L,0) + QQ(1,L[idx-1]+L[idx])
        else:
            return f(L,0) + QQ(1,f(L,idx-1))
    for i in range(len(L)):
        q2 = f(L,i)
        #print(f"q2 = {q2}")
        done = abs(q2.numerator/q2.denominator \
                - n) < epsilon or \
               L[i] > 100
        
        if done:
            if L[i] > 100:
                music_fraction[n] = f(L,i-1)
            else:
                music_fraction[n] = q2
            break
    return q2

def segment_audio(fn_wav,chunk=1024,
                avg_threshold=1000):
    # read .wave file
    sampling_rate,data = si.wavfile.read(fn_wav)
    # segment audio into note durations
    sh = data.shape
    dt = 1/sampling_rate
    D = []
    T = []
    digits = 1000.0
    secs_fin = int(sh[0]*dt*digits)/digits
    for i in range(0,sh[0],chunk):
        secs = int(i*dt*digits)/digits
        avg = np.mean(np.abs(data[i:i+chunk,0]))
        if avg > avg_threshold:
            tup = (secs,1,avg)
            T.append(1)
        else:
            tup = (secs,0,avg)
            T.append(0)
        D.append(tup)
    F = np.array([1,-1])
    T = np.array(T)
    T2 = np.convolve(T,F)
    T2 = list(T2)[:len(T)]
    T2 = list(map(abs, T2))
    I = list(filter(lambda i: T2[i]!=0, range(len(T2))))
    J = list(filter(lambda i: D[i][1]==1, range(len(D))))
    K = list(set(I)&set(J))
    D2 = [D[i] for i in K]
    D2.sort(key=lambda tup: tup[0])
    D3 = [0] + [tup[0] for tup in D2] + [secs_fin]
    return D3

def find_rhythm(fn_wav, beat=4, quanta=8,
                chunk=1024,
                avg_threshold=1000,
                flag_reciprocal=True):
    digits = 1000.0
    D3 = segment_audio(fn_wav,chunk,avg_threshold)
    D4 = [D3[i+1] - D3[i] for i in range(len(D3)-1)]
    # find rhythm S
    smin = np.mean(D4)
    if abs(smin) > 1e-8:
        S = [val/smin for val in D4]
    else:
        S = D4
    # quantize S
    epsilon = 1e-1
    S = [reduce_fraction(val*quanta/beat,\
            epsilon) for val in S]
    H = lambda q: int(q.numerator/\
                q.denominator)/quanta
    S2 = [H(q)*beat for q in S]
    S3 = [x for x in S2 if abs(x) > 0]
    if flag_reciprocal:
        S4 = np.array([1/x for x in S3])
        tmin = np.min(S4)
        S4 = list(S4/tmin)
        S4 = [int(round(digits*x))/digits for x in S4]
        S3 = S4
    # create rhythm string
    r = ' '.join(list(map(str,S3)))
    return r
