import optimize as opt

F = lambda x: [[(x[0]-4)**2 - 4**2, (x[1]-3)**2-5**2]]
x0 = [1,2]
x = opt.Newtons_nonlinear(F,x0,N=20,epsilon=0.01)
print("x=",x)
print("F(x)=",F(x))

G = lambda x: (x[0]**2 + x[1]**2 - x[0]*x[1] - 5)**2
x0 = [1,1]
x = opt.GradientDescent(G,x0,eps=0.0001,eta = 0.001,
                    N = 100, verbose=False)
print("x=",x)
print("G(x)=",G(x))


import leastsqrs as ls
data = [[1,2],[3,2],[4,1],[5,0]]
x = list(map(lambda tup: tup[0], data))
y = list(map(lambda tup: tup[1], data))
f = lambda W: lambda x: W[0]*x+W[1]
reg = ls.fit(x,y,f,
             W0=[1,1],eta=0.0001,N=100)
g = f(reg.W)
print(reg)

f = lambda x: (x-3)**2 - 4
df = lambda x: opt.Derivative(f,x,dx=0.01)
x0 = 10
x = opt.Newtons(f,df,x0,nmax=100,epsilon=1e-3)
print("x = ",x)
print("f(x) = ",f(x))
                
