import decimal

int_sz = 8
float_sz = 16 # set size with float precision

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
    elif t == "string":
        v = String2Bytes(x,sz)
    else:
        v = None
    return v

# [2] https://www.sqlite.org/datatype3.html
def rec_to_bytes(rec,pattern):
    L = list(rec)
    assert(len(L) == len(pattern))
    rec_L = []
    for i in range(len(pattern)):
        pat = pattern[i]
        x = L[i]
        v = list(ConvertValue2Bytes(x, pat))
        rec_L = rec_L + v
    x = bytes(rec_L)
    return x

def ConvertBytes2Type(x, t):
    if t == "byte":
        v = Bytes2Byte(x)
    elif t == "int":
        v = Bytes2Int(x)
    elif t == "float":
        v = Bytes2Float(x)
    elif t == "string":
        v = Bytes2String(x)
    else:
        v = None
    return v

def partition_bytes(x, names, structure, types):
    assert(len(names)==len(structure))
    assert(len(names)==len(types))
    M = {}
    L = list(x)
    n = 0
    for i in range(len(names)):
        sz = structure[i]
        name = names[i]
        t = types[i]
        x2 = bytes(L[n:n+sz])
        M[name] = ConvertBytes2Type(x2, t)
        n = n + sz
    return M

def GetInfo(I,pattern):
    O = []
    for j in range(len(I)):
        offset_j = 0
        for i in range(len(pattern)):
            name,sz,t = pattern[i] # name, size, type
            if I[j] != name:
                offset_j = offset_j + sz
                continue
            a = offset_j
            O.append((name,sz,t,a))
            offset_j = offset_j + sz
    return O


