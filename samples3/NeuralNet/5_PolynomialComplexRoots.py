import matrix
import optimize as opt

def Display(f,X):
    global I
    flag = True
    if flag:
        import sympy
        z = sympy.symbols('z')
        p = f(z)
        print("sympy: p =",p)
        print("sympy: p.factor() =",p.factor())
        x,y = sympy.symbols('x,y')
        I = complex(0,1)
        w = x + I*y
        p = f(w)
    flag2 = True
    if flag2:
        print("sympy: p =",p)
        import numpy as np
        print("numpy: roots = ",np.roots(f(z).as_poly(z).all_coeffs()))
        print("="*30)
        
    # by plugging in z = x + I*y then write f(z) as f1([x,y]).
    def f1(x):
        z = x[0] + I*x[1]
        return f(z)
    # by plugging in f(1) = z then |z| = |f(1)| = f(1).
    def f2(x):
        val = x[0]**2+x[1]**2 - f(1)**2 # to make |z| - f(1) = 0
        return val
    # we needed two equations in two unknowns
    G = lambda x: [[f1(x),f2(x)]]
    Y = []
    for xi in X:
        print("xi =",xi)
        yi = opt.Newtons_nonlinear(G,xi,N=20,epsilon=0.001)
        y = yi[0]+I*yi[1]
        Y.append(y)
        print("yi =",y)
        print("|f1(yi)-0| =",abs(f1([y.real,y.imag])))
    print("="*30)
    return Y

I = complex(0,1)
f = lambda z: z**3 - 3*z + 1
x1 = [-100,0]
x2 = [100,0]
x3 = [0,0]
Y = Display(f, X=[x1,x2,x3])

I = complex(0,1)
f = lambda z: z**3 - 3*z + 10
x1 = [-100,0]
x2 = [2,2]
x3 = [2,-2]
Y = Display(f, X=[x1,x2,x3])
