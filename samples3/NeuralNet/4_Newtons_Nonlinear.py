import matrix
import optimize as opt

from copy import deepcopy

from math import factorial as fa
from math import sqrt


##    def arr(self):
##        return np.array(self.A)            

A = matrix.Mat([[5,4,5],[1,2,3],[4,3,2]])
I = A.identity(A.shape[0])
B = matrix.Mat([[5,4],[1,2],[2,4]])
C = A.dot(B)
b = matrix.Mat([[1,3,2]]).transpose()
if 1:
    print("A =\n",A)
    print("I =\n",I)
    print("b =\n",b)
    print('-'*30)
    n,m = A.shape
    names = list(map(lambda i: 'x%d'%i, range(n)))
    for i in range(n):
        s = ''
        for j in range(m):
            t = str(A.g(i,j))+'*'+names[j]+' + '
            s = s + t
        s = s[:-3]
        t = str(b.g(i,0))
        s = s + ' = ' + t
        print(s)
    D = A.det()
    print("det(A) = A.det() = ",D)
    epsilon = 1e-4
    if abs(D) < epsilon:
        print("A is singular")
    else:
        print("A is non-singular")
    print("A*x = b")
    print("x = A.solve(b)")
    print("x = ",A.solve(b).flatten().A[0])
    print('='*30)  
            
if 1:
    print("A =\n",A)
    print("B =\n",B)
    print("C = A*B =\n",C)
    print("I =\n",I)
    print("A.g(0,0),A.g(0,1) = ",A.g(0,0),A.g(0,1))
    print("det(A) = ",A.det())
    print("A.inv() =\n",A.inv())
    print("A.dot(A.inv()) =\n",A.dot(A.inv()))
    print("abs(A) =",abs(A))
    print("C - B =",C-B)
    print("|C-B| = abs(C-B) =",abs(C-B))
    print('='*30)

flag = False # or False
if flag:
    print("Using sympy - if error, then 'pip install sympy'")
    import sympy
    I = A.identity(A.shape[0])
    x = sympy.symbols('x')
    p = (A - x*I).det()
    p = p.expand()
    print("p = (A - x*I).det() =",p)
    L = p.as_poly(x).all_coeffs()
    print("Using numpy - if error, then 'pip install numpy'")
    import numpy as np
    roots = np.roots(L)
    print("roots = ",roots)
    print('='*30)
    
f = lambda x: -x**3 + 9*x**2 + 9*x - 10
df = lambda x: Derivative(f,x,dx=.01)

flag2 = True
if flag2:
    # required f(a)*f(b) < 0
    print("Only finding real roots ... ")
    x1 = opt.bisection(f,-10,0,tol=.1,nmax=1000,epsilon=1e-3)
    x2 = opt.bisection(f,0,2,tol=.1,nmax=1000,epsilon=1e-3)
    x3 = opt.bisection(f,2,10,tol=.1,nmax=1000,epsilon=1e-3)
    print("Finds only real eigenvalues...")
    print("eigvals(A) = Roots by bisection =",x1,x2,x3)
    print('='*30)
    
if flag and flag2:
    print("eigvals(A) by numpy = ",np.linalg.eigvals(np.array(A.A)))
    # (a,b) is graphing range here
    a = -7
    b = 12
    X = np.arange(a,b,(b-a)/100.)
    Y = list(map(f,X))
    print("If error then 'pip install matplotlib'")
    import matplotlib.pyplot as plt    
    plt.plot(X,Y,'b')
    L = [x1,x2,x3]
    print("Optimal Values of x =",L)
    plt.scatter(L,list(map(f,L)))
    plt.axhline(y=0,color='k')
    plt.show()

if 1:
    # two circles intersecting in two points
    # Fi(x1,x2) = 0
    n = 2
    F = lambda x: [
        [(x[0]+2)**2+(x[1]+0)**2 - 3**2,
        (x[0]-1)**2+(x[1]-1)**2 - 3**2]
        ]
    import sympy # pip install sympy
    x = sympy.symbols('x[0:%d]'%n)
    print("F(x)=",F(x))
    x0 = [-5,1]
    x = opt.Newtons_nonlinear(F,x0,N=200,epsilon=.01)
    print("x =",x,
          "\nF(x)=",str(F(x)))
        
    x0 = [4,-4]
    x = opt.Newtons_nonlinear(F,x0,N=200,epsilon=.01)
    print("x =",x,
          "\nF(x)=",str(F(x)))
    print('='*30)



