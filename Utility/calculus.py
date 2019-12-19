def Integral(f,a,b,dx):
     if a > b:
          return -Integral(f,b,a,dx)
     x = a
     s = 0
     while x < b:
         s += f(x)*dx
         x += dx
     return s

def Derivative(f,x,dx):
     slope = 1.0*(f(x+dx)-f(x))/dx
     return slope
