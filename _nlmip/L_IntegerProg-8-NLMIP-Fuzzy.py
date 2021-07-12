import numpy as np
from math import floor, ceil, tanh

import nlmip

def sigmoid(x):
    return (tanh(x)+1)*0.5
def f_and(x,y):
    return min(x,y)
def f_or(x,y):
    return max(x,y)
def f_not(x):
    return 1-x
def f_nor(x,y):
    return f_not(f_or(x,y))
# https://en.wikipedia.org/wiki/Material_implication_(rule_of_inference)
def f_imply(x,y):
    return f_or(f_not(x),y)
def f_equiv(x,y):
    return f_and(f_imply(x,y),f_imply(y,x))

from math import sqrt
def h1(x):
    return 1.5*f_and(x[1],x[4])
def g1(x):
    return x[0]
def h2(x):
    return 1*x[3]
def g2(x):
    return x[2]
def h3(x):
    return 2.0*sqrt(x[1]*x[3])
def g3(x):
    return f_and(x[0],x[2])
def h4(x):
    return .1*(x[1] + x[3])
def g4a(x):
    return f_imply(x[0],x[2])
def g4b(x):
    return f_imply(x[2],x[0])

print("="*30)
A = [[-150, 30, -800, 20, -500, 25],
     [1,-1,0,0,0,0],
     [0,0,1,-1,0,0],
     [0,0,0,0,1,-1]]
b = [3500,0,0,0]
bounds = [(0,1),(0,None),(0,1),(0,None),(0,1),(0,None)]
x0 = [0,0,0,0,0,0]

fa = lambda x: -(h1(x)*g1(x) + h2(x)*g2(x) + h3(x)*g3(x) + \
                h4(x)*g4a(x))
x = nlmip.NLMIP(fa,x0,A,b,bounds, J=[0,1,2,3,4,5])
print("A = ",A)
print("b = ",b)
print("x=",x)
print("fa(x)=",fa(x))
print("="*30)

fb = lambda x: -(h1(x)*g1(x) + h2(x)*g2(x) + h3(x)*g3(x) + \
                h4(x)*g4b(x))
x = nlmip.NLMIP(fb,x0,A,b,bounds, J=[0,1,2,3,4,5])
print("A = ",A)
print("b = ",b)
print("x=",x)
print("fb(x)=",fb(x))
print("="*30)
