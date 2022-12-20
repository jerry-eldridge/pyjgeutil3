import DCT
import bytedatatypes as bdt

import zlib

import numpy as np

def encode_DCT(x,n0=0):
    print("encode_DCT")
    y = DCT.DCT2(x,n=n0)
    return y
def decode_DCT(y):
    print("decode_DCT")
    x = DCT.IDCT2(y)
    return x

Int2Bytes = bdt.Int2Bytes
Bytes2Int = bdt.Bytes2Int

def encode_image_compress_1D(x, n_compression = 1,
                             zlib_level = 0):
    print("encode_image_compress_1D")
    N = len(x)
    n0 = int(N/n_compression)
    # use DCT to lossy compress x
    x2 = encode_DCT(x,n0)
    # convert x2 list of integers to bytes array x3
    L = []
    for i in range(len(x2)):
        n = x2[i]
        v = list(Int2Bytes(n))
        L = L + v
    x3 = bytes(L)
    # compress x3 with zlib to x4
    x4 = zlib.compress(x3,level=zlib_level)
    x4 = bytes(x4)
    
    # convert to list of bytes y
    y = list(x4)
    # append signal size N to beginning of y
    N2 = list(Int2Bytes(N))
    n02 = list(Int2Bytes(n0))
    x3_sz = list(Int2Bytes(len(x3)))
    y_sz = list(Int2Bytes(len(y)))
    y2 = N2 + n02 + x3_sz + y_sz + y
    y3 = bytes(y2)
    return y3

def decode_image_compress_1D(y):
    print("decode_image_compress_1D")
    # get data size N2
    int_sz = bdt.int_sz
    b = 0

    sz = int_sz
    a = b
    b = a + sz
    N2 = y[a:b]
    N = Bytes2Int(N2)

    sz = int_sz
    a = b
    b = a + sz
    n02 = y[a:b]
    n0 = Bytes2Int(n02)

    sz = int_sz
    a = b
    b = a + sz
    x3_sz_b = y[a:b]
    x3_sz = Bytes2Int(x3_sz_b)

    sz = int_sz
    a = b
    b = a + sz
    y_sz_b = y[a:b]
    y_sz = Bytes2Int(y_sz_b)

    sz = y_sz
    a = b
    b = a + sz
    data = y[a:b]

    # decompress data with zlib to y2
    x4 = zlib.decompress(data)
    
    y3 = []
    L = list(x4)
    for i in range(n0):
        val = bytes(L[i*int_sz:(i+1)*int_sz])
        n = Bytes2Int(val)
        y3.append(n)
    # pad with zeros
    y4 = y3 + [0]*(N-n0)
    # convert list of integers with inverse DCT
    z = decode_DCT(y4)
    return z

def encode_image_compress_2D_Y(im,
            n_compression = 1,
            zlib_level = 1):
    print("encode_image_compress_2D_Y")
    sh = im.shape
    height,width = sh
    x = list(im.flatten())

    hh = list(Int2Bytes(height))
    ww = list(Int2Bytes(width))
    
    y = encode_image_compress_1D(x,
                n_compression,
                zlib_level)

    n = len(y)
    n2 = list(Int2Bytes(n))

    y2 = list(y)
    
    z = ww + hh + n2 + y2
    z2 = bytes(z)
    return z2

def decode_image_compress_2D_Y(z):
    print("decode_image_compress_2D_Y")
    int_sz = bdt.int_sz
    b = 0

    # get width of size int_sz
    sz = int_sz
    a = b
    b = a + sz
    ww = z[a:b]
    width = Bytes2Int(ww)

    # get height of size int_sz
    sz = int_sz
    a = b
    b = a + sz
    hh = z[a:b]
    height = Bytes2Int(hh)

    sh = (height,width)

    # get data of size int_size*n0
    sz = int_sz
    a = b
    b = a + sz
    ds = z[a:b]
    datasize = Bytes2Int(ds)
    sz = datasize
    a = b
    b = a + sz
    data = z[a:b]

    x = decode_image_compress_1D(data)

    im = np.array(x,dtype=np.uint8)
    im = im.reshape(sh)
    return im

def encode_image_compress_2D_C(im,
            n_compression = 1,
            zlib_level = 1):
    print("encode_image_compress_2D_C")
    height,width,c = im.shape
    planes = []
    for i in range(c):
        im_i = im[:,:,i]
        p_i = encode_image_compress_2D_Y(im_i,
            n_compression,
            zlib_level)
        v = list(p_i)
        planes.append(v)
    n = len(planes[0])

    hh = list(Int2Bytes(height))
    ww = list(Int2Bytes(width))
    nn = list(Int2Bytes(n))
    cc = list(Int2Bytes(c))

    x = ww + hh + cc + nn
    for i in range(c):
        v = planes[i]
        sz = list(Int2Bytes(len(v)))
        x = x + sz + v
    x2 = bytes(x)
    
    return x2

def decode_image_compress_2D_C(z):
    print("decode_image_compress_2D_C")
    int_sz = bdt.int_sz
    b = 0

    # get width of size int_sz
    sz = int_sz
    a = b
    b = a + sz
    ww = z[a:b]
    width = Bytes2Int(ww)

    # get height of size int_sz
    sz = int_sz
    a = b
    b = a + sz
    hh = z[a:b]
    height = Bytes2Int(hh)

    # get c of size int_sz
    sz = int_sz
    a = b
    b = a + sz
    cc = z[a:b]
    c = Bytes2Int(cc)

    # get n of size int_sz
    sz = int_sz
    a = b
    b = a + sz
    nn = z[a:b]
    n = Bytes2Int(nn)

    sh = (height,width,c)

    planes = []
    im = np.zeros(sh,dtype=np.uint8)
    b2 = b
    for i in range(c):
        sz2 = int_sz
        a2 = b2
        b2 = a2 + sz2
        szsz = z[a2:b2]
        sz = Bytes2Int(szsz)
        sz2 = sz
        a2 = b2
        b2 = a2 + sz2    
        p_i = z[a2:b2]
        im[:,:,i] = decode_image_compress_2D_Y(p_i)
    return im
