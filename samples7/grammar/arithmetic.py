from copy import deepcopy

import nor
Nor = nor.Nor
##def Nor(x,y):
##    z = ~(x|y) % 2
##    return z

# https://en.wikipedia.org/wiki/Flash_memory NAND flash
# https://en.wikipedia.org/wiki/NAND_gate
def Nand(A,B):
    v1 = Nor(A,A)
    v2 = Nor(B,B)
    v3 = Nor(v1,v2)
    Q = Nor(v3,v3)
    return Q

# https://en.wikipedia.org/wiki/AND_gate
def And(A,B):
    v1 = Nor(A,A)
    v2 = Nor(B,B)
    Q = Nor(v1,v2)
    return Q

# https://en.wikipedia.org/wiki/OR_gate
def Or(A,B):
    v1 = Nor(A,B)
    Q = Nor(v1,v1)
    return Q

# https://en.wikipedia.org/wiki/XOR_gate
def Xor(A,B):
    v11 = Nor(A,B)
    v21 = Nor(A,v11)
    v22 = Nor(v11,B)
    v31 = Nor(v21,v22)
    Q = Nor(v31,v31)
    return Q

# https://en.wikipedia.org/wiki/XOR_gate
def XNor(A,B):
    v11 = Nor(A,B)
    v21 = Nor(A,v11)
    v22 = Nor(v11,B)
    Q = Nor(v21,v22)
    return Q

def Not(x):
    Q = Nor(x,x)
    return Q

# https://en.wikipedia.org/wiki/Digital_comparator
def Comp(A,B):
    v11 = Not(A)
    v12 = B
    v13 = A
    v14 = B
    v15 = A
    v16 = Not(B)
    vlt = And(v11,v12)
    veq = XNor(v13,v14)
    vgt = And(v15,v16)
    return [vlt,veq,vgt]

# https://en.wikipedia.org/wiki/Digital_comparator
def Comp4(x,y):
    # use reverse wire order for x,y as A,B
    A = deepcopy(x)
    A.reverse()
    B = deepcopy(y)
    B.reverse()
    
    c = 0
    x0 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 1
    x1 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 2
    x2 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 3
    x3 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    veq = And(And(x3,x2),And(x1,x0))
    
    v1 = And(A[3],Not(B[3]))
    v2 = And(x3,And(A[2],Not(B[2])))
    v31 = And(A[1],Not(B[1]))
    v3 = And(x3,And(x2,v31))
    v41 = And(A[0],Not(B[0]))
    v4 = And(x3,And(x2,And(x1,v41)))
    vgt = Or(v1,Or(v2,Or(v3,v4)))
    
    v1 = And(Not(A[3]),B[3])
    v2 = And(x3,And(Not(A[2]),B[2]))
    v31 = And(Not(A[1]),B[1])
    v3 = And(x3,And(x2,v31))
    v41 = And(Not(A[0]),B[0])
    v4 = And(x3,And(x2,And(x1,v41)))
    vlt = Or(v1,Or(v2,Or(v3,v4)))
    return vlt,veq,vgt
def Comp8(x,y):
    # use reverse wire order for x,y as A,B
    A = deepcopy(x)
    A.reverse()
    B = deepcopy(y)
    B.reverse()
    
    c = 0
    x0 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 1
    x1 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 2
    x2 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 3
    x3 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 4
    x4 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 5
    x5 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 6
    x6 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    c = 7
    x7 = Or(And(A[c],B[c]),And(Not(A[c]),Not(B[c])))
    veq0 = And(And(x3,x2),And(x1,x0))
    veq1 = And(And(x7,x6),And(x5,x4))
    veq = And(veq0,veq1)
    
    v7 = And(A[7],Not(B[7]))
    v61 = And(A[6],Not(B[6]))
    v6 = And(x7,v61)
    v51 = And(A[5],Not(B[5]))
    v5 = And(x7,And(x6,v51))
    v41 = And(A[4],Not(B[4]))
    v4 = And(x7,And(x6,And(x5,v41)))
    v31 = And(A[3],Not(B[3]))
    v3 = And(x7,And(x6,And(x5,And(x4,v31))))
    v21 = And(A[2],Not(B[2]))
    v2 = And(x7,And(x6,And(x5,And(x4,And(x3,v21)))))
    v11 = And(A[1],Not(B[1]))
    v1 = And(x7,And(x6,And(x5,And(x4,And(x3,And(x2,v11))))))
    v01 = And(A[0],Not(B[0]))
    v0 = And(x7,And(x6,And(x5,And(x4,And(x3,And(x2,And(x1,v01)))))))
    vgt = Or(v7,Or(v6,Or(v5,Or(v4,Or(v3,Or(v2,Or(v1,v0)))))))
    
    v7 = And(Not(A[7]),B[7])
    v61 = And(Not(A[6]),B[6])
    v6 = And(x7,v61)
    v51 = And(Not(A[5]),B[5])
    v5 = And(x7,And(x6,v51))
    v41 = And(Not(A[4]),B[4])
    v4 = And(x7,And(x6,And(x5,v41)))
    v31 = And(Not(A[3]),B[3])
    v3 = And(x7,And(x6,And(x5,And(x4,v31))))
    v21 = And(Not(A[2]),B[2])
    v2 = And(x7,And(x6,And(x5,And(x4,And(x3,v21)))))
    v11 = And(Not(A[1]),B[1])
    v1 = And(x7,And(x6,And(x5,And(x4,And(x3,And(x2,v11))))))
    v01 = And(Not(A[0]),B[0])
    v0 = And(x7,And(x6,And(x5,And(x4,And(x3,And(x2,And(x1,v01)))))))
    vlt = Or(v7,Or(v6,Or(v5,Or(v4,Or(v3,Or(v2,Or(v1,v0)))))))
    return vlt,veq,vgt

