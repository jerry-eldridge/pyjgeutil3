import matrix
import LU
import optimize as opt
import leastsqrs as ls

from copy import deepcopy
import random

def RndMat(n,m,a,b):
    A = matrix.Mat([[]]).zero(n,m)
    for j in range(m):
        for i in range(n):
            v = random.uniform(a,b)
            A.s(i,j,v)
    return A

def app(A,f):
    n,m = A.shape
    # B is [f(A[i,j])]_ij
    B = matrix.Mat([[]]).zero(n,m)
    for j in range(m):
        for i in range(n):
            v = A.g(i,j)
            w = f(v)
            B.s(i,j, w)
    return B

from math import exp,log

# logistic function - obtained with sympy
# and computing sigmoid(x) and sigmoid(x).diff(x)
# and comparing
def sigmoid(x):
    if abs(x) < 10:
        y = 1.0*exp(x)/(exp(x)+1)
    elif x >= 10:
        y = 1
    elif x <= -10:
        y = 0
    return y
def relu(x):
    if abs(x) < 10:
        y = log(1 + exp(x))
    elif x >= 10:
        y = log(1 + exp(10))
    elif x <= -10:
        y = log(1 + exp(-10))
    return y

class NN:
    def __init__(self,S,A=None,init=True):
        self.S = deepcopy(S)
        self.T = self.S
        self.T = list(map(lambda x: x+1, self.T))
        if A is None:
            A = ["sigmoid"]*(len(S)-1)
        self.A = A
        self.L = len(S)
        self.W = []
        size = 0
        for l in range(len(self.T)-1):
            n = self.T[l]
            m = self.T[l+1]
            size = size + n*m
        self.size = size
        if init:
            self.rnd_init()
        return
    def rnd_init(self):
        for l in range(self.L-1):
            n = self.T[l]
            m = self.T[l+1]
            Wl = RndMat(n,m,-1,1)
            self.W.append(Wl)
        return
    def weights(self,l):
        assert(l in range(self.L-1))
        return self.W[l]
    def activation(self,l,x,t="sigmoid"):
        Wl = self.weights(l)
        y = x.dot(Wl)
        assert(t in ["sigmoid","relu"])
        if t == "sigmoid":
            w = app(y,sigmoid)
        if t == "relu":
            w = app(y,relu)
        return w
    def forward(self,x):
        y = x.copy()
        for i in range(self.L-1):
            w = self.activation(i,y,t=self.A[i])
            y = w.copy()
        return y
    def F1(self):
        U = []
        for l in range(self.L-1):
            n = self.T[l]
            m = self.T[l+1]
            Wl = self.weights(l).reshape((1,n*m))
            U = U + Wl.A[0]
        return U
    def F2(self,U):
        W = []
        idx = 0
        for l in range(self.L-1):
            n = self.T[l]
            m = self.T[l+1]
            idx2 = idx + n*m
            V = matrix.Mat([U[idx:idx2]])
            Wl = V.reshape((n,m))
            W.append(Wl)
            idx = idx2
        self.W = W
        return
    def train(self,pat,eps=1e-5,eta=0.5,N=100,verbose=False,
              verbose2=False,method = 'gd'):
        x = list(map(lambda tup: tup[0]+[1], pat))
        y = list(map(lambda tup: tup[1]+[1], pat))
        M = len(pat)
        def f(W):
            W = list(W)
            U = self.F1()
            def g(x):
                self.F2(W)
                y = self.forward(x)
                self.F2(U)
                return y
            return g
        def L(x,y,f):
            def F(X):
                s = 0
                for i in range(M):
                    xi = x[i]
                    yi = y[i]
                    xx = matrix.Mat([xi])
                    tt = matrix.Mat([yi])
                    yy = f(X)(xx)
                    val = abs(tt-yy)**2
                    s = s + val
                if verbose2:
                    print("s=",s)
                return 1.0*s/(M+1)
            return F
        U0 = list(map(lambda i: random.uniform(-1,1),
                      range(self.size)))
        #print(f(W0)(matrix.Mat([x[0]])))
        F = L(x,y,f)
        if method == 'gd':
            U = opt.GradientDescent(F,U0,eps=eps,eta=eta,
                                N=N,verbose=verbose2)
        elif method == 'nm':
            from scipy.optimize import minimize
            U = list(minimize(F,U0,method='Nelder-Mead',
                    tol=1e-7).x)
        else:
            print("Method should be 'gd' or 'nm'")
            return
        self.F2(U)
        return
    def predict(self,x):
        return self.forward(matrix.Mat([x+[1]])).A[0][:-1]
    def save(self,fn):
        print("writing to file...fn=",fn)
        U = self.F1()
        f = open(fn,'w')
        S = self.S
        A = self.A
        for x in S:
            s = 'S %d\n' % x
            f.write(s)
        for x in A:
            s = 'A %s\n' % x
            f.write(s)
        for x in U:
            s = 'u %.10f\n' % x
            f.write(s)
        f.close()
        return
    def load(self,fn):
        print("reading from file...fn=",fn)
        f = open(fn,'r')
        txt = f.read()
        f.close()
        lines = txt.split('\n')
        S = []
        A = []
        U = []
        for line in lines:
            if len(line) < 2:
                #print("line='%s'" % line)
                continue
            if line[0] == 'S':
                x = int(line[1:])
                S.append(x)
            if line[0] == 'A':
                x = line[2:]
                A.append(x)
            if line[0] == 'u':
                x = float(line[1:])
                U.append(x)
        #print(U)
        nn = NN(S,A=A,init=False)
        nn.F2(U)
        return nn
