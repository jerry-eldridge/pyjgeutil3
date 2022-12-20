import scipy.io as si
import numpy as np
import decimal
import zlib

from math import ceil

int_sz = 8
float_sz = 16 # set size with float precision
complex_sz = 2*float_sz

clamp = lambda x,lo,hi: max(lo,min(hi,x))

import scipy.fftpack as scf
from math import sqrt,cos

# Decoder decodes a bytes array
class Decoder:
    def __init__(self,data):
        self.b = 0
        self.data = data
        return
    def read(self,sz):
        self.a = self.b
        self.b = self.a + sz
        x = self.data[self.a:self.b]
        self.x = x
        return x
    def convert(self,x,t):
        v = ConvertBytes2Type(x,t)
        return v

# Encoder creates a bytes array
class Encoder:
    def __init__(self):
        self.b = 0
        self.data = bytes([])
        return
    def write(self,val,pat):
        name,sz,t = pat
        self.a = self.b
        self.b = self.a + sz
        x = ConvertValue2Bytes(val,pat)
        self.data = bytes(list(self.data) + list(x))
        return
    def append(self,x):
        self.data = bytes(list(self.data)+list(x))
    def bytes(self):
        return self.data
    def values(self):
        return list(self.data)
        
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


def String2Bytes(s,length):
    x = bytes(s.encode(encoding='utf-8'))
    n = len(x)
    n2 = length - n
    x2 = bytes([0]*n2)
    x3 = x + x2
    return x3

def Bytes2String(x):
    s = x.decode(encoding='utf-8')
    L = []
    NULL = 0 # UTF-8 NULL character
    for i in range(len(s)):
        c = s[i]
        if ord(c) != NULL:
            L.append(c)
        else:
            break
    s2 = ''.join(L)
    return s2

# [1] https://docs.python.org/3/library/decimal.html
def Float2Bytes(x,precision):
    context = decimal.Context(prec=precision,
                rounding=decimal.ROUND_DOWN)
    y = context.create_decimal_from_float(x)
    tup = y.as_tuple()
    e = tup.exponent

    sz = precision
    D = list(tup.digits)
    n1 = len(D)
    n2 = sz - n1
    D = D + [0]*n2 # add zeros to decimal
    e = e - n2 # adjust exponent
    if e < 0:
        E = [1,-e]
    if e == 0:
        E = [0,0]
    if e > 0:
        E = [0,e]
    L = [tup.sign] + D + E
    x = bytes(L)
    return x

def Bytes2Float(x):
    L = list(x)
    sgn = L[0]
    E = L[-2:]
    digits = L[1:-2]
    if sgn == 1:
        sgn2 = -1
    else:
        sgn2 = 1    
    if E[0] == 1:
        e = -E[1]
    else:
        e = E[1]
    y = decimal.DecimalTuple(sgn2, digits, e)
    s = ''.join(list(map(str,y.digits)))
    z = y.sign*int(s)*10**(y.exponent)
    return z

def Int2Bytes(n):
    if n < 0:
        sgn = 1
    else:
        sgn = 0
    L = [sgn] + list(int(abs(n)).to_bytes(
        length=int_sz-1,byteorder="little"))
    x = bytes(L)
    return x

def Bytes2Int(x):
    sgn = x[0]
    n = int.from_bytes(x[1:],byteorder="little")
    if sgn == 1:
        n = -n
    return n

def Byte2Bytes(n):
    L = [n]
    x = bytes(L)
    return x

def Bytes2Byte(x):
    L = list(x)
    n = L[0]
    return n

def Complex2Bytes(z,precision):
    x = z.real
    y = z.imag
    vx = Float2Bytes(x,precision)
    vy = Float2Bytes(y,precision)
    L = list(vx) + list(vy)
    w = bytes(L)
    return w

def Bytes2Complex(w):
    L = list(w)
    n = len(L)
    m = int(n/2)
    vx = bytes(L[:m])
    vy = bytes(L[m:])
    x = Bytes2Float(vx)
    y = Bytes2Float(vy)
    z = complex(x,y)
    return z

def ConvertValue2Bytes(x, pat):
    name, sz, t = pat
    if t == "byte":
        v = Byte2Bytes(x)
    elif t == "int":
        v = Int2Bytes(x)
    elif t == "float":
        # precision must be sz - 3 for float
        sz2 = sz - 3
        v = Float2Bytes(x, precision=max(0,sz2))
    elif t == "complex":
        # precision must be sz - 3 for float
        sz2 = int(sz/2) - 3
        v = Complex2Bytes(x, precision=max(0,sz2))
    elif t == "string":
        v = String2Bytes(x,sz)
    else:
        v = None
    return v

def ConvertBytes2Type(x, t):
    if t == "byte":
        v = Bytes2Byte(x)
    elif t == "int":
        v = Bytes2Int(x)
    elif t == "float":
        v = Bytes2Float(x)
    elif t == "complex":
        v = Bytes2Complex(x)
    elif t == "string":
        v = Bytes2String(x)
    else:
        v = None
    return v

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

def encode_audio_compress_sample(x,j,chunk=None,
                f_c=None,zlib_level=None):
    # audio signal x, encode sample j of size chunk
    F = list(map(fft_freq(chunk,sampling_rate),
                 range(chunk)))
    y = sample(x,j,chunk)

    # compute frequency domain signal Y of sample j of x
    Y = FFT(y)
    n = len(Y)
    if len(Y) < chunk:
        Y2 = list(Y)
        Y3 = [complex(0,0)]*(chunk-n)
        Y = np.array(Y2+Y3,dtype=complex)
    eps = 100
    idx_c = Get_idx(chunk,sampling_rate)(f_c,eps)
    # frequency domain signal for chunk
    z = Y[:idx_c]
    # complex number pattern
    pat = ["val",complex_sz,"complex"]

    # convert frequency domain signal z to bytes z2
    E = Encoder()
    E.write(idx_c,["idx_c",int_sz,"int"])
    for i in range(len(z)):
        E.write(z[i],pat)
    z2 = E.bytes()
    
    # compress z2 to w2 using zlib
    w = zlib.compress(z2,level=zlib_level)
    return w


