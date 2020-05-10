import matrix

# https://en.wikipedia.org/wiki/LU_decomposition
# based on C++ code
def LUPDecompose(B,Tol):
    n,m = B.shape
    A = B.copy()
    assert(n == m)
    N = n
    P = matrix.Mat([[]]).zero(N+1,1)
    for i in range(N+1):
        P.s(i,0, i)
    for i in range(N):
        maxA = 0.0
        imax = i
        for k in range(i,N):
            absA = abs(A.g(k,i))
            if (absA > maxA):
                maxA = absA
                imax = k
        if (maxA < Tol):
            return 0

        if (imax != i):
            j = P.g(i,0)
            P.s(i,0, P.g(imax,0))
            P.s(imax,0, j)

            ptr = matrix.Mat([[]]).zero(N,1)
            for k in range(N):
                ptr.s(k,0, A.g(i,k))

            for k in range(N):
                A.s(i,k, A.g(imax,k))

            for k in range(N):
                A.s(imax,k, ptr.g(k,0))

            P.s(N,0, P.g(N,0)+1)

        for j in range(i+1,N):
            A.s(j,i, 1.0*A.g(j,i)/A.g(i,i))

            for k in range(i+1,N):
                A.s(j,k, 1.0*A.g(j,k)-A.g(j,i)*A.g(i,k))
            
    return 1,A,P

def LUPSolve(A,b):
    B = A.copy()
    n,m = B.shape
    assert(n == m)
    N = n
    Tol = 1e-8
    flag,C,P = LUPDecompose(B,Tol)
    p,q = b.shape
    assert((p == N) and (q == 1))
    x = matrix.Mat([[]]).zero(N,1)
    for i in range(N):
        x.s(i,0, b.g(P.g(i,0),0))

        for k in range(i):
            x.s(i,0, x.g(i,0)-C.g(i,k)*x.g(k,0))

    for i in range(N-1,-1,-1):
        for k in range(i+1,N):
            x.s(i,0, x.g(i,0)-C.g(i,k)*x.g(k,0))

        x.s(i,0, 1.0*x.g(i,0)/C.g(i,i))
    return x

def LUPInvert(A):
    B = A.copy()
    n,m = B.shape
    assert(n == m)
    N = n
    Tol = 1e-8
    flag,C,P = LUPDecompose(B,Tol)
    IA = matrix.Mat([[]]).zero(m,n)
    for j in range(N):
        for i in range(N):
            if abs(P.g(i,0) - j) < 0.1:
                 IA.s(i,j, 1.0)
            else:
                IA.s(i,j, 0.0)

            for k in range(i):
                IA.s(i,j, IA.g(i,j)-C.g(i,k)*IA.g(k,j))

        for i in range(N-1,-1,-1):
            for k in range(i+1,N):
                IA.s(i,j, IA.g(i,j)-C.g(i,k)*IA.g(k,j))

            IA.s(i,j, 1.0*IA.g(i,j)/C.g(i,i))
                
    return IA

def LUPDeterminant(A):
    B = A.copy()
    n,m = B.shape
    assert(n == m)
    N = n
    Tol = 1e-8
    flag,C,P = LUPDecompose(B,Tol)
    D = C.g(0,0)
    for i in range(1,N):
        D = D * C.g(i,i)

    if int(P.g(N,0)- N)%2 == 0:
        return D
    else:
        return -D

det = lambda A: LUPDeterminant(A)
solve = lambda A,b: LUPSolve(A,b)
inv = lambda A: LUPInvert(A)

