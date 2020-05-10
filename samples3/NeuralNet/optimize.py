import matrix
import LU

# https://en.wikipedia.org/wiki/Bisection_method
# root finding method: Bisection method
def bisection(f,a,b,tol=.1,nmax=1000,epsilon=1e-3):
    n = 1
    while n <= nmax:
        c = (a+b)/2.
        if abs(f(c)) < epsilon or abs(b-a)/2. < tol:
            return c
        n = n + 1
        if f(c)*f(a) > 0:
            a = c
        elif f(c)*f(a) < 0:
            b = c
        else:
            return c
    return None

def Derivative(f,x,dx):
     slope = 1.0*(f(x+dx)-f(x))/dx
     return slope

# root-finding method Newton's method
# https://en.wikipedia.org/wiki/Newton%27s_method
def Newtons(f,df,x0, nmax = 1000, epsilon=1e-3):
    n = 0
    x = x0
    oo = 1e8
    x_last = -oo
    count = 0
    
    while True:
        if abs(x - x_last) < epsilon:
            break
        x_last = x
        if abs(df(x)) < epsilon:
            break
        x = x - f(x)/df(x)
    return x

def J(F,x,dx=.01):
    n = len(x)
    m = len(F(x)[0])
    #print("|x|=",n,"|F(x).A[0]|=",m)
    def d(F,x,dx):
        I = matrix.Mat([[]]).identity(n)
        def ei(i):
            L = []
            for j in range(n):
                L.append(I.g(i,j))
            return matrix.Mat([L])
        def f(i,j):
            A = matrix.Mat([x])+dx*ei(j)
            B = matrix.Mat([x])
            a = A.A[0]
            b = B.A[0]
            val = (1.0*(matrix.Mat(F(a))-matrix.Mat(F(b)))*(1./dx))
            #print(val)
            return val.g(0,i)
        return f
    G = matrix.Mat([[]]).zero(m,n)
    #print("n,m=",n,m)
    for j in range(n):
        for i in range(m):
            G.s(i,j, d(F,x,dx)(i,j))
    return G

# https://en.wikipedia.org/wiki/Newton%27s_method#Nonlinear_systems_of_equations
def Newtons_nonlinear(G,x0,N=20,epsilon=.1):
    F = lambda X: matrix.Mat(G(X)).transpose()
    k = 1
    x = matrix.Mat([x0])
    while k <= N:
        b_k = (-1*F(x.A[0]))
        A_k = J(G,x.A[0],0.01)
        #print("b_k:",b_k.shape)
        #print("A_k:",A_k.shape)
        y = (LU.solve(A_k,b_k)).transpose()
        x = x + y # x(n+1) - x(n) = y
        if abs(y) < epsilon:
            return x.flatten().A[0]
            break
        k = k + 1
    print("Error-maxiters exceeded")
    return  x.flatten().A[0]

# Jacobian matrix at X
def grad(E):
    F = lambda X: [[E(X)]]
    def G(X):
        return J(F,X,dx=0.01)
    return G

def GradientDescent(F,x0,eps=0.0001,eta=0.001,N=1000,
                    verbose=False):
    if verbose:
        print(eps,eta,N,verbose)
    count = 0
    x = matrix.Mat([x0])
    while (count < N):
        dF = grad(F)(x.A[0])
        if verbose:
            print(dF.A,",")
        x_new = x - eta*dF
        if abs(x-x_new) < eps:
            break
        x = x_new.copy()
        count = count + 1
    #print("count=",count,str(x),str(F(x.A[0])))
    return x.A[0]