def decode_audio_compress_sample(w,
                    chunk=None):
    # decompress w to z2
    z2 = zlib.decompress(w)

    # complex number pattern
    pat = ["val",complex_sz,"complex"]
    
    # convert bytes to complex signal z
    D = Decoder(z2)
    t = "complex"
    nzb = D.read(int_sz)
    nz = D.convert(nzb,"int")
    z = []
    for i in range(nz):
        u2b = D.read(complex_sz)
        u2 = D.convert(u2b,"complex")
        z.append(u2)
        
    # pad with zeros to get complex signal Z
    Y = z
    zero = complex(0,0)
    Y2 = Y + [zero]*(chunk - len(Y))

    # do IFFT to get back signal x    
    x = IFFT(Y2)
    # convert numpy array above x to list x below
    x2 = list(map(lambda i: int(round(x[i].real)),
                  range(len(x))))
    x3 = np.array(x2,dtype=np.int16)
    return x3

def encode_audio_compress(x,chunk=None,
                f_c=None,zlib_level=None):
    n = len(x)
    ns = ceil(n/chunk) # number of samples
    E = Encoder()
    E.write(ns,["x",int_sz,"int"])
    for j in range(ns):
        w = encode_audio_compress_sample(x,
                    j,chunk, f_c,zlib_level)
        vlen = len(w)
        E.write(vlen,["x",int_sz,"int"])
        E.append(w)
    y = E.bytes()
    return y

def decode_audio_compress(y,chunk=None):
    D = Decoder(y)

    nb = D.read(int_sz)
    n = D.convert(nb,"int")

    L = []
    for j in range(n):
        vb = D.read(int_sz)
        vlen = D.convert(vb,"int")

        v = D.read(vlen)
        
        # decode v to get j-th sample from x
        x_j = decode_audio_compress_sample(v,
                    chunk)

        # add j-th sample to list L
        L = L + list(x_j)
    x = np.array(L,dtype=np.int16)
    return x

def Wav2CogBytes(fn_wav,
        chunk=None,f_c=None,zlib_level=None):
    global sampling_rate
    sampling_rate,data = si.wavfile.read(fn_wav)
    x_l = data[:,0]
    x_r = data[:,1]
    
    i = complex(0,1) # complex number i

    dt = 1/sampling_rate # time increment

    x = x_l
    y_l = encode_audio_compress(x,chunk,
                f_c,zlib_level)
    x = x_r
    y_r = encode_audio_compress(x,chunk,
                f_c,zlib_level)
    return y_l,y_r,sampling_rate

def CogBytes2Wav(y_l,y_r,fn_wav2,
        chunk=None,sampling_rate=None):
    if sampling_rate == None:
        print("Error: you must specify sampling_rate")
        return
    x2 = decode_audio_compress(y_l,chunk)
    x2_l = x2
    x2 = decode_audio_compress(y_r,chunk)
    x2_r = x2

    n = len(x2_l)
    data2 = np.zeros((n,2),dtype=np.int16)
    data2[:,0] = x2_l.copy()
    data2[:,1] = x2_r.copy()
    si.wavfile.write(fn_wav2,sampling_rate, data2)
    return

def SaveCog(fn_cog,
            y_l,y_r,sampling_rate,chunk):
    # integers can be easily converted but
    # floats require ConvertValue2Bytes
    E = Encoder()
    sr = sampling_rate
    E.write(chunk, ["val",int_sz,"int"])
    E.write(sr, ["val",int_sz,"int"])
    # sampling_rate is int but not float !
    nl = len(y_l)
    E.write(nl,["val",int_sz,"int"])
    E.append(y_l)
    nr = len(y_r)
    E.write(nr,["val",int_sz,"int"])
    E.append(y_r)
    
    # create data2 bytes array from data list
    data2 = E.bytes()
    f = open(fn_cog, mode='wb')
    f.write(data2)
    f.close()

def ReadCog(fn_cog):
    f = open(fn_cog, mode='rb')
    data = f.read()
    f.close()

    D = Decoder(data)
    b = 0
    
    chunk_b = D.read(int_sz)
    chunk = D.convert(chunk_b,"int")

    sr_b = D.read(int_sz)
    sr = D.convert(sr_b,"int")
    sampling_rate = sr

    nl_b = D.read(int_sz)
    nl= D.convert(nl_b,"int")

    y_l = D.read(nl)

    nr_b = D.read(int_sz)
    nr= D.convert(nr_b,"int")

    y_r = D.read(nr)

    return y_l,y_r,sampling_rate,chunk

root = r"./"
wavroot = r"../wav/"
fn_wav = wavroot + "hello-1.wav"
fn_cog = root + "hello-1b.cog1"
fn_wav2 = root + "hello-1-cog1.wav"

chunk = 512
f_c = 1000
zlib_level = 1

create_cog = True
if create_cog:
    y_l,y_r,sampling_rate = Wav2CogBytes(fn_wav,
        chunk,f_c,zlib_level)
    SaveCog(fn_cog,y_l,y_r,sampling_rate,chunk)

y_l2,y_r2,sampling_rate2,chunk2 = ReadCog(fn_cog)
CogBytes2Wav(y_l2,y_r2,fn_wav2,
        chunk2,sampling_rate2)

