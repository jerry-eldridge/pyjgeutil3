import numpy as np
from math import floor, ceil

import nlmip

c = [-32,-16,-8,-4,  -80,-40,-20,-10,-5]
A = [[8,4,2,1, 0,0,0,0,0],
     [16,8,4,2, 48, 24,12,6,3]]
b = [15,47]
x = nlmip.BIP(c,A,b)
print("c = ",c)
print("A = ",A)
print("b = ",b)
print("x=",x)

c = [-4, -5]
A = [[1,0],
     [2,3]]
b = [15,47]
bounds = [(0,None)]*2
x = nlmip.IP(c,A,b,bounds)
print("c = ",c)
print("A = ",A)
print("b = ",b)
print("x=",x)

import sympy
y = sympy.symbols('y[0:9]')
x1 = nlmip.Number(y[:4],2)
x2 = nlmip.Number(y[4:],2)
cc = -(4*x1 + 5*x2)
print("objective: ",cc)
z1 = x1
z2 = 2*x1 + 3*x2
print("z1=",z1)
print("z2=",z2)
