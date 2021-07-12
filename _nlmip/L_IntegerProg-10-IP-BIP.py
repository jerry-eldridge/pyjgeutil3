import numpy as np
from math import floor, ceil

import nlmip

c = [-5,-2, -4]
A = [[-1,2, 1],[2,-3, 1],[2,1, 2]]
b = [6,3,25]
bounds = [(0,None)]*len(c)
x0 = nlmip.Solve(c,A,b,bounds)
print("x0=",x0)
x = nlmip.IP(c,A,b,bounds)
print("c = ",c)
print("A = ",A)
print("b = ",b)
print("bounds = ", bounds)
print("x=",x)

c = [-4,-2,-1,-1]
A = [[3,4,2,1],[0,0,1,1],[-1,0,1,0],[0,-1,0,1]]
b = [11,1,0,0]
x = nlmip.BIP(c,A,b)
print("c = ",c)
print("A = ",A)
print("b = ",b)
print("x=",x)
