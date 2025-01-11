import numpy as np
import sympy
import scipy.optimize as so

from math import floor, ceil, tanh

def BlockDesign(z,x0,n1,n2,n3,m1,m2,m3, c):
    A = sympy.symbols(f"A[0:{n1}][0:{n2}][0:{n3}]")
    A = sympy.Array(A).reshape(n1,n2,n3)
    v = list(A.reshape(n1*n2*n3))
    s = sum(v)

    A_eq = []
    b_eq = []

    # column
    for i2 in range(n2):
        for i3 in range(n3):
            si = A[0,0,0]*0
            for i1 in range(n1):
                si = si + A[i1,i2,i3]
            bi = [0]*(n1*n2*n3)
            for k in range(n1*n2*n3):
                bi[k] = si.coeff(v[k],1)
            A_eq.append(bi)
            b_eq.append(m1)

    # row
    for i1 in range(n1):
        for i3 in range(n3):
            if sum(x0[i1,:,i3]) < 2:
                continue
            si = A[0,0,0]*0
            for i2 in range(n2):
                si = si + A[i1,i2,i3]
            bi = [0]*(n1*n2*n3)
            for k in range(n1*n2*n3):
                bi[k] = si.coeff(v[k],1)
            A_eq.append(bi)
            b_eq.append(m2)

    # digit
    for i1 in range(n1):
        for i2 in range(n2):
            si = A[0,0,0]*0
            for i3 in range(n3):
                si = si + A[i1,i2,i3]
            bi = [0]*(n1*n2*n3)
            for k in range(n1*n2*n3):
                bi[k] = si.coeff(v[k],1)
            A_eq.append(bi)
            b_eq.append(m3)

    # subsquare
    for ii in range(3):
        for jj in range(3):
            for kk in range(n3):
                si = A[0,0,0]*0
                for i in range(3*ii,3*(ii+1)):
                    for j in range(3*jj,3*(jj+1)):
                        si = si + A[i,j,kk]
                bi = [0]*(n1*n2*n3)
                for k in range(n1*n2*n3):
                    bi[k] = si.coeff(v[k],1)
                A_eq.append(bi)
                b_eq.append(1.0)

    k = 0
    for i1 in range(n1):
        for i2 in range(n2):
            digit = z[i1,i2]
            for i3 in range(n2):
                bi = [0]*(n1*n2*n3)
                bi[k] = 1
                if x0[i1,i2,i3] == 1:
                    A_eq.append(bi)
                    b_eq.append(1.0)
                k = k + 1
                
    A_eq = np.array(A_eq).reshape(len(A_eq),\
                    n1*n2*n3)
    b_eq = np.array(b_eq).reshape(len(b_eq),1)

    
    bounds0 = [(0,1)]*len(c)
    res = so.linprog(-c,A_eq=A_eq,b_eq=b_eq,
                    bounds = bounds0, method='highs')
    flag = res.success
    x = list(res.x)
    x = list(map(float,x))

    X = np.array(x).reshape((n1,n2,n3))
    return X   

def create_init(data):
    x = np.zeros((data.shape[0],data.shape[1],9),
                 dtype=np.int8)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            digit = data[i,j]
            if digit != 0:
                x[i,j,digit-1] = 1
            else:
                x[i,j,:] = 2
    return x

def get_square(z,x0,x):
    sh = x0.shape
    n1,n2,n3 = sh
    y = z.copy()
    for i in range(n1):
        for j in range(n2):
            I = list(filter(lambda v: x0[i,j,v] == 2,
                    range(n3)))
            if len(I) == 0:
                continue
            digit = np.argmax([
                x[i,j,k] for k in I])+1
            y[i,j] = digit
    return y

def solve_sudoku(design):
    # https://en.wikipedia.org/wiki/Block_design
    n1 = 9 # rows
    m1 = 1 # one unique digit in each row

    n2 = 9 # columns
    m2 = 1 # one unique digit in each column

    n3 = 9 # digits
    m3 = 1 # one digit in each square (row,column)
    
    z = design.copy()
    x0 = create_init(z)
    c = np.array([0]*(n1*n2*n3))
    cc = 0
    for i in range(n1):
        for j in range(n2):
            for k in range(n3):
                if x0[i,j,k] == 2:
                    c[cc] = 1
                elif x0[i,j,k] == 1:
                    c[cc] = 2
            cc = cc + 1
            
    # Size of X is m x n with b 1's per row, and
    # a 1's per column.
    X = BlockDesign(z,x0,n1,n2,n3,m1,m2,m3, c)
    design2 = get_square(z,x0,X) 
    return design2

def demo(data):
    design = data.copy()
    print(f"Unsolved design = \n{design}")
    design2 = solve_sudoku(design)
    print(f"Solved design = \n{design2}")
    return

def design_ppt(design):
    s = '\n'
    sh = design.shape
    for i in range(sh[0]):
        if i % 3 == 0:
            s = s + '\n'
        for j in range(sh[1]):
            digit = design[i,j]
            if digit == 0:
                c = '-'
            else:
                c = str(digit)
            if j % 3 == 0:
                s = s + '  '+str(c)
            else:
                s = s + str(c)
        s = s + '\n'
    return s
