import leastsqrs as ls

import random
from math import sin,cos

import time

random.seed(0)

def encode(msg):
    def f(W):
        n = len(W)
        def g(x):
            s = 0
            for i in range(n):
                v = (W[i])*cos(i*x)
                s = s + v
            return s
        return g

    W0 = list(map(ord,list(msg)))
    def Generate(N):
        L = []
        for i in range(N):
            xi = random.uniform(-10,10)
            err = random.uniform(-1,1)
            yi = f(W0)(xi) + err
            L.append([xi,yi])
        return L
    N = 40
    data = Generate(N) # list of [xi,yi] data
    return (data,len(msg))

def decode(data,n):
    def f(W):
        n = len(W)
        def g(x):
            s = 0
            for i in range(n):
                v = (W[i])*cos(i*x)
                s = s + v
            return s
        return g

    x = list(map(lambda tup: tup[0],data))
    y = list(map(lambda tup: tup[1],data))
    W0 = [1]*n
    rec1 = ls.fit(x,y,f,W0,eta=0.005,N=100,verbose=False)
    msg_decode = ''.join(list(map(lambda x: chr(int(round(x))),rec1.W)))
    return msg_decode

def Dsp(t0):
    t1 = time.time()
    t = t1 - t0
    t0 = t1
    print("elapsed time t = ",t)
    return t0

t0 = time.time()

msg_encode = "brief"
print("msg_encode='%s'" % msg_encode)
t0 = Dsp(t0)
data,n = encode(msg_encode)
t0 = Dsp(t0)
print("data=encode(msg_encode)=",data)
msg_decode = decode(data,n)
t0 = Dsp(t0)
print("msg_decode=decode(data)='%s'" % msg_decode)
