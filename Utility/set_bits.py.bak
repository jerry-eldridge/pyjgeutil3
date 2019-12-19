from numpy import array,zeros,ones

def Base(i,base, bits):
    L = []
    j = 0
    n = 0
    ii = i
    for j in range(bits):
        a = ii%base
        ii = int(ii/base)
        n = n + a*base**j
        L.append(a)
    L.reverse()
    return L

def Indices(L,val):
     idxs = []
     i = 0
     for x in L:
         if x == val:
             idxs.append(i)
         i += 1
     return idxs

def GetVector(val,n):
    return Base(val,2,n)

def Number(L,base):
    n = 0
    k = len(L)-1
    for i in range(len(L)):
        n = n + L[k-i]*base**i
    return n

def Mod(L,base):
    for i in range(len(L)):
    	L[i] = L[i] % base
    return L

def GetSet(v):
    n = len(v)
    S = set([])
    for i in range(n):
        for k in range(v[i]):
            S = S | set([i])
    return S

def Cardinality(v):
    return len(list(GetSet(v)))

def MinorRow(A,v):
    N1,N2 = A.shape
    k = Cardinality(v)
    minor = zeros((max(1,N1),max(1,k)))
    jj = 0
    for j in range(N2):
        if v[j] == 1:
            for i in range(N1):
                minor[i,jj] = A[i,j]
        if v[j] == 1:
            jj += 1
    return minor

def MinorCol(A,v):
    N1,N2 = A.shape
    k = Cardinality(v)
    minor = zeros((max(1,k),max(1,N2)))
    ii = 0
    for i in range(N1):
        if v[i] == 1:
            for j in range(N2):
                minor[ii,j] = A[i,j]
        if v[i] == 1:
            ii += 1
    return minor

def Less(u,v):
    U = GetSet(u)
    V = GetSet(v)
    flag = U.issubset(V) and (u <> v)
    return flag

def Meet(u,v):
    n = len(u)
    w = [0]*n
    for i in range(n):
        w[i] = min(u[i],v[i])
    return w
def Join(u,v):
    n = len(u)
    w = [0]*n
    for i in range(n):
        w[i] = max(u[i],v[i])
    return w

def BitString(v):
    return reduce(lambda u,v:str(u)+str(v),v,'')
