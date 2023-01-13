import decimal

int_sz = 8
float_sz = 16 # set size with float precision
complex_sz = 2*float_sz

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
