import collections
import optimize as opt

FitTuple = collections.namedtuple("Fit",["W"])
FitTuple2 = collections.namedtuple("Fit",["slope","intercept","rhat"])

line = lambda X: lambda x: X[0]*x + X[1]

def E(x,y,f):
    data = list(map(list,zip(x,y)))
    def F(X):
        n = len(data)
        s = 0
        for i in range(n):
            xi,yi = data[i]
            val = (f(X)(xi)-yi)**2
            s = s + val
        return 1.0*s/n
    return F

def fit(x,y,f,W0,eta=0.0005,N=1000,verbose=False):
    F = E(x,y,f)
    W = opt.GradientDescent(F,W0,eta=eta,N=N,verbose=verbose)
    rec = FitTuple(W)
    return rec

def linregress(X,Y):
    S_x = sum(X)
    S_y = sum(Y)
    assert(len(X) == len(Y))
    n = len(X)
    S_xx = sum(map(lambda x: x**2, X))
    S_xy = sum(map(lambda xy: xy[0]*xy[1], zip(X,Y)))
    S_yy = sum(map(lambda x: x**2, Y))
    beta_hat = 1.*(n*S_xy - S_x*S_y)/(n*S_xx - S_x**2)
    alpha_hat = 1./n*S_y - beta_hat*1./n*S_x
    xbar = 1.*sum(X)/n
    ybar = 1.*sum(Y)/n
    xybar = S_xy/n
    from math import sqrt
    a = 1.*(n*S_xy-S_x*S_y)
    b = 1.*(n*S_xx-S_x**2)*(n*S_yy-S_y**2)
    rhat = a/sqrt(b)
    return FitTuple2._make([beta_hat,alpha_hat,rhat]) 
