import scipy.fftpack as scf
from math import sqrt,cos

clamp = lambda x,lo,hi: max(lo,min(hi,x))

R = lambda x: eval(x)

f1 = lambda x: int(round(x))
F1 = lambda y: list(map(f1,y))

f2 = lambda x: int(round(x))
F2 = lambda y: list(map(f2,y))

g1 = lambda x: clamp(int(round(x)),0,255)
G1 = lambda y: list(map(g1,y))

g2 = lambda x: clamp(int(round(x)),0,255)
G2 = lambda y: list(map(g2,y))

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

def IDCT1(x):
    N = len(list(x))
    sqrt = lambda x: mymath.sqrt_m(x,N=4)
    cos = lambda x: mymath.cos_m(x,N=18)
    
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
    L2 = G1(L)
    return L2

def IDCT2(x):
    N = len(list(x))
    A = 1/sqrt(N)
    L = A*scf.dct(x,type=3,n=N,norm=None)
    L2 = G2(L)
    return L2

IDCT = IDCT2