# The loops are just notation to show the clear pattern
# of connecting gates together
def Comp16(x,y):
    n = 16
    # use reverse wire order for x,y as A,B
    A = deepcopy(x)
    A.reverse()
    B = deepcopy(y)
    B.reverse()

    x = [0]*n
    d = 1
    for i in range(n):
        xi = Or(And(A[i],B[i]),And(Not(A[i]),Not(B[i])))
        x[i] = xi
        d = And(d,xi)
    veq = d

    v = [0]*n
    d = 0
    c = 1
    vi1 = And(A[n-1],Not(B[n-1]))
    v[n-1] = And(c,vi1)
    for i in range(n-2,-1,-1):
        vi1 = And(A[i],Not(B[i]))
        c = And(c,x[i+1])
        vi = And(c,vi1)
        v[i] = vi
        d = Or(d,vi)
    vgt = d

    v = [0]*n
    d = 0
    c = 1
    vi1 = And(Not(A[n-1]),B[n-1])
    v[n-1] = And(c,vi1)
    vi = And(c,vi1)
    d = Or(d,vi)
    for i in range(n-2,-1,-1):
        vi1 = And(Not(A[i]),B[i])
        c = And(c,x[i+1])
        vi = And(c,vi1)
        v[i] = vi
        d = Or(d,vi)
    vlt = d

    return vlt,veq,vgt

# https://en.wikipedia.org/wiki/Adder_(electronics)
# Half Adder
def HA(A,B):
    S = Xor(A,B)
    C = And(A,B)
    return [S,C]

# Full Adder
def FA(A,B,Cin):
    S1,C1 = HA(A,B)
    S,C2 = HA(S1,Cin)
    Cout = Or(C1,C2)
    return [S,Cout]

# Ripple-carry adder (RCA) 4-bit
# A : 0123; B : 0123; S : 0123 
def RCA4(A4,B4,C):
    S3,C3 = FA(A4[3],B4[3],C)
    S2,C2 = FA(A4[2],B4[2],C3)
    S1,C1 = FA(A4[1],B4[1],C2)
    S0,C0 = FA(A4[0],B4[0],C1)
    S = [S0,S1,S2,S3]
    Cout = C0
    return [S,Cout]

# Ripple-carry adder (RCA) 8-bit using two RCA4
# A : AH,AL; B : BH,BL; S = SH,SL
def RCA8(A8,B8,C0):
    AH = A8[:4]
    AL = A8[4:]
    BH = B8[:4]
    BL = B8[4:]
    SL,CL = RCA4(AL,BL,C0)
    SH,Cout = RCA4(AH,BH,CL)
    S = SH + SL # combine as list of wires
    return [S,Cout]

# Ripple-carry adder (RCA) 16-bit using two RCA8
# A : AH,AL; B : BH,BL; S = SH,SL
def RCA16(A16,B16,C0):
    n = 8
    AH = A16[:n]
    AL = A16[n:]
    BH = B16[:n]
    BL = B16[n:]
    SL,CL = RCA8(AL,BL,C0)
    SH,Cout = RCA8(AH,BH,CL)
    S = SH + SL # combine as list of wires
    return [S,Cout]

# Ripple-carry adder (RCA) 32-bit using two RCA16
# A : AH,AL; B : BH,BL; S = SH,SL
def RCA32(A32,B32,C0):
    n = 16
    AH = A32[:n]
    AL = A32[n:]
    BH = B32[:n]
    BL = B32[n:]
    SL,CL = RCA16(AL,BL,C0)
    SH,Cout = RCA16(AH,BH,CL)
    S = SH + SL # combine as list of wires
    return [S,Cout]

