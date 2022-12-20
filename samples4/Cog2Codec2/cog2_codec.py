import codec
import DCT
import FFT

import scipy.io as si
import numpy as np

import zlib

from math import ceil,log

int_sz = codec.int_sz
float_sz = codec.float_sz
complex_sz = codec.complex_sz

def encode_audio_compress_sample2(x,j,chunk=None,
                f_c=1,zlib_level=None,
                sampling_rate=None):
    # audio signal x, encode sample j of size chunk
    F = list(map(FFT.fft_freq(chunk,sampling_rate),
                 range(chunk)))
    y = FFT.sample(x,j,chunk)

    # compute frequency domain signal Y of sample j of x
    eps = 100
    N = chunk
    n0 = FFT.Get_idx(chunk,sampling_rate)(2*f_c,eps)
    Y = list(y)
    if len(Y) < chunk:
        Y2 = list(Y)
        Y3 = [0]*(chunk-n0)
        Y = np.array(Y2+Y3,dtype=np.int16)
    Y2 = DCT.DCT(Y,n=n0)
    
    # frequency domain signal for chunk
    z = Y2[:n0]
    # complex number pattern
    pat = ["val",int_sz,"int"]

    # convert frequency domain signal z to bytes z2
    E = codec.Encoder()
    E.write(n0,["n0",int_sz,"int"])
    for i in range(len(z)):
        E.write(z[i],pat)
    z2 = E.bytes()
    
    # compress z2 to w2 using zlib
    w = zlib.compress(z2,level=zlib_level)
    return w

def decode_audio_compress_sample2(w,
                    chunk=None):
    # decompress w to z2
    z2 = zlib.decompress(w)

    # complex number pattern
    pat = ["val",int_sz,"int"]
    
    # convert bytes to integer signal z
    D = codec.Decoder(z2)
    t = "int"
    nzb = D.read(int_sz)
    nz = D.convert(nzb,"int")
    z = []
    for i in range(nz):
        u2b = D.read(int_sz)
        u2 = D.convert(u2b,"int")
        z.append(u2)
        
    # pad with zeros to get complex signal Z
    Y = z
    zero = 0
    Y2 = Y + [zero]*(chunk - len(Y))

    # do IFFT to get back signal x    
    x = DCT.IDCT(Y2)
    # convert numpy array above x to list x below
    x3 = np.array(x,dtype=np.int16)
    return x3

def encode_audio_compress2(x,chunk=None,
                f_c=1,zlib_level=None,
                sampling_rate=None):
    n = len(x)
    ns = ceil(n/chunk) # number of samples
    E = codec.Encoder()
    E.write(ns,["x",int_sz,"int"])
    for j in range(ns):
        w = encode_audio_compress_sample2(x,
                    j,chunk, f_c,
                    zlib_level,
                    sampling_rate)
        vlen = len(w)
        E.write(vlen,["x",int_sz,"int"])
        E.append(w)
    y = E.bytes()
    return y

def decode_audio_compress2(y,chunk=None):
    D = codec.Decoder(y)

    nb = D.read(int_sz)
    n = D.convert(nb,"int")

    L = []
    for j in range(n):
        vb = D.read(int_sz)
        vlen = D.convert(vb,"int")

        v = D.read(vlen)
        
        # decode v to get j-th sample from x
        x_j = decode_audio_compress_sample2(v,
                    chunk)

        # add j-th sample to list L
        L = L + list(x_j)
    x = np.array(L,dtype=np.int16)
    return x

def Wav2Cog2Bytes(fn_wav,
        chunk=None,f_c = None,zlib_level=None,
        sampling_rate=None):
    sampling_rate,data = si.wavfile.read(fn_wav)
    x_l = data[:,0]
    x_r = data[:,1]
    
    i = complex(0,1) # complex number i

    dt = 1/sampling_rate # time increment

    x = x_l
    y_l = encode_audio_compress2(x,chunk,
                f_c,zlib_level,sampling_rate)
    x = x_r
    y_r = encode_audio_compress2(x,chunk,
                f_c,zlib_level,sampling_rate)
    return y_l,y_r,sampling_rate

def Data2Cog2Bytes(data,sampling_rate = None,
        chunk=None,f_c = None, zlib_level=None):
    x_l = data[:,0]
    x_r = data[:,1]
    
    i = complex(0,1) # complex number i

    dt = 1/sampling_rate # time increment

    x = x_l
    y_l = encode_audio_compress2(x,chunk,
                f_c,zlib_level,sampling_rate)
    x = x_r
    y_r = encode_audio_compress2(x,chunk,
                f_c,zlib_level,sampling_rate)
    return y_l,y_r


def Cog2Bytes2Audio(y_l,y_r,
        chunk=None):
    x2 = decode_audio_compress2(y_l,chunk)
    x2_l = x2
    x2 = decode_audio_compress2(y_r,chunk)
    x2_r = x2

    n = len(x2_l)
    data2 = np.zeros((n,2),dtype=np.int16)
    data2[:,0] = x2_l.copy()
    data2[:,1] = x2_r.copy()
    return data2

def SaveAudio2Wav(fn_wav2,sampling_rate,data2):
    si.wavfile.write(fn_wav2,sampling_rate,data2)
    return

def Cog2Bytes2Wav(y_l,y_r,fn_wav2,chunk=None,
            sampling_rate=None):
    data2 = Cog2Bytes2Audio(y_l,y_r,chunk)
    SaveAudio2Wav(fn_wav2,sampling_rate,data2)
    return

def SaveCog2(fn_cog,
            y_l,y_r,sampling_rate,chunk):
    # integers can be easily converted but
    # floats require ConvertValue2Bytes
    E = codec.Encoder()
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

def ReadCog2(fn_cog):
    f = open(fn_cog, mode='rb')
    data = f.read()
    f.close()

    D = codec.Decoder(data)
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


