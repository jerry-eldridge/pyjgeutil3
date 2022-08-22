from copy import deepcopy

import numpy as np
import random

seed = 1231234
random.seed(seed)
np.random.seed(seed)

class Queue:
    def __init__(self):
        self.L = []
        self.undef = None
        return
    def Initialize(self):
        self.__init__()
        return
    def Push(self,item):
        self.L = self.L + [item]
        return
    def Pop(self):
        if self.Empty():
            return self.undef
        item = self.L[0] # car
        self.L = self.L[1:] # cdr
        return item
    def Empty(self):
        return self.L == []
    def __str__(self):
        s = str(self.L)
        return s


class NetMem:
    def __init__(self):
        self.Q = Queue()
        return
    def Push(self, item):
        self.Q.Push(item)
        return
    def Pop(self):
        item = self.Q.Pop()
        return item
    def Clear(self):
        self.Q.Initialize()
    def Empty(self):
        return self.Q.Empty()
    def Size(self):
        return len(self.Q.L)
    def __str__(self):
        s = str(self.Q)
        return s

def Idx(M,i,j):
    ii = j
    jj = i
    I = M.I
    J = M.J
    n = M.J*jj + ii
    return n

def InvIdx(M,n):
    I = M.I
    J = M.J
    ii = n % M.J
    jj = int(round((n - ii)/M.J))
    i = jj
    j = ii
    return i,j

# PMat with P suggesting "Packet" or a matrix of
# data packets.
class PMat:
    def __init__(self, I,J):
        self.I = I
        self.J = J
        self.size = I*J
        self.L = None
        self.Create()
        return
    def Create(self):
        self.L = []
        for j in range(self.J):
            for i in range(self.I):
                Lij = NetMem()
                self.L.append(Lij)
        return
    def __setitem__(self,n,val):
        self.L[n].Push(val)
        return val
    def __getitem__(self,n):
        val = self.L[n].Pop()
        return val
    def Push(self,i,j,val):
        n = Idx(self,i,j)
        self[n] = val
        return
    def Pop(self,i,j):
        n = Idx(self,i,j)
        val = self[n]
        return val
    def Empty(self,i,j):
        n = Idx(self,i,j)
        return self.L[n].Empty()
    def __str__(self):
        s = 'Mat(\n'
        for n in range(self.size):
            i,j = InvIdx(self,n)
            if not self.L[n].Empty():
                t = '%s,%d:%s\n' % (str((i,j)),n,
                        str(self.L[n]))
                s = s + t
        s = s + ')'
        return s
    def send(self,b, i,j,n):
        assert(self.I == b.I)
        assert(self.J == b.J)
        for k in range(n):
            v = b.Pop(i,j)
            self.Push(i,j, v)
        return
    def peek(self,b, i,j,n):
        assert(self.I == b.I)
        assert(self.J == b.J)
        m = Idx(b,i,j)
        M = b.L[m].Q.L
        p = min(len(M),n)
        for k in range(p):
            v = b.L[m].Q.L[k]
            self.Push(i,j, v)
        return
    def remove(self, i, j, n):
        m = Idx(self,i,j)
        for k in range(n):
            vk = self.Pop(i,j)
        return
    def flow(self, b, C):
        sh = C.shape
        I,J = sh
        assert(self.I == I and b.I == I)
        assert(self.J == J and b.J == J)
        for j in range(J):
            for i in range(I):
                self.peek(b, i, j, int(C[i,j]))
        for j in range(J):
            for i in range(I):
                b.remove(i,j, int(C[i,j]))
        return

# (I,J) is shape of PMat matrix with values queues
# Lmin and Lmax is the maximum number of random
# items to push on the queue as position (i,j).
def RndMat(I,J, Lmin,Lmax, V):
    M = PMat(I,J)
    for j in range(J):
        for i in range(I):
            K = int(round(random.uniform(Lmin,Lmax)))    
            for k in range(K):
                v = random.choice(V)
                M.Push(i,j, v)
    return M

N1 = 3
N2 = 3
print("Creating Mat objects...")
M1 = PMat(N1,N2)
M2 = PMat(N1,N2)
M1.Push(0,0, 3)
M1.Push(0,0, 4)
M1.Push(1,0, 2)
M2.Push(0,0, 5)
M2.Push(0,0, 7)
M2.Push(1,0, 6)
print("M1=\n",M1)
print("M2=\n",M2)
print()

V = ['a','b','c','d','e','f']
Lmin = 0
Lmax = 5
M3 = RndMat(N1,N2, Lmin,Lmax, V)
M4 = RndMat(N1,N2, Lmin,Lmax, V)
print("M3=\n",M3)
print("M4=\n",M4)
print()

C = np.round(np.random.rand(N1,N2)*3)
print("C = \n", C)

M3.flow(M4, C)
print("M3=\n",M3)
print("M4=\n",M4)
print()
