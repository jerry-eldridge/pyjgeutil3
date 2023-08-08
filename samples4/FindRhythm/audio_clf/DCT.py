import scipy.fftpack as scf
from math import sqrt,cos

# use FFT freq for DCT
fft_freq = lambda chunk,sampling_rate: lambda i:\
           1.0*sampling_rate*i/chunk

clamp = lambda x,lo,hi: max(lo,min(hi,x))

R = lambda x: eval(str(x))

f1 = lambda x: int(round(x))
F1 = lambda y: list(map(f1,y))

f2 = lambda x: int(round(x))
F2 = lambda y: list(map(f2,y))

# clamp audio amplitude to [-Vol,Vol] in integer
# np.int16 integer signal. The range for audio
# not [0,255]. To reflect this the functions
# G1,G2 are suffixed with 'a' for 'audio' as G1a,G2a.
Vol = 3e4
g1a = lambda x: clamp(int(round(x)),-Vol,Vol)
G1a = lambda y: list(map(g1a,y))

g2a = lambda x: clamp(int(round(x)),-Vol,Vol)
G2a = lambda y: list(map(g2a,y))

# https://en.wikipedia.org/wiki/Discrete_cosine_transform
def DCT1(x,n=0):
    N = len(list(x))
    
    A = R(1)/sqrt(R(N))
    pi = R("3.14159")
    B = pi/R(N)
    C = B*R(0.5)

    def SEQ1(k):
        M =  list(map(lambda j: A*R(x[j])*\
                cos((B*R(j)+C)*R(k)),
                range(N)))
        s = R(0)
        for i in range(len(M)):
            v = M[i]
            s = s + v
        val = s
        return val
    L = list(map(SEQ1, range(n)))
    L2 = F1(L)
    return L2

def DCT2(x,n=0):
    N = len(list(x))
    A = 1/sqrt(N)
    L = A*0.5*scf.dct(x,type=2,n=N,norm=None)
    L = list(L)
    L2 = L[:n]
    L3 = F2(L2)
    return L3

DCT = DCT2

def IDCT1F(x):
    N = len(list(x))
    #sqrt = lambda x: mymath.sqrt_m(x,N=4)
    #cos = lambda x: mymath.cos_m(x,N=18)
    
    A = R(2)/sqrt(R(N))
    pi = R("3.14159")
    B = pi/R(N)
    C = B*R(0.5)
    D = A*R(0.5)

    def SEQ1(k):
        M =  list(map(lambda m: A*R(x[m])*\
                cos((B*R(k)+C)*R(m)),
                range(1,N)))
        s = D*R(x[0])
        for i in range(len(M)):
            v = M[i]
            s = s + v
        val = s
        return val
    L = list(map(SEQ1, range(N)))
    L2 = G1a(L)
    return L2

def IDCT2F(x):
    N = len(list(x))
    A = 1/sqrt(N)
    L = A*scf.dct(x,type=3,n=N,norm=None)
    L2 = G2a(L)
    return L2

IDCT = IDCT2F