# Ripple-carry adder (RCA) 64-bit using two RCA32
# A : AH,AL; B : BH,BL; S = SH,SL
def RCA64(A64,B64,C0):
    n = 32
    AH = A64[:n]
    AL = A64[n:]
    BH = B64[:n]
    BL = B64[n:]
    SL,CL = RCA32(AL,BL,C0)
    SH,Cout = RCA32(AH,BH,CL)
    S = SH + SL # combine as list of wires
    return [S,Cout]

def Bits8(x):
    s = '{0:08b}'.format(x)
    L = list(s)
    L2 = list(map(int,L))
    return L2

def Bits4(x):
    s = '{0:04b}'.format(x)
    L = list(s)
    L2 = list(map(int,L))
    return L2

def Bits16(x):
    s = '{0:016b}'.format(x)
    L = list(s)
    L2 = list(map(int,L))
    return L2

def Bits32(x):
    s = '{0:032b}'.format(x)
    L = list(s)
    L2 = list(map(int,L))
    return L2

def Bits64(x):
    s = '{0:064b}'.format(x)
    L = list(s)
    L2 = list(map(int,L))
    return L2

# Encode 8-bit number as character
def Enc(x):
    ch = chr(x)
    return ch
# Decode ASCII character as 8-bit number
def Dec(ch):
    x = ord(ch)
    return x

def Inc8(A8):
    C0 = 0
    B8 = Bits8(1)
    S8,Cout = RCA8(A8,B8,C0)
    return S8

def Add8(A8,B8):
    C0 = 0
    C8,Cout = RCA8(A8,B8,C0)
    return C8,Cout

def Mov8(x):
    L = Bits8(x)
    return L

def OnesComplement(A):
    B = list([Not(b) for b in A])
    return B

def TwosComplement8(A8):
    B8 = OnesComplement(A8)
    Cin = 0
    One = Bits8(1)
    C8,Cout = RCA8(B8,One,Cin)
    return C8

def TwosComplement16(A16):
    B16 = OnesComplement(A16)
    Cin = 0
    One = Bits16(1)
    C16,Cout = RCA16(B16,One,Cin)
    return C16

# Negative of 8-bit number stored in binary A8
def Minus8(A8):
    return TwosComplement8(A8)

# Negative of 16-bit number stored in binary A8
def Minus16(A16):
    return TwosComplement16(A16)

# Subtract B8 from A8 two 8-bit numbers and
# return 8-bit C8 and 1-bit carry Cout.
def Sub8(A8,B8):
    C0 = 0
    D8 = Minus8(B8)
    C8,C1 = RCA8(A8,D8,C0)
    return C8,C1

def RShift(Val,n):
    m = len(Val)
    b = m - n
    val0 = Val[0]
    if b <= 0:
        val = [val0]*m
    else:
        val = [val0]*n+Val[0:b]
    return val

acc_Mul8 = 8

acc_Mul8 = 8

# https://en.wikipedia.org/wiki/Booth%27s_multiplication_algorithm
# Multiply m and times r two 8-bit numbers and
# return P a 8-bit number
def Mul8(m,r):
    global acc_Mul8
    x = len(m)
    y = len(r)
    A = m + [0]*(y) + [0]
    mc = TwosComplement8(m)
    S = mc+[0]*y + [0]
    P = [0]*x + r + [0]
    for i in range(y):
        a,b = P[-2:]
        if [a,b] == [0,1]:
            Val,CP = RCA16(P,A,0)
            Val = Val + [CP]
        elif [a,b] == [1,0]:
            Val,CP = RCA16(P,S,0)
            Val = Val + [CP]
        elif [a,b] == [0,0]:
            Val = deepcopy(P)
        elif [a,b] == [1,1]:
            Val = deepcopy(P)
        P = RShift(Val,1)
    P8 = RShift(P,1)
    P8 = P8[-acc_Mul8:]
    return P8

acc_Mul16 = 16
# https://en.wikipedia.org/wiki/Booth%27s_multiplication_algorithm
# Multiply m and times r two 16-bit numbers and
# return P a 16-bit number
def Mul16(m,r):
    global acc_Mul16
    x = len(m)
    y = len(r)
    A = m + [0]*(y) + [0]
    mc = TwosComplement16(m)
    S = mc+[0]*y + [0]
    P = [0]*x + r + [0]
    for i in range(y):
        a,b = P[-2:]
        if [a,b] == [0,1]:
            Val,CP = RCA32(P,A,0)
            Val = Val + [CP]
        elif [a,b] == [1,0]:
            Val,CP = RCA32(P,S,0)
            Val = Val + [CP]
        elif [a,b] == [0,0]:
            Val = deepcopy(P)
        elif [a,b] == [1,1]:
            Val = deepcopy(P)
        P = RShift(Val,1)
    P16 = RShift(P,1)
    P16 = P16[-acc_Mul16:]
    return P16

##https://en.wikipedia.org/wiki/Division_algorithm

