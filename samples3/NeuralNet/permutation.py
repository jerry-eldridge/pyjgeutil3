from copy import deepcopy

import random

def perm(n):
    if n <= 1:
        P = [[0]]
        return P
    P = perm(n-1)
    Q = []
    for pi in P:
        for i in range(n):
            pi2 = deepcopy(pi)
            pi2.insert(i,n-1)
            Q.append(pi2)
    return Q

class Permutation:
    def __init__(self,L=[]):
        self.L = L
        self.n = len(L)
    def __str__(self): # print(sigma) or str(sigma)
        s = str(self.L)
        return s
    # https://en.wikipedia.org/wiki/Bubble_sort
    # each time a transposition (a swap) is done
    # add one to s and when done determine if
    # even or odd. If even return 1 if odd return -1.
    def sign(self): # s = pi.sign()
        s = 0
        n = self.n
        M = deepcopy(self.L)
        while True:
            swapped = False
            for i in range(1,n):
                if M[i-1] > M[i]:
                    tmp = M[i-1]
                    M[i-1] = M[i]
                    M[i] = tmp
                    swapped = True
                    s = (s + 1)%2
            if not swapped:
                break
        return [1,-1][s % 2]
    def g(self,i): # j = sigma.g(i), get or map i to j
        if self.n > 0:
            return self.L[i]
        else:
            return None
    def __mul__(self,sigma):
        def f(i):
            return self.g(sigma.g(i))
        L = list(map(f, range(self.n)))
        return Permutation(L)
    def inv(self):
        L = self.L
        M = list(zip(L,range(self.n)))
        M.sort(key = lambda tup: tup[0])
        L2 = list(map(lambda tup: tup[1], M))
        return Permutation(L2)
    def one(self,n):
        L = list(range(n))
        return Permutation(L)
    def cyc(self):
        n = self.n
        N = list(range(n))
        P = []
        while len(N) > 0:
            i = random.choice(N)
            j = i
            T = [i]
            try:
                N.remove(j)
            except:
                nn = 0
            for k in N:
                j = self.g(j)
                if j not in T:
                    T.append(j)
                try:
                    N.remove(j)
                except:
                    nn = 0
            P.append(T)
        return P
