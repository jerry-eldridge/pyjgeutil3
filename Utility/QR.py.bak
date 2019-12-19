import GramSchmidt as GS

import numpy as np

# QR decomposition
# https://en.wikipedia.org/wiki/QR_decomposition
def sgn(x):
    if abs(x)==x:
        return 1
    else:
        return -1

def QR(A):
    u = []
    n,m = A.shape
    for j in range(m):
        u.append(A[:,j])
    v = GS.GramSchmidtProcess(u)
    Q = np.array(v).transpose()
    s = -sgn(Q[0,0])
    N = len(v)
    R = np.zeros((N,N))
    for j in range(N):
        for i in range(N):
            R[i,j] = GS.dot(v[i],A[:,j])
    Q = s*Q
    R = s*R
    return Q,R