# Divide numerator n by denominator d where
# n is 16-bit number and d is 16-bit number
# and get quotient Q and remainder R an 16-bit number
def Div_unsigned16(n16,d16):
    Q = Bits16(0)
    R = deepcopy(n16)
    # unsigned comparision r >= d
    while Number(R) >= Number(d16):
        #print "(Q,R)=",(Number(Q),Number(R))
        # Q := Q + 1
        Q,Cout = RCA16(Q,Bits16(1),0)
        # Subtract R := R - D
        C0 = 0
        R,C1 = RCA16(R,Minus16(d16),C0)
    return (Q,R)

# Assumes numerator n16 and denominator d16,
# two 16-bit numbers, and returns quotient Q
# and remainder R two 16-bit numbers
def Div16(n16,d16):
    if SNumber(d16) == 0:
        print("Error: Division by zero")
        return (n16,d16)
    if SNumber(d16) < 0:
        Dm = Minus16(d16)
        Q,R = Div16(n16,Dm)
        Qm = Minus16(Q)
        return (Qm,R)
    if SNumber(n16) < 0:
        Nm = Minus16(n16)
        Q,R = Div16(Nm,d16)
        if SNumber(R) == 0:
            Qm = Minus16(Q)
            zero = Bits16(0)
            return (Qm,zero)
        else:
            Qm = Minus16(Q)
            one = Bits16(1)
            onem = Minus16(one)
            Q2,Cout = RCA16(Qm,onem,0)
            Rm = Minus16(R)
            R2,Cout = RCA16(d16,Rm,0)
            return (Q2,R2)
    return Div_unsigned16(n16,d16)

def DisplaySigned():
    x = Bits8(0)
    for i in range(256):
        print(x,SNumber(x))
        x = Inc8(x)
    return

def DisplayASCII():
    x = Bits8(32)
    for i in range(32,127):
        print(x, Number(x), Enc(Number(x)))
        x = Inc8(x)
    return

#DisplaySigned()
# SignedNumber

def Hex(L):
    n = len(L)
    i = n % 4
    j = (4-i) % 4
    L = [0]*j + L
    s = '0x'
    while len(L) > 0:
        val = L[0:4]
        L = L[4:]
        if val == [0,0,0,0]:
            s = s + '0'
        elif val == [0,0,0,1]:
            s = s + '1'
        elif val == [0,0,1,0]:
            s = s + '2'
        elif val == [0,0,1,1]:
            s = s + '3'
        elif val == [0,1,0,0]:
            s = s + '4'
        elif val == [0,1,0,1]:
            s = s + '5'
        elif val == [0,1,1,0]:
            s = s + '6'
        elif val == [0,1,1,1]:
            s = s + '7'
        elif val == [1,0,0,0]:
            s = s + '8'
        elif val == [1,0,0,1]:
            s = s + '9'
        elif val == [1,0,1,0]:
            s = s + 'A'
        elif val == [1,0,1,1]:
            s = s + 'B'
        elif val == [1,1,0,0]:
            s = s + 'C'
        elif val == [1,1,0,1]:
            s = s + 'D'
        elif val == [1,1,1,0]:
            s = s + 'E'
        elif val == [1,1,1,1]:
            s = s + 'F'
        else:
            print("Error",val)
            break 
    return s

def Bin(s):
    assert(s[:2]=='0x')
    s = s[2:]
    M = list(s)
    L = []
    for x in M:
        if x == '0':
            L = L + [0,0,0,0]
        elif x == '1':
            L = L + [0,0,0,1]
        elif x == '2':
            L = L + [0,0,1,0]
        elif x == '3':
            L = L + [0,0,1,1]
        elif x == '4':
            L = L + [0,1,0,0]
        elif x == '5':
            L = L + [0,1,0,1]
        elif x == '6':
            L = L + [0,1,1,0]
        elif x == '7':
            L = L + [0,1,1,1]
        elif x == '8':
            L = L + [1,0,0,0]
        elif x == '9':
            L = L + [1,0,0,1]
        elif x == 'A':
            L = L + [1,0,1,0]
        elif x == 'B':
            L = L + [1,0,1,1]
        elif x == 'C':
            L = L + [1,1,0,0]
        elif x == 'D':
            L = L + [1,1,0,1]
        elif x == 'E':
            L = L + [1,1,1,0]
        elif x == 'F':
            L = L + [1,1,1,1]
    return L

def Number(L):
    L2 = deepcopy(L)
    L2.reverse()
    
    n = 0
    for i in range(len(L2)):
        ai = L2[i]
        n = n + ai*2**i
    return n

def SNumber(L):
    L2 = deepcopy(L)
    L2.reverse()
    n = 0
    for i in range(len(L2)-1):
        ai = L2[i]
        n = n + ai*2**i
    N = len(L2)
    ai = L2[N-1]
    n = -ai*2**(N-1) + n
    return n
