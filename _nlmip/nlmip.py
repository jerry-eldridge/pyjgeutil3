import numpy as np
import scipy.optimize as so

from math import floor, ceil, tanh

# [1] Operations Research, 11th edition,
# Frederick S. Hillier and Gerald J. Lieberman,
# McGraw Hill, 2021
# [2] "branch and bound method" integer programming

def CMP(x,y):
    eps = 0.0005
    if abs(x - y) < eps:
        return True
    else:
        return False

def Feasible(x,J):
    y = list(map(round,x))
    I = []
    for i in range(len(y)):
        flag1 = (CMP(x[i],y[i]) == False)
        flag2 = (i in J)
        flag = flag1 and flag2
        if flag:
            I.append(i)
    return I

def Solve(c,A,b,bounds0):
    res = so.linprog(c,A_ub=A,b_ub=b,bounds = bounds0, method='simplex')
    flag = res.success
    x = list(res.x)
    return x, flag

def Iter(c,A,b,bounds, J, x,flag0):
    if len(J) == 0:
        return x,flag0
    I = Feasible(x,J)
    print("Iter: x = ",x, I)
    if len(I) == 0:
        return x,flag0
    else:
        i = J[0]
        J2 = list(J[1:])
        xmin = floor(x[i])
        xmax = xmin + 1
        xx = [0]*len(x)
        xx[i] = 1
        b2 = b + [xmin]
        A2 = A + [xx]
        b3 = b + [-xmax]
        xx2 = [0]*len(x)
        xx2[i] = -1
        A3 = A + [xx2]
        V = [[c,A2,b2,bounds, J2],
             [c,A3,b3,bounds, J2]]
    a1,flag1 = Solve(c,A2,b2,bounds)
    a2,flag2 = Solve(c,A3,b3,bounds)
    if flag1 and flag2:
        if np.inner(a1,c) <= np.inner(a2,c):
            W = V[0] + [a1] + [flag1]
            x1,flag = Iter(*W)
            I1 = Feasible(x1, J2)
            if len(I1) == 0:
                return x1,flag
        elif np.inner(a2,c) <= np.inner(a1,c):
            W = V[1] + [a2] + [flag2]
            x2,flag = Iter(*W)
            I2 = Feasible(x2, J2)
            if len(I2) == 0:
                return x2,flag
    elif flag1 or flag2:
        if flag1:
            W = V[0] + [a1] + [flag1]
            x1,flag = Iter(*W)
            I1 = Feasible(x1, J2)
            if len(I1) == 0:
                return x1,flag
        elif flag2:
            W = V[1] + [a2] + [flag2]
            print("4: W = ",W)
            x2,flag = Iter(*W)
            I2 = Feasible(x2, J2)
            if len(I2) == 0:
                return x2,flag
        else:
            print("Error")
            return a1,flag1
    return a1,flag1

def IP(c,A,b,bounds):
    print("IP")
    J = range(len(c))
    a,flag0 = Solve(c,A,b,bounds)
    x,flag = Iter(c,A,b,bounds, J, a, flag0)
    print("success =",flag)
    I1 = Feasible(x, J)
    print("Nonfeasible: ",I1)
    x = list(map(round, x))
    return x

def BIP(c,A,b):
    print("BIP")
    bounds = [(0,1)]*len(c)
    x = IP(c,A,b,bounds)
    return x

def MIP(c,A,b,bounds, J):
    print("MIP")
    a,flag0 = Solve(c,A,b,bounds)

    x,flag = Iter(c,A,b,bounds, J, a, flag0)
    print("success =",flag)
    for i in J:
        x[i] = int(round(x[i]))
    return x

def MBIP(c,A,b,bounds, J):
    for i in J:
        bounds[i] = (0,1)
    x = MIP(c,A,b,bounds, J)
    return x

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

def Number(L,base):
    n = 0
    k = len(L)-1
    for i in range(len(L)):
        n = n + L[k-i]*base**i
    return n

# Constraint definition
def LC(i,AA,b):
    cons_i = {'type':'ineq',
        'fun': lambda x: b[i]-np.inner(AA[i,:],x)}
    return cons_i

def NL_Iter(f,x0,A,b,bounds, J):
    cons = []
    AA = np.array(A)
    n1,n2 = AA.shape
    for i in range(n1):
        cons_i = LC(i,AA,b)
        cons.append(cons_i)
    cons = tuple(cons)
    res = so.minimize(f,x0,method='SLSQP',
            bounds=bounds,
            constraints=cons,
            tol=1e-6)
    success = res.success
    x = list(res.x)
    if not success:
        return x,False
    I = Feasible(x,J)
    #print("NL_Iter: x = ",x, I)
    if len(I) == 0:
        return x,True
    else:
        i = J[0]
        J2 = J[1:]
        xmin = floor(x[i])
        xmax = xmin + 1
        xx = [0]*len(x)
        xx[i] = 1
        b2 = b + [xmin]
        A2 = A + [xx]
        b3 = b + [-xmax]
        xx2 = [0]*len(x)
        xx2[i] = -1
        A3 = A + [xx2]
        V = [[f,x0,A2,b2,bounds, J2],
             [f,x0,A3,b3,bounds, J2]]
    x1,flag1 = NL_Iter(*V[0])
    I1 = Feasible(x1, J2)
    x2,flag2 = NL_Iter(*V[1])
    I2 = Feasible(x2, J2)
    X = list(res.x)
    aa = len(I1)
    bb = len(I2)
    cc = len(J)
    L = [(aa,x1,flag1),(bb,x2,flag2),
         (cc,X,success)]
    F = list(filter(lambda i: L[i][2], range(len(L))))
    L2 = list(map(lambda i: L[i], F))
    L2.sort(key = lambda tup: tup[0])
    return L2[0][1],L2[0][2]
def NLMIP(f,x0, A, b, bounds, J):
    print("NLMIP")
    x,flag = NL_Iter(f,x0,A,b,bounds, J)
    print("success=",flag)
    for i in J:
        x[i] = int(round(x[i]))
    AA = np.array(A)
    n1,n2 = AA.shape
    eps = 0.00001
    for i in range(n1):
        cons_i = LC(i,AA,b)
        val_i = cons_i['fun'](x)
        print(i,"cons_i=",val_i, val_i > -eps)
    return x
